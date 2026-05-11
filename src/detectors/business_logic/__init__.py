"""Business logic vulnerability detectors."""


def __getattr__(name):
    _registry = {
        "WorkflowBypassDetector": "src.detectors.business_logic.workflow_bypass",
        "RaceConditionDetector": "src.detectors.business_logic.race_condition",
    }
    if name in _registry:
        import importlib
        module = importlib.import_module(_registry[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["WorkflowBypassDetector", "RaceConditionDetector"]
