import ipaddress
import json
from datetime import datetime, timedelta
from typing import List, Dict
import requests
from .security_base import SecurityConfigurationError

class SecurityAuditAnalyzer:
    """Enhanced real-time monitoring with threat intelligence integration"""
    
    def __init__(self, services: list, threat_api_key: str = None):
        self.services = services
        self.threat_api_key = threat_api_key
        self.anomaly_thresholds = {
            'failed_attempts': 5,
            'time_window': timedelta(minutes=5),
            'data_exfiltration_limit': 10_000_000  # 10MB
        }
        self.threat_intel_cache = {}
        
    def analyze_logs(self, logs: List[Dict]) -> Dict:
        """Comprehensive log analysis with multiple detection vectors"""
        results = {
            'brute_force': self.detect_brute_force(logs),
            'data_exfiltration': self.detect_data_exfiltration(logs),
            'suspicious_ips': self.check_threat_intel(logs)
        }
        if any(results.values()):
            self.trigger_incident_response(results)
        return results

    def detect_data_exfiltration(self, logs: List[Dict]) -> bool:
        """Identify unusual data outflow patterns"""
        total_out = sum(
            log['metadata']['compressed_size'] 
            for log in logs 
            if log['event_type'] == 'COMPRESSION_SUCCESS'
        )
        
        if total_out > self.anomaly_thresholds['data_exfiltration_limit']:
            self.log_audit_event("DATA_EXFILTRATION_SUSPECTED", {
                "total_data": total_out,
                "limit": self.anomaly_thresholds['data_exfiltration_limit']
            })
            return True
        return False

    def check_threat_intel(self, logs: List[Dict]) -> List[str]:
        """Query threat intelligence feeds for suspicious IPs"""
        suspicious_ips = []
        unique_ips = {log['metadata'].get('source_ip') for log in logs}
        
        for ip in unique_ips:
            if ip and self._is_malicious_ip(ip):
                suspicious_ips.append(ip)
                self.log_audit_event("MALICIOUS_IP_DETECTED", {"ip": ip})
                
        return suspicious_ips

    def _is_malicious_ip(self, ip: str) -> bool:
        """Check cached threat intelligence or query external API.

        The ``ip`` value originates from log metadata (source_ip), so it is
        validated as a real IP address before it is interpolated into the request
        URL — this prevents header/path injection from attacker-influenced logs
        and avoids sending the Bearer key to an unintended host.
        """
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            # Not a valid IP (possibly attacker-influenced) — never query external
            # threat-intel with it.
            return False

        if ip in self.threat_intel_cache:
            return self.threat_intel_cache[ip]

        if self.threat_api_key:
            try:
                response = requests.get(
                    f"https://api.threatintel.com/v1/ip/{ip}",
                    headers={"Authorization": f"Bearer {self.threat_api_key}"},
                    timeout=2
                )
                is_malicious = response.json().get('risk_score', 0) > 80
                self.threat_intel_cache[ip] = is_malicious
                return is_malicious
            except Exception as e:
                raise SecurityConfigurationError(
                    f"Threat intel API failed: {str(e)}"
                ) from e
        return False

    def trigger_incident_response(self, findings: Dict):
        """Automated response framework with severity grading"""
        severity = self._calculate_severity(findings)
        responses = []
        
        if severity >= 3:  # Critical
            responses.append(self._disable_affected_services())
            responses.append(self._alert_security_team(findings))
        
        if severity >= 2:  # High
            responses.append(self._rotate_credentials())
            responses.append(self._capture_forensic_snapshot())
        
        self.log_audit_event("INCIDENT_RESPONSE_ACTIVATED", {
            "severity": severity,
            "actions_taken": responses
        })

    def _calculate_severity(self, findings: Dict) -> int:
        """NIST-based severity scoring"""
        score = 0
        if findings['brute_force']:
            score += 2
        if findings['data_exfiltration']:
            score += 3
        if findings['suspicious_ips']:
            score += len(findings['suspicious_ips'])
        return min(5, score)

    def detect_brute_force(self, logs) -> bool:
        """Identify rapid successive failures.

        Returns a bool (``False`` when not a brute force) and does NOT fire the
        incident response itself — ``analyze_logs`` orchestrates incident
        activation once it holds the complete findings dict.
        """
        failures = [log for log in logs if 'FAILURE' in log['event_type']]
        time_window = self.anomaly_thresholds['time_window']

        if len(failures) > self.anomaly_thresholds['failed_attempts']:
            try:
                first = datetime.fromisoformat(failures[0]['timestamp'])
                last = datetime.fromisoformat(failures[-1]['timestamp'])
            except (KeyError, ValueError):
                return False
            if (last - first) < time_window:
                return True
        return False

    def _disable_affected_services(self):
        """Implementation of disabling affected services"""
        # Implementation needed
        pass

    def _alert_security_team(self, findings: Dict):
        """Implementation of alerting the security team"""
        # Implementation needed
        pass

    def _rotate_credentials(self):
        """Implementation of rotating credentials"""
        # Implementation needed
        pass

    def _capture_forensic_snapshot(self):
        """Implementation of capturing a forensic snapshot"""
        # Implementation needed
        pass

    def log_audit_event(self, event_type: str, metadata: Dict):
        """Implementation of logging an audit event"""
        # Implementation needed
        pass 