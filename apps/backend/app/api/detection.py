from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.detection.rule_schema import DetectionRuleCreate
from app.schemas.detection.rule_schema import DetectionRuleUpdate

from app.services import detection_service

router = APIRouter(
    prefix="/api/v1/detection",
    tags=["Detection Rules"]
)


@router.post("/rules")
def create_rule(
    rule: DetectionRuleCreate,
    db: Session = Depends(get_db)
):

    return detection_service.create_detection_rule(
        db,
        rule
    )


@router.get("/rules")
def list_rules(
    db: Session = Depends(get_db)
):

    return detection_service.get_detection_rules(db)


@router.get("/rules/{rule_id}")
def get_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):

    return detection_service.get_detection_rule(
        db,
        rule_id
    )


@router.put("/rules/{rule_id}")
def update_rule(
    rule_id: int,
    rule: DetectionRuleUpdate,
    db: Session = Depends(get_db)
):

    return detection_service.update_detection_rule(
        db,
        rule_id,
        rule
    )


@router.delete("/rules/{rule_id}")
def delete_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):

    return detection_service.delete_detection_rule(
        db,
        rule_id
    )