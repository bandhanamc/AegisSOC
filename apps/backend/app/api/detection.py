from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.detection import (
    DetectionRuleCreate,
    DetectionRuleUpdate,
    DetectionRuleResponse
)

from app.services.detection_service import (
    create_detection_rule,
    get_detection_rules,
    get_detection_rule,
    update_detection_rule,
    delete_detection_rule
)

from app.dependencies.permissions import require_role



router = APIRouter(
    prefix="/api/v1/detection",
    tags=["Detection Engine"]
)



@router.post(
    "/rules",
    response_model=DetectionRuleResponse
)
def create_rule(
    rule: DetectionRuleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_role(
            ["admin","analyst"]
        )
    )
):

    return create_detection_rule(
        db,
        rule
    )



@router.get(
    "/rules",
    response_model=list[DetectionRuleResponse]
)
def list_rules(
    db: Session = Depends(get_db),
    current_user = Depends(
        require_role(
            ["admin","analyst","viewer"]
        )
    )
):

    return get_detection_rules(db)



@router.get(
    "/rules/{rule_id}",
    response_model=DetectionRuleResponse
)
def read_rule(
    rule_id:int,
    db:Session=Depends(get_db),
    current_user=Depends(
        require_role(
            ["admin","analyst","viewer"]
        )
    )
):

    rule=get_detection_rule(
        db,
        rule_id
    )


    if not rule:
        raise HTTPException(
            status_code=404,
            detail="Detection rule not found"
        )

    return rule



@router.put(
    "/rules/{rule_id}",
    response_model=DetectionRuleResponse
)
def edit_rule(
    rule_id:int,
    rule:DetectionRuleUpdate,
    db:Session=Depends(get_db),
    current_user=Depends(
        require_role(
            ["admin","analyst"]
        )
    )
):

    updated=update_detection_rule(
        db,
        rule_id,
        rule
    )


    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Detection rule not found"
        )

    return updated



@router.delete(
    "/rules/{rule_id}"
)
def remove_rule(
    rule_id:int,
    db:Session=Depends(get_db),
    current_user=Depends(
        require_role(
            ["admin"]
        )
    )
):

    deleted=delete_detection_rule(
        db,
        rule_id
    )


    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Detection rule not found"
        )


    return {
        "message":"Detection rule deleted"
    }