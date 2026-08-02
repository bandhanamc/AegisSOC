from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.detection_generator import DetectionGenerator


router = APIRouter(
    prefix="/api/v1/detection",
    tags=["AI Detection"]
)

generator = DetectionGenerator()


@router.post("/generate/{vulnerability_id}")
def generate_detection(
    vulnerability_id: int,
    detection_type: str,
    db: Session = Depends(get_db)
):

    try:

        rule = generator.generate(
            db=db,
            vulnerability_id=vulnerability_id,
            detection_type=detection_type
        )

        return {
            "success": True,
            "vulnerability_id": vulnerability_id,
            "detection_type": detection_type,
            "rule": rule
        }

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )