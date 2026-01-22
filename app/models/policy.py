from typing import Literal

from pydantic import BaseModel, Field

from app.models.assessment import AIUseCase, OrganisationProfile


class PolicyRequest(BaseModel):
    profile: OrganisationProfile
    use_case: AIUseCase
    risk_appetite: Literal["low", "medium", "high"] = "low"
    notes: str | None = None


class PolicySection(BaseModel):
    title: str
    bullets: list[str]


class PolicyResponse(BaseModel):
    policy_title: str
    version: str = "0.1.0"
    status: Literal["draft"] = "draft"
    purpose: str
    scope: list[str]
    sections: list[PolicySection]
    review_cadence_days: int = Field(..., ge=7, le=365)
