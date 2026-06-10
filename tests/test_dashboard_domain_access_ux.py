from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app, get_config


ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_domain_access_copy_is_cloudflare_first():
    html = (ROOT / "app" / "static" / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")

    combined = html + "\n" + js
    assert "Use SSH tunnel to access the dashboard" not in combined
    assert "Cloudflare Access" in combined
    assert "外部入口" in combined
    assert "公网直连" in combined
    assert "管理入口：3X-UI 面板" in combined
    assert "进入 3X-UI 面板" in combined


def test_dashboard_masks_panel_hidden_path_and_prevents_overflow():
    html = (ROOT / "app" / "static" / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")
    css = (ROOT / "app" / "static" / "styles.css").read_text(encoding="utf-8")

    combined = html + "\n" + js
    assert "已配置隐藏路径" in combined
    assert "脱敏" in combined
    assert "secret-hidden-path" not in combined
    assert "overflow-wrap: anywhere" in css
    assert "word-break: break-word" in css


def test_dashboard_contains_no_mojibake_markers():
    html = (ROOT / "app" / "static" / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")

    combined = html + "\n" + js
    assert "????" not in combined
    assert "绠＄悊" not in combined
    assert "闅愯棌" not in combined


def test_meta_api_exposes_domain_access_fields(tmp_path, monkeypatch):
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
    response = client.get("/api/meta", headers={"host": "tower.conanxin.com"})
    payload = response.json()

    assert response.status_code == 200
    assert payload["public_entry"].endswith("tower.conanxin.com")
    assert payload["external_access_mode"] == "Cloudflare Access + Tunnel"
    assert payload["direct_public_bind"] is False
    assert payload["access_protection"] == "Cloudflare Access"
    assert "token" not in str(payload).lower()
    assert "password" not in str(payload).lower()
    assert "chat_id" not in str(payload).lower()

    get_config.cache_clear()
