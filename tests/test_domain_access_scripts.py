from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_domain_access_scripts_exist():
    assert (ROOT / "scripts" / "discover-panel-and-tower-local.sh").exists()
    assert (ROOT / "scripts" / "check-domain-access-readiness.sh").exists()


def test_domain_access_scripts_do_not_restart_proxy_or_modify_firewall():
    scripts = [
        ROOT / "scripts" / "discover-panel-and-tower-local.sh",
        ROOT / "scripts" / "check-domain-access-readiness.sh",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in scripts)

    forbidden = [
        "systemctl restart x-ui",
        "systemctl restart 3x-ui",
        "systemctl restart xray",
        "systemctl restart sing-box",
        "systemctl restart v2ray",
        "ufw allow",
        "iptables ",
        "nft add",
        "firewall-cmd",
        "cloudflared tunnel create",
        "cloudflared login",
        "apt-get install",
    ]
    for phrase in forbidden:
        assert phrase not in combined


def test_domain_access_scripts_show_safe_targets():
    text = (ROOT / "scripts" / "discover-panel-and-tower-local.sh").read_text(encoding="utf-8")

    assert "tower target: http://127.0.0.1:3001" in text
    assert "panel target: https://127.0.0.1:" in text
    assert "0.0.0.0:3001" in text
