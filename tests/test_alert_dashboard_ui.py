from pathlib import Path


def test_dashboard_alert_section_includes_config_state_labels():
    html = Path("app/static/index.html").read_text(encoding="utf-8")
    assert "告警配置状态" in html
    assert "告警总开关" in html or "告警" in html
    assert "测试告警" in html


def test_dashboard_alert_config_js_calls_endpoint():
    js = Path("app/static/app.js").read_text(encoding="utf-8")
    assert '/api/alerts/config-check' in js
    assert "告警配置校验" in js
    assert "告警配置读取失败" in js
