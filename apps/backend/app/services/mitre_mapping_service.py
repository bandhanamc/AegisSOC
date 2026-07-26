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
        Convert JSON alert fields into searchable text.
        """

        if isinstance(text, dict):

            values = []


            for key, value in text.items():

                if isinstance(value, list):

                    values.append(
                        " ".join(
                            map(str, value)
                        )
                    )


                elif isinstance(value, dict):

                    values.append(
                        self.convert_alert_to_text(value)
                    )


                else:

                    values.append(
                        str(value)
                    )


            return " ".join(values)


        return str(text)



    def ensure_string(self, data):
        """
        Ensure alert data is always string.
        """

        if isinstance(data, dict):

            return self.convert_alert_to_text(data)


        return str(data)



    def get_existing_mapping(
        self,
        db: Session,
        alert_id: int,
        technique_id: str
    ):

        return (

            db.query(
                MitreMapping
            )

            .filter(

                MitreMapping.alert_id == alert_id,

                MitreMapping.technique_id == technique_id

            )

            .first()

        )



    def map_alert(
        self,
        db: Session,
        alert_id: int,
        text
    ):


        # -------------------------------
        # Convert alert to text
        # -------------------------------

        alert_text = self.convert_alert_to_text(
            text
        )


        print(
            "ALERT TEXT:",
            alert_text
        )



        # -------------------------------
        # Normalize alert
        # -------------------------------

        normalized_text = self.normalizer.normalize(
            alert_text
        )


        normalized_text = self.ensure_string(
            normalized_text
        )


        print(
            "NORMALIZED TEXT:",
            normalized_text
        )



        # -------------------------------
        # Load MITRE techniques
        # -------------------------------

        techniques = (

            db.query(
                MitreTechnique
            )

            .all()

        )


        technique_data = []



        for technique in techniques:

            technique_data.append(

                {

                    "technique_id":
                        technique.technique_id,


                    "name":
                        technique.name,


                    "description":
                        technique.description or "",


                    "detection":
                        technique.detection or ""

                }

            )



        # -------------------------------
        # Semantic matching
        # -------------------------------

        matches = self.semantic_engine.match(

            normalized_text,

            technique_data

        )


        print(
            "MATCH COUNT:",
            len(matches)
        )



        saved = []



        for item in matches:



            technique = (

                db.query(
                    MitreTechnique
                )

                .filter(

                    MitreTechnique.technique_id
                    ==
                    item["technique_id"]

                )

                .first()

            )



            if not technique:

                continue



            # -------------------------------
            # Technique name validation
            # -------------------------------

            technique_name_match = (

                technique.name.lower()

                in normalized_text.lower()

            )



            # -------------------------------
            # Use boosted score
            # -------------------------------

            semantic_score = item.get(

                "score",

                item.get(
                    "semantic_score",
                    0
                )

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

                    "technique":
                        technique.name,

                    "score":
                        semantic_score,

                    "keyword":
                        keyword_score,

                    "confidence":
                        confidence

                }

            )



            # Ignore weak mappings

            if confidence == "LOW":

                print(
                    "LOW CONFIDENCE SKIPPED:",
                    technique.name
                )

                continue



            # -------------------------------
            # Check existing mapping
            # -------------------------------

            existing = self.get_existing_mapping(

                db,

                alert_id,

                technique.technique_id

            )



            if existing:


                print(

                    "UPDATING EXISTING MAPPING:",
                    technique.technique_id

                )


                existing.technique_name = technique.name

                existing.tactic = (

                    technique.tactic
                    or "unknown"

                )

                existing.confidence = confidence

                existing.ai_generated = True

                existing.reasoning = item.get(

                    "reason",

                    "Updated AI semantic similarity mapping"

                )


                saved.append(existing)


                continue



            # -------------------------------
            # Create new mapping
            # -------------------------------

            mapping = MitreMapping(

                alert_id=alert_id,


                technique_id=
                    technique.technique_id,


                technique_name=
                    technique.name,


                tactic=
                    technique.tactic
                    or "unknown",


                confidence=
                    confidence,


                ai_generated=True,


                reasoning=item.get(

                    "reason",

                    "AI semantic similarity with evidence correlation"

                )

            )



            db.add(mapping)

            saved.append(mapping)



        # -------------------------------
        # Commit transaction
        # -------------------------------

        try:

            db.commit()


        except Exception as e:


            db.rollback()


            print(

                "MITRE MAPPING ERROR:",

                str(e)

            )


            raise e



        print(

            "TOTAL SAVED/UPDATED MAPPINGS:",

            len(saved)

        )


        return saved