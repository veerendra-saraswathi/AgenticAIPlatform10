from typing import Callable, Dict, Any


class ReflectionFailed(Exception):
    pass


def reflect(primary_fn: Callable, validator_fn: Callable, context: Dict[str, Any]):
    """
    Runs a self-check after decision.

    FinTech use:
    - reduce false positives
    - enforce confidence thresholds
    """

    result = primary_fn(context)
    ok = validator_fn(result, context)

    if not ok:
        raise ReflectionFailed("Self-check failed")

    return result

