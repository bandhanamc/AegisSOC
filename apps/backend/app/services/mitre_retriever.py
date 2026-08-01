from sqlalchemy.orm import Session

from app.ai.semantic_matcher import SemanticMatcher
from app.ai.vector_store import VectorStore
from app.models.mitre_technique import MitreTechnique


class MitreRetriever:

    def __init__(self, db: Session):

        self.db = db

        self.matcher = SemanticMatcher()

        self.vector_store = VectorStore(
            self.matcher.embedding_dimension()
        )

        self.techniques = []

        self.build_index()

    def build_index(self):

        self.techniques = (
            self.db.query(MitreTechnique)
            .all()
        )

        documents = []

        for t in self.techniques:

            documents.append(
                f"""
Technique ID: {t.technique_id}
Technique: {t.name}
Tactic: {t.tactic}
Description: {t.description}
Detection: {t.detection}
Mitigation: {t.mitigation}
"""
            )

        embeddings = self.matcher.encode(
            documents
        )

        self.vector_store.build(
            embeddings,
            documents,
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
    ):

        query_embedding = self.matcher.encode(
            [query]
        )[0]

        matches = self.vector_store.search(
            query_embedding,
            top_k,
        )

        results = []

        for document, score in matches:

            for technique in self.techniques:

                text = f"""
Technique ID: {technique.technique_id}
Technique: {technique.name}
Tactic: {technique.tactic}
Description: {technique.description}
Detection: {technique.detection}
Mitigation: {technique.mitigation}
"""

                if text == document:

                    results.append(
                        {
                            "technique_id": technique.technique_id,
                            "name": technique.name,
                            "tactic": technique.tactic,
                            "score": round(score, 4),
                        }
                    )

        return results