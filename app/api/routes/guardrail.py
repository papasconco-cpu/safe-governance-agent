import re
from fastapi import APIRouter, Request

from app.models.guardrail import GuardrailCheckRequest, GuardrailCheckResponse, Finding
from app.services.audit import write_audit_event


router = APIRouter(tags=["guardrail"])


EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"\b(?:\+?44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}\b")
NI_RE = re.compile(r"\b(?!BG|GB|KN|NK|NT|TN|ZZ)[A-CEGHJ-PR-TW-Z]{2}\d{6}[A-D]\b", re.IGNORECASE)
CC_RE = re.compile(r"\b(?:\d[ -]*?){13,19}\b")


def _luhn_check(number: str) -> bool:
    digits = [int(d) for d in re.sub(r"\D", "", number)]
    if len(digits) < 13 or len(digits) > 19:
        return False
    checksum = 0
    parity = len(digits) % 2
    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0


def _mask(pattern: re.Pattern, text: str, token: str) -> str:
    return pattern.sub(token, text)


@router.post("/guardrail/check", response_model=GuardrailCheckResponse)
def guardrail_check(payload: GuardrailCheckRequest, request: Request) -> GuardrailCheckResponse:
    text = payload.text

    email_matches = EMAIL_RE.findall(text)
    phone_matches = PHONE_RE.findall(text)
    ni_matches = NI_RE.findall(text)

    cc_candidates = CC_RE.findall(text)
    cc_matches = [c for c in cc_candidates if _luhn_check(c)]

    findings: list[Finding] = []
    risk_score = 0

    def add_finding(f_type: str, label: str, count: int, severity: str, recommendation: str, score_add: int):
        nonlocal risk_score
        if count > 0:
            findings.append(
                Finding(
                    type=f_type,  # type: ignore[arg-type]
                    label=label,
                    matches_count=count,
                    severity=severity,  # type: ignore[arg-type]
                    recommendation=recommendation,
                )
            )
            risk_score += score_add

    add_finding(
        "email",
        "Email address detected",
        len(email_matches),
        "medium",
        "Replace emails with placeholders like [REDACTED_EMAIL] before using AI.",
        20 if len(email_matches) > 0 else 0,
    )

    add_finding(
        "phone",
        "Phone number detected",
        len(phone_matches),
        "medium",
        "Replace phone numbers with placeholders like [REDACTED_PHONE].",
        20 if len(phone_matches) > 0 else 0,
    )

    add_finding(
        "ni_number",
        "UK National Insurance number detected",
        len(ni_matches),
        "high",
        "Do not send NI numbers to AI. Remove or replace with [REDACTED_NI].",
        40 if len(ni_matches) > 0 else 0,
    )

    add_finding(
        "credit_card",
        "Possible payment card number detected (Luhn validated)",
        len(cc_matches),
        "high",
        "Do not send card numbers to AI. Remove or replace with [REDACTED_CARD].",
        40 if len(cc_matches) > 0 else 0,
    )

    # Cap risk score
    risk_score = min(risk_score, 100)

    # Redaction suggestions
    redacted = text
    if email_matches:
        redacted = _mask(EMAIL_RE, redacted, "[REDACTED_EMAIL]")
    if phone_matches:
        redacted = _mask(PHONE_RE, redacted, "[REDACTED_PHONE]")
    if ni_matches:
        redacted = _mask(NI_RE, redacted, "[REDACTED_NI]")

    # Credit card: replace only Luhn-valid matches
    for cc in cc_matches:
        redacted = redacted.replace(cc, "[REDACTED_CARD]")

    # Decision: block if any high severity finding exists
    has_high = any(f.severity == "high" for f in findings)
    allow = not has_high

    # Audit event (SAFE: no raw text stored)
    client_ip = request.client.host if request.client else None
    write_audit_event(
        "guardrail_check",
        path=str(request.url.path),
        method=request.method,
        client_ip=client_ip,
        outcome="allow" if allow else "block",
        details={
            "context": payload.context,
            "risk_score": risk_score,
            "findings": [f.model_dump() for f in findings],
            "text_length": len(text),
        },
    )

    return GuardrailCheckResponse(
        allow=allow,
        risk_score=risk_score,
        findings=findings,
        redacted_text=redacted,
    )
