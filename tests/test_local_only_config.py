from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_config_example_defaults_to_local_only():
    config = yaml.safe_load((ROOT / "config.example.yaml").read_text(encoding="utf-8"))

    assert config["server"]["host"] == "127.0.0.1"
    assert config["server"]["port"] == 3001


def test_systemd_service_binds_localhost():
    service = (ROOT / "scripts" / "conan-vps-control-tower.service").read_text(encoding="utf-8")

    assert "--host 127.0.0.1" in service
    assert "--port 3001" in service
    assert "--host 0.0.0.0" not in service


def test_run_dev_does_not_bind_publicly():
    script = (ROOT / "scripts" / "run-dev.sh").read_text(encoding="utf-8")

    assert "--host 127.0.0.1" in script
    assert "0.0.0.0" not in script
