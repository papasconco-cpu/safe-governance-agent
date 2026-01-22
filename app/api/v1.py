from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.core.config import settings

router = APIRouter(prefix="/api/v1", tags=["v1"])

@router.get("/")
def api_root():
    return {"status": "ok", "service": "safe-governance-agent"}

@router.get("/health")
def health():
    return {
        "status": "healthy",
        "python_version": "3.11",
        "environment": settings.environment,
    }

@router.get("/meta")
def meta():
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "log_level": settings.log_level,
        "openai_api_key_set": bool(settings.openai_api_key),
        "anthropic_api_key_set": bool(settings.anthropic_api_key),
        "together_api_key_set": bool(settings.together_api_key),
        "models": {
            "openai_model": settings.openai_model,
            "anthropic_model": settings.anthropic_model,
            "fallback_model": settings.fallback_model,
        },
    }
