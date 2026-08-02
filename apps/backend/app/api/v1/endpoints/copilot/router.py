from fastapi import APIRouter


from app.services.copilot.service import CopilotService



router = APIRouter(

    prefix="/api/v1/copilot",

    tags=["AI SOC Copilot"]

)



service = CopilotService()



@router.post("/ask")
def ask_copilot(
    payload:dict
):


    question = payload.get(
        "question"
    )


    context = payload.get(
        "context",
        {}
    )


    return service.chat(

        question,

        context

    )