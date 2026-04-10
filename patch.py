import os, glob, re

# 1. Fix dummy parsers (html, sql, csharp that I created)
for f in glob.glob('src/parsers/*_parser.py'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    if 'return {"language"' in content or 'return {' in content:
        if 'from .base_parser import BaseParser' in content:
            content = content.replace('from .base_parser import BaseParser', 'from .base_parser import BaseParser, ParsedFile')
        if 'Dict[str, Any]' in content:
            content = re.sub(r'def parse\(.*?\) -> Dict\[str, Any\]:', 'def parse(self, file_path) -> ParsedFile:', content)
        # Replace dict return with ParsedFile
        content = re.sub(r'return \{\s*"language": "([^"]+)",.*?\}', r'return ParsedFile(file_path, content if \'content\' in locals() else "", "\1")', content, flags=re.DOTALL)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)

# 2. Fix all detectors
for f in glob.glob('src/detectors/**/*.py', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    original_content = content
    # Fix signature
    content = re.sub(r'def run\(self,\s*scan_context(?:[:\s]*ScanContext)?\)\s*->\s*List\[Finding\]:', 'def run(self, parsed_data: dict) -> list:', content)
    # Fix loop
    content = content.replace('for parsed_file in scan_context.parsed_files:', 'for _, parsed_file in parsed_data.items():')
    # Fix attribute access
    content = content.replace('parsed_file.parsed_data', 'getattr(parsed_file, "metadata", {})')
    content = content.replace('parsed_file.metadata', 'getattr(parsed_file, "metadata", {})')
    
    if content != original_content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
