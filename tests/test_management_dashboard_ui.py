from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_contains_management_entry_copy():
    html = (ROOT / "app" / "static" / "index.html").read_text(encoding="utf-8")

    assert "管理入口" in html
    assert "进入 3X-UI 面板" in html
    assert "本地协议检测" in html
    assert "推荐本地入口" in html
    assert "为避免泄露 3X-UI 隐藏路径" in html
    assert "url-value" in html
    assert "Control Tower 不读取或修改 3X-UI 配置" in html
    assert "当前配置的面板协议可能不匹配" in html
    assert "<iframe" not in html.lower()


def test_dashboard_management_js_uses_api_and_does_not_iframe():
    js = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")

    assert "/api/management" in js
    assert "panel_public_url" in js
    assert "panel_public_display_url" in js
    assert "detected_scheme" in js
    assert "recommended_local_url" in js
    assert "protocol_warning" in js
    assert "如需修改代理配置，可通过“管理入口”进入 3X-UI 面板" in js
    assert "iframe" not in js.lower()


def test_dashboard_styles_prevent_long_management_url_overflow():
    css = (ROOT / "app" / "static" / "styles.css").read_text(encoding="utf-8")

    assert ".url-value" in css
    assert "overflow-wrap: anywhere" in css
    assert ".management-card" in css
