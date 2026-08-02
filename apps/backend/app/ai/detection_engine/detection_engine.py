from app.ai.detection_engine.generators.sigma_generator import SigmaGenerator
from app.ai.detection_engine.generators.yara_generator import YaraGenerator
from app.ai.detection_engine.generators.kql_generator import KQLGenerator
from app.ai.detection_engine.generators.spl_generator import SPLGenerator
from app.ai.detection_engine.generators.eql_generator import EQLGenerator


class DetectionEngine:

    def __init__(self):

        self.generators = {

            "sigma": SigmaGenerator(),

            "yara": YaraGenerator(),

            "kql": KQLGenerator(),

            "spl": SPLGenerator(),

            "eql": EQLGenerator()

        }

    def generate_detection(

        self,

        detection_type: str,

        title: str,

        description: str,

        mitre=None

    ):

        detection_type = detection_type.lower()

        if detection_type not in self.generators:

            raise ValueError(
                f"Unsupported detection type: {detection_type}"
            )

        return self.generators[
            detection_type
        ].generate(

            title,

            description,

            mitre

        )