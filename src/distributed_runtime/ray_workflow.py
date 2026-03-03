import ray
from distributed_runtime.ray_executor import RayAgentExecutor


def run_agent_distributed(agent, payload: dict) -> dict:
    """
    Run a single agent using Ray Actor execution.

    This function acts as a thin adapter between:
    - Existing Agentic workflows
    - Distributed execution runtime
    """

    if not ray.is_initialized():
        ray.init(ignore_reinit_error=True)

    executor = RayAgentExecutor.remote(agent)
    result_ref = executor.run.remote(payload)

    return ray.get(result_ref)
