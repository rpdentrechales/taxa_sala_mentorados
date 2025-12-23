from typing import Dict, List, Any, Optional
from google.cloud import firestore
from services.firestore_db import get_db

def _tenant_root(tenant_id: str):
    db = get_db()
    return db.collection("tenants").document(tenant_id)

def load_store_params(tenant_id: str) -> Optional[Dict[str, Any]]:
    doc = _tenant_root(tenant_id).collection("config").document("store_params").get()
    return doc.to_dict() if doc.exists else None

def save_store_params(tenant_id: str, data: Dict[str, Any]) -> None:
    _tenant_root(tenant_id).collection("config").document("store_params").set(data, merge=True)

def load_fixed_costs(tenant_id: str) -> Optional[Dict[str, Any]]:
    doc = _tenant_root(tenant_id).collection("config").document("fixed_costs").get()
    return doc.to_dict() if doc.exists else None

def save_fixed_costs(tenant_id: str, data: Dict[str, Any]) -> None:
    _tenant_root(tenant_id).collection("config").document("fixed_costs").set(data, merge=True)

def load_procedures(tenant_id: str) -> List[Dict[str, Any]]:
    doc = _tenant_root(tenant_id).collection("data").document("procedures").get()
    if not doc.exists:
        return []
    payload = doc.to_dict() or {}
    return payload.get("items", []) or []

def save_procedures(tenant_id: str, items: List[Dict[str, Any]]) -> None:
    _tenant_root(tenant_id).collection("data").document("procedures").set({"items": items}, merge=True)
