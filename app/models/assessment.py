from pydantic import BaseModel, Field
from typing import List, Literal, Optional


MaturityLevel = Literal["initial", "developing", "managed", "optimised"]


class OrganisationProfile(BaseModel):
    org_name: str = Field(..., min_length=2)
    sector: str = Field(..., min_length=2)
    org_size: Literal["micro", "sme", "enterprise"] = "sme"
    geography: Optional[str] = "UK"
    regulated: bool = True


class AIUseCase(BaseModel):
    name: str = Field(..., min_length=3)
    description: str = Field(..., min_length=10)
    data_types: List[Literal["public", "internal", "personal", "special_category", "financial", "health"]] = Field(
        default_factory=list
    )
    channels: List[Literal["email", "chat", "voice", "documents", "web"]] = Field(default_factory=list)
    users: List[Literal["staff", "contractors", "customers"]] = Field(default_factory=list)
    third_parties: bool = False


class AssessmentRequest(BaseModel):
    profile: OrganisationProfile
    use_case: AIUseCase
    notes: Optional[str] = None  # free text, will be guardrail-scanned


class Gap(BaseModel):
    area: str
    severity: Literal["low", "medium", "high"]
    why_it_matters: str
    recommendation: str


class ActionItem(BaseModel):
    timeframe: Literal["30_days", "60_days", "90_days"]
    action: str
    owner_role: str


class AssessmentResponse(BaseModel):
    maturity_score: int = Field(..., ge=0, le=100)
    maturity_level: MaturityLevel
    top_gaps: List[Gap]
    action_plan: List[ActionItem]
