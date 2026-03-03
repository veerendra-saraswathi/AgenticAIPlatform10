"""
Location / geography-based fraud signal agent.
"""

from typing import Dict, Any

from platform10.agents.base.signal_agent import SignalAgent
from platform10.contracts.fraud_case import FraudCase


HIGH_RISK_COUNTRIES = {
    "RU",
    "IR",
    "KP",
}


class LocationSignalAgent(SignalAgent):
    """
    Evaluates geographic risk based on transaction country.
    """

    name = "location-signal-agent"

    def evaluate(self, case: FraudCase) -> Dict[str, Any]:
        transaction = case.transaction
        country = transaction.get("country")

        if not country:
            risk = "UNKNOWN"
        elif country in HIGH_RISK_COUNTRIES:
            risk = "HIGH"
        else:
            risk = "LOW"

        return {
            "agent": self.name,
            "signal_type": "geo_risk",
            "country": country,
            "risk": risk,
        }
