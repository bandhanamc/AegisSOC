from app.ai.core.service_manager import AIServiceManager


class DetectionGenerator:

    def __init__(self):

        self.ai = AIServiceManager()

    def generate_sigma(

        self,

        title: str,

        description: str,

        mitre

    ):

        techniques = "\n".join(

            f"- {t['technique_id']} {t['name']}"

            for t in mitre

        )

        prompt = f"""

You are a Senior Detection Engineer.

Generate a production-ready Sigma rule.

Vulnerability

Title:
{title}

Description:
{description}

MITRE ATT&CK

{techniques}

Return ONLY valid Sigma YAML.

"""

        return self.ai.llm.ask(prompt)