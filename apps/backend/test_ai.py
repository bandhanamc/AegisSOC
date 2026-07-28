from app.core.llm.ollama_client import OllamaClient
from app.core.llm.prompt_builder import PromptBuilder

client = OllamaClient()

prompt = PromptBuilder.build_mitre_prompt(
    "powershell.exe downloaded file with encoded command"
)

response = client.generate(prompt)

print(response)