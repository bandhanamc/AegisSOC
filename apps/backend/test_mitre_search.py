from app.database.database import SessionLocal
from app.services.mitre_retriever import MitreRetriever

db = SessionLocal()

retriever = MitreRetriever(db)

results = retriever.search(
    "SQL Injection vulnerability in login page",
    top_k=5,
)

for result in results:
    print(result)

db.close()