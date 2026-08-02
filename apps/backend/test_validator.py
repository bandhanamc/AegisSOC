from app.ai.validator.detection_validator import DetectionValidator

sample = """

rule Test
{

meta:

author="AI"

strings:

$a="test"

condition:

$a

}

"""

result = DetectionValidator.validate_yara(sample)

print(result)