"""
Infrastructure Operations Workflow
----------------------------------
Governed, auditable infra-ops decision workflow.
"""

from platform10.runtime.executor import Executor
from platform10.policies.execution_policy import ExecutionPolicy
from platform10.governance.audit_log import record_audit_log

from platform10.solutions.infra_ops_ai.agents.anomaly_detection_agent import (
    AnomalyDetectionAgent,
)
from platform10.solutions.infra_ops_ai.agents.maintenance_decision_agent import (
    MaintenanceDecisionAgent,
)


class InfraOpsWorkflow:
    """
    Predictive maintenance workflow for infrastructure assets.
    """

    # 🔐 ENTERPRISE POLICY
    execution_policy = ExecutionPolicy(
        max_tokens=50,
        max_latency_ms=2000,
    )

    def __init__(self):
        self.execution_id = "INFRA-OPS-001"
        self.agents = []

    def build(self):
        self.agents = [
            AnomalyDetectionAgent(),
            MaintenanceDecisionAgent(),
        ]
        return self

    def run(self, context: dict):
        record_audit_log(
            execution_id=self.execution_id,
            event_type="WORKFLOW_STARTED",
            details={"workflow": "infra_ops"},
        )

        result = Executor().execute(self, context)

        record_audit_log(
            execution_id=self.execution_id,
            event_type="WORKFLOW_COMPLETED",
            details={"result": result},
        )

        return result

