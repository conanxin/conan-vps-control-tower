from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def read_static():
    html = (ROOT / "app" / "static" / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")
    return html, js


def test_frontend_runtime_dom_chain_guard():
    _, js = read_static()
    assert "getElementById(" in js
    assert not re.search(r"getElementById\\([^\\)]*\\)\\.closest", js)
    assert not re.search(r"getElementById\\([^\\)]*\\)\\.classList", js)


def test_no_unsafe_getElementById_chain():
    _, js = read_static()
    for line in js.splitlines():
        if "getElementById(" in line:
            assert ".closest" not in line
            assert ".classList" not in line


def test_management_cta_uses_panel_public_url_for_jump():
    _, js = read_static()
    assert "window.open(targetUrl, \"_blank\", \"noopener,noreferrer\")" in js
    assert 'setAttr(button, "data-target-url", publicUrl);' in js
    assert "panel_public_url" in js


def test_cache_busting_for_static_assets():
    html, _ = read_static()
    assert 'styles.css?v=' in html
    assert 'app.js?v=' in html


def test_no_regression_text_leaks():
    html, js = read_static()
    combined = html + "\n" + js
    assert "Use SSH tunnel to access the dashboard" not in combined
    assert "YOUR_PANEL_PORT" not in combined
    assert "????" not in combined
    assert "No active diagnostic issues detected" not in combined
    assert "当前未发现需要处理的问题。继续保持观察即可。" in combined
    assert "panel.conanxin.com / 已配置隐藏路径" in combined
    assert "已脱敏" in combined
    assert "进入 3X-UI 面板" in combined
