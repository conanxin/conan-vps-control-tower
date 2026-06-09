from app.diagnostics.engine import diagnose
from app.health.evaluator import evaluate
from app.models import CheckResult


def test_panel_diagnostics_use_real_panel_port_without_placeholder():
    result = diagnose(
        evaluate(
            [
                CheckResult(
                    name="xui_panel",
                    status="critical",
                    message="panel down",
                    details={
                        "scheme": "https",
                        "port": 2053,
                        "hidden_path_configured": True,
                        "url": "https://127.0.0.1:2053/<hidden>",
                    },
                ),
                CheckResult(name="proxy_core", status="healthy", message="ok"),
                CheckResult(name="proxy_ports", status="healthy", message="ok"),
            ]
        )
    )

    item = next(item for item in result.items if item.diagnosis_id == "panel_down_but_proxy_may_work")
    commands = "\n".join(item.read_only_commands)

    assert "YOUR_PANEL_PORT" not in commands
    assert "https://127.0.0.1:2053/<hidden>" in commands
    assert "ss -lntup | grep -E ':2053\\b' || true" in commands
    assert "优先不要重启代理" in item.impact
    assert "管理入口" in item.suggested_first_check


def test_panel_diagnostics_ask_for_port_when_missing():
    result = diagnose(
        evaluate(
            [
                CheckResult(name="xui_panel", status="critical", message="panel down"),
                CheckResult(name="proxy_core", status="healthy", message="ok"),
                CheckResult(name="proxy_ports", status="healthy", message="ok"),
            ]
        )
    )

    item = next(item for item in result.items if item.diagnosis_id == "panel_down_but_proxy_may_work")
    commands = "\n".join(item.read_only_commands)

    assert "YOUR_PANEL_PORT" not in commands
    assert "请先确认 3X-UI 面板端口" in commands
