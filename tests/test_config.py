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
    assert config.history.enabled is True
    assert config.history.max_snapshots == 2880
    assert config.history.max_events == 500
    assert config.history.summary_window_hours == 24
    assert config.management.enabled is True
    assert config.management.panel_local_url == "https://127.0.0.1:2096"
    assert config.management.panel_public_url == "https://panel.conanxin.com"


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
    assert config.history.enabled is True


def test_alerts_default_disabled(tmp_path):
    config = load_config(tmp_path / "missing.yaml")

    assert config.alerts.enabled is False
    assert config.alerts.telegram.enabled is False
    assert config.alerts.email.enabled is False
    assert config.alerts.state_file == "data/alert_state.json"


def test_env_placeholder_loading_does_not_crash_and_expands_when_available(tmp_path, monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "env-token")
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
alerts:
  enabled: true
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    chat_id: "${TELEGRAM_CHAT_ID}"
""",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.alerts.telegram.bot_token == "env-token"
    assert config.alerts.telegram.chat_id == "${TELEGRAM_CHAT_ID}"


def test_load_config_supports_history(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
history:
  enabled: false
  data_file: "custom-health-history.json"
  event_file: "custom-events.json"
  max_snapshots: 100
  max_events: 50
  min_record_interval_seconds: 120
  summary_window_hours: 12
""",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.history.enabled is False
    assert config.history.data_file == "custom-health-history.json"
    assert config.history.event_file == "custom-events.json"
    assert config.history.max_snapshots == 100
    assert config.history.max_events == 50
    assert config.history.min_record_interval_seconds == 120
    assert config.history.summary_window_hours == 12


def test_load_config_supports_management(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
management:
  enabled: false
  panel_name: "Custom Panel"
  panel_local_url: "http://127.0.0.1:2096"
  panel_public_url: "https://panel.conanxin.com"
  open_in_new_tab: false
""",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.management.enabled is False
    assert config.management.panel_name == "Custom Panel"
    assert config.management.panel_local_url == "http://127.0.0.1:2096"
    assert config.management.panel_public_url == "https://panel.conanxin.com"
    assert config.management.open_in_new_tab is False
