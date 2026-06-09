from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_domain_access_docs_exist_and_describe_access_model():
    doc = ROOT / "docs" / "DOMAIN_ACCESS_CLOUDFLARE_TUNNEL.md"
    policy = ROOT / "docs" / "CLOUDFLARE_ACCESS_POLICY.md"

    assert doc.exists()
    assert policy.exists()

    text = doc.read_text(encoding="utf-8")
    policy_text = policy.read_text(encoding="utf-8")

    assert "Cloudflare Access" in text
    assert "tower.example.com" in text
    assert "panel.example.com" in text
    assert "http://127.0.0.1:3001" in text
    assert "https://127.0.0.1:YOUR_3XUI_PANEL_PORT" in text
    assert "HTTPS returning `404`" in text or "HTTPS probe returns `404`" in text
    assert "hidden path" in text
    assert "Do not mix" in text or "Do not mix these with your proxy main domain" in text
    assert "No public VPS port is required" in policy_text


def test_readme_includes_mobile_domain_access_section():
    text = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "Domain access / 手机访问" in text
    assert "Cloudflare Tunnel + Access" in text
    assert "tower.example.com" in text
    assert "panel.example.com" in text
    assert "docs/DOMAIN_ACCESS_CLOUDFLARE_TUNNEL.md" in text
