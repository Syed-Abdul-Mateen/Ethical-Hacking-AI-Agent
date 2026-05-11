"""Deserialization vulnerability detectors."""


def __getattr__(name):
    _registry = {
        "PythonPickleDetector": "src.detectors.deserialization.python_pickle",
        "PHPDeserializeDetector": "src.detectors.deserialization.php_deserialize",
        "JavaSerializationDetector": "src.detectors.deserialization.java_serialization",
    }
    if name in _registry:
        import importlib
        module = importlib.import_module(_registry[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["PythonPickleDetector", "PHPDeserializeDetector", "JavaSerializationDetector"]
