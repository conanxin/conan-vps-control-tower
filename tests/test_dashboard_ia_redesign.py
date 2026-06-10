from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_static() -> tuple[str, str, str]:
    html = (ROOT / "app" / "static" / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")
    css = (ROOT / "app" / "static" / "styles.css").read_text(encoding="utf-8")
    return html, js, css


def test_dashboard_contains_new_information_architecture():
    html, _, _ = read_static()

    assert 'id="hero"' in html
    assert "快速操作" in html
    assert "代理链路" in html
    assert "核心状态" in html or "core-grid" in html
    assert "管理入口：3X-UI 面板" in html
    assert "流量概览" in html
    assert "次级信息区" in html
    assert "可选检查" in html
    assert "告警通知" in html
    assert "健康历史" in html
    assert "最近事件" in html
    assert "诊断详情" in html


def test_dashboard_domain_access_and_masking_copy():
    html, js, _ = read_static()
    combined = html + "\n" + js

    assert "Use SSH tunnel to access the dashboard" not in combined
    assert "Cloudflare Access" in combined
    assert "公网直连" in combined
    assert "进入 3X-UI 面板" in combined
    assert "已配置隐藏路径" in combined
    assert "已脱敏" in combined
    assert "YOUR_PANEL_PORT" not in combined
    assert "????" not in combined
    assert "secret-hidden-path" not in combined


def test_management_cta_uses_real_public_url_not_display_url():
    _, js, _ = read_static()

    assert "panel_public_url" in js
    assert "panel_public_display_url" in js
    assert "data-target-url" in js
    assert "window.open(targetUrl, \"_blank\", \"noopener,noreferrer\")" in js
    assert "panel_public_display_url" not in js.split("window.open(targetUrl", 1)[0].split("function bindNavigationGuards", 1)[-1]
    assert "window.location.href" not in js
    assert "location.href" not in js


def test_frontend_has_dom_guards_and_history_copy():
    _, js, _ = read_static()

    assert "function el(id)" in js
    assert "if (!node)" in js
    assert "Array.isArray" in js
    assert "当前状态健康；最近 24 小时曾出现告警，当前已恢复。" in js
    assert "当前未发现需要处理的问题" in js or "当前无需执行命令" in js


def test_visual_system_uses_subtle_status_treatments():
    _, _, css = read_static()

    assert ".hero" in css
    assert ".quick-actions" in css
    assert ".management-card" in css
    assert ".traffic-card" in css
    assert "details summary" in css
    assert "border-left: 4px solid var(--healthy)" in css
    assert "background: var(--critical-soft)" in css
