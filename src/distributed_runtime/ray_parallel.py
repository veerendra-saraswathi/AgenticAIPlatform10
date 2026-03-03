import ray
from distributed_runtime.ray_executor import RayAgentExecutor


def run_agents_in_parallel(agents_with_payloads: list) -> list:
    """
    Run multiple agents in parallel using Ray Actors.

    Input:
        agents_with_payloads = [
            (agent1, payload1),
            (agent2, payload2),
            ...
        ]

    Output:
        List of agent results in the same order.
    """

    if not ray.is_initialized():
        ray.init(ignore_reinit_error=True)

    futures = []

    for agent, payload in agents_with_payloads:
        actor = RayAgentExecutor.remote(agent)
        futures.append(actor.run.remote(payload))

    return ray.get(futures)
