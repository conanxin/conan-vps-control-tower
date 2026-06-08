from __future__ import annotations

from email.message import EmailMessage

from app.alerts.models import AlertEvent


def telegram_text(event: AlertEvent) -> str:
    prefix = "Recovery" if event.is_recovery else event.severity.capitalize()
    return (
        f"[{prefix}] Conan VPS Control Tower\n"
        f"Overall status: {event.status}\n"
        f"Module: {event.module}\n"
        f"Message: {event.message}\n"
        f"Suggested first check: {event.suggested_first_check}"
    )


def email_subject(event: AlertEvent) -> str:
    prefix = "Recovery" if event.is_recovery else event.severity.capitalize()
    return f"[{prefix}] Conan VPS Control Tower: {event.title}"


def email_body(event: AlertEvent) -> str:
    return telegram_text(event) + f"\nChecked at: {event.checked_at}\nSummary: {event.summary}\n"


def build_email_message(event: AlertEvent, from_addr: str, to_addrs: list[str]) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = email_subject(event)
    message["From"] = from_addr
    message["To"] = ", ".join(to_addrs)
    message.set_content(email_body(event))
    return message
