# SAFE Governance Agent — Architecture (V1)

## What this project is
A control-first, JSON-first FastAPI backend that generates governance artefacts for AI use cases in regulated environments.

It prioritises:
- safe input handling (guardrails)
- auditability (append-only logs)
- predictable outputs (deterministic logic)
- versioned APIs for scalability (/api/v1)

## Core idea: Control-first before generation
Every request follows the same pipeline:

1) Receive request (profile + use case)
2) Run SAFE guardrail scan on free-text fields
3) If blocked: return error + log a blocked audit event
4) If allowed: generate the governance artefact
5) Write an audit event (who/what/when/outcome)

This ensures governance controls happen before any “AI output”.

## Components

### API Layer (FastAPI)
- Entry point: `app/main.py`
- Versioned router mounted at: `/api/v1`
- Swagger UI available at: `/docs`

### Config Layer
- `app/core/config.py`
- Uses environment variables via `.env`
- Protects secrets: never returned directly by endpoints

### Guardrails
- Endpoint: `/api/v1/guardrail/check`
- Used internally before policy, risk register, board brief
- Detects common sensitive identifiers (email/phone/card-like patterns)
- Produces:
  - allow/block decision
  - risk score
  - redacted preview

### Governance Deliverables (JSON-first)
- `POST /api/v1/assess`
  - returns maturity score, level, and a 30/60/90 action plan
- `POST /api/v1/policy`
  - returns a draft AI use policy (sections + controls)
- `POST /api/v1/risk-register`
  - returns a structured risk register (likelihood/impact/controls)
- `POST /api/v1/board-brief`
  - returns board-ready decision asks and recommended next steps

### Audit Logging
- File: `logs/audit.jsonl`
- Format: one JSON record per line (append-only)
- Captures:
  - endpoint path + method
  - timestamp
  - event type
  - outcome (allow/block)
  - key details

## Why JSON-first matters
- predictable outputs
- easy testing (pytest)
- safe baseline for regulated environments
- enables future upgrades (V1.5/V2) without breaking contracts

## Scaling plan
### V1.5
- Add a simple UI/dashboard
- Add stored artefacts per organisation
- Add an approval workflow (manual review gates)
- Add more guardrail patterns + configurable policies

### V2
- Add multi-model routing (OpenAI/Claude/etc)
- Add retrieval (RAG) for sector rules and templates
- Add evidence links/citations in outputs
- Add per-tenant controls, role-based access, and signed audit trails
