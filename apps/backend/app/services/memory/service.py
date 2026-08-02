from app.ai.memory.engine.memory_engine import MemoryEngine



class MemoryService:


    def __init__(self):

        self.engine = MemoryEngine()



    def store(
        self,
        document_id,
        content
    ):


        return self.engine.remember(

            document_id,

            content

        )



    def search(
        self,
        query
    ):


        return self.engine.recall(
            query
        )