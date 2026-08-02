from datetime import datetime

from pydantic import BaseModel


class DetectionRuleBase(BaseModel):

    name: str

    description: str

    rule_type: str

    severity: str

    query: str

    enabled: bool = True


class DetectionRuleCreate(DetectionRuleBase):
    pass


class DetectionRuleUpdate(BaseModel):

    name: str | None = None

    description: str | None = None

    severity: str | None = None

    query: str | None = None

    enabled: bool | None = None


class DetectionRuleResponse(DetectionRuleBase):

    id: int

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }