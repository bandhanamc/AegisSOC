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

    return create_asset(
        db,
        asset
    )



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

    return get_assets(db)



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

    return search_assets(
        db,
        hostname,
        ip_address
    )



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


    return {
        "message": "Asset deleted"
    }