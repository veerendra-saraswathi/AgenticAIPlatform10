# src/platform10/agents/echo_agent.py

class EchoAgent:
    name = "echo-agent"

    def run(self, context):
        return {
            "message": "Echo from agent",
            "input_received": context
        }

