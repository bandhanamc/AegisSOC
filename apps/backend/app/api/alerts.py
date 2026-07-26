from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.alert import (
    AlertCreate,
    AlertResponse
)

from app.services.alert_service import (
    create_alert,
    get_alerts,
    get_alert
)

from app.dependencies.permissions import require_role


router = APIRouter(
    prefix="/api/v1/alerts",
    tags=["Alerts"]
)



@router.post(
    "",
    response_model=AlertResponse
)
def add_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_role(
            ["admin","analyst"]
        )
    )
):

    return create_alert(
        db,
        alert
    )



@router.get(
    "",
    response_model=list[AlertResponse]
)
def list_alerts(
    db: Session = Depends(get_db),
    current_user = Depends(
        require_role(
            ["admin","analyst","viewer"]
        )
    )
):

    return get_alerts(db)



@router.get(
    "/{alert_id}",
    response_model=AlertResponse
)
def read_alert(
    alert_id:int,
    db:Session = Depends(get_db),
    current_user = Depends(
        require_role(
            ["admin","analyst","viewer"]
        )
    )
):

    alert = get_alert(
        db,
        alert_id
    )

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert