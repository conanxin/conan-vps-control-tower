from app.alerts.severity import is_at_least


def test_severity_ordering_and_unknown_behavior():
    assert is_at_least("critical", "warning") is True
    assert is_at_least("degraded", "warning") is True
    assert is_at_least("warning", "degraded") is False
    assert is_at_least("unknown", "warning") is False
