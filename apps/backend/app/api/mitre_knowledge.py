from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.mitre_technique import (
    MitreTechniqueCreate,
    MitreTechniqueResponse,
)

from app.services import mitre_knowledge_service

router = APIRouter(
    prefix="/api/v1/mitre",
    tags=["MITRE Knowledge Base"],
)


@router.post(
    "",
    response_model=MitreTechniqueResponse,
)
def create_technique(
    technique: MitreTechniqueCreate,
    db: Session = Depends(get_db),
):
    return mitre_knowledge_service.create_technique(
        db,
        technique,
    )


@router.get(
    "",
    response_model=list[MitreTechniqueResponse],
)
def get_all(
    db: Session = Depends(get_db),
):
    return mitre_knowledge_service.get_all_techniques(db)


@router.get(
    "/{technique_id}",
    response_model=MitreTechniqueResponse,
)
def get_one(
    technique_id: str,
    db: Session = Depends(get_db),
):
    return mitre_knowledge_service.get_technique(
        db,
        technique_id,
    )