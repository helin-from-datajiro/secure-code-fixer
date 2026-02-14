#!/usr/bin/env python3
"""
Secure Code Fixer - Main Application
Automatically detects and fixes security vulnerabilities in source code
Author: Helin Turan
Date: February 2026
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict
import json

from scanner.python_scanner import PythonScanner
from reporters.console_reporter import ConsoleReporter
from reporters.json_reporter import JSONReporter
from reporters.html_reporter import HTMLReporter


class SecureCodeFixer:
    """Main application class for Secure Code Fixer"""
    
    def __init__(self, target_path: str, auto_fix: bool = False):
        self.target_path = Path(target_path)
        self.auto_fix = auto_fix
        self.vulnerabilities = []
        self.fixed_count = 0
        
    def scan(self) -> List[Dict]:
        """Scan target path for vulnerabilities"""
        print(f"[*] Scanning: {self.target_path}")
        
        if self.target_path.is_file():
            files = [self.target_path]
        else:
            files = list(self.target_path.rglob("*.py"))
        
        print(f"[*] Found {len(files)} Python files to scan\n")
        
        for file_path in files:
            print(f"  Scanning: {file_path.name}")
            scanner = PythonScanner(str(file_path))
            file_vulns = scanner.scan()
            
            if file_vulns:
                self.vulnerabilities.extend(file_vulns)
                print(f"    [!] Found {len(file_vulns)} vulnerabilities")
                
                if self.auto_fix:
                    fixed = scanner.fix_vulnerabilities(file_vulns)
                    self.fixed_count += fixed
                    print(f"    [+] Fixed {fixed} vulnerabilities")
            else:
                print(f"    [OK] No vulnerabilities found")
        
        return self.vulnerabilities
    
    def generate_reports(self, output_dir: str = "reports"):
        """Generate vulnerability reports"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Console report
        console_reporter = ConsoleReporter(self.vulnerabilities)
        console_reporter.generate()
        
        # JSON report
        json_reporter = JSONReporter(self.vulnerabilities)
        json_file = output_path / "vulnerability_report.json"
        json_reporter.generate(str(json_file))
        print(f"\n[*] JSON report saved: {json_file}")
        
        # HTML report
        html_reporter = HTMLReporter(self.vulnerabilities)
        html_file = output_path / "vulnerability_report.html"
        html_reporter.generate(str(html_file))
        print(f"[*] HTML report saved: {html_file}")
        
    def print_summary(self):
        """Print scan summary"""
        print("\n" + "="*60)
        print("SCAN SUMMARY")
        print("="*60)
        print(f"Total vulnerabilities found: {len(self.vulnerabilities)}")
        
        if self.auto_fix:
            print(f"Vulnerabilities fixed: {self.fixed_count}")
            print(f"Remaining vulnerabilities: {len(self.vulnerabilities) - self.fixed_count}")
        
        # Count by severity
        severity_count = {}
        for vuln in self.vulnerabilities:
            severity = vuln.get('severity', 'UNKNOWN')
            severity_count[severity] = severity_count.get(severity, 0) + 1
        
        print("\nBy Severity:")
        for severity, count in sorted(severity_count.items()):
            print(f"  {severity}: {count}")
        
        # Count by type
        type_count = {}
        for vuln in self.vulnerabilities:
            vuln_type = vuln.get('type', 'UNKNOWN')
            type_count[vuln_type] = type_count.get(vuln_type, 0) + 1
        
        print("\nBy Type:")
        for vuln_type, count in sorted(type_count.items()):
            print(f"  {vuln_type}: {count}")
        
        print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Secure Code Fixer - Automated Security Vulnerability Detection and Fixing"
    )
    parser.add_argument(
        "target",
        help="Target file or directory to scan"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically fix detected vulnerabilities"
    )
    parser.add_argument(
        "--output",
        default="reports",
        help="Output directory for reports (default: reports)"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.target):
        print(f"❌ Error: Target path '{args.target}' does not exist")
        sys.exit(1)
    
    print("="*60)
    print("[SECURE CODE FIXER]")
    print("Automated Security Vulnerability Detection & Fixing")
    print("="*60 + "\n")
    
    fixer = SecureCodeFixer(args.target, auto_fix=args.fix)
    vulnerabilities = fixer.scan()
    
    if vulnerabilities:
        fixer.generate_reports(args.output)
        fixer.print_summary()
    else:
        print("\n[OK] No vulnerabilities found! Your code looks secure.\n")


if __name__ == "__main__":
    main()
