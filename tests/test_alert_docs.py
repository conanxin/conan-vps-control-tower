from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_alert_docs_exist():
    docs = ROOT / "docs"
    assert (docs / "TELEGRAM_ALERT_SETUP.md").exists()
    assert (docs / "ALERT_SYSTEMD_ENV.md").exists()
    assert (docs / "ALERT_TEST_PLAYBOOK.md").exists()
    assert (ROOT / "scripts" / "check-alert-config.sh").exists()


def test_alert_docs_include_safe_placeholders_and_no_real_secrets():
    doc_files = [
        ROOT / "docs" / "TELEGRAM_ALERT_SETUP.md",
        ROOT / "docs" / "ALERT_SYSTEMD_ENV.md",
        ROOT / "docs" / "ALERT_TEST_PLAYBOOK.md",
        ROOT / "README.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in doc_files)

    assert "YOUR_TELEGRAM_BOT_TOKEN" in text
    assert "YOUR_TELEGRAM_CHAT_ID" in text
    assert "YOUR_SMTP_PASSWORD" in text
    assert "dmit-control-tower" in text
