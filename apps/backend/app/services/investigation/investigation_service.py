from sqlalchemy.orm import Session

from app.ai.investigation.investigation_engine import InvestigationEngine



class InvestigationService:


    def __init__(self):

        self.engine = InvestigationEngine()



    def investigate(

        self,

        db: Session,

        vulnerability_id: int

    ):

        return self.engine.investigate(

            db,

            vulnerability_id

        )