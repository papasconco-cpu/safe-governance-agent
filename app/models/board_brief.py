from pydantic import BaseModel, Field
from typing import List, Optional, Literal

from app.models.assessment import OrganisationProfile, AIUseCase, AssessmentResponse
from app.models.policy import PolicyResponse
from app.models.risk_register import RiskRegisterResponse


class BoardBriefRequest(BaseModel):
    profile: OrganisationProfile
    use_case: AIUseCase

    # Optional: allow caller to include outputs from other endpoints
    assessment: Optional[AssessmentResponse] = None
    policy: Optional[PolicyResponse] = None
    risk_register: Optional[RiskRegisterResponse] = None

    notes: Optional[str] = None


class DecisionAsk(BaseModel):
    decision: str
    why: str
    owner_role: str
    timeframe: Literal["now", "30_days", "60_days", "90_days"]


class BoardBriefResponse(BaseModel):
    brief_title: str
    version: str = "0.1.0"
    executive_summary: List[str]
    key_risks: List[str]
    recommended_controls: List[str]
    decision_asks: List[DecisionAsk]
    next_steps_30_60_90: List[str]
