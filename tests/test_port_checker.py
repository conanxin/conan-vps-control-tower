import socket

from app.health.port_checker import check_ports, is_port_open


def test_is_port_open_detects_open_local_port():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    port = server.getsockname()[1]

    try:
        assert is_port_open("127.0.0.1", port, timeout_seconds=1) is True
    finally:
        server.close()


def test_check_ports_reports_closed_port():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    port = server.getsockname()[1]
    server.close()

    result = check_ports([port], timeout_seconds=0.2)

    assert result.status == "critical"
    assert result.details["ports"][0]["open"] is False
