import os

def _parse_admin_emails() -> set[str]:
    raw = os.getenv("ADMIN_EMAILS", "")
    emails = {e.strip().lower() for e in raw.split(",") if e.strip()}
    return emails

def is_admin_email(email: str) -> bool:
    if not email:
        return False
    admins = _parse_admin_emails()
    return email.strip().lower() in admins
