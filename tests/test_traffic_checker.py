import json

from app.config import TrafficConfig
from app.health.traffic_checker import check_traffic


def write_interface(root, name, rx_bytes, tx_bytes):
    stats = root / name / "statistics"
    stats.mkdir(parents=True)
    (stats / "rx_bytes").write_text(str(rx_bytes), encoding="utf-8")
    (stats / "tx_bytes").write_text(str(tx_bytes), encoding="utf-8")


def make_config(tmp_path, **overrides):
    data = {
        "monthly_limit_gb": 1,
        "reset_day": 1,
        "warning_percent": 70,
        "degraded_percent": 85,
        "critical_percent": 95,
        "interfaces": ["auto"],
        "data_file": str(tmp_path / "traffic_state.json"),
    }
    data.update(overrides)
    return TrafficConfig(**data)


def test_traffic_baseline_creation(tmp_path):
    sys_net = tmp_path / "sys" / "class" / "net"
    write_interface(sys_net, "eth0", 1000, 2000)
    config = make_config(tmp_path)

    result = check_traffic(config, sys_net)

    assert result.status == "healthy"
    assert "baseline created" in result.message.lower()
    assert (tmp_path / "traffic_state.json").exists()


def test_traffic_threshold_warning_degraded_critical(tmp_path):
    sys_net = tmp_path / "sys" / "class" / "net"
    write_interface(sys_net, "eth0", 0, 0)
    config = make_config(tmp_path)

    state_path = tmp_path / "traffic_state.json"
    state_path.write_text(
        json.dumps(
            {
                "cycle_start_date": "2026-06-01",
                "reset_day": 1,
                "baseline_rx_bytes": 0,
                "baseline_tx_bytes": 0,
                "latest_rx_bytes": 0,
                "latest_tx_bytes": 0,
            }
        ),
        encoding="utf-8",
    )

    gib = 1024**3

    write_interface(sys_net, "eth0-warning", int(gib * 0.71), 0)
    warning = check_traffic(make_config(tmp_path, interfaces=["eth0-warning"]), sys_net)
    assert warning.status == "warning"

    write_interface(sys_net, "eth0-degraded", int(gib * 0.86), 0)
    degraded = check_traffic(make_config(tmp_path, interfaces=["eth0-degraded"]), sys_net)
    assert degraded.status == "degraded"

    write_interface(sys_net, "eth0-critical", int(gib * 0.96), 0)
    critical = check_traffic(make_config(tmp_path, interfaces=["eth0-critical"]), sys_net)
    assert critical.status == "critical"
