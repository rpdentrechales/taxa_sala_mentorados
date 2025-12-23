import os

def is_admin_email(email: str) -> bool:
    allowed = os.environ.get("ADMIN_EMAILS", "")
    allowed_set = {e.strip().lower() for e in allowed.split(",") if e.strip()}
    return email.strip().lower() in allowed_set
