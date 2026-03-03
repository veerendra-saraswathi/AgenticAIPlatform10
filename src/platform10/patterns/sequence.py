# src/platform10/patterns/sequence.py

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import time

from platform10.runtime.engine import WorkflowEngine
from platform10.runtime.executor import ExecutionResult
from platform10.patterns.retry import RetryPolicy


@dataclass
class PipelineStep:
    """
    One step in a sequential agent pipeline.
    """
    name: str
    agent: Any
    retry_policy: Optional[RetryPolicy] = None
    stop_on_failure: bool = True


class AgentPipeline:
    """
    Executes a sequence of agents with shared context.
    Supports retry and fallback semantics.
    """

    def __init__(self, engine: WorkflowEngine, steps: List[PipelineStep]):
        self.engine = engine
        self.steps = steps

    def run(self, initial_context: Dict[str, Any]) -> Dict[str, Any]:
        context = dict(initial_context)
        results: List[ExecutionResult] = []

        for step in self.steps:
            policy = step.retry_policy
            attempt = 0
            last_result: Optional[ExecutionResult] = None

            # ---------- Retry loop ----------
            while True:
                last_result = self.engine.run_agent(
                    agent=step.agent,
                    context=context,
                )
                results.append(last_result)

                if last_result.status == "SUCCESS":
                    break

                if policy is None or attempt >= policy.retries:
                    break

                attempt += 1
                if policy.retry_delay_sec > 0:
                    time.sleep(policy.retry_delay_sec)

            # ---------- Fallback ----------
            if last_result and last_result.status != "SUCCESS":
                if policy and policy.fallback_agent:
                    fallback_result = self.engine.run_agent(
                        agent=policy.fallback_agent,
                        context=context,
                    )
                    results.append(fallback_result)

                    if fallback_result.status == "SUCCESS":
                        context[f"{step.name}_output"] = fallback_result.output
                        continue

                if step.stop_on_failure:
                    break

            # ---------- Context propagation ----------
            if last_result and last_result.status == "SUCCESS":
                context[f"{step.name}_output"] = last_result.output

        return {
            "final_context": context,
            "results": results,
        }
