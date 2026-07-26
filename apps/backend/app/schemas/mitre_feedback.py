from pydantic import BaseModel



class MitreFeedbackCreate(BaseModel):

    mapping_id:int

    analyst:str

    decision:str

    comment:str | None = None