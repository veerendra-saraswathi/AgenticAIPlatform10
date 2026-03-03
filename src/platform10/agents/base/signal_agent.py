"""
Base class for all signal agents.

Enterprise-safe execution contract.
Agents operate on execution context, not raw dict chaining.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

from platform10.contracts.fraud_case import FraudCase


class SignalAgent(ABC):
    """
    Base class for fraud signal agents.

    Execution contract:
        input_data = {
            "case": FraudCase,
            "signals": list,
            ...
        }
    """

    name: str = "base-signal-agent"

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standard execution entry point expected by runtime engine.
        """

        # Ensure context container exists
        if "case" not in input_data:
            raise ValueError(
                "Execution context must contain 'case'"
            )

        case = input_data["case"]

        if not isinstance(case, FraudCase):
            case = FraudCase(**case)

        # Ensure signals list exists
        if "signals" not in input_data:
            input_data["signals"] = []

        result = self.evaluate(case)

        if not isinstance(result, dict):
            raise TypeError(
                f"{self.__class__.__name__}.evaluate() must return dict"
            )

        input_data["signals"].append(result)

        return input_data

    @abstractmethod
    def evaluate(self, case: FraudCase) -> Dict[str, Any]:
        """
        Deterministic business logic.
        """
        pass