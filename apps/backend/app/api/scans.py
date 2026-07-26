from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.scan import (
    ScanCreate,
    ScanResponse
)

from app.services.scan_service import (
    create_scan,
    get_scans,
    get_scan,
    update_scan_status,
    delete_scan,
    get_scan_count
)

from app.dependencies.permissions import require_role


router = APIRouter(
    prefix="/api/v1/scans",
    tags=["Scans"]
)


@router.post(
    "",
    response_model=ScanResponse
)
def start_scan(
    scan: ScanCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role(
            [
                "admin",
                "analyst"
            ]
        )
    )
):

    return create_scan(
        db,
        scan
    )


@router.get(
    "",
    response_model=list[ScanResponse]
)
def list_scans(
    skip: int = 0,
    limit: int = 50,
    status: str | None = None,
    scanner: str | None = None,
    asset_id: int | None = None,
    scan_type: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role(
            [
                "admin",
                "analyst",
                "viewer"
            ]
        )
    )
):

    return get_scans(
        db,
        skip,
        limit,
        status,
        scanner,
        asset_id,
        scan_type
    )


@router.get("/count")
def scan_count(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role(
            [
                "admin",
                "analyst",
                "viewer"
            ]
        )
    )
):

    return {
        "count": get_scan_count(db)
    }


@router.get(
    "/{scan_id}",
    response_model=ScanResponse
)
def scan_detail(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role(
            [
                "admin",
                "analyst",
                "viewer"
            ]
        )
    )
):

    scan = get_scan(
        db,
        scan_id
    )

    if not scan:
        raise HTTPException(
            status_code=404,
            detail="Scan not found"
        )

    return scan


@router.patch(
    "/{scan_id}"
)
def change_scan_status(
    scan_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role(
            [
                "admin",
                "analyst"
            ]
        )
    )
):

    scan = update_scan_status(
        db,
        scan_id,
        status
    )

    if not scan:
        raise HTTPException(
            status_code=404,
            detail="Scan not found"
        )

    return scan


@router.delete(
    "/{scan_id}"
)
def remove_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role(
            [
                "admin"
            ]
        )
    )
):

    scan = delete_scan(
        db,
        scan_id
    )

    if not scan:
        raise HTTPException(
            status_code=404,
            detail="Scan not found"
        )

    return {
        "message": "Scan deleted successfully"
    }