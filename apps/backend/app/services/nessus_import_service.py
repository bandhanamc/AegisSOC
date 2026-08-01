from sqlalchemy.orm import Session

from app.models.vulnerability import Vulnerability
from app.models.asset import Asset

from app.services.cve_intelligence_service import CVEIntelligence
from app.ai.faiss_mitre_mapper import FaissMitreMapper



cve_service = CVEIntelligence()

mitre_mapper = FaissMitreMapper()



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


        asset = db.query(
            Asset
        ).filter(
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




        cve_id = finding.get(
            "cve"
        )



        cwe_id = None



        if cve_id:


            enrichment = cve_service.enrich(
                cve_id
            )


            cwe_id = enrichment.get(
                "cwe"
            )





        vulnerability = Vulnerability(


            asset_id=asset.id,


            plugin_id=finding.get(
                "plugin_id"
            ),


            cve_id=cve_id,


            cwe_id=cwe_id,


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

        db.commit()

        db.refresh(
            vulnerability
        )



        #
        # AI MITRE Mapping
        #

        try:


            mitre_mapper.map_vulnerability(

                db,

                vulnerability,

                top_k=5

            )


        except Exception as e:


            print(
                "MITRE mapping failed:",
                e
            )




        imported += 1




    return {

        "imported": imported,

        "skipped": skipped

    }