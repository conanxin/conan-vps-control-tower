from app.diagnostics import commands
from app.diagnostics.engine import diagnose
from app.health.evaluator import evaluate
from app.models import CheckResult


def ids(result):
    return [item.diagnosis_id for item in result.items]


def test_all_healthy_returns_no_active_issues():
    result = diagnose(evaluate([CheckResult(name="proxy_core", status="healthy", message="ok")]))

    assert result.items[0].diagnosis_id == "all_healthy"
    assert "No active diagnostic issues" in result.summary


def test_proxy_core_critical_rule():
    result = diagnose(evaluate([CheckResult(name="proxy_core", status="critical", message="missing")]))

    assert "proxy_core_critical" in ids(result)


def test_proxy_port_critical_rule():
    result = diagnose(evaluate([CheckResult(name="proxy_ports", status="critical", message="closed")]))

    assert "proxy_port_not_listening" in ids(result)


def test_panel_down_but_proxy_may_work_rule():
    result = diagnose(
        evaluate(
            [
                CheckResult(name="xui_panel", status="critical", message="down"),
                CheckResult(name="proxy_core", status="healthy", message="ok"),
                CheckResult(name="proxy_ports", status="healthy", message="ok"),
            ]
        )
    )

    assert "panel_down_but_proxy_may_work" in ids(result)


def test_domain_tls_traffic_rules():
    result = diagnose(
        evaluate(
            [
                CheckResult(name="domain_dns", status="critical", message="dns failed"),
                CheckResult(name="tls_certificate", status="warning", message="expiring"),
                CheckResult(name="traffic", status="degraded", message="near limit"),
            ]
        )
    )

    assert "domain_resolution_failed" in ids(result)
    assert "tls_expiring" in ids(result)
    assert "traffic_near_limit" in ids(result)


def test_domain_mismatch_and_tls_failed_rules():
    result = diagnose(
        evaluate(
            [
                CheckResult(name="domain_dns", status="warning", message="mismatch"),
                CheckResult(name="tls_certificate", status="critical", message="handshake failed"),
            ]
        )
    )

    assert "domain_expected_ip_mismatch" in ids(result)
    assert "tls_handshake_failed" in ids(result)


def test_system_resource_warning_and_multiple_critical():
    result = diagnose(
        evaluate(
            [
                CheckResult(name="vps_system", status="warning", message="pressure"),
                CheckResult(name="proxy_core", status="critical", message="down"),
                CheckResult(name="proxy_ports", status="critical", message="closed"),
            ]
        )
    )

    assert result.items[0].diagnosis_id == "multiple_critical"
    assert "system_resource_warning" in ids(result)


def test_read_only_commands_do_not_contain_dangerous_words():
    haystack = "\n".join(commands.READ_ONLY_COMMANDS).lower()

    for word in commands.DANGEROUS_WORDS:
        assert word not in f" {haystack} "
