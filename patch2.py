import os, glob

for f in glob.glob('src/detectors/**/*.py', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    original_content = content
    content = content.replace('parsed_file.file_path', 'parsed_file.path')
    content = content.replace('def analyze(self, parsed_file: Any) -> List[Any]:', 'def run(self, parsed_data: dict) -> list:\n        return []')
    
    if content != original_content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
