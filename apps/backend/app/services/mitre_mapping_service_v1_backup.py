from sqlalchemy.orm import Session

from app.models.mitre_mapping import MitreMapping
from app.models.mitre_technique import MitreTechnique

from app.services.technique_matcher import TechniqueMatcher


class MitreMappingService:

    def __init__(self):
        self.matcher = TechniqueMatcher()


    def map_alert(
        self,
        db: Session,
        alert_id: int,
        text: str
    ):

        #
        # Load MITRE ATT&CK techniques
        #
        techniques = (
            db.query(MitreTechnique)
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
                        technique.description,

                    "detection":
                        technique.detection
                }
            )


        #
        # Match alert behavior
        #
        matches = self.matcher.match(
            text,
            technique_data
        )


        #
        # Remove parent techniques
        # Example:
        # Keep T1059.001 PowerShell
        # Remove T1059 Command and Scripting Interpreter
        #
        subtechnique_parents = set()


        for item in matches:

            technique_id = item.get(
                "technique_id"
            )

            if technique_id and "." in technique_id:

                parent_id = (
                    technique_id.split(".")[0]
                )

                subtechnique_parents.add(
                    parent_id
                )


        matches = [
            item
            for item in matches
            if not (
                item["technique_id"]
                in subtechnique_parents
            )
        ]


        #
        # Keep only top 3 techniques
        #
        matches = matches[:3]


        saved = []


        for item in matches:


            technique = (
                db.query(MitreTechnique)
                .filter(
                    MitreTechnique.technique_id
                    ==
                    item["technique_id"]
                )
                .first()
            )


            if not technique:
                continue



            #
            # Avoid duplicate mapping
            #
            existing = (
                db.query(MitreMapping)
                .filter(
                    MitreMapping.alert_id
                    ==
                    alert_id,

                    MitreMapping.technique_id
                    ==
                    technique.technique_id
                )
                .first()
            )


            if existing:
                continue



            mapping = MitreMapping(

                alert_id=alert_id,


                technique_id=
                    technique.technique_id,


                technique_name=
                    technique.name,


                tactic=
                    technique.tactic,


                confidence=
                    "HIGH"
                    if item.get("score", 0) >= 10
                    else "MEDIUM",


                ai_generated=False,


                reasoning=
                    item.get(
                        "reason",
                        "Behavior based MITRE ATT&CK matching"
                    )
            )


            db.add(mapping)

            saved.append(mapping)



        db.commit()


        return saved