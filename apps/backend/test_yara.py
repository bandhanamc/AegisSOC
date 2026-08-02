from app.ai.detection_engine.detection_engine import DetectionEngine

engine = DetectionEngine()

mitre = [

    {

        "technique_id": "T1059",

        "name": "Command and Scripting Interpreter"

    }

]

result = engine.generate_detection(

    "yara",

    "PowerShell Malware",

    "Detect suspicious PowerShell malware",

    mitre

)

print(result["validation"])

print()

print(result["rule"])