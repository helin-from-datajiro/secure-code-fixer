"""
Hardcoded Secrets Detector
Detects hardcoded passwords, API keys, and other sensitive credentials
"""

import re
from typing import List, Dict


class HardcodedSecretsDetector:
    """Detects hardcoded secrets and credentials"""
    
    def __init__(self, scanner):
        self.scanner = scanner
        
    def detect(self) -> List[Dict]:
        """Detect hardcoded secrets"""
        vulnerabilities = []
        
        # Patterns for common secret variable names
        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password'),
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key'),
            (r'secret_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret key'),
            (r'access_token\s*=\s*["\'][^"\']+["\']', 'Hardcoded access token'),
            (r'private_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded private key'),
            (r'aws_secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded AWS secret'),
            (r'db_password\s*=\s*["\'][^"\']+["\']', 'Hardcoded database password'),
        ]
        
        for pattern, secret_type in secret_patterns:
            matches = self.scanner.find_pattern(pattern, re.IGNORECASE)
            for line_num, line, match in matches:
                if line.strip().startswith('#'):
                    continue
                
                # Skip if it's an empty string or placeholder
                matched_text = match.group(0)
                if '""' in matched_text or "''" in matched_text:
                    continue
                if any(placeholder in matched_text.lower() for placeholder in ['your_', 'example', 'placeholder', 'xxx', 'test']):
                    continue
                
                vuln = self.scanner.create_vulnerability(
                    vuln_type='HARDCODED_SECRETS',
                    line_num=line_num,
                    description=f'{secret_type} detected in source code. This is a security risk.',
                    severity='CRITICAL',
                    code_snippet=line.strip(),
                    recommendation='Never hardcode secrets in source code. Use environment variables, configuration files (not in version control), or secret management services like AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault.'
                )
                vulnerabilities.append(vuln)
        
        # Pattern for potential API keys (long alphanumeric strings)
        api_key_pattern = r'["\'][A-Za-z0-9]{32,}["\']'
        matches = self.scanner.find_pattern(api_key_pattern)
        
        for line_num, line, match in matches:
            if line.strip().startswith('#'):
                continue
            
            # Skip if already detected
            if any(v['line'] == line_num for v in vulnerabilities):
                continue
            
            # Check if it looks like a real key (has mixed case and numbers)
            key_value = match.group(0).strip('"\'')
            if re.search(r'[A-Z]', key_value) and re.search(r'[a-z]', key_value) and re.search(r'[0-9]', key_value):
                vuln = self.scanner.create_vulnerability(
                    vuln_type='HARDCODED_SECRETS',
                    line_num=line_num,
                    description='Potential hardcoded API key or secret detected (long alphanumeric string).',
                    severity='HIGH',
                    code_snippet=line.strip(),
                    recommendation='If this is a secret or API key, move it to environment variables or a secure secret management system.'
                )
                vulnerabilities.append(vuln)
        
        return vulnerabilities
