from pydantic import BaseModel
from datetime import datetime


class SecurityEventCreate(BaseModel):

    source: str
    event_type: str
    raw_event: str

    username: str | None = None
    hostname: str | None = None

    source_ip: str | None = None
    destination_ip: str | None = None

    severity: str | None = "LOW"


class SecurityEventResponse(BaseModel):

    id: int

    source: str
    event_type: str
    raw_event: str

    username: str | None
    hostname: str | None

    source_ip: str | None
    destination_ip: str | None

    severity: str | None

    processed: bool

    created_at: datetime


    class Config:
        from_attributes = True