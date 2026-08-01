from sqlalchemy.orm import Session

from app.models.vulnerability import Vulnerability
from app.models.asset import Asset
from app.models.mitre_mapping import MitreMapping


class ContextBuilder:

    def build(
        self,
        db: Session,
        vulnerability_id: int
    ):

        vulnerability = (
            db.query(Vulnerability)
            .filter(
                Vulnerability.id == vulnerability_id
            )
            .first()
        )

        if vulnerability is None:
            return None

        asset = (
            db.query(Asset)
            .filter(
                Asset.id == vulnerability.asset_id
            )
            .first()
        )

        mitre = (
            db.query(MitreMapping)
            .filter(
                MitreMapping.vulnerability_id ==
                vulnerability.id
            )
            .all()
        )

        similar = (
            db.query(Vulnerability)
            .filter(
                Vulnerability.title ==
                vulnerability.title,
                Vulnerability.id != vulnerability.id
            )
            .limit(5)
            .all()
        )

        return {

            "vulnerability": vulnerability,

            "asset": asset,

            "mitre": mitre,

            "similar": similar

        }