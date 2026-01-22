from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"


def test_assess_smoke():
    payload = {
        "profile": {
            "org_name": "Steve Academy Ltd",
            "sector": "Training",
            "org_size": "sme",
            "geography": "UK",
            "regulated": True,
        },
        "use_case": {
            "name": "AI policy assistant",
            "description": "Draft internal policy templates without identifiers.",
            "data_types": ["internal"],
            "channels": ["documents"],
            "users": ["staff"],
            "third_parties": False,
        },
        "notes": "test",
    }
    r = client.post("/api/v1/assess", json=payload)
    assert r.status_code == 200
    assert "maturity_score" in r.json()


def test_policy_smoke():
    payload = {
        "profile": {
            "org_name": "Steve Academy Ltd",
            "sector": "Training",
            "org_size": "sme",
            "geography": "UK",
            "regulated": True,
        },
        "use_case": {
            "name": "AI policy assistant",
            "description": "Draft internal policy templates without identifiers.",
            "data_types": ["internal"],
            "channels": ["documents"],
            "users": ["staff"],
            "third_parties": False,
        },
        "risk_appetite": "low",
        "notes": "test",
    }
    r = client.post("/api/v1/policy", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "draft"


def test_risk_register_smoke():
    payload = {
        "profile": {
            "org_name": "Steve Academy Ltd",
            "sector": "Training",
            "org_size": "sme",
            "geography": "UK",
            "regulated": True,
        },
        "use_case": {
            "name": "AI policy assistant",
            "description": "Draft internal policy templates without identifiers.",
            "data_types": ["internal"],
            "channels": ["documents"],
            "users": ["staff"],
            "third_parties": False,
        },
        "notes": "test",
    }
    r = client.post("/api/v1/risk-register", json=payload)
    assert r.status_code == 200
    assert "items" in r.json()


def test_board_brief_smoke():
    payload = {
        "profile": {
            "org_name": "Steve Academy Ltd",
            "sector": "Training",
            "org_size": "sme",
            "geography": "UK",
            "regulated": True,
        },
        "use_case": {
            "name": "AI policy assistant",
            "description": "Draft internal policy templates without identifiers.",
            "data_types": ["internal"],
            "channels": ["documents"],
            "users": ["staff"],
            "third_parties": False,
        },
        "notes": "test",
    }
    r = client.post("/api/v1/board-brief", json=payload)
    assert r.status_code == 200
    assert "decision_asks" in r.json()
