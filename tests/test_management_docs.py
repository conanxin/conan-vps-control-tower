from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_management_docs_exist():
    assert (ROOT / "docs" / "UNIFIED_MANAGEMENT_ENTRY.md").exists()
    assert (ROOT / "docs" / "CONTROL_TOWER_AND_3XUI_RELATIONSHIP.md").exists()


def test_management_docs_describe_boundaries():
    text = "\n".join(
        [
            (ROOT / "docs" / "UNIFIED_MANAGEMENT_ENTRY.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "CONTROL_TOWER_AND_3XUI_RELATIONSHIP.md").read_text(encoding="utf-8"),
        ]
    )

    assert "Not a code-level merge" in text or "does not include 3X-UI code" in text
    assert "not call 3X-UI write APIs" in text or "write APIs" in text
    assert "Not an iframe embed" in text or "iframe" in text
    assert "tower.conanxin.com" in text
    assert "panel.conanxin.com" in text
