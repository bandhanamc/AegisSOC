from app.ai.detection_engine.generators.sigma_generator import SigmaGenerator
from app.ai.detection_engine.generators.yara_generator import YaraGenerator
from app.ai.detection_engine.generators.kql_generator import KQLGenerator
from app.ai.detection_engine.generators.eql_generator import EQLGenerator
from app.ai.detection_engine.generators.spl_generator import SPLGenerator


class DetectionEngine:

    def __init__(self):

        self.generators = {
            "sigma": SigmaGenerator(),
            "yara": YaraGenerator(),
            "kql": KQLGenerator(),
            "eql": EQLGenerator(),
            "spl": SPLGenerator(),
        }

    def generate(
        self,
        rule_type: str,
        title: str,
        description: str,
    ):

        generator = self.generators.get(rule_type.lower())

        if generator is None:
            raise ValueError(
                f"Unsupported rule type: {rule_type}"
            )

        return generator.generate(
            title=title,
            description=description,
        )