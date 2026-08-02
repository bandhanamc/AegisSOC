"""
AegisSOC Backend API

Purpose:
Main FastAPI application.

Security:
- No secrets stored here.
- Logging enabled.
- Authentication routes enabled.
- MITRE ATT&CK database auto update scheduler enabled.
"""


from fastapi import FastAPI, Request

from app.core.config import settings


# ==============================
# API ROUTERS
# ==============================

from app.api.auth import router as auth_router
from app.api.assets import router as asset_router
from app.api.vulnerabilities import router as vulnerability_router
from app.api.scans import router as scan_router
from app.api.uploads import router as upload_router
from app.api.users import router as user_router
from app.api.audit import router as audit_router
from app.api.detection import router as detection_router
from app.api.events import router as events_router
from app.api.alerts import router as alerts_router
from app.api.mitre_knowledge import router as mitre_router
from app.api.mitre_import import router as mitre_import_router
from app.api.mitre_mapping import router as mitre_mapping_router
from app.api.copilot import router as copilot_router
from app.api.detection import router as detection_router
from app.api.v1.endpoints.investigation import router as investigation_router
from app.api.v1.endpoints.correlation.router import router as correlation_router


# ==============================
# BACKGROUND JOBS
# ==============================

from app.jobs.mitre_scheduler import start_scheduler



# ==============================
# LOGGING
# ==============================

from app.logging.logger import (
    app_logger,
    api_logger
)



# ==============================
# FASTAPI APPLICATION
# ==============================


app = FastAPI(

    title=settings.APP_NAME,

    version=settings.APP_VERSION,

    description=(
        "MITRE ATT&CK Based "
        "SOC and Threat Hunting Platform"
    )

)



# ==============================
# ROUTER REGISTRATION
# ==============================


app.include_router(
    auth_router
)

app.include_router(
    asset_router
)

app.include_router(
    vulnerability_router
)

app.include_router(
    scan_router
)

app.include_router(
    upload_router
)

app.include_router(
    user_router
)

app.include_router(
    audit_router
)

app.include_router(
    detection_router
)

app.include_router(
    events_router
)

app.include_router(
    alerts_router
)

app.include_router(
    mitre_router
)

app.include_router(
    mitre_import_router
)

app.include_router(
    mitre_mapping_router
)

app.include_router(copilot_router)

app.include_router(detection_router)

app.include_router(
    investigation_router
)

app.include_router(
    correlation_router
)



# ==============================
# REQUEST LOGGING
# ==============================


@app.middleware("http")
async def request_logging(
    request: Request,
    call_next
):

    """
    API request logging.

    Never logs:
    - Authorization headers
    - JWT tokens
    - Passwords
    """


    api_logger.info(
        f"REQUEST "
        f"{request.method} "
        f"{request.url.path}"
    )


    response = await call_next(
        request
    )


    api_logger.info(
        f"RESPONSE "
        f"{response.status_code}"
    )


    return response



# ==============================
# STARTUP
# ==============================


scheduler_started = False



@app.on_event("startup")
async def startup_event():

    """
    Application startup.

    Starts:
    - API service
    - MITRE ATT&CK scheduler

    MITRE scheduler:
    - Downloads latest MITRE dataset
    - Updates database
    - Removes duplicates
    - Rebuilds FAISS index

    Frequency:
    Every 48 hours
    """


    global scheduler_started



    app_logger.info(
        "Starting AegisSOC Backend"
    )



    if not scheduler_started:

        try:

            start_scheduler()


            scheduler_started = True


            app_logger.info(
                "MITRE ATT&CK scheduler started"
            )


        except Exception as e:


            app_logger.error(
                f"MITRE scheduler failed: {e}"
            )


    else:


        app_logger.info(
            "MITRE scheduler already running"
        )



    app_logger.info(
        "AegisSOC Backend started successfully"
    )




# ==============================
# HEALTH CHECK
# ==============================


@app.get(
    "/api/v1/health"
)
async def health_check():

    """
    Health monitoring endpoint.

    Used by:
    - Monitoring systems
    - Deployment validation
    """


    app_logger.info(
        "Health check executed"
    )


    return {

        "status":
            "healthy",

        "service":
            settings.APP_NAME,

        "version":
            settings.APP_VERSION

    }