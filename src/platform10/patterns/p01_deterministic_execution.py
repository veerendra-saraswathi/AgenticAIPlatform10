from typing import Dict, Any
from .base import AgenticPattern


class DeterministicExecutionPattern(AgenticPattern):
    pattern_id = "P01"
    name = "Deterministic Task Execution"
    description = "Executes a task with deterministic inputs and outputs."

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        task = context.get("task")
        inputs = context.get("inputs", {})

        if not task:
            raise ValueError("Task is required for deterministic execution")

        result = task(inputs)

        return {
            "pattern_id": self.pattern_id,
            "task": task.__name__,
            "inputs": inputs,
            "output": result,
            "status": "SUCCESS"
        }

