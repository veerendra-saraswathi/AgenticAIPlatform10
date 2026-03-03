"""
Execution Engine

Purpose:
- Orchestrates agent execution
- Emits immutable audit events for every step
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

from platform10.governance.audit_log import get_audit_log


class ExecutionEngine:
    """
    Core runtime engine for agentic execution.
    """

    def __init__(self, execution_policy: Optional[Any] = None):
        self.execution_policy = execution_policy
        self.audit_log = get_audit_log()

    def execute_agent(
        self,
        agent: Any,
        input_data: Dict[str, Any],
        trace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute a single agent and record its behavior.
        """
        trace_id = trace_id or str(uuid.uuid4())

        # --- Pre-execution audit ---
        self.audit_log.record_event(
            trace_id=trace_id,
            component=agent.__class__.__name__,
            action="agent_execute_start",
            input_data=input_data,
            output_data={},
            metadata={"timestamp": datetime.utcnow().isoformat()},
        )

        # --- Execute agent ---
        output = agent.run(input_data)

        # --- Post-execution audit ---
        self.audit_log.record_event(
            trace_id=trace_id,
            component=agent.__class__.__name__,
            action="agent_execute_end",
            input_data=input_data,
            output_data=output,
            metadata={"timestamp": datetime.utcnow().isoformat()},
        )

        return output

    def execute_sequence(
        self,
        agents: List[Any],
        initial_input: Dict[str, Any],
        trace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute a sequence of agents deterministically.
        """
        trace_id = trace_id or str(uuid.uuid4())
        current_data = initial_input

        self.audit_log.record_event(
            trace_id=trace_id,
            component="ExecutionEngine",
            action="sequence_start",
            input_data=initial_input,
            output_data={},
        )

        for agent in agents:
            current_data = self.execute_agent(
                agent=agent,
                input_data=current_data,
                trace_id=trace_id,
            )

        self.audit_log.record_event(
            trace_id=trace_id,
            component="ExecutionEngine",
            action="sequence_end",
            input_data=initial_input,
            output_data=current_data,
        )

        return current_data
