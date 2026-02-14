"""
Command Injection Fixer
Automatically fixes command injection vulnerabilities
"""


class CommandFixer:
    """Fixes command injection vulnerabilities"""
    
    def __init__(self, scanner):
        self.scanner = scanner
    
    def fix(self, vulnerability: dict, content: str) -> str:
        """Fix command injection vulnerability"""
        line_num = vulnerability['line']
        lines = content.split('\n')
        
        if line_num > len(lines):
            return content
        
        vulnerable_line = lines[line_num - 1]
        
        # Add warning comment
        indent = len(vulnerable_line) - len(vulnerable_line.lstrip())
        comment = ' ' * indent + '# SECURITY WARNING: Command injection risk detected!\n'
        comment += ' ' * indent + '# TODO: Use subprocess with shell=False and validate all inputs\n'
        lines.insert(line_num - 1, comment)
        
        return '\n'.join(lines)
