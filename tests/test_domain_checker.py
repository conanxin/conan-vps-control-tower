from app.config import DomainConfig
from app.health import domain_checker
from app.health.domain_checker import check_domain


def test_domain_disabled_is_ignored():
    result = check_domain(DomainConfig(enabled=False))

    assert result.status == "unknown"
    assert result.ignored is True
    assert result.details["enabled"] is False


def test_domain_resolved_ip_matches_expected(monkeypatch):
    monkeypatch.setattr(domain_checker, "resolve_domain", lambda name, timeout: ["203.0.113.10"])

    result = check_domain(
        DomainConfig(enabled=True, names=["example.com"], expected_ips=["203.0.113.10"])
    )

    assert result.status == "healthy"
    assert result.details["resolved_ips"]["example.com"] == ["203.0.113.10"]


def test_domain_mismatch_returns_warning(monkeypatch):
    monkeypatch.setattr(domain_checker, "resolve_domain", lambda name, timeout: ["203.0.113.20"])

    result = check_domain(
        DomainConfig(enabled=True, names=["example.com"], expected_ips=["203.0.113.10"])
    )

    assert result.status == "warning"
    assert result.details["mismatches"][0]["name"] == "example.com"
