from app.database.database import SessionLocal

from app.services.mitre.mitre_update_service import (
    update_mitre_database
)


db=SessionLocal()


result=update_mitre_database(
    db
)


print(result)


db.close()