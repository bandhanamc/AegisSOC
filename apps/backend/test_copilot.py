from app.database.database import SessionLocal

from app.ai.copilot.copilot_service import CopilotService

db = SessionLocal()

copilot = CopilotService()

print(

    copilot.explain_vulnerability(

        db,

        1102

    )

)

db.close()