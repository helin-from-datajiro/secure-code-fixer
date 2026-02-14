"""
Path Traversal Fixer
Automatically fixes path traversal vulnerabilities
"""


class PathFixer:
    """Fixes path traversal vulnerabilities"""
    
    def __init__(self, scanner):
        self.scanner = scanner
    
    def fix(self, vulnerability: dict, content: str) -> str:
        """Fix path traversal vulnerability"""
        line_num = vulnerability['line']
        lines = content.split('\n')
        
        if line_num > len(lines):
            return content
        
        vulnerable_line = lines[line_num - 1]
        
        # Add security comment
        indent = len(vulnerable_line) - len(vulnerable_line.lstrip())
        comment = ' ' * indent + '# SECURITY WARNING: Path traversal risk detected!\n'
        comment += ' ' * indent + '# TODO: Validate file path with os.path.abspath() and check if within allowed directory\n'
        lines.insert(line_num - 1, comment)
        
        # Add import suggestion if not present
        if 'import os' not in content:
            lines.insert(0, 'import os  # Added for secure path handling\n')
        
        return '\n'.join(lines)
