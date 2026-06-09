from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_contains_management_entry_copy():
    html = (ROOT / "app" / "static" / "index.html").read_text(encoding="utf-8")

    assert "管理面板入口" in html
    assert "进入 3X-UI 面板" in html
    assert "面板名称" in html
    assert "当前状态" in html
    assert "保护方式" in html
    assert "只读边界" in html
    assert "公开入口已脱敏显示" in html
    assert "Control Tower 不读取或修改 3X-UI 配置。" in html
    assert "请先确认协议方式" in html or "管理入口" in html


def test_dashboard_management_js_uses_api_and_does_not_iframe():
    js = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")

    assert "/api/management" in js
    assert "panel_public_url" in js
    assert "panel_public_display_url" in js
    assert "detected_scheme" in js
    assert "recommended_local_url" in js
    assert "protocol_warning" in js
    assert "公开入口已脱敏显示" in js
    assert "iframe" not in js.lower()


def test_management_button_targets_public_url_and_new_tab():
    js = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")

    assert "management-open-button" in js
    assert "setAttr(button, \"href\", publicUrl)" in js or "button.href" in js
    assert "setAttr(button, \"target\", panelData.open_in_new_tab === false ? \"_self\" : \"_blank\")" in js
    assert "setAttr(button, \"aria-disabled\", \"true\")" in js


def test_dashboard_layout_high_value_sections_exist():
    html = (ROOT / "app" / "static" / "index.html").read_text(encoding="utf-8")

    assert "class=\"overview\"" in html
    assert "class=\"pipeline\"" in html
    assert "class=\"grid core-grid\"" in html
    assert "class=\"secondary-grid\"" in html
    assert "class=\"history-panel\"" in html


def test_dashboard_styles_prevent_long_management_url_overflow():
    css = (ROOT / "app" / "static" / "styles.css").read_text(encoding="utf-8")

    assert ".url-value" in css
    assert "overflow-wrap: anywhere" in css
    assert ".management-entry-card" in css
    assert "management-entry-card" in css


def test_dom_queries_are_guarded_in_js():
    js = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")

    assert not re.search(r"document\.getElementById\([^\)]*\)\.textContent", js)
    assert not re.search(r"document\.querySelector\([^\)]*\)\.textContent", js)
    assert not re.search(r"document\.querySelectorAll\([^\)]*\)\.", js)
