from app.database.database import SessionLocal
from app.models.vulnerability import Vulnerability
from app.ai.faiss_mitre_mapper import FaissMitreMapper


db = SessionLocal()


vulnerability = db.query(
    Vulnerability
).offset(10).first()


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


print("\nResults")


for r in results:
    print(r)



db.close()