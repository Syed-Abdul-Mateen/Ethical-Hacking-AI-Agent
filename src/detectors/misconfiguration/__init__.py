"""Misconfiguration vulnerability detectors."""


def __getattr__(name):
    _registry = {
        "MissingHeadersDetector": "src.detectors.misconfiguration.missing_headers",
        "DebugCodeDetector": "src.detectors.misconfiguration.debug_code",
        "DefaultCredentialsDetector": "src.detectors.misconfiguration.default_credentials",
    }
    if name in _registry:
        import importlib
        module = importlib.import_module(_registry[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["MissingHeadersDetector", "DebugCodeDetector", "DefaultCredentialsDetector"]
