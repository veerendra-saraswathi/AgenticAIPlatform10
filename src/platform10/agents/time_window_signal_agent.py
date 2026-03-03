from datetime import datetime
from typing import Dict, Any

from platform10.agents.base.signal_agent import SignalAgent
from platform10.contracts.fraud_case import FraudCase


class TimeWindowSignalAgent(SignalAgent):
    """
    Detects anomalous transaction time windows.
    Simple, deterministic, explainable.
    """

    name = "time-window-signal-agent"
    signal_type = "time_window_risk"

    # Configurable policy thresholds (can be externalized later)
    HIGH_RISK_START_HOUR = 0    # 00:00
    HIGH_RISK_END_HOUR = 5      # 05:00

    def evaluate(self, case: FraudCase) -> Dict[str, Any]:
        # Expect ISO timestamp in context; fallback to current time
        ts = case.context.get("timestamp")

        if ts:
            try:
                event_time = datetime.fromisoformat(ts)
            except ValueError:
                event_time = datetime.utcnow()
        else:
            event_time = datetime.utcnow()

        hour = event_time.hour

        risk = (
            "HIGH"
            if self.HIGH_RISK_START_HOUR <= hour < self.HIGH_RISK_END_HOUR
            else "LOW"
        )

        return {
            "agent": self.name,
            "signal_type": self.signal_type,
            "hour": hour,
            "risk": risk,
        }

