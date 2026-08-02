from app.ai.copilot.local_llm import LocalLLM
from app.ai.detection_engine.generators.base_generator import BaseGenerator


class YaraGenerator(BaseGenerator):

    def __init__(self):

        self.llm = LocalLLM()

    def generate(
        self,
        title,
        description,
        mitre=None
    ):

        prompt = f"""
Generate a production-ready YARA rule.

Title:
{title}

Description:
{description}

Return ONLY valid YARA.
"""

        return self.llm.ask(prompt)