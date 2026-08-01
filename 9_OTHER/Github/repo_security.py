import os
import re
import subprocess
import logging
from typing import List, Dict, Optional, Tuple, Any, Union
from github import Github, GithubException, Repository, Branch
from dotenv import load_dotenv
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from dataclasses import dataclass, field
from enum import Enum, auto
import requests
from cryptography.fernet import Fernet
from abc import ABC, abstractmethod
from collections import defaultdict
import time
from ratelimit import limits, sleep_and_retry

class SecuritySeverity(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

@dataclass
class SecurityFinding:
    file: str
    line: int
    pattern: str
    content: str
    severity: SecuritySeverity = SecuritySeverity.MEDIUM

@dataclass
class SecurityVulnerability:
    package: str
    severity: str
    description: str
    affected_range: str
    fixed_in: str
    cve_id: Optional[str] = None
    references: List[str] = field(default_factory=list)

@dataclass
class SecurityReport:
    sensitive_data: List[SecurityFinding] = field(default_factory=list)
    access_audit: Dict[str, List[str]] = field(default_factory=dict)
    vulnerabilities: List[SecurityVulnerability] = field(default_factory=list)
    branch_protection: bool = False
    security_features: Dict[str, bool] = field(default_factory=dict)
    code_quality_metrics: Dict[str, Any] = field(default_factory=dict)
    dependency_audit: List[Dict[str, Any]] = field(default_factory=list)
    security_policy: Optional[str] = None
    two_factor_auth: bool = False
    signed_commits: bool = False
    open_issues: int = 0
    closed_issues: int = 0
    last_commit_date: Optional[str] = None
    contributors: List[str] = field(default_factory=list)

class SecurityScanner(ABC):
    @abstractmethod
    def scan(self, repo_path: str) -> List[SecurityFinding]:
        pass

class SensitiveDataScanner(SecurityScanner):
    def __init__(self, patterns: List[Tuple[str, str, SecuritySeverity]]):
        self.patterns = patterns

    def scan(self, repo_path: str) -> List[SecurityFinding]:
        findings = []
        excluded_dirs = {'.git', 'node_modules', 'venv', '__pycache__', 'build', 'dist'}
        
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.txt', '.env', '.json', '.yml', '.yaml', '.xml', '.properties', '.sh', '.bash', '.zsh', '.config')):
                    file_path = os.path.join(root, file)
                    findings.extend(self._scan_file(file_path))
        
        return findings

    def _scan_file(self, file_path: str) -> List[SecurityFinding]:
        local_findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_number, line in enumerate(f, 1):
                    for pattern, description, severity in self.patterns:
                        if re.search(pattern, line):
                            local_findings.append(SecurityFinding(
                                file=file_path,
                                line=line_number,
                                pattern=description,
                                content=line.strip(),  # Note: Encryption moved to GitHubRepoSecurity class
                                severity=severity
                            ))
                            break  # Avoid multiple detections of the same line
        except Exception as e:
            logging.warning(f"Error reading file {file_path}: {str(e)}")
        return local_findings

class GitHubRepoSecurity:
    """
    A comprehensive class to manage and enhance GitHub repository security.
    """

    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize the GitHubRepoSecurity class.

        Args:
            github_token (Optional[str]): GitHub API token for authentication. If not provided, it will attempt to load from environment variables.
        """
        load_dotenv()  # Load environment variables from .env file
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        if not self.github_token:
            raise ValueError("GitHub token is required. Please provide it or set the GITHUB_TOKEN environment variable.")
        self.github = Github(self.github_token)
        self.logger = self._setup_logger()
        self.encryption_key = self._load_or_create_encryption_key()
        self.fernet = Fernet(self.encryption_key)
        self.sensitive_data_scanner = self._setup_sensitive_data_scanner()

    @staticmethod
    def _load_or_create_encryption_key() -> bytes:
        """Return a durable Fernet key.

        Uses ``ENCRYPTION_KEY`` if set; otherwise loads a persisted key from
        ``~/.active_inferants_encryption.key``, creating it (mode 0600) on first
        run. This keeps the key stable across runs so encrypted findings remain
        decryptable — a freshly generated ephemeral key would silently destroy
        the scanner's own evidence.
        """
        configured = os.getenv('ENCRYPTION_KEY')
        if configured:
            return configured.encode()
        key_file = os.path.expanduser('~/.active_inferants_encryption.key')
        try:
            if os.path.exists(key_file):
                with open(key_file, 'rb') as fh:
                    return fh.read().strip()
            key = Fernet.generate_key()
            with open(key_file, 'wb') as fh:
                fh.write(key)
            os.chmod(key_file, 0o600)
            return key
        except OSError as e:
            # Could not persist; fall back to an ephemeral key but warn loudly
            # so the operator knows encrypted findings are non-recoverable.
            logging.getLogger('GitHubRepoSecurity').warning(
                "Could not persist encryption key (%s); encrypted findings are "
                "non-recoverable this run.", e
            )
            return Fernet.generate_key()

    @staticmethod
    def _setup_logger() -> logging.Logger:
        """Set up and return a logger for the class."""
        logger = logging.getLogger('GitHubRepoSecurity')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _setup_sensitive_data_scanner(self) -> SensitiveDataScanner:
        """Set up and return a SensitiveDataScanner with predefined patterns."""
        patterns = [
            (r'\b[A-Za-z0-9+/]{40}\b', 'Generic API key', SecuritySeverity.HIGH),
            (r'\b[0-9a-fA-F]{32}\b', '32-character hexadecimal token', SecuritySeverity.MEDIUM),
            (r'\b[0-9a-fA-F]{64}\b', '64-character hexadecimal token', SecuritySeverity.MEDIUM),
            (r'(?i)password\s*=\s*["\']?[\w@#$%^&*()-+=]{8,}["\']?', 'Potential password', SecuritySeverity.CRITICAL),
            (r'(?i)api[_-]?key\s*=\s*["\']?[\w-]{16,}["\']?', 'Potential API key', SecuritySeverity.HIGH),
            (r'(?i)secret\s*=\s*["\']?[\w-]{16,}["\']?', 'Potential secret', SecuritySeverity.HIGH),
            (r'(?i)access[_-]?token\s*=\s*["\']?[\w-]{16,}["\']?', 'Potential access token', SecuritySeverity.HIGH),
            (r'(?i)(aws_access_key_id|aws_secret_access_key)\s*=\s*["\']?[\w-]{16,}["\']?', 'Potential AWS credentials', SecuritySeverity.CRITICAL),
            (r'(?i)private_key\s*=\s*["\']?[-]+BEGIN\s+PRIVATE\s+KEY[-]+', 'Potential private key', SecuritySeverity.CRITICAL),
        ]
        return SensitiveDataScanner(patterns)

    @sleep_and_retry
    @limits(calls=30, period=60)
    def scan_for_sensitive_data(self, repo_path: str) -> List[SecurityFinding]:
        """
        Scans the specified repository for sensitive data like API keys, passwords, etc.
        
        Args:
            repo_path (str): The path to the GitHub repository.
        
        Returns:
            List[SecurityFinding]: A list of SecurityFinding objects containing information about potential sensitive data.
        """
        findings = self.sensitive_data_scanner.scan(repo_path)
        
        # Encrypt sensitive data
        for finding in findings:
            finding.content = self.fernet.encrypt(finding.content.encode()).decode()
        
        self.logger.info(f"Scan completed. Found {len(findings)} potential issues.")
        return findings

    @sleep_and_retry
    @limits(calls=30, period=60)
    def enforce_branch_protection_rules(self, repo_name: str, branch_name: str = 'main') -> bool:
        """
        Enforces branch protection rules on the specified branch of a GitHub repository using the GitHub API.
        
        Args:
            repo_name (str): The name of the GitHub repository.
            branch_name (str): The name of the branch to enforce protection rules on. Defaults to 'main'.
        
        Returns:
            bool: True if enforcement was successful, False otherwise.
        """
        try:
            repo = self.github.get_repo(repo_name)
            branch = repo.get_branch(branch_name)
            
            branch.edit_protection(
                required_approving_review_count=2,
                enforce_admins=True,
                dismiss_stale_reviews=True,
                require_code_owner_reviews=True,
                required_status_checks={
                    "strict": True,
                    "contexts": ["continuous-integration/travis-ci", "security/code-scanning"]
                },
                restrictions=None,
                require_linear_history=True,
                allow_force_pushes=False,
                allow_deletions=False,
                required_conversation_resolution=True,
                lock_branch=False,
                allow_fork_syncing=True
            )
            
            self.logger.info(f"Branch protection rules enforced on {branch_name} in {repo_name}")
            return True
        except GithubException as e:
            self.logger.error(f"Failed to enforce branch protection rules: {str(e)}")
            return False

    @sleep_and_retry
    @limits(calls=30, period=60)
    def audit_repository_access(self, repo_name: str) -> Dict[str, List[str]]:
        """
        Audits and reports on who has access to the specified GitHub repository using the GitHub API.
        
        Args:
            repo_name (str): The name of the GitHub repository.
        
        Returns:
            Dict[str, List[str]]: A dictionary with user roles as keys and lists of usernames with that role as values.
        """
        try:
            repo = self.github.get_repo(repo_name)
            collaborators = repo.get_collaborators()
            
            access_audit = defaultdict(list)
            
            for collaborator in collaborators:
                permissions = repo.get_collaborator_permission(collaborator)
                access_audit[permissions].append(collaborator.login)
            
            # Audit team access
            teams = repo.get_teams()
            for team in teams:
                team_permission = team.permission
                team_members = team.get_members()
                for member in team_members:
                    if member.login not in access_audit[team_permission]:
                        access_audit[team_permission].append(f"{member.login} (via {team.name})")
            
            self.logger.info(f"Access audit completed for {repo_name}")
            return dict(access_audit)
        except GithubException as e:
            self.logger.error(f"Failed to audit repository access: {str(e)}")
            return {}

    @sleep_and_retry
    @limits(calls=30, period=60)
    def check_security_vulnerabilities(self, repo_name: str) -> List[SecurityVulnerability]:
        """
        Checks for security vulnerabilities in the repository using GitHub's security features.
        
        Args:
            repo_name (str): The name of the GitHub repository.
        
        Returns:
            List[SecurityVulnerability]: A list of SecurityVulnerability objects containing vulnerability information.
        """
        try:
            repo = self.github.get_repo(repo_name)
            vulnerabilities = repo.get_vulnerability_alert()
            
            vulnerability_info = []
            for vuln in vulnerabilities:
                vulnerability_info.append(SecurityVulnerability(
                    package=vuln.package.name,
                    severity=vuln.severity,
                    description=vuln.description,
                    affected_range=vuln.affected_range,
                    fixed_in=vuln.fixed_in,
                    cve_id=vuln.cve_id if hasattr(vuln, 'cve_id') else None,
                    references=vuln.references if hasattr(vuln, 'references') else []
                ))
            
            self.logger.info(f"Vulnerability check completed for {repo_name}")
            return vulnerability_info
        except GithubException as e:
            self.logger.error(f"Failed to check security vulnerabilities: {str(e)}")
            return []

    @sleep_and_retry
    @limits(calls=30, period=60)
    def enable_security_features(self, repo_name: str) -> Dict[str, bool]:
        """
        Enables various security features for the repository.
        
        Args:
            repo_name (str): The name of the GitHub repository.
        
        Returns:
            Dict[str, bool]: A dictionary indicating which features were successfully enabled.
        """
        try:
            repo = self.github.get_repo(repo_name)
            results = {}
            
            # Enable Dependabot alerts
            try:
                repo.enable_vulnerability_alert()
                results['dependabot_alerts'] = True
            except GithubException:
                results['dependabot_alerts'] = False
            
            # Enable automated security fixes
            try:
                repo.enable_automated_security_fixes()
                results['automated_security_fixes'] = True
            except GithubException:
                results['automated_security_fixes'] = False
            
            # Enable code scanning alerts (requires GitHub Advanced Security)
            if repo.get_license() and repo.get_license().spdx_id != "UNLICENSED":
                try:
                    repo.enable_code_scanning_default_setup()
                    results['code_scanning'] = True
                except GithubException:
                    results['code_scanning'] = False
            else:
                results['code_scanning'] = False
            
            # Enable secret scanning
            try:
                repo.enable_secret_scanning()
                results['secret_scanning'] = True
            except GithubException:
                results['secret_scanning'] = False
            
            # Enable Dependabot security updates
            try:
                repo.enable_dependabot_security_updates()
                results['dependabot_security_updates'] = True
            except GithubException:
                results['dependabot_security_updates'] = False
            
            self.logger.info(f"Security features enabled for {repo_name}: {results}")
            return results
        except GithubException as e:
            self.logger.error(f"Failed to enable security features: {str(e)}")
            return {feature: False for feature in ['dependabot_alerts', 'automated_security_fixes', 'code_scanning', 'secret_scanning', 'dependabot_security_updates']}

    @sleep_and_retry
    @limits(calls=30, period=60)
    def generate_security_report(self, repo_name: str) -> SecurityReport:
        """
        Generates a comprehensive security report for the repository.
        
        Args:
            repo_name (str): The name of the GitHub repository.
        
        Returns:
            SecurityReport: A SecurityReport object containing various security metrics and information.
        """
        report = SecurityReport()
        
        # Gather all security-related information
        report.sensitive_data = self.scan_for_sensitive_data(repo_name)
        report.access_audit = self.audit_repository_access(repo_name)
        report.vulnerabilities = self.check_security_vulnerabilities(repo_name)
        
        # Add branch protection status
        repo = self.github.get_repo(repo_name)
        default_branch = repo.default_branch
        branch = repo.get_branch(default_branch)
        report.branch_protection = branch.protected
        
        # Add security feature status
        report.security_features = {
            'dependabot_alerts': repo.get_vulnerability_alert(),
            'automated_security_fixes': repo.get_automated_security_fixes(),
            'code_scanning': repo.get_code_scanning_default_setup(),
            'secret_scanning': repo.get_secret_scanning(),
            'dependabot_security_updates': repo.get_dependabot_security_updates()
        }
        
        # Add code quality metrics
        report.code_quality_metrics = self.get_code_quality_metrics(repo_name)
        
        # Add dependency audit
        report.dependency_audit = self.audit_dependencies(repo_name)
        
        # Check for security policy
        report.security_policy = self.check_security_policy(repo_name)
        
        # Check for two-factor authentication
        report.two_factor_auth = self.check_two_factor_auth(repo_name)
        
        # Check for signed commits
        report.signed_commits = self.check_signed_commits(repo_name)
        
        self.logger.info(f"Security report generated for {repo_name}")
        return report

    def export_report_to_json(self, report: SecurityReport, output_file: str) -> None:
        """
        Exports the security report to a JSON file.
        
        Args:
            report (SecurityReport): The security report to export.
            output_file (str): The path to the output JSON file.
        """
        with open(output_file, 'w') as f:
            json.dump(report.__dict__, f, indent=2, default=lambda o: o.__dict__)
        self.logger.info(f"Security report exported to {output_file}")

    def get_code_quality_metrics(self, repo_name: str) -> Dict[str, Any]:
        """
        Retrieves code quality metrics for the repository.
        
        Args:
            repo_name (str): The name of the GitHub repository.
        
        Returns:
            Dict[str, Any]: A dictionary containing various code quality metrics.
        """
        # This is a placeholder. In a real-world scenario, you might integrate with
        # services like SonarQube or use GitHub's code scanning API for more detailed metrics.
        return {
            "lines_of_code": self._count_lines_of_code(repo_name),
            "code_smells": self._count_code_smells(repo_name),
            "test_coverage": self._get_test_coverage(repo_name),
        }

    def _count_lines_of_code(self, repo_name: str) -> int:
        """Placeholder implementation."""
        return 0


# Example usage:
# security = GitHubRepoSecurity()
# report = security.generate_security_report("owner/repo")
# security.export_report_to_json(report, "security_report.json")
