from pydantic import BaseModel
from datetime import datetime


class ScanCreate(BaseModel):

    asset_id: int
    scanner: str
    scan_type: str



class ScanResponse(BaseModel):

    id: int
    asset_id: int
    scanner: str
    scan_type: str
    status: str
    started_at: datetime
    completed_at: datetime | None


    class Config:
        from_attributes = True