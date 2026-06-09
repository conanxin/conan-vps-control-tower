from fastapi.testclient import TestClient

from app.main import app, get_config


def test_management_api_returns_200_and_safe_payload(tmp_path, monkeypatch):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
management:
  enabled: false
  panel_local_url: "http://127.0.0.1:2096"
  panel_public_url: "https://panel.conanxin.com/secret-hidden-path"
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
    assert payload["panel_public_url"] == "https://panel.conanxin.com/secret-hidden-path"
    assert payload["panel_public_display_url"] == "https://panel.conanxin.com / 已配置隐藏路径"
    assert "detected_scheme" in payload
    assert "recommended_local_url" in payload
    assert "protocol_warning" in payload
    assert "tcp_reachable" in payload
    assert "password" not in str(payload).lower()
    assert "token" not in str(payload).lower()
    assert "cookie" not in str(payload).lower()
    assert "secret-hidden-path" not in payload["panel_public_display_url"]

    get_config.cache_clear()
