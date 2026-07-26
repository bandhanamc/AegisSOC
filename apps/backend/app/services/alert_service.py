from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.schemas.alert import AlertCreate



def create_alert(
    db: Session,
    alert: AlertCreate
):

    db_alert = Alert(
        event_id=alert.event_id,
        rule_id=alert.rule_id,
        title=alert.title,
        description=alert.description,
        severity=alert.severity,
        mitre_technique=alert.mitre_technique,
        status="OPEN",
        investigated=False
    )

    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)

    return db_alert



def get_alerts(
    db: Session
):

    return (
        db.query(Alert)
        .order_by(
            Alert.created_at.desc()
        )
        .all()
    )



def get_alert(
    db: Session,
    alert_id: int
):

    return (
        db.query(Alert)
        .filter(
            Alert.id == alert_id
        )
        .first()
    )