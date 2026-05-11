"""Cryptography vulnerability detectors."""


def __getattr__(name):
    _registry = {
        "WeakEncryptionDetector": "src.detectors.crypto.weak_encryption",
        "HardcodedSecretsDetector": "src.detectors.crypto.hardcoded_secrets",
        "InsecureRandomDetector": "src.detectors.crypto.insecure_random",
    }
    if name in _registry:
        import importlib
        module = importlib.import_module(_registry[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["WeakEncryptionDetector", "HardcodedSecretsDetector", "InsecureRandomDetector"]
