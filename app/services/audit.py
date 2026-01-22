import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from app.core.config import settings

AUDIT_LOG_PATH = Path("logs") / "audit.jsonl"


def write_audit_event(
    event_type: str,
    *,
    path: str,
    method: str,
    client_ip: str | None,
    outcome: str,
    details: dict[str, Any],
) -> str:
    """
    Writes one line per event to logs/audit.jsonl (JSONL format).
    MVP-friendly audit trail: easy to parse, easy to ship later.
    """
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    event_id = str(uuid4())
    payload = {
        "event_id": event_id,
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "environment": settings.environment,
        "event_type": event_type,
        "http": {
            "path": path,
            "method": method,
            "client_ip": client_ip,
        },
        "outcome": outcome,
        "details": details,
    }

    with AUDIT_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    return event_id
