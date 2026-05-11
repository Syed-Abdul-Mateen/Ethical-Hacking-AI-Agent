"""Denial of Service vulnerability detectors."""


def __getattr__(name):
    _registry = {
        "ReDoSDetector": "src.detectors.dos.regex_dos",
        "LargeAllocationsDetector": "src.detectors.dos.large_allocations",
    }
    if name in _registry:
        import importlib
        module = importlib.import_module(_registry[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["ReDoSDetector", "LargeAllocationsDetector"]
