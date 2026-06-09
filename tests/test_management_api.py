from fastapi.testclient import TestClient

from app.main import app, get_config


def test_management_api_returns_200_and_safe_payload(tmp_path, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
management:
  enabled: false
  panel_local_url: "http://127.0.0.1:2096"
  panel_public_url: "https://panel.conanxin.com"
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("CONAN_CONFIG_PATH", str(config_path))
    get_config.cache_clear()

    client = TestClient(app)
    response = client.get("/api/management")
    payload = response.json()

    assert response.status_code == 200
    assert payload["enabled"] is False
    assert payload["panel_local_url"] == "http://127.0.0.1:2096"
    assert payload["panel_public_url"] == "https://panel.conanxin.com"
    assert "password" not in str(payload).lower()
    assert "token" not in str(payload).lower()
    assert "cookie" not in str(payload).lower()

    get_config.cache_clear()
