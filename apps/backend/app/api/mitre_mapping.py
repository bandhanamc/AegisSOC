from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.mitre_mapping_request import (
    MitreMappingRequest
)

from app.services.mitre_mapping_service import (
    MitreMappingService
)


router = APIRouter(
    prefix="/api/v1/mitre",
    tags=["MITRE Mapping"]
)



service = MitreMappingService()



@router.post("/map")
def map_alert(
    request:MitreMappingRequest,
    db:Session=Depends(get_db)
):


    result = service.map_alert(

        db,

        request.alert_id,

        request.text

    )


    return {

        "mapped":
            len(result),

        "techniques":[

            {
            "id":x.technique_id,
            "name":x.technique_name,
            "tactic":x.tactic,
            "confidence":x.confidence
            }

            for x in result

        ]

    }