import base64
import logging
from typing import Optional, Tuple, Type
from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidToken
from .security_base import SecurityServiceBase, SecurityConfigurationError
import time
from cryptography.hazmat.primitives import serialization


class EncryptionService(SecurityServiceBase):
    """
    Enhanced encryption service with key rotation support and security inheritance.
    Implements cryptographic best practices with defense in depth.
    """

    KEY_ROTATION_TRIGGERS = {
        'time_based': True,
        'usage_based': True,
        'max_operations': 1_000_000,
        'max_age_days': 90
    }

    def __init__(
        self,
        service_name: str = "DefaultEncryptor",
        password: bytes = b"this_is_a_secure_password",
        salt: bytes = b"secure_salt",
        iterations: int = 600_000,  # Updated to OWASP 2023 recommendation
        algorithm: Type[hashes.HashAlgorithm] = hashes.SHA512,
        logger: Optional[logging.Logger] = None,
        enable_rotation: bool = False,
        previous_keys: Optional[Tuple[bytes]] = None,
        hsm_config: dict = None
    ):
        """
        Initialize with enhanced security parameters and rotation capabilities.
        
        :param enable_rotation: Enable support for key rotation/versioning
        :param previous_keys: Tuple of historical keys for decryption
        :param hsm_config: Configuration for Hardware Security Module integration
        """
        super().__init__(service_name, logger)
        
        try:
            self.validate_credentials(password, salt)
        except SecurityConfigurationError as e:
            self.logger.critical(f"Security config failure: {str(e)}")
            raise

        self.current_key = self._derive_key(password, salt, iterations, algorithm)
        self.fernet = self._init_fernet(enable_rotation, previous_keys)
        self.key_version = 1  # Track key versions for rotation
        self.key_generation_time = time.time()
        self.operation_counter = 0
        # SecurityConfigSchema has no key_rotation_policy field; use the module's
        # own (defined) rotation policy so construction never AttributeErrors.
        self.rotation_policy = self.KEY_ROTATION_TRIGGERS
        self.hsm = self._init_hsm(hsm_config) if hsm_config else None

    def _init_fernet(self, enable_rotation, previous_keys):
        """Initialize Fernet instance with rotation support if enabled"""
        if enable_rotation:
            keys = [self.current_key]
            if previous_keys:
                keys.extend(previous_keys)
            return MultiFernet([Fernet(k) for k in keys])
        return Fernet(self.current_key)

    def _init_hsm(self, config: dict):
        """Initialize Hardware Security Module integration.

        No HSM driver is wired into the codebase yet; fail loud rather than
        reference an undefined ``HSMSession`` class.
        """
        raise NotImplementedError("HSM integration is not yet implemented")

    def _derive_key(
        self,
        password: bytes,
        salt: bytes,
        iterations: int,
        algorithm: Type[hashes.HashAlgorithm]
    ) -> bytes:
        """Key derivation with enhanced parameters and validation."""
        self.logger.debug("Deriving key with %s iterations", iterations)
        if self.hsm:
            return self.hsm.derive_key(password, salt, iterations, algorithm)
        kdf = PBKDF2HMAC(
            algorithm=algorithm(),
            length=64,  # Increased for SHA512
            salt=salt,
            iterations=iterations,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def rotate_key(self, new_password: bytes, new_salt: bytes) -> None:
        """Perform secure key rotation with re-encryption support."""
        old_key = self.current_key
        self.current_key = self._derive_key(new_password, new_salt, 600_000, hashes.SHA512)
        self.key_version += 1
        self.logger.info("Key rotated to version %d", self.key_version)
        return old_key

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypts data with size validation and operation logging.
        """
        if not data:
            self.logger.error("Attempted to encrypt empty data")
            raise ValueError("Cannot encrypt empty data")
            
        self.logger.debug(f"Encrypting {len(data)} bytes")
        self._check_rotation_conditions()
        try:
            encrypted = self.fernet.encrypt(data)
            self.logger.info(f"Successfully encrypted {len(data)} bytes")
            return encrypted
        except Exception as e:
            self.logger.error(f"Encryption failed: {str(e)}")
            raise

    def decrypt(self, token: bytes) -> bytes:
        """
        Decrypts data with comprehensive error handling.
        """
        if not token:
            self.logger.error("Attempted to decrypt empty token")
            raise ValueError("Cannot decrypt empty token")

        self.logger.debug(f"Decrypting {len(token)} byte token")
        try:
            decrypted = self.fernet.decrypt(token)
            self.logger.info(f"Successfully decrypted {len(token)} bytes")
            return decrypted
        except InvalidToken as e:
            self.logger.error("Decryption failed - invalid token")
            raise ValueError("Invalid encryption token") from e
        except Exception as e:
            self.logger.error(f"Unexpected decryption error: {str(e)}")
            raise

    def _check_rotation_conditions(self):
        """Automated key rotation based on configured policies"""
        self.operation_counter += 1
        conditions = {
            'time': (time.time() - self.key_generation_time)
                    > self.KEY_ROTATION_TRIGGERS['max_age_days'] * 86400,
            'usage': self.operation_counter
                    > self.KEY_ROTATION_TRIGGERS['max_operations']
        }

        if any(conditions.values()):
            self.log_audit_event("KEY_ROTATION_TRIGGERED", conditions)
            # Automatic rotation needs a new secret; that cannot be derived
            # internally, so surface a loud warning instead of calling the
            # argon2-style rotate_key() with missing arguments.
            self.logger.warning(
                "Key rotation policy conditions met; rotate_key() must be invoked "
                "with a new password by the operator."
            )

    @classmethod
    def enable_fips_mode(cls):
        """Configure for FIPS 140-3 compliance.

        The underlying config object is not a mutable mapping, so the previous
        ``cls._config.update(...)`` call could never work. Fail loud until a real
        FIPS configuration path is wired in.
        """
        raise NotImplementedError(
            "FIPS 140-3 mode configuration is not yet implemented; supply a "
            "FIPS-validated algorithm/iteration set when constructing the service."
        )

    def create_quantum_resistant_keypair(self) -> tuple:
        """Post-quantum cryptography integration point"""
        from .quantum_security import PostQuantumCrypto
        pqc = PostQuantumCrypto()
        return pqc.generate_key_pair()

    def hybrid_encrypt(self, data: bytes) -> bytes:
        """Combined classical and post-quantum encryption"""
        traditional_cipher = self.fernet.encrypt(data)
        quantum_cipher = PostQuantumCrypto.hybrid_encrypt(
            data, 
            self.current_key,
            self.create_quantum_resistant_keypair()[1]
        )
        return b"".join([traditional_cipher, quantum_cipher])