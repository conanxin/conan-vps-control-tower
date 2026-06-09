from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def test_media_documents_exist():
    assert (DOCS / "media" / "DASHBOARD_SCREENSHOT_GUIDE.md").exists()
    assert (DOCS / "media" / "dashboard-zh-local-only-v0.2.placeholder.md").exists()
    assert (DOCS / "DEMO_WALKTHROUGH.md").exists()
    assert (DOCS / "README_SHOWCASE_NOTES.md").exists()


def test_media_docs_reference_safe_examples():
    files = [
        DOCS / "media" / "DASHBOARD_SCREENSHOT_GUIDE.md",
        DOCS / "DEMO_WALKTHROUGH.md",
        DOCS / "README_SHOWCASE_NOTES.md",
        DOCS / "media" / "README.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in files)

    for path in files:
        text = path.read_text(encoding="utf-8")
        assert "token" not in text.lower()
        assert "uuid" not in text.lower()
        assert "subscription" not in text.lower()

    assert "127.0.0.1:3001" in combined
    assert "YOUR_VPS_HOST" in combined or "YOUR_DOMAIN" in combined

    # Ensure no other IPv4 literals in these docs besides local 127.0.0.1 examples
    sample = combined
    assert "192.168." not in sample
    assert "10.0." not in sample
    assert "8.8.8.8" not in sample

    publicish_sample = sample.replace("127.0.0.1", "")
    publicish_sample = publicish_sample.replace("0.0.0.0", "")
    assert re.search(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", publicish_sample) is None
