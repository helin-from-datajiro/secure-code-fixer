"""
HTML Reporter
Generates HTML format vulnerability report
"""

from typing import List, Dict


class HTMLReporter:
    """Generates HTML report for vulnerabilities"""
    
    def __init__(self, vulnerabilities: List[Dict]):
        self.vulnerabilities = vulnerabilities
        
    def generate(self, output_file: str):
        """Generate HTML report"""
        html_content = self._generate_html()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _generate_html(self) -> str:
        """Generate HTML content"""
        severity_colors = {
            'CRITICAL': '#dc3545',
            'HIGH': '#fd7e14',
            'MEDIUM': '#ffc107',
            'LOW': '#28a745'
        }
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Vulnerability Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .summary-card h3 {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}
        .summary-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        .vulnerabilities {{
            padding: 30px;
        }}
        .vulnerability {{
            background: white;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .vulnerability.critical {{ border-left-color: #dc3545; }}
        .vulnerability.high {{ border-left-color: #fd7e14; }}
        .vulnerability.medium {{ border-left-color: #ffc107; }}
        .vulnerability.low {{ border-left-color: #28a745; }}
        .vulnerability-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .vulnerability-type {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }}
        .severity-badge {{
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
        }}
        .vulnerability-details {{
            color: #666;
            line-height: 1.6;
        }}
        .code-snippet {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            padding: 15px;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
        }}
        .recommendation {{
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin-top: 15px;
            border-radius: 4px;
        }}
        .recommendation strong {{
            color: #2196F3;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #dee2e6;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Security Vulnerability Report</h1>
            <p>Automated Security Analysis</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Total Vulnerabilities</h3>
                <div class="number">{len(self.vulnerabilities)}</div>
            </div>
            {self._generate_severity_cards()}
        </div>
        
        <div class="vulnerabilities">
            <h2 style="margin-bottom: 20px; color: #333;">Detected Vulnerabilities</h2>
            {self._generate_vulnerability_cards()}
        </div>
        
        <div class="footer">
            <p>Generated by Secure Code Fixer | Developed by Helin Turan</p>
        </div>
    </div>
</body>
</html>"""
        return html
    
    def _generate_severity_cards(self) -> str:
        """Generate severity summary cards"""
        severity_count = {}
        for vuln in self.vulnerabilities:
            severity = vuln.get('severity', 'UNKNOWN')
            severity_count[severity] = severity_count.get(severity, 0) + 1
        
        cards = ""
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            count = severity_count.get(severity, 0)
            if count > 0:
                cards += f"""
            <div class="summary-card">
                <h3>{severity}</h3>
                <div class="number" style="color: {self._get_severity_color(severity)};">{count}</div>
            </div>"""
        return cards
    
    def _generate_vulnerability_cards(self) -> str:
        """Generate vulnerability detail cards"""
        cards = ""
        for vuln in self.vulnerabilities:
            severity = vuln.get('severity', 'UNKNOWN').lower()
            severity_color = self._get_severity_color(vuln.get('severity', 'UNKNOWN'))
            
            cards += f"""
            <div class="vulnerability {severity}">
                <div class="vulnerability-header">
                    <div class="vulnerability-type">{vuln.get('type', 'UNKNOWN')}</div>
                    <span class="severity-badge" style="background-color: {severity_color};">
                        {vuln.get('severity', 'UNKNOWN')}
                    </span>
                </div>
                <div class="vulnerability-details">
                    <p><strong>📄 File:</strong> {vuln.get('file', 'Unknown')}</p>
                    <p><strong>📍 Line:</strong> {vuln.get('line', 'Unknown')}</p>
                    <p><strong>📝 Description:</strong> {vuln.get('description', 'No description')}</p>
                    <div class="code-snippet">
                        <strong>Code:</strong><br>
                        {vuln.get('code', 'No code snippet available')}
                    </div>
                    {self._generate_recommendation(vuln)}
                </div>
            </div>"""
        return cards
    
    def _generate_recommendation(self, vuln: Dict) -> str:
        """Generate recommendation section"""
        recommendation = vuln.get('recommendation', '')
        if recommendation:
            return f"""
                    <div class="recommendation">
                        <strong>💡 Recommendation:</strong><br>
                        {recommendation}
                    </div>"""
        return ""
    
    def _get_severity_color(self, severity: str) -> str:
        """Get color for severity level"""
        colors = {
            'CRITICAL': '#dc3545',
            'HIGH': '#fd7e14',
            'MEDIUM': '#ffc107',
            'LOW': '#28a745'
        }
        return colors.get(severity, '#6c757d')
