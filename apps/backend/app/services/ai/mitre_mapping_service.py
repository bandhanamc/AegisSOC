from sqlalchemy.orm import Session

from app.models.mitre_technique import MitreTechnique
from app.models.mitre_mapping import MitreMapping

from app.ai.semantic_matcher import SemanticMatcher



matcher = SemanticMatcher()



def map_vulnerability_to_mitre(
    db: Session,
    vulnerability_id: int,
    description: str
):


    results = matcher.search(
        db,
        description,
        top_k=5
    )


    mappings = []


    for item in results:


        mapping = MitreMapping(

            vulnerability_id=vulnerability_id,

            technique_id=item["technique_id"],

            technique_name=item["name"],

            confidence_score=item["score"],

            reasoning=
            "Matched using local semantic similarity model"

        )


        db.add(mapping)

        mappings.append(mapping)



    db.commit()


    return mappings