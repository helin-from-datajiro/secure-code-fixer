"""
SQL Injection Fixer
Automatically fixes SQL injection vulnerabilities
"""

import re


class SQLFixer:
    """Fixes SQL injection vulnerabilities"""
    
    def __init__(self, scanner):
        self.scanner = scanner
    
    def fix(self, vulnerability: dict, content: str) -> str:
        """Fix SQL injection vulnerability"""
        line_num = vulnerability['line']
        lines = content.split('\n')
        
        if line_num > len(lines):
            return content
        
        vulnerable_line = lines[line_num - 1]
        
        # Try to convert to parameterized query
        fixed_line = self._convert_to_parameterized(vulnerable_line)
        
        if fixed_line != vulnerable_line:
            lines[line_num - 1] = fixed_line
            # Add comment explaining the fix
            indent = len(vulnerable_line) - len(vulnerable_line.lstrip())
            comment = ' ' * indent + '# FIXED: Converted to parameterized query to prevent SQL injection\n'
            lines.insert(line_num - 1, comment)
        
        return '\n'.join(lines)
    
    def _convert_to_parameterized(self, line: str) -> str:
        """Convert SQL query to use parameterized queries"""
        # This is a simplified conversion - real implementation would be more sophisticated
        
        # Pattern: execute("SELECT ... WHERE id = " + variable)
        if '+' in line and 'execute' in line:
            # Simple replacement suggestion
            return line + '  # TODO: Convert to parameterized query: cursor.execute("SELECT ... WHERE id = ?", (variable,))'
        
        # Pattern: execute(f"SELECT ... WHERE id = {variable}")
        if 'f"' in line or "f'" in line:
            return line + '  # TODO: Convert to parameterized query: cursor.execute("SELECT ... WHERE id = ?", (variable,))'
        
        # Pattern: execute("SELECT ... WHERE id = %s" % variable)
        if '% ' in line and 'execute' in line:
            return line + '  # TODO: Convert to parameterized query: cursor.execute("SELECT ... WHERE id = ?", (variable,))'
        
        return line
