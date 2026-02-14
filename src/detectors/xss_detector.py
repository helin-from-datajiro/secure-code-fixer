"""
XSS (Cross-Site Scripting) Detector
Detects potential XSS vulnerabilities in Python web applications
"""

import re
from typing import List, Dict


class XSSDetector:
    """Detects XSS vulnerabilities"""
    
    def __init__(self, scanner):
        self.scanner = scanner
        
    def detect(self) -> List[Dict]:
        """Detect XSS vulnerabilities"""
        vulnerabilities = []
        
        # Pattern 1: Direct rendering of user input in Flask/Django templates
        patterns = [
            r'render_template\s*\(.*?\|safe',  # Flask: {{ user_input|safe }}
            r'mark_safe\s*\(',  # Django: mark_safe(user_input)
            r'\.write\s*\(\s*["\']<.*?\{.*?\}.*?["\']',  # response.write(f"<div>{user_input}</div>")
            r'\.write\s*\(.*?\+.*?["\']<',  # response.write("<div>" + user_input + "</div>")
        ]
        
        for pattern in patterns:
            matches = self.scanner.find_pattern(pattern, re.IGNORECASE)
            for line_num, line, match in matches:
                if line.strip().startswith('#'):
                    continue
                    
                vuln = self.scanner.create_vulnerability(
                    vuln_type='XSS',
                    line_num=line_num,
                    description='Potential XSS vulnerability. User input is rendered without proper sanitization.',
                    severity='HIGH',
                    code_snippet=line.strip(),
                    recommendation='Always sanitize user input before rendering. Use template auto-escaping or html.escape() function.'
                )
                vulnerabilities.append(vuln)
        
        # Pattern 2: innerHTML or similar DOM manipulation
        js_patterns = [
            r'innerHTML\s*=',
            r'outerHTML\s*=',
            r'document\.write\s*\(',
        ]
        
        for pattern in js_patterns:
            matches = self.scanner.find_pattern(pattern, re.IGNORECASE)
            for line_num, line, match in matches:
                if line.strip().startswith('#') or line.strip().startswith('//'):
                    continue
                    
                if not any(v['line'] == line_num for v in vulnerabilities):
                    vuln = self.scanner.create_vulnerability(
                        vuln_type='XSS',
                        line_num=line_num,
                        description='Potential XSS vulnerability in JavaScript code. Direct DOM manipulation can be exploited.',
                        severity='HIGH',
                        code_snippet=line.strip(),
                        recommendation='Use textContent instead of innerHTML, or sanitize input with DOMPurify library.'
                    )
                    vulnerabilities.append(vuln)
        
        return vulnerabilities
