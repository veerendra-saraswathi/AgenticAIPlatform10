class UppercaseAgent:
    name = "uppercase-agent"

    def run(self, context):
        text = context.get("text", "")
        return {"upper": text.upper()}

