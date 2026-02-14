"""
JSON Reporter
Generates JSON format vulnerability report
"""

import json
from typing import List, Dict


class JSONReporter:
    """Generates JSON report for vulnerabilities"""
    
    def __init__(self, vulnerabilities: List[Dict]):
        self.vulnerabilities = vulnerabilities
        
    def generate(self, output_file: str):
        """Generate JSON report"""
        report = {
            'total_vulnerabilities': len(self.vulnerabilities),
            'vulnerabilities': self.vulnerabilities,
            'summary': self._generate_summary()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    
    def _generate_summary(self) -> Dict:
        """Generate summary statistics"""
        summary = {
            'by_severity': {},
            'by_type': {},
            'by_file': {}
        }
        
        for vuln in self.vulnerabilities:
            # Count by severity
            severity = vuln.get('severity', 'UNKNOWN')
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
            
            # Count by type
            vuln_type = vuln.get('type', 'UNKNOWN')
            summary['by_type'][vuln_type] = summary['by_type'].get(vuln_type, 0) + 1
            
            # Count by file
            file_path = vuln.get('file', 'UNKNOWN')
            summary['by_file'][file_path] = summary['by_file'].get(file_path, 0) + 1
        
        return summary
