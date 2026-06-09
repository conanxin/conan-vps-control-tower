from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_install_systemd_script_exists():
    path = ROOT / "scripts" / "install-systemd-local-only.sh"
    assert path.exists(), "install-systemd-local-only.sh missing"


def test_check_systemd_script_exists():
    path = ROOT / "scripts" / "check-systemd-local-only.sh"
    assert path.exists(), "check-systemd-local-only.sh missing"


def test_uninstall_systemd_script_exists():
    path = ROOT / "scripts" / "uninstall-systemd-local-only.sh"
    assert path.exists(), "uninstall-systemd-local-only.sh missing"
