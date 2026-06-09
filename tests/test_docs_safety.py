from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = list((ROOT / "docs").glob("*.md")) + [ROOT / "README.md"]


def test_docs_do_not_encourage_public_dashboard_exposure():
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in DOCS)

    dangerous_phrases = [
        "0.0.0.0",
        "open port 3001 to the public",
        "expose dashboard to the public internet",
        "publicly expose the dashboard",
    ]
    for phrase in dangerous_phrases:
        if phrase == "0.0.0.0":
            assert " --host 0.0.0.0 " not in combined
            continue
        assert phrase not in combined


def test_docs_use_safe_example_hosts():
    combined = "\n".join(path.read_text(encoding="utf-8") for path in DOCS)

    assert "YOUR_VPS_HOST" in combined
    assert "example.com" in combined
    assert "203.0.113.10" in combined
    assert "192.168." not in combined
    assert "10.0." not in combined
