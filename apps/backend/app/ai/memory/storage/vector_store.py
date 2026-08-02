import chromadb



class VectorStore:


    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="./data/vector"
        )


        self.collection = (
            self.client.get_or_create_collection(
                "aegissoc_memory"
            )
        )


    def add(
        self,
        document_id,
        text,
        embedding
    ):


        self.collection.add(

            ids=[
                document_id
            ],

            documents=[
                text
            ],

            embeddings=[
                embedding
            ]

        )



    def search(
        self,
        embedding,
        limit=5
    ):


        return self.collection.query(

            query_embeddings=[
                embedding
            ],

            n_results=limit

        )