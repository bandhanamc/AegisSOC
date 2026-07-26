from app.database.database import Base, engine

from app.models.user import User
from app.models.asset import Asset


Base.metadata.create_all(
    bind=engine
)


print("Database tables created")