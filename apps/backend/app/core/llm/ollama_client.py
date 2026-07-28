import httpx


class OllamaClient:
    """
    Enterprise Ollama Client

    Supports multiple models.

    The ModelManager decides which model to use.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        timeout: int = 180,
    ):

        self.base_url = base_url
        self.timeout = timeout

    def generate(
        self,
        model: str,
        prompt: str,
    ) -> str:

        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]