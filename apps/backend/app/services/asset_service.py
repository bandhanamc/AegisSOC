from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.asset import AssetCreate



def create_asset(
    db: Session,
    asset: AssetCreate
):

    db_asset = Asset(
        hostname=asset.hostname,
        ip_address=asset.ip_address,
        operating_system=asset.operating_system,
        criticality=asset.criticality
    )


    db.add(db_asset)

    db.commit()

    db.refresh(db_asset)


    return db_asset



def get_assets(
    db: Session
):

    return (
        db.query(Asset)
        .all()
    )



def get_asset(
    db: Session,
    asset_id: int
):

    return (
        db.query(Asset)
        .filter(
            Asset.id == asset_id
        )
        .first()
    )



def delete_asset(
    db: Session,
    asset_id: int
):

    asset = get_asset(
        db,
        asset_id
    )


    if asset:

        db.delete(asset)

        db.commit()


    return asset