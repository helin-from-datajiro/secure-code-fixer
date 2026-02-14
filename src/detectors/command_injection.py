"""
Command Injection Detector
Detects potential command injection vulnerabilities
"""

import re
from typing import List, Dict


class CommandInjectionDetector:
    """Detects command injection vulnerabilities"""
    
    def __init__(self, scanner):
        self.scanner = scanner
        
    def detect(self) -> List[Dict]:
        """Detect command injection vulnerabilities"""
        vulnerabilities = []
        
        # Dangerous functions that execute system commands
        dangerous_functions = [
            r'os\.system\s*\(',
            r'subprocess\.call\s*\(',
            r'subprocess\.run\s*\(',
            r'subprocess\.Popen\s*\(',
            r'os\.popen\s*\(',
            r'eval\s*\(',
            r'exec\s*\(',
        ]
        
        for pattern in dangerous_functions:
            matches = self.scanner.find_pattern(pattern, re.IGNORECASE)
            for line_num, line, match in matches:
                if line.strip().startswith('#'):
                    continue
                
                # Check if user input is used (common variable names)
                user_input_indicators = ['input', 'request', 'user', 'param', 'arg', 'data', 'f"', "f'", '.format(', '%']
                
                has_user_input = any(indicator in line for indicator in user_input_indicators)
                
                if has_user_input:
                    severity = 'CRITICAL'
                    description = 'Command injection vulnerability detected. User input is used in system command execution.'
                    recommendation = 'Avoid using user input in system commands. If necessary, use subprocess with shell=False and validate/sanitize all inputs.'
                else:
                    severity = 'MEDIUM'
                    description = 'Potentially dangerous system command execution detected.'
                    recommendation = 'Review this code to ensure no user input can reach this command. Consider using safer alternatives.'
                
                vuln = self.scanner.create_vulnerability(
                    vuln_type='COMMAND_INJECTION',
                    line_num=line_num,
                    description=description,
                    severity=severity,
                    code_snippet=line.strip(),
                    recommendation=recommendation
                )
                vulnerabilities.append(vuln)
        
        return vulnerabilities
