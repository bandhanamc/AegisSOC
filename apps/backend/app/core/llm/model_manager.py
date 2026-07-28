from app.core.llm.ollama_client import OllamaClient


class ModelManager:
    """
    Enterprise AI Model Manager

    Chooses the appropriate local LLM
    for every AI task.
    """

    MODELS = {
        "mitre_mapping": "mistral:7b",
        "investigation": "mistral:7b",
        "ioc_extraction": "mistral:7b",
        "attack_chain": "mistral:7b",

        "sigma_generation": "qwen2.5-coder:14b",
        "parser_generation": "qwen2.5-coder:14b",
        "code_generation": "qwen2.5-coder:14b",
    }

    def ask(self, task: str, prompt: str):

        model = self.MODELS.get(task, "mistral:7b")

        client = OllamaClient(model=model)

        return client.generate(prompt)