"""
Path Traversal Detector
Detects potential path traversal vulnerabilities
"""

import re
from typing import List, Dict


class PathTraversalDetector:
    """Detects path traversal vulnerabilities"""
    
    def __init__(self, scanner):
        self.scanner = scanner
        
    def detect(self) -> List[Dict]:
        """Detect path traversal vulnerabilities"""
        vulnerabilities = []
        
        # File operation functions
        file_operations = [
            r'open\s*\(',
            r'os\.path\.join\s*\(',
            r'Path\s*\(',
            r'file\s*\(',
            r'\.read\s*\(',
            r'\.write\s*\(',
        ]
        
        for pattern in file_operations:
            matches = self.scanner.find_pattern(pattern, re.IGNORECASE)
            for line_num, line, match in matches:
                if line.strip().startswith('#'):
                    continue
                
                # Check if user input is used
                user_input_indicators = ['input', 'request', 'user', 'param', 'arg', 'data', 'filename', 'filepath', 'f"', "f'", '.format(', '%']
                
                has_user_input = any(indicator in line for indicator in user_input_indicators)
                
                # Check for path traversal patterns
                has_traversal_pattern = '..' in line or '../' in line or '..\\' in line
                
                if has_user_input:
                    severity = 'HIGH'
                    description = 'Path traversal vulnerability detected. User input is used in file operations without validation.'
                    recommendation = 'Validate and sanitize file paths. Use os.path.abspath() and check if the result is within allowed directory. Never trust user input for file paths.'
                    
                    vuln = self.scanner.create_vulnerability(
                        vuln_type='PATH_TRAVERSAL',
                        line_num=line_num,
                        description=description,
                        severity=severity,
                        code_snippet=line.strip(),
                        recommendation=recommendation
                    )
                    vulnerabilities.append(vuln)
                elif has_traversal_pattern:
                    severity = 'MEDIUM'
                    description = 'Potential path traversal pattern detected in file operation.'
                    recommendation = 'Review this code to ensure path traversal is intentional and secure.'
                    
                    vuln = self.scanner.create_vulnerability(
                        vuln_type='PATH_TRAVERSAL',
                        line_num=line_num,
                        description=description,
                        severity=severity,
                        code_snippet=line.strip(),
                        recommendation=recommendation
                    )
                    vulnerabilities.append(vuln)
        
        return vulnerabilities
