from app.ai.detection_engine.detection_engine import DetectionEngine


engine = DetectionEngine()

mitre = [

    {

        "technique_id": "T1190",

        "name": "Exploit Public Facing Application"

    }

]

rule = engine.generate_detection(

    "sigma",

    "SQL Injection",

    "SQL Injection allows database compromise",

    mitre

)

print(rule)