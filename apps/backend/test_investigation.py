from app.database.database import SessionLocal
from app.ai.investigation import InvestigationEngine

db = SessionLocal()

engine = InvestigationEngine()

report = engine.investigate(
    db,
    1102
)

print(report)

db.close()