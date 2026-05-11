"""XSS vulnerability detectors."""


def __getattr__(name):
    _registry = {
        "ReflectedXssDetector": "src.detectors.xss.reflected_xss",
        "StoredXssDetector": "src.detectors.xss.stored_xss",
        "DomXssDetector": "src.detectors.xss.dom_xss",
    }
    if name in _registry:
        import importlib
        module = importlib.import_module(_registry[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["ReflectedXssDetector", "StoredXssDetector", "DomXssDetector"]
