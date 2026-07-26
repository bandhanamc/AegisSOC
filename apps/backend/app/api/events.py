from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.database import get_db


from app.schemas.security_event import (
    SecurityEventCreate,
    SecurityEventResponse
)


from app.services.event_ingestion_service import (
    ingest_event,
    get_events
)


from app.dependencies.permissions import require_role



router = APIRouter(

    prefix="/api/v1/events",

    tags=["Event Ingestion"]

)



@router.post(
    "/ingest",
    response_model=SecurityEventResponse
)
def ingest_security_event(

    event: SecurityEventCreate,

    db: Session = Depends(get_db),

    current_user = Depends(
        require_role(
            [
                "admin",
                "analyst"
            ]
        )
    )

):

    return ingest_event(
        db,
        event
    )





@router.get(
    "",
    response_model=list[SecurityEventResponse]
)
def list_events(

    db: Session = Depends(get_db),

    current_user = Depends(
        require_role(
            [
                "admin",
                "analyst",
                "viewer"
            ]
        )
    )

):

    return get_events(db)