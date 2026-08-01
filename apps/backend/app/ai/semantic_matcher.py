from sentence_transformers import SentenceTransformer
import numpy as np

from sqlalchemy.orm import Session

from app.models.mitre_technique import MitreTechnique


class SemanticMatcher:


    def __init__(
        self,
        model_name="all-MiniLM-L6-v2",
    ):

        self.model = SentenceTransformer(model_name)

        self.technique_cache = None
        self.embedding_cache = None



    def encode(
        self,
        texts
    ):

        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )



    def similarity(
        self,
        text1,
        text2,
    ):

        emb = self.encode(
            [
                text1,
                text2
            ]
        )

        return float(
            np.dot(
                emb[0],
                emb[1],
            )
        )



    def embedding_dimension(self):

        return self.model.get_embedding_dimension()



    def load_mitre_database(
        self,
        db: Session
    ):


        if self.technique_cache is not None:

            return



        techniques = (
            db.query(
                MitreTechnique
            )
            .all()
        )


        self.technique_cache = techniques



        texts = []


        for t in techniques:

            text = (
                f"{t.name}. "
                f"{t.description or ''}. "
                f"Detection: {t.detection or ''}"
            )

            texts.append(text)



        self.embedding_cache = self.encode(
            texts
        )



    def search(
        self,
        db: Session,
        query: str,
        top_k: int = 5
    ):


        self.load_mitre_database(
            db
        )


        query_embedding = self.encode(
            [
                query
            ]
        )[0]



        scores = np.dot(
            self.embedding_cache,
            query_embedding
        )


        indexes = np.argsort(
            scores
        )[::-1][:top_k]



        results = []


        for index in indexes:

            technique = (
                self.technique_cache[index]
            )


            results.append(

                {

                    "technique_id":
                    technique.technique_id,


                    "name":
                    technique.name,


                    "score":
                    round(
                        float(
                            scores[index]
                        ),
                        4
                    )

                }

            )


        return results