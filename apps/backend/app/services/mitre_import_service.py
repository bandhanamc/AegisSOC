import json
import re

from pathlib import Path

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.mitre_technique import MitreTechnique



class MitreImportService:


    DATASET_PATH = Path(
        "data/enterprise-attack.json"
    )



    @staticmethod
    def clean_text(text_value):

        if not text_value:
            return ""

        text_value = re.sub(
            r"\[\d+\]",
            "",
            text_value
        )

        return text_value.strip()



    @staticmethod
    def extract_technique_id(obj):

        for ref in obj.get(
            "external_references",
            []
        ):

            if ref.get(
                "source_name"
            ) == "mitre-attack":

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

            phase_name = phase.get(
                "phase_name"
            )

            if phase_name:
                tactics.append(
                    phase_name
                )


        return ",".join(
            tactics
        )



    @staticmethod
    def remove_duplicates(
        db: Session
    ):

        db.execute(
            text(
                """
                DELETE FROM mitre_techniques
                WHERE id NOT IN
                (
                    SELECT MIN(id)
                    FROM mitre_techniques
                    GROUP BY technique_id
                )
                """
            )
        )

        db.commit()



    @staticmethod
    def import_dataset(
        db: Session
    ):


        inserted = 0
        updated = 0
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


            if obj.get(
                "type"
            ) != "attack-pattern":

                continue



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



            name = obj.get(
                "name"
            )


            description = (
                MitreImportService
                .clean_text(
                    obj.get(
                        "description"
                    )
                )
            )


            platform = ",".join(
                obj.get(
                    "x_mitre_platforms",
                    []
                )
            )


            tactic = (
                MitreImportService
                .extract_tactics(
                    obj
                )
            )



            existing = db.query(
                MitreTechnique
            ).filter(
                MitreTechnique.technique_id
                ==
                technique_id
            ).first()



            if existing:


                existing.name = name

                existing.description = description

                existing.platform = platform

                existing.tactic = tactic


                updated += 1


            else:


                technique = MitreTechnique(

                    technique_id=technique_id,

                    name=name,

                    description=description,

                    platform=platform,

                    tactic=tactic

                )


                db.add(
                    technique
                )


                inserted += 1



        db.commit()



        # Cleanup duplicates after import

        MitreImportService.remove_duplicates(
            db
        )



        return {


            "inserted":
                inserted,


            "updated":
                updated,


            "skipped":
                skipped

        }