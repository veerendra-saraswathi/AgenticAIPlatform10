import time
from typing import Callable


class TimeoutExceeded(Exception):
    pass


def with_timeout(fn: Callable, timeout_ms: int, *args, **kwargs):
    """
    Enforces strict execution budget.

    FinTech relevance:
    - Fraud decisions must complete under SLA
    """

    start = time.time()
    result = fn(*args, **kwargs)
    elapsed_ms = (time.time() - start) * 1000

    if elapsed_ms > timeout_ms:
        raise TimeoutExceeded(
            f"Execution exceeded {timeout_ms}ms (actual={elapsed_ms:.2f}ms)"
        )

    return result

