from pydantic import BaseModel


class MitreMappingRequest(BaseModel):

    alert_id:int

    text:str