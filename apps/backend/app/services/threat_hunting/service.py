from sqlalchemy.orm import Session

from app.models.threat_hunting import ThreatHuntingReport



def save_report(
    db:Session,
    alert,
    report
):

    record = ThreatHuntingReport(

        alert_type=alert.get(
            "type"
        ),

        mitre=alert.get(
            "mitre"
        ),

        host=alert.get(
            "host"
        ),

        report=report

    )


    db.add(record)

    db.commit()

    db.refresh(record)

    return record