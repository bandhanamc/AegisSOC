from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.ai.copilot.copilot_service import CopilotService
from app.models.vulnerability import Vulnerability


router = APIRouter(
    prefix="/api/v1/copilot",
    tags=["AI Copilot"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



# ==========================================
# Normal AI Response
# ==========================================

@router.post("/explain/{vulnerability_id}")
def explain_vulnerability(

    vulnerability_id: int,

    db: Session = Depends(get_db)

):

    copilot = CopilotService()


    answer = copilot.explain_vulnerability(

        db,

        vulnerability_id

    )


    return {

        "vulnerability_id": vulnerability_id,

        "analysis": answer

    }



# ==========================================
# Streaming AI Response (Token Based)
# ==========================================

@router.post("/stream/{vulnerability_id}")
def explain_vulnerability_stream(

    vulnerability_id: int,

    db: Session = Depends(get_db)

):


    copilot = CopilotService()



    vulnerability = db.query(

        Vulnerability

    ).filter(

        Vulnerability.id == vulnerability_id

    ).first()



    if vulnerability is None:

        return {

            "error": "Vulnerability not found"

        }



    mitre = copilot.mapper.map_vulnerability(

        db,

        vulnerability,

        top_k=5

    )



    prompt = copilot.prompt.build_vulnerability_prompt(

        vulnerability,

        mitre,

        vulnerability.cwe_id

    )



    return StreamingResponse(

        copilot.llm.stream(prompt),

        media_type="text/plain"

    )