from typing import Optional, Dict, Any
from services.firestore_db import get_db

def get_user_tenant(uid: str) -> Optional[Dict[str, Any]]:
    db = get_db()
    doc = db.collection("user_tenants").document(uid).get()
    return doc.to_dict() if doc.exists else None

def set_user_tenant(uid: str, tenant_id: str, email: str, role: str = "user") -> None:
    db = get_db()
    db.collection("user_tenants").document(uid).set(
        {"tenant_id": tenant_id, "email": email, "role": role},
        merge=True
    )
