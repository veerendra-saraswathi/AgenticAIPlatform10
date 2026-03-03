from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, Optional
import uuid
import json


@dataclass
class AgentTrace:
    execution_id: str
    agent_name: str
    task_type: str
    inputs: Dict[str, Any]
    signals: Dict[str, Any]
    decision: Optional[str]
    reasoning: Optional[str]
    confidence: Optional[float]
    outcome: Optional[str]
    timestamp: str

    @staticmethod
    def create(
        agent_name: str,
        task_type: str,
        inputs: Dict[str, Any],
        signals: Dict[str, Any],
    ) -> "AgentTrace":
        return AgentTrace(
            execution_id=str(uuid.uuid4()),
            agent_name=agent_name,
            task_type=task_type,
            inputs=inputs,
            signals=signals,
            decision=None,
            reasoning=None,
            confidence=None,
            outcome=None,
            timestamp=datetime.utcnow().isoformat(),
        )

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str)
