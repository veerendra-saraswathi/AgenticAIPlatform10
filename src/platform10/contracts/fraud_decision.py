from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class FraudDecision:
    """
    Canonical output contract for fraud investigation.
    """
    case_id: str
    decision: str          # e.g. FLAG / CLEAR / REVIEW
    risk_score: float
    signals: List[Dict[str, Any]]
    explanation: str
