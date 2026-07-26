from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os


class MitreSemanticEngine:
    """
    Semantic MITRE ATT&CK similarity engine.
    """


    def __init__(self):

        self.model_name = (
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.model = None



    def load_model(self):

        if self.model is None:

            self.model = SentenceTransformer(
                self.model_name
            )



    def match(
        self,
        alert_text,
        techniques
    ):

        self.load_model()


        alert_vector = self.model.encode(
            [alert_text]
        )


        descriptions = []


        for technique in techniques:

            text = (
                technique.get("description")
                or
                technique.get("name")
                or
                ""
            )

            descriptions.append(text)



        technique_vectors = self.model.encode(
            descriptions
        )


        scores = cosine_similarity(
            alert_vector,
            technique_vectors
        )[0]



        results=[]


        for index, score in enumerate(scores):

            results.append(
                {
                    "technique":
                        techniques[index],

                    "semantic_score":
                        float(score)
                }
            )



        results.sort(
            key=lambda x:
            x["semantic_score"],
            reverse=True
        )


        return results[:10]