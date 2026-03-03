"""
Regulator-Mode Replay

Purpose:
- Deterministically reconstruct how a decision was made
- Used for audit, compliance, regulator review, and post-mortems
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime

from platform10.governance.audit_log import AuditEvent


# -----------------------------
# Replay Data Structures
# -----------------------------

@dataclass
class ReplayStep:
    timestamp: datetime
    component: str
    action: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecisionReplay:
    trace_id: str
    steps: List[ReplayStep]
    final_decision: Dict[str, Any]
    confidence_score: Optional[float]
    flags: List[str]
    created_at: datetime


# -----------------------------
# Replay Engine
# -----------------------------

class RegulatorReplayEngine:
    """
    Reconstructs historical decisions from audit logs.
    """

    def __init__(self, audit_log_backend: Any):
        self.audit_log_backend = audit_log_backend

    def replay_trace(self, trace_id: str) -> DecisionReplay:
        events: List[AuditEvent] = self.audit_log_backend.fetch_events(trace_id)

        if not events:
            raise ValueError(f"No audit events found for trace_id={trace_id}")

        steps: List[ReplayStep] = []
        final_output: Dict[str, Any] = {}
        confidence_score: Optional[float] = None
        flags: List[str] = []

        for event in events:
            steps.append(
                ReplayStep(
                    timestamp=event.timestamp,
                    component=event.component,
                    action=event.action,
                    input_data=event.input_data,
                    output_data=event.output_data,
                    metadata=event.metadata,
                )
            )

            # Heuristic extraction (safe, deterministic)
            if event.action.endswith("_end") and event.output_data:
                final_output = event.output_data

            if "confidence" in event.metadata:
                confidence_score = event.metadata["confidence"]

            if "flags" in event.metadata:
                flags.extend(event.metadata["flags"])

        return DecisionReplay(
            trace_id=trace_id,
            steps=steps,
            final_decision=final_output,
            confidence_score=confidence_score,
            flags=list(set(flags)),
            created_at=datetime.utcnow(),
        )


# -----------------------------
# Public API
# -----------------------------

def replay_trace(trace_id: str, audit_log_backend: Any) -> DecisionReplay:
    engine = RegulatorReplayEngine(audit_log_backend)
    return engine.replay_trace(trace_id)
