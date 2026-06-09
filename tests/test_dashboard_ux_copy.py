from pathlib import Path


def test_dashboard_index_contains_core_chinese_titles():
    html = Path("app/static/index.html").read_text(encoding="utf-8")
    assert "个人 VPS 代理健康控制塔" in html
    assert "总体状态" in html
    assert "VPS 状态" in html
    assert "代理核心状态" in html
    assert "3X-UI 面板状态" in html
    assert "端口状态" in html
    assert "流量风险" in html
    assert "告警通知" in html
    assert "诊断摘要" in html


def test_risk_sections_and_local_read_text():
    html = Path("app/static/index.html").read_text(encoding="utf-8")
    assert "活跃风险" in html
    assert "未配置的可选检查" in html
    assert "当前没有活跃风险。" in html
    assert "本地只读" in html
