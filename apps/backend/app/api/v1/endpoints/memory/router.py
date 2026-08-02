from fastapi import APIRouter


from app.services.memory.service import MemoryService



router = APIRouter(

    prefix="/api/v1/memory",

    tags=["AI Memory"]

)



service = MemoryService()



@router.post("/store")
def store_memory(
    payload:dict
):


    return service.store(

        payload["id"],

        payload["content"]

    )




@router.post("/search")
def search_memory(
    payload:dict
):


    return service.search(

        payload["query"]

    )