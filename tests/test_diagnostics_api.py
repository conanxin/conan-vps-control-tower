from fastapi.testclient import TestClient

from app.main import app


def test_diagnostics_api_returns_200():
    client = TestClient(app)

    response = client.get("/api/diagnostics")

    assert response.status_code == 200
    payload = response.json()
    assert "summary" in payload
    assert "items" in payload


def test_health_api_keeps_old_fields():
    client = TestClient(app)

    payload = client.get("/api/health").json()

    assert "overall_status" in payload
    assert "readable_summary" in payload
    assert "risk_summary" in payload
    assert "checks" in payload
