from typing import Dict, Any

from platform10.agents.base.signal_agent import SignalAgent
from platform10.contracts.fraud_case import FraudCase


class TimeWindowVelocitySignalAgent(SignalAgent):
    """
    Detects transaction bursts within a short time window.
    Deterministic and enterprise-safe.
    """

    name = "time-window-velocity-signal-agent"
    signal_type = "time_window_velocity_risk"

    # Policy threshold
    HIGH_RISK_TX_COUNT = 10

    def evaluate(self, case: FraudCase) -> Dict[str, Any]:
        """
        Expects `tx_count_last_10_min` in case.context.
        """
        tx_count = case.context.get("tx_count_last_10_min")

        if tx_count is None:
            risk = "LOW"
        elif tx_count >= self.HIGH_RISK_TX_COUNT:
            risk = "HIGH"
        else:
            risk = "LOW"

        return {
            "agent": self.name,
            "signal_type": self.signal_type,
            "tx_count_last_10_min": tx_count,
            "risk": risk,
        }

