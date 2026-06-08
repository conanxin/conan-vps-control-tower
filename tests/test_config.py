from app.config import load_config


def test_load_config_uses_defaults_when_file_missing(tmp_path):
    config = load_config(tmp_path / "missing.yaml")

    assert config.server.host == "127.0.0.1"
    assert config.server.port == 3001
    assert config.checks.interval_seconds == 30
    assert config.proxy.ports == [443]
    assert config.domain.enabled is False
    assert config.tls.enabled is False
    assert config.traffic.warning_percent == 70
    assert config.traffic.interfaces == ["auto"]


def test_load_config_merges_partial_yaml(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text("server:\n  port: 3010\n", encoding="utf-8")

    config = load_config(config_path)

    assert config.server.host == "127.0.0.1"
    assert config.server.port == 3010
    assert config.proxy.panel.timeout_seconds == 3
    assert config.domain.names == ["example.com"]
    assert config.tls.targets[0].host == "example.com"


def test_load_config_supports_domain_tls_and_traffic(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
domain:
  enabled: true
  names:
    - "example.com"
  expected_ips:
    - "203.0.113.10"
tls:
  enabled: true
  targets:
    - host: "example.com"
      port: 443
      server_name: "example.com"
traffic:
  warning_percent: 60
  degraded_percent: 80
  critical_percent: 95
  interfaces:
    - "eth0"
  data_file: "data/traffic_state.json"
""",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.domain.enabled is True
    assert config.domain.expected_ips == ["203.0.113.10"]
    assert config.tls.enabled is True
    assert config.tls.targets[0].server_name == "example.com"
    assert config.traffic.warning_percent == 60
    assert config.traffic.interfaces == ["eth0"]
