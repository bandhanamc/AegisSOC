import json
import re

from pathlib import Path

from sqlalchemy.orm import Session

from app.models.mitre_technique import MitreTechnique


class MitreImportService:

    DATASET_PATH = Path(
        "data/enterprise-attack.json"
    )


    @staticmethod
    def clean_text(text):

        if not text:
            return ""

        # Remove MITRE citation references
        text = re.sub(
            r"\[\d+\]",
            "",
            text
        )

        return text.strip()



    @staticmethod
    def extract_technique_id(obj):

        for ref in obj.get(
            "external_references",
            []
        ):

            if (
                ref.get("source_name")
                == "mitre-attack"
            ):

                return ref.get(
                    "external_id"
                )

        return None



    @staticmethod
    def extract_tactics(obj):

        tactics = []


        for phase in obj.get(
            "kill_chain_phases",
            []
        ):

            name = phase.get(
                "phase_name"
            )

            if name:
                tactics.append(
                    name
                )


        return ",".join(
            tactics
        )



    @staticmethod
    def import_dataset(
        db: Session
    ):


        imported = 0
        skipped = 0


        with open(
            MitreImportService.DATASET_PATH,
            "r",
            encoding="utf-8"
        ) as file:


            dataset = json.load(
                file
            )



        for obj in dataset.get(
            "objects",
            []
        ):


            # Only ATT&CK techniques
            if obj.get(
                "type"
            ) != "attack-pattern":

                continue



            # Ignore revoked techniques
            if obj.get(
                "revoked"
            ):

                skipped += 1
                continue



            technique_id = (
                MitreImportService
                .extract_technique_id(
                    obj
                )
            )


            if not technique_id:
                continue



            existing = (
                db.query(
                    MitreTechnique
                )
                .filter(
                    MitreTechnique
                    .technique_id
                    ==
                    technique_id
                )
                .first()
            )


            if existing:

                skipped += 1
                continue



            technique = MitreTechnique(


                technique_id=(
                    technique_id
                ),



                name=(
                    obj.get(
                        "name"
                    )
                ),



                description=(
                    MitreImportService
                    .clean_text(
                        obj.get(
                            "description"
                        )
                    )
                ),



                platform=",".join(
                    obj.get(
                        "x_mitre_platforms",
                        []
                    )
                ),



                tactic=(
                    MitreImportService
                    .extract_tactics(
                        obj
                    )
                )

            )



            db.add(
                technique
            )


            imported += 1



        db.commit()



        return {

            "imported":
                imported,

            "skipped":
                skipped

        }