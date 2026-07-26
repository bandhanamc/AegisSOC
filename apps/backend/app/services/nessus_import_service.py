from sqlalchemy.orm import Session

from app.models.vulnerability import Vulnerability
from app.models.asset import Asset


def import_findings(
    db: Session,
    findings: list
):

    imported = 0
    skipped = 0


    for finding in findings:

        hostname = finding.get(
            "host"
        )


        asset = db.query(Asset).filter(
            Asset.hostname == hostname
        ).first()


        if asset is None:

            asset = Asset(
                hostname=hostname,
                ip_address="unknown",
                operating_system="Unknown",
                criticality="medium"
            )

            db.add(asset)
            db.commit()
            db.refresh(asset)



        existing = db.query(
            Vulnerability
        ).filter(
            Vulnerability.asset_id == asset.id,
            Vulnerability.plugin_id == finding.get("plugin_id"),
            Vulnerability.cve_id == finding.get("cve")
        ).first()



        if existing:

            skipped += 1
            continue



        vulnerability = Vulnerability(

            asset_id=asset.id,

            plugin_id=finding.get(
                "plugin_id"
            ),

            cve_id=finding.get(
                "cve"
            ),

            title=finding.get(
                "plugin_name"
            ),

            description=finding.get(
                "description"
            ),

            cvss_score=finding.get(
                "cvss"
            ),

            severity=finding.get(
                "severity"
            ),

            status="Open",

            solution=finding.get(
                "solution"
            )
        )


        db.add(vulnerability)

        imported += 1



    db.commit()


    return {
        "imported": imported,
        "skipped": skipped
    }