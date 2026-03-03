"""
Execution Governor Pattern
--------------------------
Enforces cost, latency, and execution budgets at runtime.

Enterprise purpose:
- Prevent runaway LLM / agent execution
- Enforce SLAs
- Enable per-tenant / per-workflow budgets
"""


class ExecutionBudgetExceeded(Exception):
    """Raised when execution exceeds allowed budget."""
    pass


class ExecutionGovernor:
    def __init__(
        self,
        max_tokens: int | None = None,
        max_latency_ms: int | None = None,
    ):
        self.max_tokens = max_tokens
        self.max_latency_ms = max_latency_ms

    def enforce(self, metrics: dict):
        """
        Enforce execution budgets using runtime metrics.
        """
        tokens = metrics.get("tokens", 0)
        latency = metrics.get("latency_ms", 0)

        if self.max_tokens is not None and tokens > self.max_tokens:
            raise ExecutionBudgetExceeded(
                f"Token budget exceeded: {tokens} > {self.max_tokens}"
            )

        if self.max_latency_ms is not None and latency > self.max_latency_ms:
            raise ExecutionBudgetExceeded(
                f"Latency budget exceeded: {latency}ms > {self.max_latency_ms}ms"
            )
