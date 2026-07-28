import httpx


class OllamaClient:
    """
    Enterprise Ollama Client

    Every AI module communicates with Ollama through this class.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "mistral:7b",
        timeout: int = 120,
    ):
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

    def generate(self, prompt: str) -> str:
        """
        Generate a response from Ollama.
        """

        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=self.timeout
        )

        response.raise_for_status()

        return response.json()["response"]