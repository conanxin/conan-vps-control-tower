from pathlib import Path


def test_dashboard_index_contains_core_chinese_titles():
    html = Path("app/static/index.html").read_text(encoding="utf-8")
    assert "个人 VPS 代理健康控制塔" in html
    assert "总体状态" in html
    assert "VPS" in html
    assert "代理核心" in html
    assert "3X-UI 面板" in html
    assert "端口" in html
    assert "流量风险" in html
    assert "告警通知" in html
    assert "诊断建议" in html


def test_risk_sections_and_local_read_text():
    html = Path("app/static/index.html").read_text(encoding="utf-8")
    assert "活跃风险" in html
    assert "未配置" in html
    assert "当前没有活跃风险。" in html
    assert "本地只读" in html
    assert "公开入口已脱敏显示" in html
    assert "未配置公开入口" in html
    assert "暂无诊断问题。" in html
