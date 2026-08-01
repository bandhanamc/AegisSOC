import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatIP(dimension)
        self.documents = []

    def build(self, embeddings: np.ndarray, documents: list):

        self.index.reset()

        self.index.add(
            embeddings.astype(np.float32)
        )

        self.documents = documents

    def search(
        self,
        embedding: np.ndarray,
        top_k: int = 5,
    ):

        scores, ids = self.index.search(
            embedding.reshape(1, -1).astype(np.float32),
            top_k,
        )

        results = []

        for score, idx in zip(scores[0], ids[0]):

            if idx == -1:
                continue

            results.append(
                (
                    self.documents[idx],
                    float(score),
                )
            )

        return results