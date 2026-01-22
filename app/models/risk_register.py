from pydantic import BaseModel, Field
from typing import List, Literal, Optional

from app.models.assessment import OrganisationProfile, AIUseCase


RiskCategory = Literal[
    "data_privacy",
    "security",
    "model_risk",
    "conduct",
    "operational",
    "third_party",
    "legal_regulatory",
]


class RiskRegisterRequest(BaseModel):
    profile: OrganisationProfile
    use_case: AIUseCase
    notes: Optional[str] = None


class RiskItem(BaseModel):
    risk_id: str
    category: RiskCategory
    title: str
    description: str
    likelihood: int = Field(..., ge=1, le=5)
    impact: int = Field(..., ge=1, le=5)
    risk_score: int = Field(..., ge=1, le=25)
    controls: List[str]
    owner_role: str
    review_days: int = Field(..., ge=7, le=365)


class RiskRegisterResponse(BaseModel):
    register_title: str
    version: str = "0.1.0"
    items: List[RiskItem]
