from pathlib import Path


def test_frontend_script_uses_chinese_risk_text():
    js = Path("app/static/app.js").read_text(encoding="utf-8")
    assert "当前没有活跃风险。" in js
    assert "未配置的可选检查" in js
    assert "本地流量估算安全" in js
    assert "以下命令仅用于只读排查" in js
    assert "测试告警" in js


def test_not_configured_is_not_treated_as_active_risk():
    js = Path("app/static/app.js").read_text(encoding="utf-8")
    assert "not-configured" in js
    assert "activeRiskChecks" in js
