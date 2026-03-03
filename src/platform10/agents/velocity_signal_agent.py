"""
Velocity-based fraud signal agent.
"""

from typing import Dict, Any

from platform10.agents.base.signal_agent import SignalAgent
from platform10.contracts.fraud_case import FraudCase


class VelocitySignalAgent(SignalAgent):
    """
    Evaluates transaction velocity risk.
    """

    name = "velocity-signal-agent"

    def evaluate(self, case: FraudCase) -> Dict[str, Any]:
        transaction = case.transaction
        tx_count = transaction.get("tx_count", 0)

        if tx_count >= 50:
            risk = "HIGH"
        elif tx_count >= 20:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        return {
            "agent": self.name,
            "signal_type": "velocity_risk",
            "tx_count": tx_count,
            "risk": risk,
        }
