from app.models.board_brief import BoardBriefRequest, BoardBriefResponse, DecisionAsk


def generate_board_brief(req: BoardBriefRequest) -> BoardBriefResponse:
    profile = req.profile
    use_case = req.use_case

    title = f"Board Brief — AI Use Case Approval: {use_case.name}"

    exec_summary: list[str] = [
        f"Organisation: {profile.org_name} ({profile.sector}, {profile.geography}).",
        f"Use case: {use_case.name} — {use_case.description}",
        "Approach: Control-first. SAFE guardrails and audit logging are enforced before outputs are produced.",
    ]

    if profile.regulated:
        exec_summary.append("Regulated context: governance, privacy controls, and auditability are required.")

    # Key risks: use risk register if provided; else provide baseline risks
    key_risks: list[str] = []
    if req.risk_register and req.risk_register.items:
        key_risks = [f"{item.risk_id}: {item.title} (score {item.risk_score})" for item in req.risk_register.items[:5]]
    else:
        key_risks = [
            "Inaccurate outputs could be used without validation.",
            "Prompt injection or unsafe inputs could bypass intended controls.",
            "Sensitive data exposure risk if staff paste identifiers into prompts.",
        ]

    # Recommended controls: policy + SAFE baseline
    controls: list[str] = [
        "Mandatory SAFE guardrail checks before AI processing.",
        "Human oversight: a person remains accountable for outputs and decisions.",
        "Audit logging for all requests and governance artefacts.",
        "Approved templates and restricted input types (placeholders only).",
    ]

    if req.policy:
        controls.append("Formal AI Use Policy drafted for this use case (draft status).")

    if req.assessment:
        controls.append(f"Maturity assessment completed: score {req.assessment.maturity_score} ({req.assessment.maturity_level}).")

    # Decision asks
    asks: list[DecisionAsk] = [
        DecisionAsk(
            decision="Approve the use case for controlled MVP testing (internal only).",
            why="Allows learning and evidence collection while maintaining governance controls.",
            owner_role="Board / Executive Sponsor",
            timeframe="now",
        ),
        DecisionAsk(
            decision="Approve policy and training rollout for staff using this capability.",
            why="Reduces operational risk and prevents accidental data exposure.",
            owner_role="Compliance / Risk",
            timeframe="30_days",
        ),
        DecisionAsk(
            decision="Approve DPIA and vendor due diligence if third parties are introduced.",
            why="Required to manage privacy, security, and regulatory risk in supplier relationships.",
            owner_role="DPO / Procurement",
            timeframe="60_days",
        ),
    ]

    next_steps = [
        "30 days: finalise AI Use Policy + staff briefing + enforce guardrails in workflow.",
        "60 days: implement approval workflow for higher-risk prompts/outputs; review audit logs weekly.",
        "90 days: reassess risk register, run DPIA where applicable, and report outcomes to leadership.",
    ]

    return BoardBriefResponse(
        brief_title=title,
        executive_summary=exec_summary,
        key_risks=key_risks,
        recommended_controls=controls,
        decision_asks=asks,
        next_steps_30_60_90=next_steps,
    )
