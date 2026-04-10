# Architecture

The Ethical Hacking AI Agent is modular and consists of several components:

- **Orchestrator**: Manages the scan workflow, loads detectors, and handles reporting.
- **File System**: Walks directories, classifies files, and ignores patterns.
- **Parsers**: Language-specific extractors that produce ParsedFile objects.
- **Detectors**: Modules that analyze parsed data and generate Findings.
- **Secrets Detector**: Finds hardcoded secrets using regex and entropy.
- **Dependency Analyzer**: Scans package files for known vulnerabilities.
- **Dynamic Tester**: Launches a local server and runs dynamic tests.
- **Knowledge Base**: Local CWE descriptions, CVE cache, YARA rules.
- **Reporting**: Generates reports in various formats.
- **Web UI**: Flask dashboard to start scans and view results.
- **Utilities**: Logging, config, deduplicator, CVSS calculator, etc.

Data flow: Target folder → FileWalker → FileClassifier → Parsers → Detectors → Deduplicator → CVSS scoring → Report generation.