"""
Base Scanner Class
Provides common functionality for all language-specific scanners
"""

from abc import ABC, abstractmethod
from typing import List, Dict
import re


class BaseScanner(ABC):
    """Abstract base class for code scanners"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.content = self._read_file()
        self.lines = self.content.split('\n')
        
    def _read_file(self) -> str:
        """Read file content"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {self.file_path}: {e}")
            return ""
    
    @abstractmethod
    def scan(self) -> List[Dict]:
        """Scan file for vulnerabilities - must be implemented by subclasses"""
        pass
    
    def create_vulnerability(self, vuln_type: str, line_num: int, 
                           description: str, severity: str = "HIGH",
                           code_snippet: str = "", recommendation: str = "") -> Dict:
        """Create a vulnerability dictionary"""
        return {
            'file': self.file_path,
            'line': line_num,
            'type': vuln_type,
            'severity': severity,
            'description': description,
            'code': code_snippet or self.lines[line_num - 1] if line_num > 0 else "",
            'recommendation': recommendation
        }
    
    def find_pattern(self, pattern: str, flags=0) -> List[tuple]:
        """Find all matches of a regex pattern in the code"""
        matches = []
        for i, line in enumerate(self.lines, 1):
            for match in re.finditer(pattern, line, flags):
                matches.append((i, line, match))
        return matches
