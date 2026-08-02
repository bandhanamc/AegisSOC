from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.investigation import InvestigationService



router = APIRouter(

    prefix="/api/v1/investigation",

    tags=["AI Investigation"]

)



service = InvestigationService()



@router.post("/{vulnerability_id}")

def investigate(

    vulnerability_id: int,

    db: Session = Depends(get_db)

):

    return service.investigate(

        db,

        vulnerability_id

    )