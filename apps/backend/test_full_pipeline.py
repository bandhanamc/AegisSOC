from app.database.database import SessionLocal
from app.models.vulnerability import Vulnerability
from app.models.mitre_mapping import MitreMapping


db = SessionLocal()


vulnerability = db.query(
    Vulnerability
).first()



print(
    "Vulnerability:"
)

print(
    vulnerability.title
)



mappings = db.query(
    MitreMapping
).filter(
    MitreMapping.vulnerability_id == vulnerability.id
).all()



print(
    "\nMITRE mappings:"
)



for m in mappings:

    print(
        m.technique_id,
        m.technique_name,
        m.confidence_score
    )



db.close()