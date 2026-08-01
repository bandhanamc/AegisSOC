from sqlalchemy.orm import Session

from app.ai.faiss_search import FaissMitreSearch
from app.models.mitre_mapping import MitreMapping



class MitreMapper:


    def __init__(self):

        self.search_engine = FaissMitreSearch()



    def map_vulnerability(
        self,
        db: Session,
        vulnerability,
        top_k=5
    ):


        text = f"""

        Vulnerability:
        {vulnerability.title}


        Description:
        {vulnerability.description or ""}


        Solution:
        {vulnerability.solution or ""}

        """



        results = self.search_engine.search(
            text,
            top_k
        )



        mapped = []



        for result in results:


            existing = db.query(
                MitreMapping
            ).filter(

                MitreMapping.vulnerability_id ==
                vulnerability.id,

                MitreMapping.technique_id ==
                result["technique_id"]

            ).first()



            if existing:

                continue



            mapping = MitreMapping(

                vulnerability_id=vulnerability.id,

                technique_id=result["technique_id"],

                technique_name=result["name"],

                confidence_score=result["score"],

                reasoning=(
                    "Mapped using local FAISS vector similarity "
                    "against MITRE ATT&CK knowledge base"
                )

            )


            db.add(mapping)



            mapped.append(result)



        db.commit()


        return mapped