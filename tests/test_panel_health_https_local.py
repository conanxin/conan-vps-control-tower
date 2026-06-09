from app.config import PanelConfig
from app.health.http_checker import check_panel


class FakeResponse:
    def __init__(self, status_code: int):
        self.status_code = status_code


def test_local_https_panel_check_skips_tls_verify(monkeypatch):
    calls = {}

    def fake_get(url, **kwargs):
        calls["url"] = url
        calls["verify"] = kwargs.get("verify")
        return FakeResponse(200)

    monkeypatch.setattr("app.health.http_checker.httpx.get", fake_get)

    result = check_panel(PanelConfig(url="https://127.0.0.1:2053/secret-path/", timeout_seconds=3))

    assert result.status == "healthy"
    assert calls["verify"] is False
    assert result.details["url"] == "https://127.0.0.1:2053/<hidden>"
    assert "secret-path" not in str(result.details)


def test_non_local_https_panel_check_keeps_tls_verify(monkeypatch):
    calls = {}

    def fake_get(url, **kwargs):
        calls["verify"] = kwargs.get("verify")
        return FakeResponse(200)

    monkeypatch.setattr("app.health.http_checker.httpx.get", fake_get)

    result = check_panel(PanelConfig(url="https://example.com/panel/", timeout_seconds=3))

    assert result.status == "healthy"
    assert calls["verify"] is True


def test_panel_reachable_status_codes(monkeypatch):
    for code in [200, 301, 302, 307, 401, 403]:
        monkeypatch.setattr("app.health.http_checker.httpx.get", lambda *args, **kwargs: FakeResponse(code))
        result = check_panel(PanelConfig(url="https://127.0.0.1:2053/hidden/", timeout_seconds=3))
        assert result.status == "healthy"


def test_panel_404_is_path_warning_not_healthy(monkeypatch):
    monkeypatch.setattr("app.health.http_checker.httpx.get", lambda *args, **kwargs: FakeResponse(404))

    result = check_panel(PanelConfig(url="https://127.0.0.1:2053/wrong-hidden/", timeout_seconds=3))

    assert result.status == "warning"
    assert "path may be wrong" in result.message
