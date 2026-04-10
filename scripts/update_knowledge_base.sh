#!/bin/bash
# Update knowledge base and CVE data

python3 -m src.dependency_analyzer.vuln_db_updater
python3 -m src.knowledge_base.updater
echo "Knowledge base updated."