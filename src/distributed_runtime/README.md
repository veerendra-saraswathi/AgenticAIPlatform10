# Distributed Runtime – AgenticAIPlatform10

This module introduces a **distributed execution runtime**
for AgenticAIPlatform10 using Ray-compatible infrastructure
(Anyscale, KubeRay, local Ray).

## Why this exists

- Core agents remain pure Python
- Distribution is isolated at runtime
- Enterprise-safe, infrastructure-agnostic design

## Single Agent Execution

```python
from platform10.agents.fraud_signal_agent import FraudSignalAgent
from distributed_runtime.ray_workflow import run_agent_distributed

agent = FraudSignalAgent()

result = run_agent_distributed(agent, {
    "tx_count_last_10_min": 15,
    "country": "IN"
})

print(result)
