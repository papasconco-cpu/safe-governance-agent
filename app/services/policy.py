from app.models.policy import PolicyRequest, PolicyResponse, PolicySection


def generate_ai_use_policy(req: PolicyRequest) -> PolicyResponse:
    profile = req.profile
    use_case = req.use_case

    data = set(use_case.data_types)
    channels = set(use_case.channels)
    users = set(use_case.users)

    policy_title = f"AI Use Policy — {profile.org_name} — {use_case.name}"

    purpose = (
        f"This policy defines how {profile.org_name} will use AI for '{use_case.name}' "
        f"to support staff while protecting confidentiality, privacy, and regulatory obligations."
    )

    scope = [
        f"Applies to: {', '.join(users) if users else 'staff'}",
        f"Channels: {', '.join(channels) if channels else 'unspecified'}",
        f"Data types: {', '.join(data) if data else 'unspecified'}",
    ]

    # Risk appetite drives strictness
    strict = req.risk_appetite in ("low", "medium")

    allowed = [
        "Draft internal documents using non-identifiable examples.",
        "Summarise internal procedures and policies without including personal identifiers.",
        "Generate checklists and templates for governance activities.",
    ]

    prohibited = [
        "Do not enter National Insurance numbers, card numbers, passwords, or authentication codes.",
        "Do not input customer names, addresses, emails, phone numbers, account numbers, or unique identifiers.",
        "Do not upload confidential documents unless explicitly approved and redacted.",
    ]

    if "health" in data or "special_category" in data:
        prohibited.append("Do not use AI with health or special category data unless a DPIA and explicit controls are approved.")
    if "customers" in users:
        prohibited.append("Do not allow AI to communicate directly with customers without approved scripts and human oversight.")

    data_handling = [
        "Classify data before use: public, internal, personal, special category.",
        "Use placeholders: [CLIENT], [ACCOUNT], [DATE] instead of real identifiers.",
        "Run SAFE guardrail checks before sending text to any AI provider.",
        "Store outputs securely and only in approved systems.",
    ]

    if strict:
        data_handling.append("Default to blocking uncertain or high-risk inputs. Escalate to Compliance or DPO.")
    else:
        data_handling.append("If risk is unclear, pause and confirm the data classification before proceeding.")

    oversight = [
        "A human remains accountable for all decisions and communications.",
        "Review AI outputs for accuracy, bias, and suitability before use.",
        "Escalate when the output affects customers, compliance, or regulated decisions.",
    ]

    incident = [
        "If sensitive data is entered, stop immediately and report to the DPO/Security.",
        "Capture the incident context and initiate containment steps.",
        "Review controls and update training to prevent recurrence.",
    ]

    review_days = 90 if profile.regulated else 180

    sections = [
        PolicySection(title="Allowed Use", bullets=allowed),
        PolicySection(title="Prohibited Use", bullets=prohibited),
        PolicySection(title="Data Handling", bullets=data_handling),
        PolicySection(title="Human Oversight", bullets=oversight),
        PolicySection(title="Incident Handling", bullets=incident),
        PolicySection(
            title="Governance",
            bullets=[
                "Maintain an audit trail for usage and changes.",
                "Review and update the policy on schedule or after incidents.",
                "Ensure training and onboarding includes this policy.",
            ],
        ),
    ]

    return PolicyResponse(
        policy_title=policy_title,
        purpose=purpose,
        scope=scope,
        sections=sections,
        review_cadence_days=review_days,
    )
