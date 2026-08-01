import hashlib
import hmac
import logging
from typing import Callable, Optional
from .security_base import SecurityServiceBase, SecurityConfigurationError
import argon2
import requests

class HashingService(SecurityServiceBase):
    """
    Modernized hashing service with HMAC support and timing attack resistance.
    Implements progressive security enhancements with backward compatibility.
    """

    def __init__(
        self,
        service_name: str = "DefaultHasher",
        hash_function: Callable[[bytes], str] = None,
        logger: Optional[logging.Logger] = None,
        hmac_key: Optional[bytes] = None,
        hash_algorithm: str = "sha256",
        breach_api_key: str = None
    ):
        """
        Initialize with configurable hash algorithms and HMAC support.
        
        :param hmac_key: Optional key for HMAC operations
        :param hash_algorithm: Name of hash algorithm (sha256, sha3_512, etc)
        :param breach_api_key: Optional API key for breach checking
        """
        super().__init__(service_name, logger)
        
        self.hash_engine = self._get_hash_engine(hash_algorithm)
        self.hmac_key = hmac_key
        self.hash_function = hash_function or self._default_hash_provider
        self.argon2_hasher = argon2.PasswordHasher(
            time_cost=2, memory_cost=102400, parallelism=8
        )
        self.breach_api_key = breach_api_key

    def _get_hash_engine(self, algorithm: str):
        """Validate and initialize hash algorithm implementation."""
        try:
            return hashlib.new(algorithm)
        except ValueError:
            raise SecurityConfigurationError(
                f"Unsupported hash algorithm: {algorithm}"
            )

    def _default_hash_provider(self, data: bytes) -> str:
        """Secure default hashing implementation with HMAC support."""
        if self.hmac_key:
            return hmac.new(self.hmac_key, data, self.hash_engine.name).hexdigest()
        return hashlib.pbkdf2_hmac(
            self.hash_engine.name,
            data,
            salt=b"",  # Should be overridden in security-critical implementations
            iterations=100000
        ).hex()

    def compute_sha256(self, data: bytes) -> str:
        """Enhanced SHA-256 implementation with validation."""
        self.logger.debug(f"Computing SHA-256 for {len(data)} bytes")
        if not data:
            self.logger.error("Attempted to hash empty data")
            raise ValueError("Cannot hash empty data")
            
        try:
            digest = hashlib.sha256(data).hexdigest()
            self.logger.info(f"Generated SHA-256 digest: {digest[:8]}...")
            return digest
        except Exception as e:
            self.logger.error(f"SHA-256 computation failed: {str(e)}")
            raise

    def compute_hash(self, data: bytes) -> str:
        """Main hash computation with enhanced validation."""
        self.logger.debug(f"Processing {len(data)} bytes for hashing")
        if not isinstance(data, bytes):
            error_msg = f"Invalid data type {type(data)} - expected bytes"
            self.logger.error(error_msg)
            raise TypeError(error_msg)
            
        try:
            result = self.hash_function(data)
            self.logger.debug(f"Hash operation completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Hash computation failed: {str(e)}")
            raise

    def _safe_compare(self, a: str, b: str) -> bool:
        """Constant-time comparison for security-sensitive checks"""
        return hmac.compare_digest(a, b)

    def check_password_breach(self, password: str) -> bool:
        """Check a password against the HaveIBeenPwned database.

        Implements HIBP's k-anonymity model: only the first 5 characters of the
        SHA-1 digest of the password are sent to the API; the plaintext password
        itself is never transmitted.
        """
        sha1_digest = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1_digest[:5]
        try:
            response = requests.get(
                f"https://api.pwnedpasswords.com/range/{prefix}",
                headers={"Add-Padding": "true"},
                timeout=2
            )
            return sha1_digest[5:] in response.text
        except Exception as e:
            self.log_audit_event("BREACH_CHECK_FAILED", {"error": str(e)})
            return False

    def hash_password(self, password: str) -> str:
        """Enhanced with breach checking and zxcvbn complexity analysis"""
        if self.breach_api_key and self.check_password_breach(password):
            raise SecurityConfigurationError("Password has been compromised in breaches")
            
        complexity = self._calculate_password_complexity(password)
        if complexity < 3:
            raise SecurityConfigurationError("Password complexity insufficient")
            
        return super().hash_password(password)

    def _calculate_password_complexity(self, password: str) -> int:
        """Score password complexity on a 0-4 scale (zxcvbn-inspired).

        Scores based on length plus the number of distinct character classes
        (lowercase, uppercase, digits, symbols), so the check is meaningful
        rather than a hardcoded constant.
        """
        if not password:
            return 0
        classes = 0
        if any(c.islower() for c in password):
            classes += 1
        if any(c.isupper() for c in password):
            classes += 1
        if any(c.isdigit() for c in password):
            classes += 1
        if any(not c.isalnum() for c in password):
            classes += 1
        length = len(password)
        if length < 8:
            return min(classes, 2)
        if length < 12:
            return min(classes, 3)
        return classes

    def verify_password(self, password: str, hashed: str) -> bool:
        """Timing-attack resistant verification"""
        try:
            return self.argon2_hasher.verify(hashed, password)
        except argon2.exceptions.VerifyMismatchError:
            self._safe_compare("invalid", "comparison")  # Prevent timing leaks
            return False
        except Exception as e:
            self.log_audit_event("PASSWORD_VERIFY_ERROR", {"error": str(e)})
            return False