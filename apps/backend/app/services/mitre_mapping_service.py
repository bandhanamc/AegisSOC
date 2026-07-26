from sqlalchemy.orm import Session

from app.models.mitre_mapping import MitreMapping
from app.models.mitre_technique import MitreTechnique

from app.services.alert_normalizer import AlertNormalizer
from app.services.mitre_semantic_engine import MitreSemanticEngine
from app.services.mitre_confidence_engine import MitreConfidenceEngine
from app.services.technique_matcher import TechniqueMatcher



class MitreMappingService:
    """
    AI assisted MITRE ATT&CK mapping engine.

    Flow:

    Alert
      |
    Normalization
      |
    Keyword Matching
      |
    Semantic Similarity
      |
    Confidence Calculation
      |
    MITRE Mapping
    """


    def __init__(self):

        self.normalizer = AlertNormalizer()

        self.semantic_engine = MitreSemanticEngine()

        self.confidence_engine = MitreConfidenceEngine()

        self.keyword_engine = TechniqueMatcher()



    def map_alert(
        self,
        db: Session,
        alert_id: int,
        text: str
    ):


        # -----------------------------
        # Normalize alert
        # -----------------------------

        normalized = (
            self.normalizer
            .normalize(text)
        )



        # -----------------------------
        # Load MITRE techniques
        # -----------------------------

        techniques = (
            db.query(MitreTechnique)
            .all()
        )


        technique_data=[]


        for technique in techniques:

            technique_data.append(
                {
                    "technique_id":
                        technique.technique_id,

                    "name":
                        technique.name,

                    "description":
                        technique.description
                }
            )



        # -----------------------------
        # Keyword matching
        # -----------------------------

        keyword_matches = (
            self.keyword_engine.match(
                text,
                technique_data
            )
        )



        keyword_map={}


        for item in keyword_matches:

            keyword_map[
                item["technique_id"]
            ] = item["score"]



        # -----------------------------
        # Semantic matching
        # -----------------------------

        semantic_matches = (
            self.semantic_engine.match(
                text,
                technique_data
            )
        )



        final=[]


        for item in semantic_matches:


            technique = item["technique"]


            technique_id = (
                technique["technique_id"]
            )


            keyword_score = (
                keyword_map.get(
                    technique_id,
                    0
                )
            )



            confidence = (
                self.confidence_engine.calculate(
                    keyword_score / 10,
                    item["semantic_score"]
                )
            )



            final.append(
                {
                    "technique": technique,
                    "confidence": confidence
                }
            )



        final.sort(
            key=lambda x:
                x["confidence"]["score"],
            reverse=True
        )



        saved=[]



        for item in final[:5]:


            technique=item["technique"]


            mapping = MitreMapping(

                alert_id=alert_id,

                technique_id=
                    technique["technique_id"],

                technique_name=
                    technique["name"],

                tactic=
                    technique.get(
                        "tactic",
                        "unknown"
                    ),

                confidence=
                    item["confidence"]["level"],

                ai_generated=True,

                reasoning=
                    "AI semantic similarity + keyword correlation"

            )


            db.add(mapping)

            saved.append(mapping)



        db.commit()


        return saved