from app.core.llm.ollama_client import OllamaClient


class ModelManager:

    def __init__(self):

        self.client = OllamaClient()

    MODELS = {
        "mitre_mapping": "mistral:7b",
        "ioc": "mistral:7b",
        "investigation": "mistral:7b",
        "sigma": "qwen2.5-coder:14b",
        "code": "qwen2.5-coder:14b"
    }

    def ask(self, task: str, prompt: str):

        model = self.MODELS.get(task, "mistral:7b")

        return self.client.generate(
            model=model,
            prompt=prompt
        )