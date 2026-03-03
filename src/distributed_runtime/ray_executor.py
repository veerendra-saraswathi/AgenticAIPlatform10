import ray
from typing import Any, Dict

from platform10.runtime.executor import AgentExecutor, ExecutionResult


@ray.remote
class RayAgentExecutor:
    """
    Ray Actor wrapper around Platform10's AgentExecutor.

    IMPORTANT:
    - Agents are NOT executed directly
    - All execution flows through AgentExecutor
    - This preserves execution_id, timestamps, status, etc.
    """

    def __init__(self, agent: Any):
        self.agent = agent
        self.executor = AgentExecutor()

    def run(self, input_payload: Dict[str, Any]) -> ExecutionResult:
        """
        Execute the agent via the Platform10 runtime executor.
        """
        return self.executor.execute(self.agent, input_payload)
