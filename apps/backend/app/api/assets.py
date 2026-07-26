from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.database.database import get_db

from app.schemas.asset import (
    AssetCreate,
    AssetResponse
)

from app.services.asset_service import (
    create_asset,
    get_assets,
    get_asset,
    delete_asset
)

from app.dependencies.permissions import require_role



router = APIRouter(
    prefix="/api/v1/assets",
    tags=["Assets"]
)



# Create Asset
# Allowed:
# admin
# analyst
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
# Allowed:
# admin
# analyst
# viewer
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



# Get Single Asset
# Allowed:
# admin
# analyst
# viewer
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



# Delete Asset
# Allowed:
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