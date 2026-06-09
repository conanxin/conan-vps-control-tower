from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [ROOT / "scripts" / "install-systemd-local-only.sh", ROOT / "scripts" / "check-systemd-local-only.sh", ROOT / "scripts" / "uninstall-systemd-local-only.sh"]
SERVICE_FILE = ROOT / "scripts" / "conan-vps-control-tower.service"


def test_service_and_scripts_bind_localhost():
    combined = "\n".join(p.read_text(encoding="utf-8") for p in SCRIPTS + [SERVICE_FILE])
    assert "--host 127.0.0.1" in combined
    assert "--port 3001" in combined


def test_service_and_scripts_do_not_bind_publicly():
    combined = "\n".join(p.read_text(encoding="utf-8") for p in SCRIPTS + [SERVICE_FILE])
    assert "--host 0.0.0.0" not in combined


def test_service_and_scripts_do_not_use_80_or_443():
    combined = "\n".join(p.read_text(encoding="utf-8") for p in SCRIPTS + [SERVICE_FILE])
    assert " --port 80" not in combined
    assert " --port 443" not in combined


def test_scripts_do_not_touch_proxy_services():
    dangerous = [
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
        "systemctl enable x-ui",
        "systemctl enable 3x-ui",
        "systemctl disable x-ui",
        "systemctl disable 3x-ui",
    ]
    combined = "\n".join(p.read_text(encoding="utf-8") for p in SCRIPTS)
    for token in dangerous:
        assert token not in combined


def test_uninstall_script_only_handles_project_service():
    uninstall_script = (ROOT / "scripts" / "uninstall-systemd-local-only.sh").read_text(encoding="utf-8")
    assert "conan-vps-control-tower" in uninstall_script
    assert "systemctl stop \"${SERVICE_NAME}\"" in uninstall_script
    assert "systemctl disable \"${SERVICE_NAME}\"" in uninstall_script
    assert "SERVICE_FILE=\"/etc/systemd/system/${SERVICE_NAME}.service\"" in uninstall_script
