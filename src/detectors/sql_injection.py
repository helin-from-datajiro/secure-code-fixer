"""
SQL Injection Detector
Detects potential SQL injection vulnerabilities in Python code
"""

import re
from typing import List, Dict


class SQLInjectionDetector:
    """Detects SQL injection vulnerabilities"""
    
    def __init__(self, scanner):
        self.scanner = scanner
        
    def detect(self) -> List[Dict]:
        """Detect SQL injection vulnerabilities"""
        vulnerabilities = []
        
        # Pattern 1: String formatting in SQL queries
        patterns = [
            r'execute\s*\(\s*["\'].*?%s.*?["\'].*?%',  # cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)
            r'execute\s*\(\s*["\'].*?\{.*?\}.*?["\'].*?\.format',  # cursor.execute("SELECT * FROM users WHERE id = {}".format(user_id))
            r'execute\s*\(\s*f["\'].*?\{.*?\}.*?["\']',  # cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
            r'execute\s*\(\s*["\'].*?\+',  # cursor.execute("SELECT * FROM users WHERE id = " + user_id)
        ]
        
        for pattern in patterns:
            matches = self.scanner.find_pattern(pattern, re.IGNORECASE)
            for line_num, line, match in matches:
                # Skip if it's a comment
                if line.strip().startswith('#'):
                    continue
                    
                vuln = self.scanner.create_vulnerability(
                    vuln_type='SQL_INJECTION',
                    line_num=line_num,
                    description='Potential SQL Injection vulnerability detected. SQL query uses string formatting which can be exploited.',
                    severity='CRITICAL',
                    code_snippet=line.strip(),
                    recommendation='Use parameterized queries instead. Example: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))'
                )
                vulnerabilities.append(vuln)
        
        # Pattern 2: Raw SQL with concatenation
        raw_sql_pattern = r'(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE).*?\+.*?["\']'
        matches = self.scanner.find_pattern(raw_sql_pattern, re.IGNORECASE)
        
        for line_num, line, match in matches:
            if line.strip().startswith('#'):
                continue
                
            # Check if not already detected
            if not any(v['line'] == line_num for v in vulnerabilities):
                vuln = self.scanner.create_vulnerability(
                    vuln_type='SQL_INJECTION',
                    line_num=line_num,
                    description='SQL query uses string concatenation which is vulnerable to SQL injection.',
                    severity='CRITICAL',
                    code_snippet=line.strip(),
                    recommendation='Use parameterized queries with placeholders instead of string concatenation.'
                )
                vulnerabilities.append(vuln)
        
        return vulnerabilities
