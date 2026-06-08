from app.config import load_config


def test_load_config_uses_defaults_when_file_missing(tmp_path):
    config = load_config(tmp_path / "missing.yaml")

    assert config.server.host == "127.0.0.1"
    assert config.server.port == 3001
    assert config.checks.interval_seconds == 30
    assert config.proxy.ports == [443]


def test_load_config_merges_partial_yaml(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text("server:\n  port: 3010\n", encoding="utf-8")

    config = load_config(config_path)

    assert config.server.host == "127.0.0.1"
    assert config.server.port == 3010
    assert config.proxy.panel.timeout_seconds == 3
