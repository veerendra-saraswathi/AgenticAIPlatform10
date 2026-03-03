"""
Execution Context
-----------------
Tracks runtime metrics for a single workflow execution.

Used by:
- Governor (budget enforcement)
- Observability
- Audit & tracing
"""

import time


class ExecutionContext:
    def __init__(self, execution_id: str | None = None):
        self.execution_id = execution_id
        self.start_time = time.time()
        self.tokens_used = 0

    def record_tokens(self, tokens: int):
        """
        Called by agents / LLM adapters to report token usage.
        """
        self.tokens_used += tokens

    def metrics(self) -> dict:
        """
        Runtime metrics snapshot.
        """
        return {
            "tokens": self.tokens_used,
            "latency_ms": int((time.time() - self.start_time) * 1000),
        }
