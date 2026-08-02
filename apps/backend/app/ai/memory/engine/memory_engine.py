from app.ai.memory.embedding.embedding_service import EmbeddingService
from app.ai.memory.storage.vector_store import VectorStore



class MemoryEngine:


    def __init__(self):

        self.embedding = EmbeddingService()

        self.vector = VectorStore()



    def remember(
        self,
        document_id,
        content
    ):


        vector = self.embedding.generate(
            content
        )


        self.vector.add(

            document_id,

            content,

            vector

        )


        return {

            "status":"stored",

            "id":document_id

        }



    def recall(
        self,
        query
    ):


        vector = self.embedding.generate(
            query
        )


        return self.vector.search(
            vector
        )