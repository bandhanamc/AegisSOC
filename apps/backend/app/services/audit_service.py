from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    action: str,
    resource: str,
    user_id: int | None = None,
    resource_id: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    status: str = "SUCCESS",
    details: str | None = None
):

    audit = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        resource_id=resource_id,
        ip_address=ip_address,
        user_agent=user_agent,
        status=status,
        details=details
    )

    db.add(audit)
    db.commit()
    db.refresh(audit)

    return audit



def get_audit_logs(
    db: Session,
    limit: int = 100
):

    return (
        db.query(AuditLog)
        .order_by(
            AuditLog.created_at.desc()
        )
        .limit(limit)
        .all()
    )