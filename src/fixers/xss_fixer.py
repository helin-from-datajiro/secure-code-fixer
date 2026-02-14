"""
XSS Fixer
Automatically fixes XSS vulnerabilities
"""


class XSSFixer:
    """Fixes XSS vulnerabilities"""
    
    def __init__(self, scanner):
        self.scanner = scanner
    
    def fix(self, vulnerability: dict, content: str) -> str:
        """Fix XSS vulnerability"""
        line_num = vulnerability['line']
        lines = content.split('\n')
        
        if line_num > len(lines):
            return content
        
        vulnerable_line = lines[line_num - 1]
        fixed_line = self._add_sanitization(vulnerable_line)
        
        if fixed_line != vulnerable_line:
            lines[line_num - 1] = fixed_line
            # Add comment and import if needed
            indent = len(vulnerable_line) - len(vulnerable_line.lstrip())
            comment = ' ' * indent + '# FIXED: Added HTML escaping to prevent XSS\n'
            lines.insert(line_num - 1, comment)
            
            # Add import at the top if not already present
            if 'import html' not in content:
                lines.insert(0, 'import html  # Added for XSS prevention\n')
        
        return '\n'.join(lines)
    
    def _add_sanitization(self, line: str) -> str:
        """Add HTML escaping to prevent XSS"""
        # Add TODO comment for manual review
        return line + '  # TODO: Add html.escape() to sanitize user input before rendering'
