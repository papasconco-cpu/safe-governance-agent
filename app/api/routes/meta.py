from fastapi import APIRouter, Depends

from app.core.config import settings
from app.core.deps import require_admin_key

router = APIRouter(tags=["meta"], dependencies=[Depends(require_admin_key)])


@router.get("/meta")
def meta():
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "log_level": settings.log_level,
        # SAFE: never return secrets
        "openai_api_key_set": bool(settings.openai_api_key),
        "anthropic_api_key_set": bool(settings.anthropic_api_key),
        "together_api_key_set": bool(settings.together_api_key),
        "models": {
            "openai_model": settings.openai_model,
            "anthropic_model": settings.anthropic_model,
            "fallback_model": settings.fallback_model,
        },
    }
