from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.database.database import get_db

from app.schemas.vulnerability import (
    VulnerabilityCreate,
    VulnerabilityResponse,
    VulnerabilityUpdate
)


from app.services.vulnerability_service import (
    create_vulnerability,
    get_vulnerabilities,
    get_vulnerability,
    get_vulnerability_count,
    update_status
)


from app.dependencies.permissions import require_role



router = APIRouter(
    prefix="/api/v1/vulnerabilities",
    tags=["Vulnerabilities"]
)



@router.post(
    "",
    response_model=VulnerabilityResponse
)
def add_vulnerability(
    vulnerability: VulnerabilityCreate,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_role(
            ["admin", "analyst"]
        )
    )
):

    return create_vulnerability(
        db,
        vulnerability
    )



@router.get(
    "",
    response_model=list[VulnerabilityResponse]
)
def list_vulnerabilities(
    skip: int = 0,
    limit: int = 50,
    severity: str | None = None,
    asset_id: int | None = None,
    search: str | None = None,

    db: Session = Depends(get_db),

    current_user = Depends(
        require_role(
            ["admin", "analyst", "viewer"]
        )
    )
):

    return get_vulnerabilities(
        db,
        skip,
        limit,
        severity,
        asset_id,
        search
    )



@router.get(
    "/count"
)
def vulnerability_count(
    severity: str | None = None,
    asset_id: int | None = None,

    db: Session = Depends(get_db),

    current_user = Depends(
        require_role(
            ["admin", "analyst", "viewer"]
        )
    )
):

    return {
        "count": get_vulnerability_count(
            db,
            severity,
            asset_id
        )
    }



@router.get(
    "/{vulnerability_id}",
    response_model=VulnerabilityResponse
)
def vulnerability_detail(
    vulnerability_id: int,

    db: Session = Depends(get_db),

    current_user = Depends(
        require_role(
            ["admin", "analyst", "viewer"]
        )
    )
):

    vuln = get_vulnerability(
        db,
        vulnerability_id
    )


    if not vuln:

        raise HTTPException(
            status_code=404,
            detail="Vulnerability not found"
        )


    return vuln



@router.patch(
    "/{vulnerability_id}",
    response_model=VulnerabilityResponse
)
def change_status(
    vulnerability_id: int,

    data: VulnerabilityUpdate,

    db: Session = Depends(get_db),

    current_user = Depends(
        require_role(
            ["admin", "analyst"]
        )
    )
):

    vuln = update_status(
        db,
        vulnerability_id,
        data
    )


    if not vuln:

        raise HTTPException(
            status_code=404,
            detail="Vulnerability not found"
        )


    return vuln