from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.audit_log import AuditLogResponse
from app.services.audit_service import get_audit_logs
from app.dependencies.permissions import require_role


router = APIRouter(
    prefix="/api/v1/audit",
    tags=["Audit Logs"]
)


@router.get(
    "/logs",
    response_model=list[AuditLogResponse]
)
def read_audit_logs(
    db: Session = Depends(get_db),
    current_user = Depends(
        require_role(
            ["admin"]
        )
    )
):

    return get_audit_logs(db)