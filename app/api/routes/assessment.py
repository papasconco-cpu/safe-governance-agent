from fastapi import APIRouter, HTTPException, Request, status

from app.models.assessment import AssessmentRequest, AssessmentResponse
from app.services.assessment import run_maturity_assessment
from app.services.audit import write_audit_event

# Reuse your guardrail endpoint logic by importing the regex-based checker
# (We’ll refactor into a shared service later; for MVP this is fine.)
from app.api.routes.guardrail import guardrail_check
from app.models.guardrail import GuardrailCheckRequest

router = APIRouter(tags=["assessment"])


@router.post("/assess", response_model=AssessmentResponse)
def assess(payload: AssessmentRequest, request: Request) -> AssessmentResponse:
    # 1) SAFE: guardrail scan free-text fields before doing anything else
    combined_text = "\n".join(
        [
            payload.profile.org_name,
            payload.profile.sector,
            payload.use_case.name,
            payload.use_case.description,
            payload.notes or "",
        ]
    ).strip()

    guardrail_result = guardrail_check(
        GuardrailCheckRequest(text=combined_text, context="assessment"),
        request,
    )

    if not guardrail_result.allow:
        # Audit blocked request (no raw text stored)
        write_audit_event(
            "assessment_blocked",
            path=str(request.url.path),
            method=request.method,
            client_ip=request.client.host if request.client else None,
            outcome="block",
            details={
                "reason": "guardrail_block",
                "risk_score": guardrail_result.risk_score,
                "findings": [f.model_dump() for f in guardrail_result.findings],
            },
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Input blocked by SAFE guardrails. Remove sensitive identifiers and retry.",
                "risk_score": guardrail_result.risk_score,
                "findings": [f.model_dump() for f in guardrail_result.findings],
                "redacted_preview": guardrail_result.redacted_text[:500],
            },
        )

    # 2) Deterministic assessment logic (no AI call yet)
    result = run_maturity_assessment(payload)

    # 3) Audit allowed request
    write_audit_event(
        "assessment_completed",
        path=str(request.url.path),
        method=request.method,
        client_ip=request.client.host if request.client else None,
        outcome="allow",
        details={
            "maturity_score": result.maturity_score,
            "maturity_level": result.maturity_level,
            "gaps_count": len(result.top_gaps),
        },
    )

    return result
