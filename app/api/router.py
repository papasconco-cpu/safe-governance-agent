from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.meta import router as meta_router
from app.api.routes.guardrail import router as guardrail_router
from app.api.routes.assessment import router as assessment_router
from app.api.routes.policy import router as policy_router
from app.api.routes.risk_register import router as risk_register_router
from app.api.routes.board_brief import router as board_brief_router




api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(meta_router)
api_router.include_router(guardrail_router)

api_router.include_router(assessment_router)
api_router.include_router(policy_router)
api_router.include_router(risk_register_router)
api_router.include_router(board_brief_router)

