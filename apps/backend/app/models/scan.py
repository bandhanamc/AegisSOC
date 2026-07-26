from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.database.database import Base


class Scan(Base):

    __tablename__ = "scans"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    asset_id = Column(
        Integer,
        ForeignKey("assets.id"),
        nullable=False
    )


    scanner = Column(
        String,
        nullable=False
    )


    scan_type = Column(
        String,
        nullable=False
    )


    status = Column(
        String,
        default="Pending"
    )


    started_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    completed_at = Column(
        DateTime,
        nullable=True
    )