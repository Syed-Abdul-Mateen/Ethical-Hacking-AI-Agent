"""
Parsers for different file types.
"""

from src.parsers.base_parser import BaseParser, ParsedFile
from src.parsers.html_parser import HTMLParser
from src.parsers.js_parser import JavaScriptParser
from src.parsers.php_parser import PHPParser
from src.parsers.python_parser import PythonParser
from src.parsers.java_parser import JavaParser
from src.parsers.csharp_parser import CSharpParser
from src.parsers.ruby_parser import RubyParser
from src.parsers.go_parser import GoParser
from src.parsers.config_parser import JSONParser, YAMLParser, XMLParser, EnvParser
from src.parsers.sql_parser import SQLParser

__all__ = [
    "BaseParser",
    "ParsedFile",
    "HTMLParser",
    "JavaScriptParser",
    "PHPParser",
    "PythonParser",
    "JavaParser",
    "CSharpParser",
    "RubyParser",
    "GoParser",
    "JSONParser",
    "YAMLParser",
    "XMLParser",
    "EnvParser",
    "SQLParser",
]