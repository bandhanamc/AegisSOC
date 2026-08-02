from fastapi import APIRouter


from app.services.agent.service import AgentService



router=APIRouter(

    prefix="/api/v1/agent",

    tags=[
        "AI Agent"
    ]

)



service=AgentService()



@router.post("/run")
def run_agent(
    payload:dict
):


    return service.process(
        payload
    )