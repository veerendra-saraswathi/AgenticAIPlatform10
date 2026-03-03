"""
Execution Policy
----------------
Defines execution budgets and SLA constraints per workflow.

Enterprise intent:
- Per-workflow SLA
- Per-tenant extensibility
- Deterministic enforcement
"""

from dataclasses import dataclass


@dataclass
class ExecutionPolicy:
    """
    Execution budget and SLA constraints.
    """
    max_tokens: int | None = None
    max_latency_ms: int | None = None
