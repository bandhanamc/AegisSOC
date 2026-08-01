from sqlalchemy.orm import Session

from app.ai.semantic_matcher import SemanticMatcher

from app.models.mitre_technique import MitreTechnique
from app.models.mitre_mapping import MitreMapping



class MitreMapper:


    def __init__(
        self,
        minimum_score=0.30
    ):

        self.matcher = SemanticMatcher()

        self.minimum_score = minimum_score



    def map_vulnerability(
        self,
        db: Session,
        vulnerability,
        top_k=5
    ):


        try:

            vulnerability_text = f"""

            Vulnerability Title:
            {vulnerability.title}


            Description:
            {vulnerability.description or ""}


            Solution:
            {vulnerability.solution or ""}

            """



            techniques = db.query(
                MitreTechnique
            ).all()



            if not techniques:

                return []



            technique_texts = []


            for technique in techniques:


                technique_texts.append(
                    f"""

                    Technique ID:
                    {technique.technique_id}


                    Name:
                    {technique.name}


                    Description:
                    {technique.description or ""}


                    Detection:
                    {technique.detection or ""}


                    Mitigation:
                    {technique.mitigation or ""}

                    """
                )



            vulnerability_embedding = self.matcher.encode(
                [
                    vulnerability_text
                ]
            )[0]



            technique_embeddings = self.matcher.encode(
                technique_texts
            )



            similarity_results = []



            for index, embedding in enumerate(
                technique_embeddings
            ):


                score = float(
                    vulnerability_embedding @ embedding
                )



                if score >= self.minimum_score:


                    similarity_results.append(
                        {
                            "technique": techniques[index],
                            "score": score
                        }
                    )



            similarity_results.sort(
                key=lambda x: x["score"],
                reverse=True
            )



            mapped_results = []



            for item in similarity_results[:top_k]:


                technique = item["technique"]


                existing = db.query(
                    MitreMapping
                ).filter(
                    MitreMapping.vulnerability_id == vulnerability.id,
                    MitreMapping.technique_id == technique.technique_id
                ).first()



                if existing:

                    continue



                mapping = MitreMapping(


                    vulnerability_id=vulnerability.id,


                    technique_id=technique.technique_id,


                    technique_name=technique.name,


                    confidence_score=item["score"],


                    reasoning=(

                        "Local AI semantic similarity mapping "
                        "between vulnerability details and "
                        "MITRE ATT&CK technique knowledge base."

                    )

                )



                db.add(mapping)



                mapped_results.append(
                    {

                        "technique_id":
                            technique.technique_id,


                        "name":
                            technique.name,


                        "score":
                            round(
                                item["score"],
                                4
                            )

                    }
                )



            db.commit()


            return mapped_results



        except Exception:


            db.rollback()

            raise