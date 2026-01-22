from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Control-first AI governance and compliance agent",
    version="0.1.0",
)

# Everything under /api/v1
app.include_router(api_router, prefix="/api/v1")
