from fastapi import APIRouter, HTTPException, Request, status

from app.models.risk_register import RiskRegisterRequest, RiskRegisterResponse
from app.services.risk_register import build_risk_register
from app.services.audit import write_audit_event

from app.api.routes.guardrail import guardrail_check
from app.models.guardrail import GuardrailCheckRequest


router = APIRouter(tags=["risk-register"])


@router.post("/risk-register", response_model=RiskRegisterResponse)
def create_risk_register(payload: RiskRegisterRequest, request: Request) -> RiskRegisterResponse:
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
        GuardrailCheckRequest(text=combined_text, context="risk-register"),
        request,
    )

    if not guardrail_result.allow:
        write_audit_event(
            "risk_register_blocked",
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

    result = build_risk_register(payload)

    write_audit_event(
        "risk_register_created",
        path=str(request.url.path),
        method=request.method,
        client_ip=request.client.host if request.client else None,
        outcome="allow",
        details={
            "register_title": result.register_title,
            "items_count": len(result.items),
        },
    )

    return result
