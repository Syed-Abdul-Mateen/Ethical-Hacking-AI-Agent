# Security Scan Report

**Target:** D:\Projects\Ethical Hacking AI Agent

**Scan Date:** 2026-05-03T23:15:46.475744

## Summary

- Files Scanned: 176
- Files Parsed: 145
- Total Findings: 217

### Findings by Severity

- **High**: 18
- **Medium**: 15
- **Low**: 184

## Detailed Findings

### Potential SQL Injection

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dependency_analyzer\vuln_db_updater.py
- **Line:** 56
- **Description:** A SQL query appears to be constructed using string concatenation or interpolation with user-controlled data. This can lead to SQL injection if the input is not properly sanitized.
- **Remediation:** Use parameterized queries or prepared statements instead of string concatenation. Escape user inputs if dynamic SQL is unavoidable.
- **CWE:** CWE-89
- **CVSS Score:** 7.5

---

### Potential SQL Injection

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dependency_analyzer\vuln_db_updater.py
- **Line:** 58
- **Description:** A SQL query appears to be constructed using string concatenation or interpolation with user-controlled data. This can lead to SQL injection if the input is not properly sanitized.
- **Remediation:** Use parameterized queries or prepared statements instead of string concatenation. Escape user inputs if dynamic SQL is unavoidable.
- **CWE:** CWE-89
- **CVSS Score:** 7.5

---

### Potential SQL Injection

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\deserialization\python_pickle.py
- **Line:** 89
- **Description:** A SQL query appears to be constructed using string concatenation or interpolation with user-controlled data. This can lead to SQL injection if the input is not properly sanitized.
- **Remediation:** Use parameterized queries or prepared statements instead of string concatenation. Escape user inputs if dynamic SQL is unavoidable.
- **CWE:** CWE-89
- **CVSS Score:** 7.5

---

### Potential SQL Injection

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\ai_analyzer.py
- **Line:** 58
- **Description:** A SQL query appears to be constructed using string concatenation or interpolation with user-controlled data. This can lead to SQL injection if the input is not properly sanitized.
- **Remediation:** Use parameterized queries or prepared statements instead of string concatenation. Escape user inputs if dynamic SQL is unavoidable.
- **CWE:** CWE-89
- **CVSS Score:** 7.5

---

### Potential SQL Injection

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\planner.py
- **Line:** 59
- **Description:** A SQL query appears to be constructed using string concatenation or interpolation with user-controlled data. This can lead to SQL injection if the input is not properly sanitized.
- **Remediation:** Use parameterized queries or prepared statements instead of string concatenation. Escape user inputs if dynamic SQL is unavoidable.
- **CWE:** CWE-89
- **CVSS Score:** 7.5

---

### Potential SQL Injection

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\planner.py
- **Line:** 77
- **Description:** A SQL query appears to be constructed using string concatenation or interpolation with user-controlled data. This can lead to SQL injection if the input is not properly sanitized.
- **Remediation:** Use parameterized queries or prepared statements instead of string concatenation. Escape user inputs if dynamic SQL is unavoidable.
- **CWE:** CWE-89
- **CVSS Score:** 7.5

---

### Potential SQL Injection

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\tests\test_detectors\test_sql_injection.py
- **Line:** 47
- **Description:** A SQL query appears to be constructed using string concatenation or interpolation with user-controlled data. This can lead to SQL injection if the input is not properly sanitized.
- **Remediation:** Use parameterized queries or prepared statements instead of string concatenation. Escape user inputs if dynamic SQL is unavoidable.
- **CWE:** CWE-89
- **CVSS Score:** 7.5

---

### Potential SQL Injection

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\tests\test_detectors\test_sql_injection.py
- **Line:** 61
- **Description:** A SQL query appears to be constructed using string concatenation or interpolation with user-controlled data. This can lead to SQL injection if the input is not properly sanitized.
- **Remediation:** Use parameterized queries or prepared statements instead of string concatenation. Escape user inputs if dynamic SQL is unavoidable.
- **CWE:** CWE-89
- **CVSS Score:** 7.5

---

### Potential SQL Injection

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\tests\test_detectors\test_sql_injection.py
- **Line:** 74
- **Description:** A SQL query appears to be constructed using string concatenation or interpolation with user-controlled data. This can lead to SQL injection if the input is not properly sanitized.
- **Remediation:** Use parameterized queries or prepared statements instead of string concatenation. Escape user inputs if dynamic SQL is unavoidable.
- **CWE:** CWE-89
- **CVSS Score:** 7.5

---

### Potential SQL Injection

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\tests\test_detectors\test_sql_injection.py
- **Line:** 101
- **Description:** A SQL query appears to be constructed using string concatenation or interpolation with user-controlled data. This can lead to SQL injection if the input is not properly sanitized.
- **Remediation:** Use parameterized queries or prepared statements instead of string concatenation. Escape user inputs if dynamic SQL is unavoidable.
- **CWE:** CWE-89
- **CVSS Score:** 7.5

---

### Potential SQL Injection

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\tests\test_parsers\test_python_parser.py
- **Line:** 33
- **Description:** A SQL query appears to be constructed using string concatenation or interpolation with user-controlled data. This can lead to SQL injection if the input is not properly sanitized.
- **Remediation:** Use parameterized queries or prepared statements instead of string concatenation. Escape user inputs if dynamic SQL is unavoidable.
- **CWE:** CWE-89
- **CVSS Score:** 7.5

---

### Potential SQL Injection

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\web_ui\app.py
- **Line:** 66
- **Description:** A SQL query appears to be constructed using string concatenation or interpolation with user-controlled data. This can lead to SQL injection if the input is not properly sanitized.
- **Remediation:** Use parameterized queries or prepared statements instead of string concatenation. Escape user inputs if dynamic SQL is unavoidable.
- **CWE:** CWE-89
- **CVSS Score:** 7.5

---

### Potential Reflected XSS

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 273
- **Description:** User input appears to be directly output to the HTML response without proper encoding or sanitization. This can lead to reflected Cross-Site Scripting (XSS) if the input contains malicious scripts.
- **Remediation:** Always escape output based on the context (HTML, JavaScript, URL, etc.). Use a templating engine that auto-escapes, or manually apply functions like htmlspecialchars() in PHP, or equivalent in other languages.
- **CWE:** CWE-79
- **CVSS Score:** 7.5

---

### Potential Reflected XSS

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 309
- **Description:** User input appears to be directly output to the HTML response without proper encoding or sanitization. This can lead to reflected Cross-Site Scripting (XSS) if the input contains malicious scripts.
- **Remediation:** Always escape output based on the context (HTML, JavaScript, URL, etc.). Use a templating engine that auto-escapes, or manually apply functions like htmlspecialchars() in PHP, or equivalent in other languages.
- **CWE:** CWE-79
- **CVSS Score:** 7.5

---

### Potential Reflected XSS

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\xss\reflected_xss.py
- **Line:** 17
- **Description:** User input appears to be directly output to the HTML response without proper encoding or sanitization. This can lead to reflected Cross-Site Scripting (XSS) if the input contains malicious scripts.
- **Remediation:** Always escape output based on the context (HTML, JavaScript, URL, etc.). Use a templating engine that auto-escapes, or manually apply functions like htmlspecialchars() in PHP, or equivalent in other languages.
- **CWE:** CWE-79
- **CVSS Score:** 7.5

---

### Potential Reflected XSS

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\xss\reflected_xss.py
- **Line:** 23
- **Description:** User input appears to be directly output to the HTML response without proper encoding or sanitization. This can lead to reflected Cross-Site Scripting (XSS) if the input contains malicious scripts.
- **Remediation:** Always escape output based on the context (HTML, JavaScript, URL, etc.). Use a templating engine that auto-escapes, or manually apply functions like htmlspecialchars() in PHP, or equivalent in other languages.
- **CWE:** CWE-79
- **CVSS Score:** 7.5

---

### Hardcoded Bearer Token

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\crypto\hardcoded_secrets.py
- **Line:** 47
- **Description:** A bearer token appears to be hardcoded in source code. Matched pattern: ***
- **Remediation:** Remove hardcoded secrets from source code. Use environment variables, a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault), or encrypted configuration files instead.
- **CWE:** CWE-798
- **CVSS Score:** 7.5

---

### Hardcoded Hardcoded Password

- **Severity:** high
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\misconfiguration\default_credentials.py
- **Line:** 34
- **Description:** A hardcoded password appears to be hardcoded in source code. Matched pattern: ***
- **Remediation:** Remove hardcoded secrets from source code. Use environment variables, a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault), or encrypted configuration files instead.
- **CWE:** CWE-259
- **CVSS Score:** 7.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\patch2.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\patch3.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\patch.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\run_web.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\setup.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\scratch\fix_signatures.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dependency_analyzer\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dependency_analyzer\package_parsers\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dependency_analyzer\package_parsers\composer_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dependency_analyzer\package_parsers\gem_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dependency_analyzer\package_parsers\pip_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dependency_analyzer\package_parsers\npm_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dependency_analyzer\package_parsers\maven_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dependency_analyzer\scanner.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dependency_analyzer\vuln_db_updater.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\access_control\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\api\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\access_control\missing_function_level.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\access_control\idor_patterns.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\api\graphql_introspection.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\api\openapi_info_leak.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\authentication\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\api\rate_limiting.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\authentication\insecure_auth.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\authentication\session_fixation.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\base_detector.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\authentication\weak_passwords.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\business_logic\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\business_logic\race_condition.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\business_logic\workflow_bypass.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\crypto\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\crypto\insecure_random.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\crypto\weak_encryption.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\deserialization\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\deserialization\python_pickle.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\deserialization\java_serialization.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\deserialization\php_deserialize.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\dos\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\dos\regex_dos.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\dos\large_allocations.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\file_handling\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\file_handling\file_inclusion.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\file_handling\path_traversal.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\file_handling\unsafe_file_upload.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\injection\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\crypto\hardcoded_secrets.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\injection\command_injection.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\injection\nosql_injection.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\injection\ldap_injection.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\misconfiguration\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\injection\xpath_injection.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\injection\sql_injection.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\misconfiguration\default_credentials.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\misconfiguration\debug_code.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\misconfiguration\missing_headers.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\xss\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\rule_engine.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\xss\dom_xss.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\xss\stored_xss.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dynamic_tester\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\xss\reflected_xss.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dynamic_tester\crawler.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\file_system\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dynamic_tester\scanner.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dynamic_tester\downloader.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dynamic_tester\server_launcher.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\file_system\file_classifier.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\knowledge_base\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\file_system\ignore_list.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\file_system\walker.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\main.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\agent.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\knowledge_base\updater.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\context.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\exceptions.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\ai_analyzer.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\planner.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\remediation_engine.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\registry.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\parsers\base_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\parsers\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\parsers\csharp_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\parsers\config_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\parsers\go_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\parsers\html_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\parsers\java_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\parsers\js_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\parsers\php_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\parsers\sql_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\parsers\ruby_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\reporting\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\parsers\python_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\reporting\exporters\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\reporting\exporters\json_exporter.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\reporting\exporters\markdown_exporter.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\reporting\exporters\html_exporter.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\reporting\exporters\pdf_exporter.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\reporting\exporters\sarif_exporter.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\reporting\generator.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\secrets_detector\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\secrets_detector\detector.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\secrets_detector\high_entropy.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\tests\conftest.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\tests\integration\test_full_scan.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\tests\test_detectors\test_sql_injection.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\tests\test_orchestrator\test_agent.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\tests\test_orchestrator\test_parsers\test_html_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\tests\test_parsers\test_python_parser.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\tests\test_utils\test_config.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\utils\config.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\tests\test_utils\test_deduplicator.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\utils\cvss_calculator.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\utils\deduplicator.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\utils\file_utils.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\utils\logger.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\utils\subprocess_wrapper.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\utils\validators.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\web_ui\api\routes.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\web_ui\app.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\web_ui\__init__.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Missing Security Headers

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\web_ui\forms.py
- **Description:** No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.
- **Remediation:** Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.
- **CWE:** CWE-693
- **CVSS Score:** 3.5

---

### Weak Encryption

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 332
- **Description:** Use of weak or deprecated cryptographic algorithm: md5
- **Remediation:** Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.
- **CWE:** CWE-326
- **CVSS Score:** 5.0

---

### Weak Encryption

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 335
- **Description:** Use of weak or deprecated cryptographic algorithm: ECB
- **Remediation:** Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.
- **CWE:** CWE-326
- **CVSS Score:** 5.0

---

### Weak Encryption

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 356
- **Description:** Use of weak or deprecated cryptographic algorithm: ECB
- **Remediation:** Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.
- **CWE:** CWE-326
- **CVSS Score:** 5.0

---

### Weak Encryption

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 359
- **Description:** Use of weak or deprecated cryptographic algorithm: ECB
- **Remediation:** Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.
- **CWE:** CWE-326
- **CVSS Score:** 5.0

---

### Weak Encryption

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 118
- **Description:** Use of weak or deprecated cryptographic algorithm: md5
- **Remediation:** Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.
- **CWE:** CWE-326
- **CVSS Score:** 5.0

---

### Weak Encryption

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1684
- **Description:** Use of weak or deprecated cryptographic algorithm: md5
- **Remediation:** Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.
- **CWE:** CWE-326
- **CVSS Score:** 5.0

---

### Weak Encryption

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 124
- **Description:** Use of weak or deprecated cryptographic algorithm: ECB
- **Remediation:** Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.
- **CWE:** CWE-326
- **CVSS Score:** 5.0

---

### Weak Encryption

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 131
- **Description:** Use of weak or deprecated cryptographic algorithm: ECB
- **Remediation:** Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.
- **CWE:** CWE-326
- **CVSS Score:** 5.0

---

### Weak Encryption

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 137
- **Description:** Use of weak or deprecated cryptographic algorithm: ECB
- **Remediation:** Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.
- **CWE:** CWE-326
- **CVSS Score:** 5.0

---

### Weak Encryption

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1690
- **Description:** Use of weak or deprecated cryptographic algorithm: ECB
- **Remediation:** Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.
- **CWE:** CWE-326
- **CVSS Score:** 5.0

---

### Weak Encryption

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1697
- **Description:** Use of weak or deprecated cryptographic algorithm: ECB
- **Remediation:** Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.
- **CWE:** CWE-326
- **CVSS Score:** 5.0

---

### Weak Encryption

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1703
- **Description:** Use of weak or deprecated cryptographic algorithm: ECB
- **Remediation:** Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.
- **CWE:** CWE-326
- **CVSS Score:** 5.0

---

### Weak Encryption

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\crypto\weak_encryption.py
- **Line:** 24
- **Description:** Use of weak or deprecated cryptographic algorithm: md5
- **Remediation:** Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.
- **CWE:** CWE-326
- **CVSS Score:** 5.0

---

### Weak Encryption

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\crypto\weak_encryption.py
- **Line:** 36
- **Description:** Use of weak or deprecated cryptographic algorithm: ECB
- **Remediation:** Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.
- **CWE:** CWE-326
- **CVSS Score:** 5.0

---

### GraphQL Introspection Enabled

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\patch3.py
- **Description:** GraphQL introspection is likely enabled. This can leak schema information.
- **Remediation:** Disable GraphQL introspection in production environments to prevent schema leakage.
- **CWE:** CWE-200
- **CVSS Score:** 3.0

---

### GraphQL Introspection Enabled

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\api\__init__.py
- **Description:** GraphQL introspection is likely enabled. This can leak schema information.
- **Remediation:** Disable GraphQL introspection in production environments to prevent schema leakage.
- **CWE:** CWE-200
- **CVSS Score:** 3.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 157
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 2514
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 2634
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 2658
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 2682
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 2706
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 2730
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 2754
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 2778
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 2802
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 2538
- **Description:** Debug code or verbose error reporting found: console.log
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 2562
- **Description:** Debug code or verbose error reporting found: var_dump
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 2586
- **Description:** Debug code or verbose error reporting found: print_r
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.html
- **Line:** 2610
- **Description:** Debug code or verbose error reporting found: debug=True
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 43
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1407
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1472
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1485
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1498
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1511
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1524
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1537
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1550
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1563
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1611
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 2971
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 3036
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 3049
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 3062
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 3075
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 3088
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 3101
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 3114
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 3127
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1420
- **Description:** Debug code or verbose error reporting found: console.log
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 2984
- **Description:** Debug code or verbose error reporting found: console.log
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1433
- **Description:** Debug code or verbose error reporting found: var_dump
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 2997
- **Description:** Debug code or verbose error reporting found: var_dump
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1446
- **Description:** Debug code or verbose error reporting found: print_r
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 3010
- **Description:** Debug code or verbose error reporting found: print_r
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 1459
- **Description:** Debug code or verbose error reporting found: debug=True
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\reports\scan_20260321_032835\report.json
- **Line:** 3023
- **Description:** Debug code or verbose error reporting found: debug=True
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\run_web.py
- **Line:** 11
- **Description:** Debug code or verbose error reporting found: debug=True
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\misconfiguration\debug_code.py
- **Line:** 26
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\misconfiguration\debug_code.py
- **Line:** 27
- **Description:** Debug code or verbose error reporting found: console.log
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\misconfiguration\debug_code.py
- **Line:** 28
- **Description:** Debug code or verbose error reporting found: var_dump
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\misconfiguration\debug_code.py
- **Line:** 29
- **Description:** Debug code or verbose error reporting found: print_r
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\misconfiguration\debug_code.py
- **Line:** 33
- **Description:** Debug code or verbose error reporting found: debug=True
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\rule_engine.py
- **Line:** 45
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\dynamic_tester\crawler.py
- **Line:** 45
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\file_system\file_classifier.py
- **Line:** 44
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\file_system\walker.py
- **Line:** 59
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\file_system\walker.py
- **Line:** 66
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\file_system\walker.py
- **Line:** 75
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\agent.py
- **Line:** 301
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\planner.py
- **Line:** 59
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\registry.py
- **Line:** 46
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Debug Code

- **Severity:** low
- **File:** D:\Projects\Ethical Hacking AI Agent\src\orchestrator\registry.py
- **Line:** 63
- **Description:** Debug code or verbose error reporting found: debug(
- **Remediation:** Remove debug code and disable verbose error messages in production. Use proper logging instead.
- **CWE:** CWE-489
- **CVSS Score:** 2.0

---

### Hardcoded Weak Password

- **Severity:** medium
- **File:** D:\Projects\Ethical Hacking AI Agent\src\detectors\misconfiguration\default_credentials.py
- **Line:** 34
- **Description:** Hardcoded weak password 'admin' found.
- **Remediation:** Do not hardcode passwords. Use environment variables or secure configuration management.
- **CWE:** CWE-259
- **CVSS Score:** 5.0

---

