from pathlib import Path

import yaml

from app.config import load_config


ROOT = Path(__file__).resolve().parents[1]


def test_config_example_contains_management_block():
    config = yaml.safe_load((ROOT / "config.example.yaml").read_text(encoding="utf-8"))

    assert config["management"]["enabled"] is True
    assert config["management"]["panel_local_url"] == "https://127.0.0.1:2096"
    assert config["management"]["panel_public_url"] == "https://panel.conanxin.com"
    assert "password" not in str(config["management"]).lower()
    assert "cookie" not in str(config["management"]).lower()


def test_management_defaults_from_loader(tmp_path):
    config = load_config(tmp_path / "missing.yaml")

    assert config.management.enabled is True
    assert config.management.panel_name == "3X-UI 面板"
    assert config.management.panel_local_url == "https://127.0.0.1:2096"
    assert config.management.panel_public_url == "https://panel.conanxin.com"
