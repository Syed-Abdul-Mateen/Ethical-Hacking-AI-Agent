"""Access control vulnerability detectors."""


def __getattr__(name):
    _registry = {
        "IDORDetector": "src.detectors.access_control.idor_patterns",
        "MissingFunctionLevelDetector": "src.detectors.access_control.missing_function_level",
    }
    if name in _registry:
        import importlib
        module = importlib.import_module(_registry[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["IDORDetector", "MissingFunctionLevelDetector"]
