from app.core.llm.model_manager import ModelManager
from app.core.llm.prompt_builder import PromptBuilder
from app.core.llm.response_parser import ResponseParser


class MitreAIEngine:

    def __init__(self):

        self.model = ModelManager()

    def analyze(self, alert, candidates):

        prompt = PromptBuilder.build_mitre_prompt(
            alert,
            candidates
        )

        response = self.model.ask(
            task="mitre_mapping",
            prompt=prompt
        )

        return ResponseParser.parse(response)