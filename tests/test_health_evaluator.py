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


def test_ignored_optional_checker_does_not_affect_overall_status():
    checks = [
        CheckResult(name="proxy_core", status="healthy", message="running"),
        CheckResult(name="domain_dns", status="unknown", message="Domain check is not configured", ignored=True),
    ]

    response = evaluate(checks)

    assert response.overall_status == "healthy"
    assert "Not configured: domain_dns" in response.readable_summary


def test_aggregate_status_orders_critical_degraded_warning():
    checks = [
        CheckResult(name="a", status="warning", message="warning"),
        CheckResult(name="b", status="degraded", message="degraded"),
        CheckResult(name="c", status="unknown", message="unknown"),
    ]

    assert aggregate_status(checks) == "degraded"
