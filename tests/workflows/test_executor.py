"""
Executor Unit Tests
-------------------
These tests are explicitly imported to ensure discovery
under LangSmith pytest plugin.
"""

import pytest

from platform10.runtime.executor import Executor
from platform10.policies.execution_policy import ExecutionPolicy


# ----------------------------
# Test Doubles
# ----------------------------

class DummyAgent:
    def __init__(self, name, tokens=0):
        self.name = name
        self.tokens = tokens

    def run(self, context):
        return {
            "agent": self.name,
            "tokens": self.tokens,
        }


class DummyWorkflow:
    def __init__(self, agents, policy=None):
        self.agents = agents
        self.execution_policy = policy
        self.execution_id = "TEST-EXEC-001"


# ----------------------------
# Tests (EXPLICIT)
# ----------------------------

def test_executor_successful_execution():
    executor = Executor()

    workflow = DummyWorkflow(
        agents=[
            DummyAgent("agent1", tokens=10),
            DummyAgent("agent2", tokens=20),
        ],
        policy=ExecutionPolicy(
            max_tokens=100,
            max_latency_ms=10_000,
        ),
    )

    result = executor.execute(workflow, context={})
    assert result["agent"] == "agent2"


def test_executor_token_budget_violation():
    executor = Executor()

    workflow = DummyWorkflow(
        agents=[
            DummyAgent("agent1", tokens=60),
            DummyAgent("agent2", tokens=60),
        ],
        policy=ExecutionPolicy(
            max_tokens=100,
            max_latency_ms=10_000,
        ),
    )

    with pytest.raises(RuntimeError):
        executor.execute(workflow, context={})
