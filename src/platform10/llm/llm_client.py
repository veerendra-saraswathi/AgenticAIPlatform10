import subprocess
from typing import Optional


class LLMResponse:
    def __init__(self, text: str, raw: Optional[str] = None):
        self.text = text.strip()
        self.raw = raw


class BaseLLMClient:
    def generate(self, prompt: str) -> LLMResponse:
        raise NotImplementedError


class OllamaClient(BaseLLMClient):
    """
    Uses local Ollama runtime in NON-INTERACTIVE mode.
    Example command:
        ollama run mistral "your prompt"
    """

    def __init__(self, model: str = "mistral"):
        self.model = model

    def generate(self, prompt: str) -> LLMResponse:
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60
            )

            output = result.stdout.decode("utf-8")
            error = result.stderr.decode("utf-8")

            if error:
                return LLMResponse(text=f"ERROR: {error}", raw=output)

            return LLMResponse(text=output, raw=output)

        except subprocess.TimeoutExpired:
            return LLMResponse(text="ERROR: LLM request timed out", raw=None)

        except Exception as e:
            return LLMResponse(text=f"ERROR: {str(e)}", raw=None)


class MockLLMClient(BaseLLMClient):
    """
    Useful for testing without calling real LLM.
    """

    def generate(self, prompt: str) -> LLMResponse:
        return LLMResponse(text="low_risk")


class LLMClientFactory:
    """
    Factory to choose LLM provider.
    Extendable for OpenAI, Mistral API, etc.
    """

    @staticmethod
    def create(provider: str = "ollama", model: str = "mistral") -> BaseLLMClient:
        if provider == "ollama":
            return OllamaClient(model=model)
        elif provider == "mock":
            return MockLLMClient()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
            