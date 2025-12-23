from typing import Optional, Dict, Any
from datetime import datetime, timezone
from services.firestore_db import get_db

def get_invite(token: str) -> Optional[Dict[str, Any]]:
    db = get_db()
    doc = db.collection("invites").document(token).get()
    return doc.to_dict() if doc.exists else None

def mark_invite_used(token: str, uid: str) -> None:
    db = get_db()
    db.collection("invites").document(token).set(
        {"usedAt": datetime.now(timezone.utc), "usedByUid": uid},
        merge=True
    )
