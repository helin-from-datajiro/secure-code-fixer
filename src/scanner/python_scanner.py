"""
Python Code Scanner
Detects security vulnerabilities in Python code
"""

from typing import List, Dict
import re
from .base_scanner import BaseScanner
from detectors.sql_injection import SQLInjectionDetector
from detectors.xss_detector import XSSDetector
from detectors.command_injection import CommandInjectionDetector
from detectors.path_traversal import PathTraversalDetector
from detectors.hardcoded_secrets import HardcodedSecretsDetector
from detectors.crypto_detector import CryptoDetector
from fixers.sql_fixer import SQLFixer
from fixers.xss_fixer import XSSFixer
from fixers.command_fixer import CommandFixer
from fixers.path_fixer import PathFixer


class PythonScanner(BaseScanner):
    """Scanner for Python source code"""
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.detectors = [
            SQLInjectionDetector(self),
            XSSDetector(self),
            CommandInjectionDetector(self),
            PathTraversalDetector(self),
            HardcodedSecretsDetector(self),
            CryptoDetector(self)
        ]
        self.fixers = {
            'SQL_INJECTION': SQLFixer(self),
            'XSS': XSSFixer(self),
            'COMMAND_INJECTION': CommandFixer(self),
            'PATH_TRAVERSAL': PathFixer(self)
        }
    
    def scan(self) -> List[Dict]:
        """Scan Python file for all vulnerability types"""
        vulnerabilities = []
        
        for detector in self.detectors:
            vulns = detector.detect()
            vulnerabilities.extend(vulns)
        
        return vulnerabilities
    
    def fix_vulnerabilities(self, vulnerabilities: List[Dict]) -> int:
        """Automatically fix detected vulnerabilities"""
        fixed_count = 0
        modified_content = self.content
        
        # Sort vulnerabilities by line number (descending) to avoid line number shifts
        sorted_vulns = sorted(vulnerabilities, key=lambda x: x['line'], reverse=True)
        
        for vuln in sorted_vulns:
            vuln_type = vuln['type']
            if vuln_type in self.fixers:
                fixer = self.fixers[vuln_type]
                modified_content = fixer.fix(vuln, modified_content)
                fixed_count += 1
        
        # Write fixed content back to file
        if fixed_count > 0:
            try:
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
            except Exception as e:
                print(f"Error writing fixed content to {self.file_path}: {e}")
                return 0
        
        return fixed_count
