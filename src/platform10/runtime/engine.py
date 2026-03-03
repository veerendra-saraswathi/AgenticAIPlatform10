"""
Execution Engine with Step-Level Deterministic Replay.
Compliance-grade isolation.
"""

from typing import List, Dict, Any
from copy import deepcopy

from platform10.governance.replay.regulator_replay import RegulatorReplay


class ExecutionEngine:
    """
    Core execution engine with regulator replay support.
    """

    def __init__(self, regulator_mode: bool = True):
        self.regulator_mode = regulator_mode
        self.replay = RegulatorReplay() if regulator_mode else None

    def execute_sequence(
        self,
        agents: List,
        initial_input: Dict[str, Any],
        trace_id: str,
    ) -> Dict[str, Any]:

        # Strict isolation
        current_data = deepcopy(initial_input)
        input_snapshot = deepcopy(initial_input)

        steps = []

        for index, agent in enumerate(agents, start=1):
            current_data = agent.run(current_data)

            step_snapshot = {
                "step": index,
                "agent": getattr(agent, "name", agent.__class__.__name__),
                "output_snapshot": deepcopy(current_data),
            }

            steps.append(step_snapshot)

        final_context = deepcopy(current_data)

        if self.regulator_mode and self.replay:
            self.replay.record(
                trace_id=trace_id,
                input_snapshot=input_snapshot,
                steps=steps,
                final_context=final_context,
            )

        return final_context
        