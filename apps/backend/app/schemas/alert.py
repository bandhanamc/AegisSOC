from datetime import datetime
from pydantic import BaseModel


class AlertBase(BaseModel):

    event_id: int
    rule_id: int
    title: str
    description: str | None = None
    severity: str
    mitre_technique: str | None = None


class AlertCreate(AlertBase):
    pass


class AlertResponse(AlertBase):

    id: int
    status: str | None = None
    assigned_to: int | None = None
    investigated: bool
    created_at: datetime

    class Config:
        from_attributes = True