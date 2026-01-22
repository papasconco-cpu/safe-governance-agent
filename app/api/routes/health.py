from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/")
def health_check():
    return {"status": "ok", "service": "safe-governance-agent"}


@router.get("/health")
def detailed_health():
    return JSONResponse(
        content={
            "status": "healthy",
            "python_version": "3.11",
            "environment": settings.environment,
        }
    )
