from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid


def utc_now() -> str:
    return datetime.utcnow().isoformat() + "Z"


@dataclass
class AgentInvocation:
    agent: str
    execution_id: str
    decision: Optional[str]
    confidence: Optional[float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowTrace:
    workflow_execution_id: str
    workflow_name: str

    started_at: str = field(default_factory=utc_now)
    ended_at: Optional[str] = None

    agents_invoked: List[AgentInvocation] = field(default_factory=list)

    final_decision: Optional[str] = None
    final_confidence: Optional[float] = None

    explainability: Dict[str, Any] = field(default_factory=dict)
    human_review_required: bool = False

    status: str = "RUNNING"

    # ---------- lifecycle ----------

    @classmethod
    def start(cls, workflow_name: str) -> "WorkflowTrace":
        """
        Start a new workflow trace.
        """
        return cls(
            workflow_execution_id=str(uuid.uuid4()),
            workflow_name=workflow_name,
        )

    def record_agent_result(
        self,
        agent_name: str,
        execution_id: str,
        decision: Optional[str],
        confidence: Optional[float],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Append an agent invocation result to the workflow trace.
        """
        self.agents_invoked.append(
            AgentInvocation(
                agent=agent_name,
                execution_id=execution_id,
                decision=decision,
                confidence=confidence,
                metadata=metadata or {},
            )
        )

    def finalize(
        self,
        final_decision: str,
        final_confidence: Optional[float] = None,
        explainability: Optional[Dict[str, Any]] = None,
        human_review_required: bool = False,
    ) -> None:
        """
        Finalize the workflow trace.
        """
        self.final_decision = final_decision
        self.final_confidence = final_confidence
        self.explainability = explainability or {}
        self.human_review_required = human_review_required

        self.ended_at = utc_now()
        self.status = "COMPLETED"

    # ---------- serialization ----------

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
