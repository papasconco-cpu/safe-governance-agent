from typing import Literal

from pydantic import BaseModel

from app.models.assessment import AIUseCase, AssessmentResponse, OrganisationProfile
from app.models.policy import PolicyResponse
from app.models.risk_register import RiskRegisterResponse


class BoardBriefRequest(BaseModel):
    profile: OrganisationProfile
    use_case: AIUseCase

    # Optional: allow caller to include outputs from other endpoints
    assessment: AssessmentResponse | None = None
    policy: PolicyResponse | None = None
    risk_register: RiskRegisterResponse | None = None

    notes: str | None = None


class DecisionAsk(BaseModel):
    decision: str
    why: str
    owner_role: str
    timeframe: Literal["now", "30_days", "60_days", "90_days"]


class BoardBriefResponse(BaseModel):
    brief_title: str
    version: str = "0.1.0"
    executive_summary: list[str]
    key_risks: list[str]
    recommended_controls: list[str]
    decision_asks: list[DecisionAsk]
    next_steps_30_60_90: list[str]
