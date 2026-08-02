from app.ai.copilot.local_llm import LocalLLM
from app.ai.detection_engine.generators.base_generator import BaseGenerator


class SPLGenerator(BaseGenerator):

    def __init__(self):

        self.llm = LocalLLM()

    def generate(
        self,
        title,
        description,
        mitre=None
    ):

        prompt = f"""
Generate Splunk SPL.

Title:
{title}

Description:
{description}

Return ONLY SPL.
"""

        return self.llm.ask(prompt)