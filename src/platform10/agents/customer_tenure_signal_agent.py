from typing import Dict, Any

from platform10.agents.base.signal_agent import SignalAgent
from platform10.contracts.fraud_case import FraudCase


class CustomerTenureSignalAgent(SignalAgent):
    """
    Flags risk based on customer tenure (how long the customer has existed).
    Deterministic and regulator-friendly.
    """

    name = "customer-tenure-signal-agent"
    signal_type = "customer_tenure_risk"

    # Policy threshold (days)
    MIN_SAFE_TENURE_DAYS = 30

    def evaluate(self, case: FraudCase) -> Dict[str, Any]:
        """
        Expects `customer_tenure_days` in case.context.
        Defaults to HIGH risk if missing.
        """
        tenure_days = case.context.get("customer_tenure_days")

        if tenure_days is None:
            risk = "HIGH"
        elif tenure_days < self.MIN_SAFE_TENURE_DAYS:
            risk = "HIGH"
        else:
            risk = "LOW"

        return {
            "agent": self.name,
            "signal_type": self.signal_type,
            "customer_tenure_days": tenure_days,
            "risk": risk,
        }

