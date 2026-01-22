from fastapi import APIRouter, HTTPException, Request, status

from app.api.routes.guardrail import guardrail_check
from app.models.board_brief import BoardBriefRequest, BoardBriefResponse
from app.models.guardrail import GuardrailCheckRequest
from app.services.audit import write_audit_event
from app.services.board_brief import generate_board_brief

router = APIRouter(tags=["board-brief"])


@router.post("/board-brief", response_model=BoardBriefResponse)
def board_brief(payload: BoardBriefRequest, request: Request) -> BoardBriefResponse:
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
        GuardrailCheckRequest(text=combined_text, context="board-brief"),
        request,
    )

    if not guardrail_result.allow:
        write_audit_event(
            "board_brief_blocked",
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

    result = generate_board_brief(payload)

    write_audit_event(
        "board_brief_created",
        path=str(request.url.path),
        method=request.method,
        client_ip=request.client.host if request.client else None,
        outcome="allow",
        details={
            "brief_title": result.brief_title,
            "key_risks_count": len(result.key_risks),
            "decision_asks_count": len(result.decision_asks),
        },
    )

    return result
