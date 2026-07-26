from pydantic import BaseModel
from datetime import datetime


class DetectionRuleCreate(BaseModel):

    name: str
    description: str | None = None
    rule_type: str
    severity: str
    query: str
    enabled: bool = True



class DetectionRuleUpdate(BaseModel):

    name: str | None = None
    description: str | None = None
    rule_type: str | None = None
    severity: str | None = None
    query: str | None = None
    enabled: bool | None = None



class DetectionRuleResponse(BaseModel):

    id: int
    name: str
    description: str | None
    rule_type: str
    severity: str
    query: str
    enabled: bool
    created_at: datetime
    updated_at: datetime | None


    class Config:
        from_attributes = True