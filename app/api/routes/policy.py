from fastapi import APIRouter, HTTPException, Request, status

from app.api.routes.guardrail import guardrail_check
from app.models.guardrail import GuardrailCheckRequest
from app.models.policy import PolicyRequest, PolicyResponse
from app.services.audit import write_audit_event
from app.services.policy import generate_ai_use_policy

router = APIRouter(tags=["policy"])


@router.post("/policy", response_model=PolicyResponse)
def create_policy(payload: PolicyRequest, request: Request) -> PolicyResponse:
    # SAFE: guardrail scan free-text inputs
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
        GuardrailCheckRequest(text=combined_text, context="policy"),
        request,
    )

    if not guardrail_result.allow:
        write_audit_event(
            "policy_blocked",
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
                "message": "Input blocked by SAFE guardrails. Remove identifiers and retry.",
                "risk_score": guardrail_result.risk_score,
                "findings": [f.model_dump() for f in guardrail_result.findings],
                "redacted_preview": guardrail_result.redacted_text[:500],
            },
        )

    result = generate_ai_use_policy(payload)

    write_audit_event(
        "policy_created",
        path=str(request.url.path),
        method=request.method,
        client_ip=request.client.host if request.client else None,
        outcome="allow",
        details={
            "policy_title": result.policy_title,
            "review_cadence_days": result.review_cadence_days,
            "sections_count": len(result.sections),
        },
    )

    return result
