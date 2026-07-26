from pydantic import BaseModel
from datetime import datetime


class AssetCreate(BaseModel):

    hostname: str
    ip_address: str
    operating_system: str | None = None
    criticality: str = "medium"
    asset_type: str = "server"
    owner: str | None = None
    environment: str = "production"
    status: str = "active"



class AssetUpdate(BaseModel):

    hostname: str | None = None
    ip_address: str | None = None
    operating_system: str | None = None
    criticality: str | None = None
    asset_type: str | None = None
    owner: str | None = None
    environment: str | None = None
    status: str | None = None



class AssetResponse(AssetCreate):

    id: int
    last_seen: datetime | None = None
    created_at: datetime | None = None


    class Config:
        from_attributes = True