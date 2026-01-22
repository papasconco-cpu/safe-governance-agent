from app.models.risk_register import RiskRegisterRequest, RiskRegisterResponse, RiskItem


def _score(likelihood: int, impact: int) -> int:
    return likelihood * impact


def build_risk_register(req: RiskRegisterRequest) -> RiskRegisterResponse:
    profile = req.profile
    use_case = req.use_case

    data = set(use_case.data_types)
    channels = set(use_case.channels)
    users = set(use_case.users)

    title = f"AI Risk Register — {profile.org_name} — {use_case.name}"

    items: list[RiskItem] = []

    # Baseline risks (always present)
    items.append(
        RiskItem(
            risk_id="RR-001",
            category="model_risk",
            title="Hallucinated or inaccurate outputs",
            description="AI output may be wrong, outdated, or misleading and could be used without validation.",
            likelihood=3,
            impact=3,
            risk_score=_score(3, 3),
            controls=[
                "Human review required before use.",
                "Use approved prompt templates.",
                "Add citation/verification step for factual claims.",
            ],
            owner_role="Service Owner",
            review_days=90,
        )
    )

    items.append(
        RiskItem(
            risk_id="RR-002",
            category="security",
            title="Prompt injection / malicious inputs",
            description="Users or external content could manipulate prompts to bypass controls or expose sensitive info.",
            likelihood=3,
            impact=4,
            risk_score=_score(3, 4),
            controls=[
                "Input guardrails and redaction checks.",
                "Do not allow system prompt disclosure.",
                "Log and monitor abnormal usage patterns.",
            ],
            owner_role="Security",
            review_days=60,
        )
    )

    # Data/privacy risks
    if "personal" in data or "financial" in data or "health" in data or "special_category" in data:
        impact = 5 if ("health" in data or "special_category" in data) else 4
        likelihood = 3
        items.append(
            RiskItem(
                risk_id="RR-003",
                category="data_privacy",
                title="Sensitive data exposure",
                description="Personal, financial, or special category data may be entered into AI systems or appear in outputs.",
                likelihood=likelihood,
                impact=impact,
                risk_score=_score(likelihood, impact),
                controls=[
                    "SAFE guardrail checks before model use.",
                    "Redaction placeholders: [REDACTED_*].",
                    "Access restrictions and staff training.",
                    "Incident response procedure for accidental disclosure.",
                ],
                owner_role="DPO / Privacy",
                review_days=30 if profile.regulated else 90,
            )
        )
    else:
        items.append(
            RiskItem(
                risk_id="RR-003",
                category="data_privacy",
                title="Data classification gaps",
                description="If data types are not classified, controls may be applied inconsistently.",
                likelihood=2,
                impact=3,
                risk_score=_score(2, 3),
                controls=[
                    "Define data classification for the use case.",
                    "Document allowed/prohibited data inputs.",
                    "Run periodic sample checks on usage logs.",
                ],
                owner_role="Compliance / Risk",
                review_days=120,
            )
        )

    # Conduct/customer-facing risk
    if "customers" in users:
        items.append(
            RiskItem(
                risk_id="RR-004",
                category="conduct",
                title="Customer harm from incorrect or unsuitable guidance",
                description="If AI influences customer outcomes, errors could lead to harm, complaints, or regulatory action.",
                likelihood=3,
                impact=5,
                risk_score=_score(3, 5),
                controls=[
                    "Human oversight for all customer-facing content.",
                    "Approved scripts and escalation routes.",
                    "Clear disclaimers and boundaries.",
                    "Audit logs for all customer-related usage.",
                ],
                owner_role="Compliance / Risk",
                review_days=30,
            )
        )

    # Channel risk
    if "email" in channels:
        items.append(
            RiskItem(
                risk_id="RR-005",
                category="operational",
                title="Uncontrolled copying of sensitive content into emails",
                description="Users may paste sensitive info into emails and into AI prompts while drafting communications.",
                likelihood=3,
                impact=4,
                risk_score=_score(3, 4),
                controls=[
                    "Guardrail checks in email drafting workflow.",
                    "Training: placeholders only.",
                    "Auto-redaction for common identifiers.",
                ],
                owner_role="Operations",
                review_days=60,
            )
        )

    # Third-party risk
    if use_case.third_parties:
        items.append(
            RiskItem(
                risk_id="RR-006",
                category="third_party",
                title="Third-party/vendor compliance risk",
                description="External AI providers may create data residency, contract, and confidentiality risks.",
                likelihood=3,
                impact=4 if profile.regulated else 3,
                risk_score=_score(3, 4 if profile.regulated else 3),
                controls=[
                    "Vendor due diligence and DPIA.",
                    "Contractual clauses for confidentiality and sub-processors.",
                    "Limit data sent to vendors (minimisation).",
                    "Monitor provider changes and incidents.",
                ],
                owner_role="Procurement / DPO",
                review_days=60,
            )
        )

    return RiskRegisterResponse(register_title=title, items=items)
