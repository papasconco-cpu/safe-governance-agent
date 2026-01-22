from pydantic import BaseModel, Field
from typing import Literal, List, Optional


FindingType = Literal["email", "phone", "ni_number", "credit_card", "other"]


class GuardrailCheckRequest(BaseModel):
    text: str = Field(..., min_length=1, description="User-provided text to scan for sensitive data")
    context: Optional[str] = Field(
        default=None,
        description="Optional context about where this text came from (e.g., 'client email draft')",
    )


class Finding(BaseModel):
    type: FindingType
    label: str
    matches_count: int
    severity: Literal["low", "medium", "high"]
    recommendation: str


class GuardrailCheckResponse(BaseModel):
    allow: bool
    risk_score: int = Field(..., ge=0, le=100)
    findings: List[Finding]
    redacted_text: str
