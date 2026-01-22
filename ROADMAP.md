# Roadmap

This roadmap shows how V1 evolves into V1.5 and V2 without breaking the API contract.

## V1 (current) — JSON-first governance MVP
Goal: produce governance artefacts with control-first guardrails and auditability.

Delivered:
- `/api/v1` versioned routes
- guardrails + audit trail
- assess / policy / risk register / board brief
- tests + formatting automation

## V1.5 — MVP SaaS layer (deployable pilot)
Goal: make this usable by real teams with minimal operational risk.

Planned:
- Persistence for generated artefacts (SQLite/Postgres)
- Simple org workspace:
  - list artefacts
  - retrieve by ID
  - export JSON
- Approval workflow (manual gate for higher-risk outputs)
- Configurable guardrail rules per org (risk appetite profiles)
- Auth v1 (API key per org) + basic rate limiting
- Structured audit viewer endpoint (read-only, admin)
- CI pipeline (GitHub Actions): lint + test on PR

Success criteria:
- A small org can run 3–5 use cases end-to-end and produce repeatable evidence.

## V2 — Control-first orchestration (LLM + RAG safely)
Goal: introduce AI generation without losing governance controls.

Planned:
- Provider routing:
  - OpenAI / Anthropic / fallback model selection
  - failover + timeouts + retries
- RAG knowledge sources per sector:
  - policy templates
  - regulatory clauses
  - internal standards
- Evidence-first outputs:
  - citations (source + section)
  - verification prompts
- Multi-tenant isolation:
  - per-org encryption keys
  - signed audit events
- Observability:
  - metrics (latency, blocks, error rates)
  - dashboards
- Extended guardrails:
  - prompt injection detection
  - output safety checks
  - PII redaction with confidence scoring

Success criteria:
- AI-assisted generation with documented controls, auditability, and defensible outputs.
