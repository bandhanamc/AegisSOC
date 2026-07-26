from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.asset import (
    AssetCreate,
    AssetResponse,
    AssetUpdate
)

from app.services.asset_service import (
    create_asset,
    get_assets,
    get_asset,
    update_asset,
    search_assets,
    count_assets,
    delete_asset
)

from app.services.audit_service import create_audit_log

from app.dependencies.permissions import require_role


router = APIRouter(
    prefix="/api/v1/assets",
    tags=["Assets"]
)


# Create Asset
# admin, analyst
@router.post(
    "",
    response_model=AssetResponse
)
def add_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_role(["admin", "analyst"])
    )
):

    new_asset = create_asset(
        db,
        asset
    )


    create_audit_log(
        db=db,
        action="CREATE_ASSET",
        resource="ASSET",
        user_id=current_user.id,
        resource_id=str(new_asset.id),
        status="SUCCESS",
        details=f"Created asset {new_asset.hostname}"
    )


    return new_asset



# List Assets
# admin, analyst, viewer
@router.get(
    "",
    response_model=list[AssetResponse]
)
def list_assets(
    db: Session = Depends(get_db),
    current_user = Depends(
        require_role(
            ["admin", "analyst", "viewer"]
        )
    )
):

    assets = get_assets(db)


    create_audit_log(
        db=db,
        action="VIEW_ASSETS",
        resource="ASSET",
        user_id=current_user.id,
        status="SUCCESS",
        details="Viewed asset list"
    )


    return assets



# Search Assets
# admin, analyst, viewer
@router.get(
    "/search",
    response_model=list[AssetResponse]
)
def search_asset_list(
    hostname: str | None = None,
    ip_address: str | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_role(
            ["admin", "analyst", "viewer"]
        )
    )
):

    assets = search_assets(
        db,
        hostname,
        ip_address
    )


    create_audit_log(
        db=db,
        action="SEARCH_ASSETS",
        resource="ASSET",
        user_id=current_user.id,
        status="SUCCESS",
        details=f"Asset search executed hostname={hostname}, ip={ip_address}"
    )


    return assets



# Asset Count
# admin, analyst, viewer
@router.get(
    "/count"
)
def asset_count(
    db: Session = Depends(get_db),
    current_user = Depends(
        require_role(
            ["admin", "analyst", "viewer"]
        )
    )
):

    return {
        "count": count_assets(db)
    }



# Get Single Asset
# admin, analyst, viewer
@router.get(
    "/{asset_id}",
    response_model=AssetResponse
)
def read_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_role(
            ["admin", "analyst", "viewer"]
        )
    )
):

    asset = get_asset(
        db,
        asset_id
    )


    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )


    create_audit_log(
        db=db,
        action="VIEW_ASSET",
        resource="ASSET",
        user_id=current_user.id,
        resource_id=str(asset.id),
        status="SUCCESS",
        details=f"Viewed asset {asset.hostname}"
    )


    return asset



# Update Asset
# admin, analyst
@router.put(
    "/{asset_id}",
    response_model=AssetResponse
)
def edit_asset(
    asset_id: int,
    asset: AssetUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_role(
            ["admin", "analyst"]
        )
    )
):

    updated_asset = update_asset(
        db,
        asset_id,
        asset
    )


    if not updated_asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )


    create_audit_log(
        db=db,
        action="UPDATE_ASSET",
        resource="ASSET",
        user_id=current_user.id,
        resource_id=str(updated_asset.id),
        status="SUCCESS",
        details=f"Updated asset {updated_asset.hostname}"
    )


    return updated_asset



# Delete Asset
# admin only
@router.delete(
    "/{asset_id}"
)
def remove_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_role(["admin"])
    )
):

    asset = delete_asset(
        db,
        asset_id
    )


    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )


    create_audit_log(
        db=db,
        action="DELETE_ASSET",
        resource="ASSET",
        user_id=current_user.id,
        resource_id=str(asset.id),
        status="SUCCESS",
        details=f"Deleted asset {asset.hostname}"
    )


    return {
        "message": "Asset deleted"
    }