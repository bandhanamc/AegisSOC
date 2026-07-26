import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.mitre_technique import MitreTechnique


class MitreImportService:

    DATASET_PATH = Path(
        "data/enterprise-attack.json"
    )

    @staticmethod
    def import_dataset(db: Session):

        imported = 0
        skipped = 0

        with open(
            MitreImportService.DATASET_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            dataset = json.load(file)


        for obj in dataset["objects"]:

            # Only ATT&CK techniques
            if obj.get("type") != "attack-pattern":
                continue


            # Skip revoked techniques
            if obj.get("revoked"):
                skipped += 1
                continue


            technique_id = None

            for ref in obj.get(
                "external_references",
                []
            ):

                if (
                    ref.get("source_name")
                    == "mitre-attack"
                ):

                    technique_id = (
                        ref.get("external_id")
                    )


            if not technique_id:
                continue


            existing = (
                db.query(MitreTechnique)
                .filter(
                    MitreTechnique.technique_id
                    == technique_id
                )
                .first()
            )


            if existing:
                skipped += 1
                continue


            technique = MitreTechnique(

                technique_id=technique_id,

                name=obj.get(
                    "name"
                ),

                description=(
                    obj.get(
                        "description"
                    )
                ),

                platform=",".join(
                    obj.get(
                        "x_mitre_platforms",
                        []
                    )
                ),

                tactic=",".join(
                    obj.get(
                        "kill_chain_phases",
                        []
                    )
                )
            )


            db.add(
                technique
            )

            imported += 1


        db.commit()


        return {
            "imported": imported,
            "skipped": skipped
        }