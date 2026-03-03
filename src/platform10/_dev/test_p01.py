from platform10.patterns.p01_deterministic_execution import (
    DeterministicExecutionPattern
)
from platform10.workflows.pattern_executor import run_pattern
import uuid


def add(inputs):
    return inputs["a"] + inputs["b"]


if __name__ == "__main__":
    pattern = DeterministicExecutionPattern()
    execution_id = str(uuid.uuid4())

    result = run_pattern(
        pattern,
        {
            "task": add,
            "inputs": {"a": 2, "b": 3}
        },
        execution_id
    )

    print(result)

