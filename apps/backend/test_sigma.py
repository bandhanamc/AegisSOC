from app.ai.detection.detection_generator import DetectionGenerator

mitre = [

    {

        "technique_id": "T1190",

        "name": "Exploit Public Facing Application"

    }

]

generator = DetectionGenerator()

rule = generator.generate_sigma(

    "SQL Injection",

    "SQL Injection allows database compromise",

    mitre

)

print(rule)