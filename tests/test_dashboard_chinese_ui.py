from pathlib import Path


def test_frontend_script_uses_chinese_risk_text():
    js = Path("app/static/app.js").read_text(encoding="utf-8")
    assert "当前没有活跃风险。" in js
    assert "可用“测试告警”验证通知链路" in js or "可发送测试通知" in js
    assert "当前状态健康" in js
    assert "测试告警" in js


def test_not_configured_is_not_treated_as_active_risk():
    js = Path("app/static/app.js").read_text(encoding="utf-8")
    assert "not-configured" in js
    assert "activeRiskChecks" in js
