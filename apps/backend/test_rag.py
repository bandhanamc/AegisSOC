from app.database.database import SessionLocal
from app.ai.copilot.rag_engine import RAGEngine


db=SessionLocal()


rag=RAGEngine()


result = rag.get_context(
    db,
    "Ethernet"
)


for item in result:

    print(item)


db.close()