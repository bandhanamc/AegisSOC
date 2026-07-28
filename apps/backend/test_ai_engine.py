from app.services.ai.mitre_ai_engine import MitreAIEngine

engine = MitreAIEngine()

alert = "powershell.exe downloaded file with encoded command"

candidates = [
    {
        "technique_id":"T1059.001",
        "name":"PowerShell",
        "description":"PowerShell execution",
        "detection":"Monitor powershell.exe"
    },
    {
        "technique_id":"T1027.010",
        "name":"Command Obfuscation",
        "description":"Encoded commands",
        "detection":"Detect base64"
    }
]

result = engine.analyze(
    alert,
    candidates
)

print(result)