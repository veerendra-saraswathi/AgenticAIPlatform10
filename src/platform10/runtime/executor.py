"""
Executor
--------
Central runtime executor for workflows.

Policy-driven, auditable, deterministic.
"""

from platform10.patterns.governor import (
    ExecutionGovernor,
    ExecutionBudgetExceeded,
)
from platform10.runtime.execution_context import ExecutionContext
from platform10.governance.audit_log import AuditLog
from platform10.policies.execution_policy import ExecutionPolicy


class Executor:
    def __init__(self):
        self.audit_log = AuditLog()

    def _resolve_policy(self, workflow) -> ExecutionPolicy:
        policy = getattr(workflow, "execution_policy", None)
        if policy is None:
            return ExecutionPolicy(max_tokens=1000, max_latency_ms=5000)
        return policy

    def execute(self, workflow, context: dict):
        execution_id = getattr(workflow, "execution_id", None)
        policy = self._resolve_policy(workflow)

        governor = ExecutionGovernor(
            max_tokens=policy.max_tokens,
            max_latency_ms=policy.max_latency_ms,
        )

        execution_context = ExecutionContext(execution_id=execution_id)
        current_context = context

        for agent in workflow.agents:
            agent_name = agent.__class__.__name__

            try:
                result = agent.run(current_context)
            except Exception as e:
                self.audit_log.record(
                    execution_id=execution_id,
                    event_type="AGENT_FAILURE",
                    details={"agent": agent_name, "error": str(e)},
                )
                raise RuntimeError(f"Agent '{agent_name}' failed") from e

            if isinstance(result, dict):
                current_context = {**current_context, **result}

            tokens = result.get("tokens") if isinstance(result, dict) else None
            if tokens:
                execution_context.record_tokens(tokens)

            try:
                governor.enforce(execution_context.metrics())
            except ExecutionBudgetExceeded as e:
                self.audit_log.record(
                    execution_id=execution_id,
                    event_type="EXECUTION_POLICY_VIOLATION",
                    details={
                        "agent": agent_name,
                        "policy": policy.__dict__,
                        "metrics": execution_context.metrics(),
                        "reason": str(e),
                    },
                )
                raise RuntimeError("Execution stopped by policy") from e

        return current_context
