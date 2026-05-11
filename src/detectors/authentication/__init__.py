"""Authentication vulnerability detectors."""


def __getattr__(name):
    _registry = {
        "WeakPasswordsDetector": "src.detectors.authentication.weak_passwords",
        "SessionFixationDetector": "src.detectors.authentication.session_fixation",
        "InsecureAuthDetector": "src.detectors.authentication.insecure_auth",
    }
    if name in _registry:
        import importlib
        module = importlib.import_module(_registry[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["WeakPasswordsDetector", "SessionFixationDetector", "InsecureAuthDetector"]
