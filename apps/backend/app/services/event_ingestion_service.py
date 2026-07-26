from sqlalchemy.orm import Session

from app.models.security_event import SecurityEvent


def ingest_event(
    db: Session,
    event
):

    security_event = SecurityEvent(

        source=event.source,

        event_type=event.event_type,

        raw_event=event.raw_event,

        username=event.username,

        hostname=event.hostname,

        source_ip=event.source_ip,

        destination_ip=event.destination_ip,

        severity=event.severity

    )


    db.add(security_event)

    db.commit()

    db.refresh(security_event)


    return security_event



def get_events(
    db: Session,
    limit: int = 100
):

    return (
        db.query(SecurityEvent)
        .order_by(
            SecurityEvent.created_at.desc()
        )
        .limit(limit)
        .all()
    )