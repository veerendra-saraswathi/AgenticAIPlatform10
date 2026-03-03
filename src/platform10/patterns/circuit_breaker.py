from datetime import datetime, timedelta
from typing import Callable


class CircuitBreakerOpen(Exception):
    pass


class CircuitBreaker:
    """
    Prevents repeated execution when failure rate exceeds threshold.

    Enterprise use:
    - Stop runaway fraud systems
    - Protect downstream services
    """

    def __init__(self, failure_threshold: int, reset_after_seconds: int):
        self.failure_threshold = failure_threshold
        self.reset_after = timedelta(seconds=reset_after_seconds)
        self.failure_count = 0
        self.last_failure_at = None
        self.opened_at = None

    def call(self, fn: Callable, *args, **kwargs):
        if self.is_open():
            raise CircuitBreakerOpen("Circuit breaker is OPEN")

        try:
            result = fn(*args, **kwargs)
            self.failure_count = 0
            return result
        except Exception:
            self.failure_count += 1
            self.last_failure_at = datetime.utcnow()
            if self.failure_count >= self.failure_threshold:
                self.opened_at = datetime.utcnow()
            raise

    def is_open(self) -> bool:
        if self.opened_at is None:
            return False

        if datetime.utcnow() - self.opened_at > self.reset_after:
            self.opened_at = None
            self.failure_count = 0
            return False

        return True

