from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.mitre_import_service import (
    MitreImportService
)


router = APIRouter(
    prefix="/api/v1/mitre",
    tags=["MITRE"]
)


@router.post("/import")
def import_mitre_dataset(
    db: Session = Depends(get_db)
):

    result = (
        MitreImportService
        .import_dataset(db)
    )

    return result