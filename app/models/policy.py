from pydantic import BaseModel, Field
from typing import List, Literal, Optional

from app.models.assessment import OrganisationProfile, AIUseCase


class PolicyRequest(BaseModel):
    profile: OrganisationProfile
    use_case: AIUseCase
    risk_appetite: Literal["low", "medium", "high"] = "low"
    notes: Optional[str] = None


class PolicySection(BaseModel):
    title: str
    bullets: List[str]


class PolicyResponse(BaseModel):
    policy_title: str
    version: str = "0.1.0"
    status: Literal["draft"] = "draft"
    purpose: str
    scope: List[str]
    sections: List[PolicySection]
    review_cadence_days: int = Field(..., ge=7, le=365)
