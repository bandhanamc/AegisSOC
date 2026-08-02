from app.ai.copilot.local_llm import LocalLLM
from app.ai.detection_engine.generators.base_generator import BaseGenerator


class KQLGenerator(BaseGenerator):

    def __init__(self):

        self.llm = LocalLLM()

    def generate(
        self,
        title,
        description,
        mitre=None
    ):

        prompt = f"""
Generate Microsoft Sentinel KQL.

Title:
{title}

Description:
{description}

Return ONLY KQL.
"""

        return self.llm.ask(prompt)