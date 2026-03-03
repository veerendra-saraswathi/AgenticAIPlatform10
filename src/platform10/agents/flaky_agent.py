import random

class FlakyAgent:
    name = "flaky-agent"

    def run(self, context):
        if random.random() < 0.7:
            raise RuntimeError("Transient failure")
        return {"status": "eventually succeeded"}
