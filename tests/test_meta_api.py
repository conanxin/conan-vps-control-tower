from fastapi.testclient import TestClient

from app.main import app, get_config


def test_meta_api_returns_safe_runtime_info(tmp_path, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
server:
  host: "127.0.0.1"
  port: 3001
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("CONAN_CONFIG_PATH", str(config_path))
    get_config.cache_clear()

    client = TestClient(app)
    response = client.get("/api/meta")
    payload = response.json()

    assert response.status_code == 200
    assert payload["app_name"] == "Conan VPS Control Tower"
    assert payload["version"] == "0.2.0"
    assert payload["ui_language"] == "zh-CN"
    assert payload["configured_host"] == "127.0.0.1"
    assert payload["configured_port"] == 3001
    assert payload["local_only"] is True
    assert payload["access_hint"] != ""
    assert payload["history_enabled"] is True
    assert payload["event_log"] is True
    assert "bot_token" not in payload
    assert "password" not in payload
    assert "chat_id" not in payload

    get_config.cache_clear()
