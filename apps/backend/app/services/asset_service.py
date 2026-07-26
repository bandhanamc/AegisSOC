from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate



def create_asset(
    db: Session,
    asset: AssetCreate
):

    db_asset = Asset(
        hostname=asset.hostname,
        ip_address=asset.ip_address,
        operating_system=asset.operating_system,
        criticality=asset.criticality,
        asset_type=asset.asset_type,
        owner=asset.owner,
        environment=asset.environment,
        status=asset.status
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



def update_asset(
    db: Session,
    asset_id: int,
    asset_data: AssetUpdate
):

    asset = get_asset(
        db,
        asset_id
    )


    if not asset:
        return None


    update_data = asset_data.model_dump(
        exclude_unset=True
    )


    for key, value in update_data.items():

        setattr(
            asset,
            key,
            value
        )


    db.commit()

    db.refresh(asset)


    return asset



def search_assets(
    db: Session,
    hostname: str | None = None,
    ip_address: str | None = None
):

    query = db.query(Asset)


    if hostname:

        query = query.filter(
            Asset.hostname.ilike(
                f"%{hostname}%"
            )
        )


    if ip_address:

        query = query.filter(
            Asset.ip_address.ilike(
                f"%{ip_address}%"
            )
        )


    return query.all()



def count_assets(
    db: Session
):

    return db.query(
        Asset
    ).count()



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