from app.health.evaluator import aggregate_status, evaluate
from app.models import CheckResult


def test_aggregate_status_uses_highest_severity():
    checks = [
        CheckResult(name="a", status="healthy", message="ok"),
        CheckResult(name="b", status="warning", message="watch"),
        CheckResult(name="c", status="critical", message="down"),
    ]

    assert aggregate_status(checks) == "critical"


def test_evaluate_builds_readable_risk_summary():
    checks = [
        CheckResult(name="proxy_core", status="healthy", message="running"),
        CheckResult(name="proxy_ports", status="degraded", message="some ports are closed"),
    ]

    response = evaluate(checks)

    assert response.overall_status == "degraded"
    assert "proxy_ports" in response.readable_summary
    assert response.risk_summary == ["proxy_ports: some ports are closed"]
