from fastapi import APIRouter

from pydantic import BaseModel

from typing import List, Dict

from app.ai.correlation import CorrelationEngine



router = APIRouter(

    prefix="/api/v1/correlation",

    tags=["AI Correlation"]

)



engine = CorrelationEngine()



class AlertInput(BaseModel):

    alerts: List[Dict]




@router.post("/analyze")
def analyze_alerts(

    data: AlertInput

):


    result = engine.correlate(

        data.alerts

    )


    return result