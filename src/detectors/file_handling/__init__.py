"""File handling vulnerability detectors."""


def __getattr__(name):
    _registry = {
        "PathTraversalDetector": "src.detectors.file_handling.path_traversal",
        "UnsafeFileUploadDetector": "src.detectors.file_handling.unsafe_file_upload",
        "FileInclusionDetector": "src.detectors.file_handling.file_inclusion",
    }
    if name in _registry:
        import importlib
        module = importlib.import_module(_registry[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["PathTraversalDetector", "UnsafeFileUploadDetector", "FileInclusionDetector"]
