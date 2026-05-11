"""Injection vulnerability detectors.

Import detectors lazily to avoid circular import chains.
"""


def __getattr__(name):
    """Lazy import to avoid circular imports during module loading."""
    _registry = {
        "SqlInjectionDetector": "src.detectors.injection.sql_injection",
        "CommandInjectionDetector": "src.detectors.injection.command_injection",
        "NoSQLInjectionDetector": "src.detectors.injection.nosql_injection",
        "LDAPInjectionDetector": "src.detectors.injection.ldap_injection",
        "XpathInjectionDetector": "src.detectors.injection.xpath_injection",
    }
    if name in _registry:
        import importlib
        module = importlib.import_module(_registry[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "SqlInjectionDetector",
    "CommandInjectionDetector",
    "NoSQLInjectionDetector",
    "LDAPInjectionDetector",
    "XpathInjectionDetector",
]
