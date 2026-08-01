"""
AegisSOC Knowledge Engine

Central intelligence retrieval layer.

Every AI feature should retrieve information
through this engine.

Future Sources
--------------
- MITRE
- FAISS
- CVE
- CWE
- Assets
- Historical Findings
- Threat Intelligence
"""

from sqlalchemy.orm import Session

from app.ai.rag.context_builder import ContextBuilder


class KnowledgeEngine:

    def __init__(self):

        self.context_builder = ContextBuilder()

    def get_context(
        self,
        db: Session,
        vulnerability_id: int
    ):

        context = self.context_builder.build(
            db,
            vulnerability_id
        )

        if context is None:
            return None

        return {

            "vulnerability":
                context["vulnerability"],

            "asset":
                context["asset"],

            "mitre":
                context["mitre"],

            "similar":
                context["similar"],

            "cve": None,

            "cwe": None,

            "ioc": [],

            "threat_intel": [],

            "attack_paths": [],

            "recommendations": []

        }