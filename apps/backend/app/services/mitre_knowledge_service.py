from sqlalchemy.orm import Session

from app.models.mitre_technique import MitreTechnique
from app.schemas.mitre_technique import MitreTechniqueCreate


def create_technique(
    db: Session,
    technique: MitreTechniqueCreate,
):
    obj = MitreTechnique(**technique.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def get_all_techniques(db: Session):
    return db.query(MitreTechnique).all()


def get_technique(
    db: Session,
    technique_id: str,
):
    return (
        db.query(MitreTechnique)
        .filter(
            MitreTechnique.technique_id == technique_id
        )
        .first()
    )