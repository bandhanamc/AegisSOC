from app.database.database import engine
from app.models.mitre_mapping import MitreMapping


MitreMapping.__table__.create(
    bind=engine
)


print("MITRE mapping table recreated successfully")
