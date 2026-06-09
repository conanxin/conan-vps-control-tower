from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def test_cloudflare_tunnel_template_exists_and_maps_local_services():
    template = ROOT / "deploy" / "cloudflare-tunnel" / "config.example.yml"

    assert template.exists()

    text = template.read_text(encoding="utf-8")
    assert "tower.example.com" in text
    assert "panel.example.com" in text
    assert "http://127.0.0.1:3001" in text
    assert "http://127.0.0.1:YOUR_3XUI_PANEL_PORT" in text
    assert "YOUR_TUNNEL_ID" in text
    assert "http_status:404" in text


def test_cloudflare_tunnel_template_has_no_real_ip_or_secret():
    text = (ROOT / "deploy" / "cloudflare-tunnel" / "config.example.yml").read_text(encoding="utf-8")

    assert "token" not in text.lower()
    assert "uuid" not in text.lower()
    assert re.search(r"\b(?!127\.0\.0\.1\b)(?:\d{1,3}\.){3}\d{1,3}\b", text) is None
