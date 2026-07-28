from app.core.llm.model_manager import ModelManager
from app.core.llm.prompt_builder import PromptBuilder

manager = ModelManager()

alert = "powershell.exe downloaded file with encoded command"

candidates = [
    {
        "technique_id": "T1059.001",
        "name": "PowerShell",
        "description": "PowerShell execution.",
        "detection": "Monitor powershell.exe."
    },
    {
        "technique_id": "T1027.010",
        "name": "Command Obfuscation",
        "description": "Encoded commands.",
        "detection": "Monitor base64."
    }
]

prompt = PromptBuilder.build_mitre_prompt(
    alert,
    candidates
)

response = manager.ask(
    task="mitre_mapping",
    prompt=prompt
)

print(response)