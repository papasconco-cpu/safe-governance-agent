from app.models.assessment import ActionItem, AssessmentRequest, AssessmentResponse, Gap


def _level(score: int) -> str:
    if score < 25:
        return "initial"
    if score < 50:
        return "developing"
    if score < 75:
        return "managed"
    return "optimised"


def run_maturity_assessment(req: AssessmentRequest) -> AssessmentResponse:
    """
    Deterministic scoring for V1 MVP.
    No LLM calls.
    """
    score = 0
    gaps: list[Gap] = []
    actions: list[ActionItem] = []

    # Baseline: regulated orgs need stronger governance
    if req.profile.regulated:
        score += 10
    else:
        score += 5

    # Data risk factors
    data = set(req.use_case.data_types)
    if "special_category" in data or "health" in data:
        gaps.append(
            Gap(
                area="Sensitive data handling",
                severity="high",
                why_it_matters="Special category/health data increases regulatory and privacy risk.",
                recommendation="Enforce strict data minimisation, redaction, and approval workflows before AI use.",
            )
        )
        score += 5
    if "financial" in data or "personal" in data:
        gaps.append(
            Gap(
                area="Personal/financial data controls",
                severity="high" if "financial" in data else "medium",
                why_it_matters="Customer or financial data requires strong governance and auditability.",
                recommendation="Add input guardrails, approved prompt patterns, and audit logging for all AI usage.",
            )
        )
        score += 5
    if not data:
        gaps.append(
            Gap(
                area="Data classification",
                severity="medium",
                why_it_matters="Unknown data types makes it hard to apply correct controls.",
                recommendation="Define a simple data classification for the use case (public/internal/personal/special).",
            )
        )
        score += 0

    # Third-party / vendor risk
    if req.use_case.third_parties:
        gaps.append(
            Gap(
                area="Third-party risk",
                severity="high",
                why_it_matters="External vendors add supply-chain, data residency, and contractual compliance risks.",
                recommendation="Complete vendor due diligence, DPIA, and ensure contractual controls & logging are in place.",
            )
        )
        score += 5
    else:
        score += 10

    # Channel risk
    channels = set(req.use_case.channels)
    if "email" in channels or "documents" in channels:
        score += 10
    if "voice" in channels:
        gaps.append(
            Gap(
                area="Voice/call data",
                severity="medium",
                why_it_matters="Voice data often contains identifiers and can be hard to redact.",
                recommendation="Implement redaction/transcription controls and restrict what can be processed.",
            )
        )
        score += 5

    # Users / access scope
    users = set(req.use_case.users)
    if "customers" in users:
        gaps.append(
            Gap(
                area="Customer-facing AI",
                severity="high",
                why_it_matters="Customer-facing AI increases reputational and conduct risk.",
                recommendation="Add human oversight, clear disclaimers, and escalation paths. Log all interactions.",
            )
        )
        score += 5
    else:
        score += 10

    # Convert into a capped score with a sensible range
    score = min(100, max(0, score + 30))  # +30 baseline so most orgs aren’t stuck at 0–20

    # Action plan (always returned)
    actions.extend(
        [
            ActionItem(
                timeframe="30_days",
                action="Define AI use policy for this use case and restrict sensitive inputs using guardrails.",
                owner_role="Compliance / Risk",
            ),
            ActionItem(
                timeframe="60_days",
                action="Implement audit logging and a simple approval workflow for higher-risk prompts and outputs.",
                owner_role="IT / Security",
            ),
            ActionItem(
                timeframe="90_days",
                action="Run a DPIA and vendor due diligence (if applicable), then document controls and review cadence.",
                owner_role="DPO / Governance Lead",
            ),
        ]
    )

    # Keep only top 5 gaps for MVP readability
    top_gaps = gaps[:5]

    return AssessmentResponse(
        maturity_score=score,
        maturity_level=_level(score),  # type: ignore[arg-type]
        top_gaps=top_gaps,
        action_plan=actions,
    )
