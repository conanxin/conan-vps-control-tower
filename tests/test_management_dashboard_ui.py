from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_contains_management_entry_copy():
    html = (ROOT / "app" / "static" / "index.html").read_text(encoding="utf-8")

    assert "管理入口" in html
    assert "进入 3X-UI 面板" in html
    assert "Control Tower 不读取或修改 3X-UI 配置" in html
    assert "<iframe" not in html.lower()


def test_dashboard_management_js_uses_api_and_does_not_iframe():
    js = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")

    assert "/api/management" in js
    assert "panel_public_url" in js
    assert "如需修改代理配置，可通过“管理入口”进入 3X-UI 面板" in js
    assert "iframe" not in js.lower()
