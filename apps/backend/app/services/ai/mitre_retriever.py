from sqlalchemy.orm import Session

from app.models.mitre import MitreTechnique
from app.services.mitre.semantic_matcher import SemanticMatcher


class MitreRetriever:
    """
    Retrieves the most relevant MITRE ATT&CK techniques
    using semantic similarity.
    """

    def __init__(self, db: Session):
        self.db = db
        self.matcher = SemanticMatcher()

    def retrieve(
        self,
        alert: str,
        limit: int = 5
    ):

        techniques = self.db.query(
            MitreTechnique
        ).all()

        matches = self.matcher.find_best_matches(
            alert,
            techniques,
            limit=limit
        )

        return matches