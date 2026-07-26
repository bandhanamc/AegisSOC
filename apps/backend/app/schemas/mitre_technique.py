from pydantic import BaseModel


class MitreTechniqueBase(BaseModel):
    technique_id: str
    name: str
    tactic: str
    platform: str | None = None
    detection: str | None = None
    mitigation: str | None = None
    description: str | None = None


class MitreTechniqueCreate(MitreTechniqueBase):
    pass


class MitreTechniqueResponse(MitreTechniqueBase):
    id: int

    class Config:
        from_attributes = True