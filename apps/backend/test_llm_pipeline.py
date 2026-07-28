from app.core.llm.prompt_builder import PromptBuilder
from app.core.llm.model_manager import ModelManager
from app.core.llm.response_parser import ResponseParser

candidates = [
    {
        "technique_id": "T1059.001",
        "name": "PowerShell",
        "description": "PowerShell execution",
        "tactic": "Execution",
        "score": 0.94,
        "detection": "Encoded PowerShell",
        "platforms": "Windows",
        "data_sources": "PowerShell Logs"
    },
    {
        "technique_id": "T1027.010",
        "name": "Command Obfuscation",
        "description": "Encoded command",
        "tactic": "Defense Evasion",
        "score": 0.88,
        "detection": "Base64",
        "platforms": "Windows",
        "data_sources": "Command Line"
    }
]

prompt = PromptBuilder.build_mitre_prompt(
    "powershell.exe downloaded file with encoded command",
    candidates
)

response = ModelManager().ask(
    task="mitre_mapping",
    prompt=prompt
)

print("========== RAW RESPONSE ==========")
print(response)

print("\n========== PARSED ==========")
print(ResponseParser.parse(response))