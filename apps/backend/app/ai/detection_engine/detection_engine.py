from app.ai.detection.detection_generator import DetectionGenerator
from app.ai.detection.yara_generator import YaraGenerator
from app.ai.validator.detection_validator import DetectionValidator


class DetectionEngine:

    def __init__(self):

        self.sigma = DetectionGenerator()
        self.yara = YaraGenerator()

    def generate_detection(

        self,

        detection_type,

        title,

        description,

        mitre

    ):

        detection_type = detection_type.lower()

        if detection_type == "sigma":

            rule = self.sigma.generate_sigma(

                title,

                description,

                mitre

            )

            validation = DetectionValidator.validate_sigma(

                rule

            )

            return {

                "rule": rule,

                "validation": validation

            }

        if detection_type == "yara":

            rule = self.yara.generate_rule(

                title,

                description,

                mitre

            )

            validation = DetectionValidator.validate_yara(

                rule

            )

            return {

                "rule": rule,

                "validation": validation

            }

        raise Exception(

            f"Unsupported detection type: {detection_type}"

        )