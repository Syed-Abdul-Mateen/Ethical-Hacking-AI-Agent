"""API vulnerability detectors."""


def __getattr__(name):
    _registry = {
        "GraphqlIntrospectionDetector": "src.detectors.api.graphql_introspection",
        "OpenAPIInfoLeakDetector": "src.detectors.api.openapi_info_leak",
        "RateLimitingDetector": "src.detectors.api.rate_limiting",
    }
    if name in _registry:
        import importlib
        module = importlib.import_module(_registry[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["GraphqlIntrospectionDetector", "OpenAPIInfoLeakDetector", "RateLimitingDetector"]
