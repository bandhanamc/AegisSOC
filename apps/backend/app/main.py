"""
AegisSOC Backend API

Purpose:
Main FastAPI application.

Security:
- No secrets stored here.
- Logging enabled.
- Authentication routes enabled.
"""

from fastapi import FastAPI, Request

from app.core.config import settings

from app.api.auth import router as auth_router

from app.api.assets import router as asset_router

from app.api.vulnerabilities import router as vulnerability_router

from app.api.scans import router as scan_router

from app.api.uploads import router as upload_router

from app.api.users import router as user_router

from app.logging.logger import (
    app_logger,
    api_logger
)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="MITRE ATT&CK Based SOC and Threat Hunting Platform"
)


# ==============================
# API ROUTERS
# ==============================

# Authentication APIs
# Routes:
# POST /auth/register
# POST /auth/login
app.include_router(auth_router)
app.include_router(asset_router)
app.include_router(vulnerability_router)
app.include_router(scan_router)
app.include_router(upload_router)
app.include_router(user_router)



@app.middleware("http")
async def request_logging(
    request: Request,
    call_next
):
    """
    Logs all API requests.

    Security:
    Does not log:
    - Authorization headers
    - Passwords
    - Tokens
    """

    api_logger.info(
        f"REQUEST {request.method} {request.url.path}"
    )

    response = await call_next(request)

    api_logger.info(
        f"RESPONSE {response.status_code}"
    )

    return response



@app.on_event("startup")
async def startup_event():
    """
    Application startup event.
    """

    app_logger.info(
        "AegisSOC Backend started successfully"
    )



@app.get("/api/v1/health")
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
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }