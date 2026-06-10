from app.management.panel import public_display_url


def test_public_display_url_masks_hidden_path():
    assert (
        public_display_url("https://panel.conanxin.com/secret-hidden-path")
        == "panel.conanxin.com / 已配置隐藏路径"
    )


def test_public_display_url_masks_query_and_fragment():
    assert (
        public_display_url("https://panel.conanxin.com/?token_like=value#frag")
        == "panel.conanxin.com / 已配置隐藏路径"
    )


def test_public_display_url_without_path_keeps_origin():
    assert public_display_url("https://panel.conanxin.com") == "panel.conanxin.com"
