"""
Console Reporter
Displays vulnerability report in the console
"""

from typing import List, Dict


class ConsoleReporter:
    """Generates console output for vulnerabilities"""
    
    def __init__(self, vulnerabilities: List[Dict]):
        self.vulnerabilities = vulnerabilities
        
    def generate(self):
        """Generate console report"""
        if not self.vulnerabilities:
            return
        
        print("\n" + "="*60)
        print("VULNERABILITY REPORT")
        print("="*60 + "\n")
        
        # Group by file
        files = {}
        for vuln in self.vulnerabilities:
            file_path = vuln['file']
            if file_path not in files:
                files[file_path] = []
            files[file_path].append(vuln)
        
        for file_path, vulns in files.items():
            print(f"\nFile: {file_path}")
            print(f"   Found {len(vulns)} vulnerabilities\n")
            
            for i, vuln in enumerate(vulns, 1):
                severity_emoji = {
                    'CRITICAL': '[CRITICAL]',
                    'HIGH': '[HIGH]',
                    'MEDIUM': '[MEDIUM]',
                    'LOW': '[LOW]'
                }.get(vuln['severity'], '[UNKNOWN]')
                
                print(f"   {i}. {severity_emoji} {vuln['type']} - Line {vuln['line']}")
                print(f"      Severity: {vuln['severity']}")
                print(f"      Description: {vuln['description']}")
                print(f"      Code: {vuln['code']}")
                if vuln.get('recommendation'):
                    print(f"      Recommendation: {vuln['recommendation']}")
                print()
