from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_history_section_present_in_dashboard_html():
    text = (ROOT / "app" / "static" / "index.html").read_text(encoding="utf-8")
    assert "健康历史" in text
    assert "最近 24 小时" in text
    assert "最近事件" in text
    assert "history-events-list" in text or "最近事件列表" in text


def test_history_summary_section_in_api_smoke_docs():
    text = (ROOT / "docs" / "DASHBOARD_SMOKE_TEST.md").read_text(encoding="utf-8")
    assert "健康历史" in text
    assert "/api/history/summary" in text
    assert "/api/history/recent" in text
