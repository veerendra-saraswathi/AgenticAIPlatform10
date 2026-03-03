from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class FraudCase:
    """
    Canonical input contract for fraud investigation.
    This file defines a STABLE enterprise boundary.
    """
    case_id: str
    transaction: Dict[str, Any]
    context: Dict[str, Any]
