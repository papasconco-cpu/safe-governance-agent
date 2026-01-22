# SAFE Governance Agent (V1)

Control-first, JSON-first governance backend for regulated AI use.

## What it does (MVP)
Generates a Governance Pack as structured JSON:
- Maturity Assessment: `POST /api/v1/assess`
- AI Use Policy: `POST /api/v1/policy`
- Risk Register: `POST /api/v1/risk-register`
- Board Brief: `POST /api/v1/board-brief`

Security-first behaviour:
- SAFE guardrails block sensitive identifiers (NI number, credit card, phone, email)
- Audit logging writes append-only events to `logs/audit.jsonl`

## Setup (WSL Ubuntu)
```bash
cd ~/dev/safe-governance-agent
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
