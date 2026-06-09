from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_contains_screenshot_section_and_local_only():
    text = README.read_text(encoding="utf-8")
    assert "Screenshot / 界面预览" in text
    assert "local-only" in text.lower()
    assert "ssh tunnel" in text.lower()


def test_readme_uses_safe_example_address():
    text = README.read_text(encoding="utf-8")
    assert "127.0.0.1:3001" in text
    assert "YOUR_VPS_HOST" in text
    assert "192.168." not in text
    assert "10.0." not in text
    assert "203.0.113." not in text
