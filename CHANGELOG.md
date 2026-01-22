# Changelog

All notable changes to this project will be documented in this file.

## v0.1.0 — 2026-01-22

### Added
- FastAPI backend with versioned routes under `/api/v1`
- Governance artefact endpoints:
  - `POST /assess` (maturity score + 30/60/90 action plan)
  - `POST /policy` (draft AI use policy)
  - `POST /risk-register` (structured risk register)
  - `POST /board-brief` (board-ready decision brief)
- SAFE guardrail checks for free-text inputs
- Admin-protected `GET /meta` endpoint (header-based admin key)
- Append-only audit logging (local-only, excluded from git)
- Smoke tests for core endpoints (pytest)
- Developer tooling:
  - Ruff + Black + pre-commit hooks
  - pytest configuration

### Notes
- V1 outputs are JSON-first and deterministic to keep behaviour testable and compliance-friendly.
