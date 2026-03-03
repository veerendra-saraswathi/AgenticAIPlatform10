"""
Audit Log

Purpose:
- Persist immutable events for every agentic decision
- Serve as the single source of truth for regulator-mode replay
"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid


# -----------------------------
# Audit Event Model
# -----------------------------

@dataclass(frozen=True)
class AuditEvent:
    """
    Immutable audit event.
    """
    event_id: str
    trace_id: str
    timestamp: datetime
    component: str               # agent / workflow / policy / engine
    action: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


# -----------------------------
# Audit Log Backend (In-Memory v1)
# -----------------------------

class InMemoryAuditLog:
    """
    Simple in-memory audit log backend.

    NOTE:
    - This will later be replaced by DB / file / S3
    - Interface must remain stable
    """

    def __init__(self):
        self._events: List[AuditEvent] = []

    def record_event(
        self,
        trace_id: str,
        component: str,
        action: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        event = AuditEvent(
            event_id=str(uuid.uuid4()),
            trace_id=trace_id,
            timestamp=datetime.utcnow(),
            component=component,
            action=action,
            input_data=input_data,
            output_data=output_data,
            metadata=metadata or {},
        )
        self._events.append(event)

    def fetch_events(self, trace_id: str) -> List[AuditEvent]:
        """
        Fetch all events for a trace_id, ordered by time.
        """
        return sorted(
            [e for e in self._events if e.trace_id == trace_id],
            key=lambda e: e.timestamp,
        )

    def all_events(self) -> List[AuditEvent]:
        return list(self._events)


# -----------------------------
# Global Default Audit Log
# -----------------------------

_default_audit_log = InMemoryAuditLog()


def get_audit_log() -> InMemoryAuditLog:
    """
    Accessor for the default audit log.
    """
    return _default_audit_log
