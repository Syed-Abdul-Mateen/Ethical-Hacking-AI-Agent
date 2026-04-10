import os, glob

for f in glob.glob('src/detectors/**/*.py', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    original_content = content
    content = content.replace('line_number=', 'line_start=')
    content = content.replace('class SQLInjectionDetector', 'class SqlInjectionDetector')
    content = content.replace('class ReflectedXSSDetector', 'class ReflectedXssDetector')
    content = content.replace('class StoredXSSDetector', 'class StoredXssDetector')
    content = content.replace('class DOMXSSDetector', 'class DomXssDetector')
    content = content.replace('class GraphQLIntrospectionDetector', 'class GraphqlIntrospectionDetector')
    
    if content != original_content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
