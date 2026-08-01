from app.database.database import SessionLocal
from app.models.vulnerability import Vulnerability
from app.ai.faiss_mitre_mapper import FaissMitreMapper


db = SessionLocal()


vulnerability = db.query(
    Vulnerability
).first()



print(
    "Testing:",
    vulnerability.title
)



mapper = FaissMitreMapper()



results = mapper.map_vulnerability(
    db,
    vulnerability,
    top_k=5
)



print("\nMITRE Results")

for r in results:
    print(r)



db.close()