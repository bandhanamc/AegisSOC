from sqlalchemy.orm import Session

from app.ai.core.service_manager import AIServiceManager
from app.ai.copilot.prompt_builder import PromptBuilder

from app.models.vulnerability import Vulnerability


class CopilotService:

    def __init__(self):

        self.ai = AIServiceManager()

        self.prompt = PromptBuilder()

    def explain_vulnerability(

        self,

        db: Session,

        vulnerability_id: int

    ):

        vulnerability = (

            db.query(Vulnerability)

            .filter(Vulnerability.id == vulnerability_id)

            .first()

        )

        if vulnerability is None:

            return "Vulnerability not found."

        query = (
            f"{vulnerability.title or ''}\n"
            f"{vulnerability.description or ''}"
        )

        embedding = self.ai.matcher.encode(query)

        mitre = self.ai.search.search(

            embedding,

            top_k=5

        )

        prompt = self.prompt.build_vulnerability_prompt(

            vulnerability,

            mitre,

            vulnerability.cwe_id

        )

        return self.ai.llm.ask(

            prompt

        )