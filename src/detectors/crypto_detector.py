"""
Cryptography Detector
Detects weak or insecure cryptographic practices
"""

import re
from typing import List, Dict


class CryptoDetector:
    """Detects insecure cryptography usage"""
    
    def __init__(self, scanner):
        self.scanner = scanner
        
    def detect(self) -> List[Dict]:
        """Detect insecure cryptography"""
        vulnerabilities = []
        
        # Weak hashing algorithms
        weak_hash_patterns = [
            (r'hashlib\.md5\s*\(', 'MD5 is cryptographically broken'),
            (r'hashlib\.sha1\s*\(', 'SHA1 is weak and should be avoided'),
            (r'Crypto\.Hash\.MD5', 'MD5 is cryptographically broken'),
            (r'Crypto\.Hash\.SHA1', 'SHA1 is weak and should be avoided'),
        ]
        
        for pattern, reason in weak_hash_patterns:
            matches = self.scanner.find_pattern(pattern, re.IGNORECASE)
            for line_num, line, match in matches:
                if line.strip().startswith('#'):
                    continue
                
                vuln = self.scanner.create_vulnerability(
                    vuln_type='WEAK_CRYPTO',
                    line_num=line_num,
                    description=f'Weak cryptographic algorithm detected. {reason}.',
                    severity='HIGH',
                    code_snippet=line.strip(),
                    recommendation='Use SHA-256 or SHA-3 for hashing. For password hashing, use bcrypt, scrypt, or Argon2.'
                )
                vulnerabilities.append(vuln)
        
        # Weak encryption algorithms
        weak_encryption_patterns = [
            (r'DES\.new\s*\(', 'DES encryption is obsolete and insecure'),
            (r'ARC4\.new\s*\(', 'RC4 is broken and should not be used'),
            (r'Blowfish\.new\s*\(', 'Blowfish has known weaknesses'),
        ]
        
        for pattern, reason in weak_encryption_patterns:
            matches = self.scanner.find_pattern(pattern, re.IGNORECASE)
            for line_num, line, match in matches:
                if line.strip().startswith('#'):
                    continue
                
                vuln = self.scanner.create_vulnerability(
                    vuln_type='WEAK_CRYPTO',
                    line_num=line_num,
                    description=f'Weak encryption algorithm detected. {reason}.',
                    severity='CRITICAL',
                    code_snippet=line.strip(),
                    recommendation='Use AES-256 with GCM mode for encryption. Consider using the cryptography library with Fernet for simple encryption needs.'
                )
                vulnerabilities.append(vuln)
        
        # Insecure random number generation
        insecure_random_patterns = [
            r'random\.random\s*\(',
            r'random\.randint\s*\(',
            r'random\.choice\s*\(',
        ]
        
        for pattern in insecure_random_patterns:
            matches = self.scanner.find_pattern(pattern, re.IGNORECASE)
            for line_num, line, match in matches:
                if line.strip().startswith('#'):
                    continue
                
                # Check if used in security context
                security_indicators = ['password', 'token', 'key', 'secret', 'salt', 'nonce', 'iv']
                is_security_context = any(indicator in line.lower() for indicator in security_indicators)
                
                if is_security_context:
                    vuln = self.scanner.create_vulnerability(
                        vuln_type='WEAK_CRYPTO',
                        line_num=line_num,
                        description='Insecure random number generator used in security context. The random module is not cryptographically secure.',
                        severity='HIGH',
                        code_snippet=line.strip(),
                        recommendation='Use secrets module or os.urandom() for cryptographically secure random number generation.'
                    )
                    vulnerabilities.append(vuln)
        
        return vulnerabilities
