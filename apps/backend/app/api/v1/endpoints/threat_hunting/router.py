from fastapi import APIRouter

from app.ai.threat_hunting.threat_hunter import ThreatHunter


router = APIRouter(
    prefix="/api/v1/threat-hunting",
    tags=["AI Threat Hunting"]
)


hunter = ThreatHunter()


@router.post("/hunt")
def hunt_threat(alert: dict):

    result = hunter.hunt(
        alert
    )

    return {
        "status": "success",
        "result": result
    }