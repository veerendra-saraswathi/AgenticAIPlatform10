# src/platform10/patterns/retry.py

from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class RetryPolicy:
    """
    Declarative retry + fallback policy.
    """
    retries: int = 0
    retry_delay_sec: float = 0.0
    fallback_agent: Optional[Any] = None
