from app.ai.copilot.local_llm import LocalLLM
from app.ai.detection_engine.generators.base_generator import BaseGenerator


class EQLGenerator(BaseGenerator):

    def __init__(self):

        self.llm = LocalLLM()

    def generate(
        self,
        title,
        description,
        mitre=None
    ):

        prompt = f"""
Generate Elastic EQL.

Title:
{title}

Description:
{description}

Return ONLY EQL.
"""

        return self.llm.ask(prompt)