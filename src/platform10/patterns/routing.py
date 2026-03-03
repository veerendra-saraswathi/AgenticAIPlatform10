# src/platform10/patterns/routing.py

from typing import Dict, Callable, Any
from dataclasses import dataclass

from platform10.patterns.sequence import AgentPipeline
from platform10.runtime.engine import WorkflowEngine


@dataclass
class Route:
    """
    A conditional route.
    """
    name: str
    condition: Callable[[Dict[str, Any]], bool]
    pipeline: AgentPipeline


class ConditionalRouter:
    """
    Executes exactly one pipeline based on conditions.
    """

    def __init__(
        self,
        engine: WorkflowEngine,
        routes: Dict[str, Route],
        default_pipeline: AgentPipeline | None = None,
    ):
        self.engine = engine
        self.routes = routes
        self.default_pipeline = default_pipeline

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        for route in self.routes.values():
            if route.condition(context):
                result = route.pipeline.run(context)
                result["selected_route"] = route.name
                return result

        if self.default_pipeline:
            result = self.default_pipeline.run(context)
            result["selected_route"] = "default"
            return result

        raise RuntimeError("No routing condition matched and no default pipeline provided")
