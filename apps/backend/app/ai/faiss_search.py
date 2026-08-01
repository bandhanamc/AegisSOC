import os
import pickle
import faiss
import numpy as np



class FaissMitreSearch:


    def __init__(self):

        base_path = os.path.dirname(
            __file__
        )


        vector_path = os.path.join(
            base_path,
            "vector_store",
            "mitre.index"
        )


        metadata_path = os.path.join(
            base_path,
            "vector_store",
            "mitre.pkl"
        )


        self.index = faiss.read_index(
            vector_path
        )


        with open(
            metadata_path,
            "rb"
        ) as f:

            self.metadata = pickle.load(
                f
            )




    def search(
        self,
        embedding,
        top_k=5
    ):


        vector = np.array(
            [
                embedding
            ],
            dtype="float32"
        )


        scores, indexes = self.index.search(
            vector,
            top_k
        )



        results=[]



        for score, idx in zip(
            scores[0],
            indexes[0]
        ):


            if idx == -1:
                continue



            item = self.metadata[idx]


            results.append(
                {
                    "technique_id": item["technique_id"],

                    "name": item["name"],

                    "score": round(
                        float(score),
                        4
                    )
                }
            )



        return results