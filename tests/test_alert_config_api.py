from fastapi.testclient import TestClient

from app.main import app, get_config


def test_alert_config_check_api_returns_200(tmp_path, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "alerts:\n  enabled: false\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("CONAN_CONFIG_PATH", str(config_path))
    get_config.cache_clear()

    client = TestClient(app)
    response = client.get("/api/alerts/config-check")

    assert response.status_code == 200
    payload = response.json()
    assert payload["enabled"] is False
    assert "关闭" in payload["message"]
    assert payload["channels"]["telegram"]["enabled"] is False

    get_config.cache_clear()


def test_alert_config_check_missing_telegram_fields(tmp_path, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "alerts:\n  enabled: true\n  telegram:\n    enabled: true\n    bot_token: \"${TELEGRAM_BOT_TOKEN}\"\n    chat_id: \"123\"\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("CONAN_CONFIG_PATH", str(config_path))
    get_config.cache_clear()

    client = TestClient(app)
    response = client.get("/api/alerts/config-check")
    payload = response.json()

    assert response.status_code == 200
    telegram = payload["channels"]["telegram"]
    assert telegram["enabled"] is True
    assert telegram["ready"] is False
    assert "bot_token" in telegram["missing_fields"]

    get_config.cache_clear()


def test_alert_config_api_does_not_return_token_or_password(tmp_path, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "alerts:\n"
        "  enabled: true\n"
        "  telegram:\n"
        "    enabled: true\n"
        "    bot_token: \"secret-token\"\n"
        "    chat_id: \"secret-chat\"\n"
        "  email:\n"
        "    enabled: true\n"
        "    smtp_host: \"smtp.example.com\"\n"
        "    smtp_port: 587\n"
        "    username: \"alerts\"\n"
        "    password: \"secret-password\"\n"
        "    from_addr: \"alerts@example.com\"\n"
        "    to_addrs: [\"you@example.com\"]\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("CONAN_CONFIG_PATH", str(config_path))
    get_config.cache_clear()

    client = TestClient(app)
    payload = client.get("/api/alerts/config-check").json()

    payload_text = str(payload)
    assert "secret-token" not in payload_text
    assert "secret-chat" not in payload_text
    assert "secret-password" not in payload_text
    assert "bot_token" not in payload_text
    assert "password" not in payload_text and "chat_id" not in payload_text

    get_config.cache_clear()
