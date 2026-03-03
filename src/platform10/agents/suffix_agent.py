class SuffixAgent:
    name = "suffix-agent"

    def run(self, context):
        base = context.get("uppercase_output", {}).get("upper", "")
        return {"final": f"{base} !!!"}

