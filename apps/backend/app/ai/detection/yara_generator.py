from app.ai.core.service_manager import AIServiceManager
from app.ai.parser.output_parser import OutputParser


class YaraGenerator:

    def __init__(self):

        self.ai = AIServiceManager()

    def generate_rule(

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
You are an expert malware detection engineer.

Generate a production-ready YARA rule.

Title:
{title}

Description:
{description}

MITRE ATT&CK:
{techniques}

Requirements:
- Return ONLY valid YARA code.
- Do NOT use markdown.
- Do NOT use triple backticks.
- Do NOT wrap the rule inside variables.
- Start directly with the word 'rule'.
- Include:
    - meta section
    - strings section
    - condition section
"""

        response = self.ai.llm.ask(

            prompt

        )

        return OutputParser.clean(

            response

        )