from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_operational_scripts_exist():
    assert (ROOT / "scripts" / "tower-status.sh").exists()
    assert (ROOT / "scripts" / "tower-logs.sh").exists()
    assert (ROOT / "scripts" / "tower-stop-temporary-uvicorn.sh").exists()


def test_operational_scripts_do_not_touch_proxy_services():
    combined = "\n".join(
        (ROOT / "scripts" / p).read_text(encoding="utf-8")
        for p in [
            "tower-status.sh",
            "tower-logs.sh",
            "tower-stop-temporary-uvicorn.sh",
        ]
    )

    disallowed = [
        "systemctl restart x-ui",
        "systemctl restart 3x-ui",
        "systemctl restart xray",
        "systemctl restart sing-box",
        "systemctl restart v2ray",
        "systemctl stop x-ui",
        "systemctl stop 3x-ui",
        "systemctl stop xray",
        "systemctl stop sing-box",
        "systemctl stop v2ray",
    ]

    for token in disallowed:
        assert token not in combined


def test_operational_scripts_do_not_bind_public():
    combined = "\n".join(
        (ROOT / "scripts" / p).read_text(encoding="utf-8")
        for p in [
            "tower-status.sh",
            "tower-logs.sh",
            "tower-stop-temporary-uvicorn.sh",
        ]
    )
    assert "--host 0.0.0.0" not in combined


def test_docs_do_not_encourage_public_dashboard_exposure():
    docs_root = ROOT / "docs"
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    docs_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in docs_root.glob("*.md"))
    combined = readme.lower() + "\n" + docs_text

    forbidden = [
        "publicly expose the dashboard",
        "open port 3001 to the public",
        "expose dashboard to the public internet",
    ]
    for phrase in forbidden:
        assert phrase not in combined
