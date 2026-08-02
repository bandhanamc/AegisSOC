from sqlalchemy.orm import Session

from app.models.mitre_mapping import MitreMapping
from app.models.mitre_technique import MitreTechnique

from app.services.mitre_semantic_engine import MitreSemanticEngine
from app.services.mitre_confidence_engine import MitreConfidenceEngine
from app.services.alert_normalizer import AlertNormalizer


class MitreMappingService:

    def __init__(self):
        self.semantic_engine = MitreSemanticEngine()
        self.confidence_engine = MitreConfidenceEngine()
        self.normalizer = AlertNormalizer()

    def convert_alert_to_text(self, text):
        """
        Convert JSON alert into searchable text.
        """

        if isinstance(text, dict):

            values = []

            for value in text.values():

                if isinstance(value, list):

                    values.append(
                        " ".join(map(str, value))
                    )

                elif isinstance(value, dict):

                    values.append(
                        self.convert_alert_to_text(value)
                    )

                else:

                    values.append(str(value))

            return " ".join(values)

        return str(text)

    def ensure_string(self, data):

        if isinstance(data, dict):
            return self.convert_alert_to_text(data)

        return str(data)

    def get_existing_mapping(
        self,
        db: Session,
        vulnerability_id,
        technique_id: str
    ):
        """
        Check whether mapping already exists.
        """

        query = db.query(MitreMapping).filter(
            MitreMapping.technique_id == technique_id
        )

        if vulnerability_id not in (None, 0):
            query = query.filter(
                MitreMapping.vulnerability_id == vulnerability_id
            )
        else:
            query = query.filter(
                MitreMapping.vulnerability_id.is_(None)
            )

        return query.first()

    def map_alert(
        self,
        db: Session,
        vulnerability_id,
        text
    ):

        # Treat 0 as NULL
        if vulnerability_id == 0:
            vulnerability_id = None

        alert_text = self.convert_alert_to_text(text)

        print("ALERT TEXT:", alert_text)

        normalized_text = self.normalizer.normalize(alert_text)

        normalized_text = self.ensure_string(normalized_text)

        print("NORMALIZED TEXT:", normalized_text)

        techniques = db.query(MitreTechnique).all()

        technique_data = []

        for technique in techniques:

            technique_data.append({

                "technique_id": technique.technique_id,

                "name": technique.name,

                "description": technique.description or "",

                "detection": technique.detection or ""

            })

        matches = self.semantic_engine.match(
            normalized_text,
            technique_data
        )

        print("MATCH COUNT:", len(matches))

        saved = []

        for item in matches:

            technique = (
                db.query(MitreTechnique)
                .filter(
                    MitreTechnique.technique_id ==
                    item["technique_id"]
                )
                .first()
            )

            if not technique:
                continue

            technique_name_match = (
                technique.name.lower()
                in normalized_text.lower()
            )

            semantic_score = item.get(
                "score",
                item.get("semantic_score", 0)
            )

            keyword_score = item.get(
                "keyword_score",
                0
            )

            confidence = self.confidence_engine.calculate(
                semantic_score=semantic_score,
                keyword_score=keyword_score,
                technique_name_match=technique_name_match
            )

            print(
                "MAPPING DECISION:",
                {
                    "technique": technique.name,
                    "score": semantic_score,
                    "keyword": keyword_score,
                    "confidence": confidence
                }
            )

            if confidence == "LOW":
                continue

            confidence_score = {
                "LOW": 0.30,
                "MEDIUM": 0.70,
                "HIGH": 0.95
            }.get(confidence, 0.50)

            existing = self.get_existing_mapping(
                db=db,
                vulnerability_id=vulnerability_id,
                technique_id=technique.technique_id
            )

            if existing:

                existing.technique_name = technique.name
                existing.confidence_score = confidence_score
                existing.reasoning = item.get(
                    "reason",
                    "Updated AI semantic mapping"
                )

                saved.append(existing)

                continue

            mapping = MitreMapping(

                vulnerability_id=vulnerability_id,

                technique_id=technique.technique_id,

                technique_name=technique.name,

                confidence_score=confidence_score,

                reasoning=item.get(
                    "reason",
                    "AI semantic similarity mapping"
                )

            )

            db.add(mapping)

            saved.append(mapping)

        try:

            db.commit()

        except Exception as e:

            db.rollback()

            print("MITRE MAPPING ERROR:", str(e))

            raise

        print("TOTAL SAVED:", len(saved))

        return saved

    def map(
        self,
        db: Session,
        vulnerability_id,
        text
    ):

        return self.map_alert(
            db=db,
            vulnerability_id=vulnerability_id,
            text=text
        )