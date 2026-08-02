from sqlalchemy.orm import Session

from app.services.mitre_mapping_service import MitreMappingService
from app.ai.detection_engine.detection_engine import DetectionEngine
from app.services.detection.audit import DetectionAudit


class DetectionIntelligenceService:

    def __init__(self):

        self.mitre = MitreMappingService()
        self.engine = DetectionEngine()
        self.audit = DetectionAudit()

    def analyze_rule(
        self,
        db: Session,
        rule_type: str,
        title: str,
        description: str
    ):

        # --------------------------------
        # Generate Detection Rule
        # --------------------------------

        generated_rule = self.engine.generate(
            rule_type=rule_type,
            title=title,
            description=description
        )

        # --------------------------------
        # Prepare text for MITRE Mapping
        # --------------------------------

        alert = {
            "rule_type": rule_type,
            "title": title,
            "description": description,
            "rule": generated_rule
        }

        # --------------------------------
        # MITRE Mapping
        # --------------------------------

        mappings = self.mitre.map_alert(
            db=db,
            vulnerability_id=None,
            text=alert
        )

        results = []

        for item in mappings:

            results.append(
                {
                    "technique_id": item.technique_id,
                    "technique_name": item.technique_name,
                    "confidence_score": item.confidence_score,
                    "reasoning": item.reasoning
                }
            )

        # --------------------------------
        # Audit
        # --------------------------------

        audit = self.audit.log(
            action="GENERATE_RULE",
            rule_type=rule_type,
            title=title
        )

        # --------------------------------
        # Final Response
        # --------------------------------

        return {
            "rule_type": rule_type,
            "title": title,
            "description": description,
            "generated_rule": generated_rule,
            "mitre_mapping": results,
            "audit": audit
        }