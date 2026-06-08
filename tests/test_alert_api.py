from fastapi.testclient import TestClient

from app.main import app, get_config


def test_alert_status_does_not_expose_secrets(tmp_path, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
alerts:
  enabled: true
  telegram:
    enabled: true
    bot_token: "secret-token"
    chat_id: "secret-chat"
  email:
    enabled: true
    password: "secret-password"
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("CONAN_CONFIG_PATH", str(config_path))
    get_config.cache_clear()
    client = TestClient(app)

    response = client.get("/api/alerts/status")
    payload = response.json()

    assert response.status_code == 200
    assert payload["telegram"] == {"enabled": True}
    assert payload["email"] == {"enabled": True}
    assert "secret-token" not in str(payload)
    assert "secret-password" not in str(payload)
    get_config.cache_clear()


def test_alert_test_skipped_when_disabled(tmp_path, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text("alerts:\n  enabled: false\n", encoding="utf-8")
    monkeypatch.setenv("CONAN_CONFIG_PATH", str(config_path))
    get_config.cache_clear()
    client = TestClient(app)

    response = client.post("/api/alerts/test")
    payload = response.json()

    assert response.status_code == 200
    assert payload["skipped"] is True
    assert payload["sent"] is False
    get_config.cache_clear()
