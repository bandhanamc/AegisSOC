from app.ai.copilot.local_llm import LocalLLM
from app.ai.detection_engine.generators.base_generator import BaseGenerator


class SigmaGenerator(BaseGenerator):

    def __init__(self):

        self.llm = LocalLLM()

    def generate(
        self,
        title,
        description,
        mitre=None
    ):

        techniques = ""

        if mitre:

            techniques = "\n".join(
                [
                    f"{x.technique_id} {x.name}"
                    for x in mitre
                ]
            )

        prompt = f"""
Generate a production-ready Sigma detection rule.

Title:
{title}

Description:
{description}

MITRE:
{techniques}

Requirements


Generate valid Sigma YAML.

Use Windows logsource if applicable.

Use MITRE ATT&CK tags.

No explanation.

Return ONLY YAML.
"""

        return self.llm.ask(prompt)