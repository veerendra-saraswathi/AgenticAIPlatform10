from abc import ABC, abstractmethod
from typing import Dict, Any


class AgenticPattern(ABC):
    """
    Base class for all Agentic AI patterns.
    Patterns must be:
    - Deterministic
    - Auditable
    - Composable
    """

    pattern_id: str  # e.g. P01, P07
    name: str
    description: str

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the pattern logic.
        Must return a structured dict suitable for audit logging.
        """
        pass

