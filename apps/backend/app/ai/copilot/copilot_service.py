from sqlalchemy.orm import Session

from app.ai.copilot.local_llm import LocalLLM
from app.ai.copilot.prompt_builder import PromptBuilder
from app.ai.faiss_mitre_mapper import FaissMitreMapper

from app.models.vulnerability import Vulnerability


class CopilotService:

    def __init__(self):

        self.llm = LocalLLM()

        self.mapper = FaissMitreMapper()

        self.prompt = PromptBuilder()

    def explain_vulnerability(

        self,

        db: Session,

        vulnerability_id: int

    ):

        vulnerability = db.query(

            Vulnerability

        ).filter(

            Vulnerability.id == vulnerability_id

        ).first()

        if vulnerability is None:

            return "Vulnerability not found."

        mitre = self.mapper.map_vulnerability(

            db,

            vulnerability,

            top_k=5

        )

        prompt = self.prompt.build_vulnerability_prompt(

            vulnerability,

            mitre,

            vulnerability.cwe_id

        )

        return self.llm.ask(

            prompt

        )