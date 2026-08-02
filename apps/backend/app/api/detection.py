from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.detection.intelligence_service import (
    DetectionIntelligenceService
)



router = APIRouter(

    prefix="/api/v1/detection",

    tags=["AI Detection"]

)



service = DetectionIntelligenceService()



@router.post("/intelligence")
def analyze_detection(

    rule_type: str,

    title: str,

    description: str,

    db: Session = Depends(get_db)

):


    return service.analyze_rule(

        db,

        rule_type,

        title,

        description

    )