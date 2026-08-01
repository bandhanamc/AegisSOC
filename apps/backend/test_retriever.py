from app.db.session import SessionLocal
from app.services.ai.mitre_retriever import MitreRetriever

db = SessionLocal()

retriever = MitreRetriever(db)

results = retriever.retrieve(
    "powershell.exe downloaded file with encoded command"
)

for item in results:
    print(item)