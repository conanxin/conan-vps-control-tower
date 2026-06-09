from app.config import ManagementConfig
from app.management.panel import check_management_panel


def test_http_config_with_https_fallback_returns_protocol_warning(monkeypatch):
    def fake_tcp(url, timeout=3):
        return True

    def fake_probe(url, timeout=3, skip_tls_verify=False):
        if url.startswith("http://"):
            return False, "UnknownProtocol"
        return True, "HTTP 404"

    monkeypatch.setattr("app.management.panel._tcp_reachable", fake_tcp)
    monkeypatch.setattr("app.management.panel._probe_url", fake_probe)

    result = check_management_panel(
        ManagementConfig(panel_local_url="http://127.0.0.1:2096")
    )

    assert result.local_reachable is True
    assert result.tcp_reachable is True
    assert result.detected_scheme == "https"
    assert result.recommended_local_url == "https://127.0.0.1:2096"
    assert result.protocol_warning is True
    assert "建议将 panel_local_url 改为 https://127.0.0.1:2096" in result.message


def test_https_config_with_404_is_protocol_reachable(monkeypatch):
    monkeypatch.setattr("app.management.panel._tcp_reachable", lambda url, timeout=3: True)
    monkeypatch.setattr(
        "app.management.panel._probe_url",
        lambda url, timeout=3, skip_tls_verify=False: (True, "HTTP 404"),
    )

    result = check_management_panel(
        ManagementConfig(panel_local_url="https://127.0.0.1:2096")
    )

    assert result.local_reachable is True
    assert result.tcp_reachable is True
    assert result.detected_scheme == "https"
    assert result.recommended_local_url == "https://127.0.0.1:2096"
    assert result.protocol_warning is False
    assert result.status == "healthy"
