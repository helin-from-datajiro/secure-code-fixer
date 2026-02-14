# Secure Code Fixer

🛡️ **Automated Security Vulnerability Detection and Fixing Tool**

Secure Code Fixer is a powerful static analysis tool that automatically detects and fixes common security vulnerabilities in Python code.

## Features

### 🔍 Vulnerability Detection

The tool detects the following security vulnerabilities:

1. **SQL Injection** - Detects unsafe SQL query construction
2. **Cross-Site Scripting (XSS)** - Identifies unsafe rendering of user input
3. **Command Injection** - Finds dangerous system command execution
4. **Path Traversal** - Detects unsafe file operations
5. **Hardcoded Secrets** - Identifies passwords, API keys, and credentials in code
6. **Weak Cryptography** - Detects use of broken or weak cryptographic algorithms

### 🔧 Automatic Fixing

- Automatically fixes detected vulnerabilities (when possible)
- Adds security comments and recommendations
- Suggests secure alternatives

### 📊 Comprehensive Reporting

- **Console Output** - Color-coded terminal output
- **JSON Report** - Machine-readable format for CI/CD integration
- **HTML Report** - Beautiful, interactive web-based report

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/secure-code-fixer.git
cd secure-code-fixer

# No external dependencies required - uses Python standard library
```

## Usage

### Basic Scan

Scan a single file:
```bash
python src/main.py path/to/your/file.py
```

Scan a directory:
```bash
python src/main.py path/to/your/project
```

### Auto-Fix Mode

Automatically fix detected vulnerabilities:
```bash
python src/main.py path/to/your/file.py --fix
```

### Custom Output Directory

Specify custom output directory for reports:
```bash
python src/main.py path/to/your/file.py --output my_reports
```

## Example Output

```
🔍 Scanning: vulnerable_code.py
📁 Found 1 Python files to scan

  Scanning: vulnerable_code.py
    ⚠️  Found 12 vulnerabilities

============================================================
📊 SCAN SUMMARY
============================================================
Total vulnerabilities found: 12

By Severity:
  CRITICAL: 6
  HIGH: 4
  MEDIUM: 2

By Type:
  SQL_INJECTION: 3
  XSS: 1
  COMMAND_INJECTION: 2
  PATH_TRAVERSAL: 1
  HARDCODED_SECRETS: 3
  WEAK_CRYPTO: 2
============================================================
```

## Project Structure

```
secure-code-fixer/
├── src/
│   ├── scanner/
│   │   ├── base_scanner.py          # Base scanner class
│   │   └── python_scanner.py        # Python-specific scanner
│   ├── detectors/
│   │   ├── sql_injection.py         # SQL Injection detector
│   │   ├── xss_detector.py          # XSS detector
│   │   ├── command_injection.py     # Command Injection detector
│   │   ├── path_traversal.py        # Path Traversal detector
│   │   ├── hardcoded_secrets.py     # Hardcoded credentials detector
│   │   └── crypto_detector.py       # Weak cryptography detector
│   ├── fixers/
│   │   ├── sql_fixer.py             # SQL Injection fixer
│   │   ├── xss_fixer.py             # XSS fixer
│   │   ├── command_fixer.py         # Command Injection fixer
│   │   └── path_fixer.py            # Path Traversal fixer
│   ├── reporters/
│   │   ├── console_reporter.py      # Console output
│   │   ├── json_reporter.py         # JSON report generator
│   │   └── html_reporter.py         # HTML report generator
│   └── main.py                      # Main application
├── tests/
│   └── vulnerable_samples/          # Test files with vulnerabilities
├── docs/
│   └── README.md                    # This file
└── requirements.txt                 # Python dependencies
```

## Development Roadmap

### Phase 1 (Completed) ✅
- [x] Core scanner engine
- [x] 6 vulnerability detectors
- [x] 4 automatic fixers
- [x] 3 report formats (Console, JSON, HTML)
- [x] Test samples

### Phase 2 (In Progress) 🔄
- [ ] Web interface (Flask/Django)
- [ ] More language support (JavaScript, Java, C#)
- [ ] Machine Learning-based detection
- [ ] CI/CD integration (GitHub Actions, GitLab CI)

### Phase 3 (Planned) 📋
- [ ] IDE plugins (VS Code, PyCharm)
- [ ] Real-time code analysis
- [ ] Custom rule engine
- [ ] Metrics dashboard

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Author

**Helin Turan**  
Cybersecurity Researcher  
February 2026

## Acknowledgments

- OWASP Top 10 for security vulnerability classifications
- Python security best practices from PEP 8 and security guidelines

---

⚠️ **Disclaimer**: This tool is for educational and security testing purposes only. Always review automatically generated fixes before deploying to production.
