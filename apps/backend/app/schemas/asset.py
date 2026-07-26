from pydantic import BaseModel


class AssetCreate(BaseModel):

    hostname: str
    ip_address: str
    operating_system: str
    criticality: str = "medium"



class AssetResponse(AssetCreate):

    id: int

    class Config:
        from_attributes = True