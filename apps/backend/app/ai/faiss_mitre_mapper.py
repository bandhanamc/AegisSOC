from sqlalchemy.orm import Session

from app.ai.core.service_manager import AIServiceManager

from app.models.mitre_mapping import MitreMapping


class FaissMitreMapper:

    def __init__(self):

        self.ai = AIServiceManager()

        self.matcher = self.ai.matcher

        self.searcher = self.ai.search

    def map_vulnerability(
        self,
        db: Session,
        vulnerability,
        top_k=5,
        threshold=0.45
    ):

        text = f"""
        Vulnerability Title:
        {vulnerability.title}

        Description:
        {vulnerability.description or ""}

        Solution:
        {vulnerability.solution or ""}
        """

        embedding = self.matcher.encode(
            [text]
        )[0]

        results = self.searcher.search(
            embedding,
            top_k
        )

        mapped = []

        for item in results:

            score = item["score"]

            # Ignore weak semantic matches
            if score < threshold:
                continue

            existing = (
                db.query(MitreMapping)
                .filter(
                    MitreMapping.vulnerability_id == vulnerability.id,
                    MitreMapping.technique_id == item["technique_id"]
                )
                .first()
            )

            if existing:

                mapped.append(
                    {
                        "technique_id": existing.technique_id,
                        "name": existing.technique_name,
                        "score": existing.confidence_score,
                        "status": "existing"
                    }
                )

                continue

            mapping = MitreMapping(

                vulnerability_id=vulnerability.id,

                technique_id=item["technique_id"],

                technique_name=item["name"],

                confidence_score=item["score"],

                reasoning=(
                    "AI semantic mapping using local "
                    "Sentence Transformer embeddings "
                    "and FAISS vector search"
                )
            )

            db.add(mapping)

            mapped.append(
                {
                    "technique_id": item["technique_id"],
                    "name": item["name"],
                    "score": round(score, 4),
                    "status": "created"
                }
            )

        db.commit()

        return mapped