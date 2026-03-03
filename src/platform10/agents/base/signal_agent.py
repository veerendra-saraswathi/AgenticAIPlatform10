"""
Base contract for all signal-producing agents.

SignalAgents are deterministic, auditable, and side-effect free.
They take a FraudCase and return a structured signal dict.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

from platform10.contracts.fraud_case import FraudCase


class SignalAgent(ABC):
    """
    Abstract base class for all fraud / risk signal agents.
    """

    #: Unique agent name (used in audit logs)
    name: str

    @abstractmethod
    def evaluate(self, case: FraudCase) -> Dict[str, Any]:
        """
        Evaluate a fraud case and return a signal.

        Requirements:
        - Must be deterministic
        - Must not mutate the case
        - Must return JSON-serializable output
        - Must be explainable

        Example return:
        {
            "agent": "geo-risk-agent",
            "risk": "HIGH",
            "details": {...}
        }
        """
        raise NotImplementedError
