from sqlalchemy.orm import Session

from app.models.mitre import MitreTechnique
from app.services.mitre.semantic_matcher import SemanticMatcher


class MitreRetriever:

    def __init__(self, db: Session):

        self.db = db
        self.matcher = SemanticMatcher()

    def retrieve(self, alert: str):

        techniques = self.db.query(
            MitreTechnique
        ).all()

        return self.matcher.find_best_matches(
            alert,
            techniques,
            limit=5
        )