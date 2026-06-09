from __future__ import annotations

from dataclasses import asdict, dataclass

from app.models import utc_now_iso


@dataclass
class ManagementPanelStatus:
    enabled: bool
    panel_name: str
    panel_local_url: str
    panel_public_url: str
    local_reachable: bool
    status: str
    message: str
    access_note: str
    readonly_note: str
    open_in_new_tab: bool
    checked_at: str
    detected_scheme: str = "unknown"
    recommended_local_url: str = ""
    protocol_warning: bool = False
    tcp_reachable: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


def disabled_status(
    panel_name: str,
    panel_local_url: str,
    panel_public_url: str,
    access_note: str,
    readonly_note: str,
    open_in_new_tab: bool,
) -> ManagementPanelStatus:
    return ManagementPanelStatus(
        enabled=False,
        panel_name=panel_name,
        panel_local_url=panel_local_url,
        panel_public_url=panel_public_url,
        local_reachable=False,
        status="disabled",
        message="管理入口已关闭。",
        access_note=access_note,
        readonly_note=readonly_note,
        open_in_new_tab=open_in_new_tab,
        checked_at=utc_now_iso(),
        detected_scheme="disabled",
        recommended_local_url=panel_local_url,
        protocol_warning=False,
        tcp_reachable=False,
    )
