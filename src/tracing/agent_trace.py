from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, Any, Optional
import uuid


def utc_now() -> str:
    return datetime.utcnow().isoformat() + "Z"


@dataclass
class AgentTrace:
    execution_id: str
    agent_name: str
    task_type: Optional[str] = None

    started_at: str = field(default_factory=utc_now)
    ended_at: Optional[str] = None

    inputs: Dict[str, Any] = field(default_factory=dict)
    signals: Dict[str, Any] = field(default_factory=dict)

    decision: Optional[str] = None
    reasoning: Optional[str] = None
    confidence: Optional[float] = None

    outcome: Optional[str] = None
    status: str = "RUNNING"

    # ---------- lifecycle ----------

    @classmethod
    def start(
        cls,
        agent_name: str,
        task_type: Optional[str] = None,
        inputs: Optional[Dict[str, Any]] = None,
    ) -> "AgentTrace":
        return cls(
            execution_id=str(uuid.uuid4()),
            agent_name=agent_name,
            task_type=task_type,
            inputs=inputs or {},
        )

    def record_signals(self, signals: Dict[str, Any]) -> None:
        self.signals.update(signals)

    def finalize(
        self,
        decision: Optional[str],
        reasoning: Optional[str] = None,
        confidence: Optional[float] = None,
        outcome: Optional[str] = None,
    ) -> None:
        self.decision = decision
        self.reasoning = reasoning
        self.confidence = confidence
        self.outcome = outcome

        self.ended_at = utc_now()
        self.status = "COMPLETED"

    # ---------- serialization ----------

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

