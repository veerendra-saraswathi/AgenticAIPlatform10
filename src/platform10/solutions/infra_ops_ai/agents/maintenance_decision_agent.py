"""
Maintenance Decision Agent
--------------------------
Decides autonomous action or escalates to human review
based on model confidence.
"""

from platform10.solutions.infra_ops_ai.agents.human_review_agent import (
    HumanReviewAgent,
)


class MaintenanceDecisionAgent:
    CONFIDENCE_THRESHOLD = 0.75

    def __init__(self):
        self.human_review_agent = HumanReviewAgent()

    def run(self, context: dict) -> dict:
        confidence = context.get("anomaly_confidence", 0.0)
        anomaly = context.get("anomaly_detected", False)

        if anomaly and confidence >= self.CONFIDENCE_THRESHOLD:
            return {
                "maintenance_action": "DISPATCH_MAINTENANCE",
                "priority": "HIGH",
                "decision_mode": "AUTONOMOUS",
                "tokens": 5,
            }

        if anomaly:
            # Escalate to human
            return self.human_review_agent.run(context)

        return {
            "maintenance_action": "NO_ACTION",
            "priority": "LOW",
            "decision_mode": "AUTONOMOUS",
            "tokens": 2,
        }
