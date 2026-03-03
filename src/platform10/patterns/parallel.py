# src/platform10/patterns/parallel.py

from typing import Dict, Any, List
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

from platform10.runtime.engine import WorkflowEngine
from platform10.runtime.executor import ExecutionResult


@dataclass
class ParallelStep:
    """
    One agent executed in parallel.
    """
    name: str
    agent: Any


class ParallelFanOut:
    """
    Executes multiple agents in parallel and aggregates results.
    """

    def __init__(
        self,
        engine: WorkflowEngine,
        steps: List[ParallelStep],
        max_workers: int | None = None,
    ):
        self.engine = engine
        self.steps = steps
        self.max_workers = max_workers or len(steps)

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        aggregated_context = dict(context)
        results: List[ExecutionResult] = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_map = {
                executor.submit(
                    self.engine.run_agent,
                    step.agent,
                    aggregated_context,
                ): step
                for step in self.steps
            }

            for future in as_completed(future_map):
                step = future_map[future]
                result = future.result()
                results.append(result)

                if result.status == "SUCCESS":
                    aggregated_context[f"{step.name}_output"] = result.output
                else:
                    aggregated_context[f"{step.name}_error"] = result.output

        return {
            "final_context": aggregated_context,
            "results": results,
        }
