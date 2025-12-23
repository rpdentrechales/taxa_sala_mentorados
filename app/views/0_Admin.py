# app/pages/0_Admin.py
import secrets
from datetime import datetime, timedelta, timezone
from services.ui import sidebar_common, footer_signature


import streamlit as st

from services.guard import require_auth_only
from services.firestore_db import get_db
from services.ui import sidebar_common, footer_signature

# (opcional, mas recomendado) se alguém cair aqui com ?invite=..., manda pro Convite
if st.query_params.get("invite"):
    st.session_state["pending_invite"] = st.query_params.get("invite")
    st.query_params.clear()
    st.switch_page("pages/00_Convite.py")

# 1) Garante login (sem exigir tenant) — e sem criar conta aqui
require_auth_only(allow_signup=False)
sidebar_common("admin")

st.title("🛠️ Admin — Tenants & Convites")

# 2) Permissão
if st.session_state.get("role") != "admin":
    st.error("Acesso restrito (admin).")
    footer_signature()
    st.stop()

db = get_db()
admin_email = st.session_state.get("email", "")
base_url = st.session_state.get("base_url", "http://localhost:8501").rstrip("/")


# ---------------------------
# Helpers
# ---------------------------
def _to_utc_str(x):
    if not x:
        return ""
    if isinstance(x, datetime):
        if x.tzinfo is None:
            x = x.replace(tzinfo=timezone.utc)
        return x.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return str(x)


def _load_tenants(limit: int = 200):
    docs = (
        db.collection("tenants")
        .order_by("updatedAt", direction="DESCENDING")
        .limit(limit)
        .stream()
    )
    out = []
    for d in docs:
        data = d.to_dict() or {}
        out.append({"tenant_id": d.id, "name": data.get("name", "")})
    return out


def _new_token() -> str:
    # token curto e seguro
    return secrets.token_urlsafe(12)


# ---------------------------
# 1) Criar / editar tenant
# ---------------------------
st.subheader("1) Criar / editar loja (tenant)")

with st.form("tenant_form", clear_on_submit=False):
    c1, c2 = st.columns([1, 2])
    tenant_id = c1.text_input("Tenant ID (ex.: loja_001)").strip()
    tenant_name = c2.text_input("Nome da loja").strip()
    submitted = st.form_submit_button("Salvar loja")

if submitted:
    if not tenant_id:
        st.error("Tenant ID é obrigatório.")
    else:
        now = datetime.now(timezone.utc)
        db.collection("tenants").document(tenant_id).set(
            {
                "name": tenant_name,
                "updatedAt": now,
                "updatedBy": admin_email,
                # createdAt só grava se não existir (merge mantém)
                "createdAt": now,
            },
            merge=True,
        )
        st.success(f"Loja salva ✅ ({tenant_id})")


st.markdown("---")

# ---------------------------
# 2) Gerar convite
# ---------------------------
st.subheader("2) Gerar convite (link)")

tenants = _load_tenants()
tenant_labels = ["(digitar manualmente)"] + [
    f"{t['tenant_id']} — {t['name']}" if t["name"] else t["tenant_id"]
    for t in tenants
]

tenant_choice = st.selectbox("Escolha a loja", tenant_labels, index=0)

prefill_tenant = ""
if tenant_choice != "(digitar manualmente)":
    prefill_tenant = tenant_choice.split(" — ")[0].strip()

with st.form("invite_form", clear_on_submit=False):
    c1, c2 = st.columns([1, 2])
    t_id = c1.text_input("Tenant ID", value=prefill_tenant).strip()
    inv_email = c2.text_input(
        "Email do usuário (recomendado)",
        placeholder="usuario@empresa.com",
    ).strip().lower()

    c3, c4 = st.columns([1, 1])
    role = c3.selectbox("Role", ["user", "admin"], index=0)
    exp_days = c4.number_input("Expira em (dias)", min_value=1, max_value=60, value=7, step=1)

    submitted2 = st.form_submit_button("Gerar convite")

if submitted2:
    if not t_id:
        st.error("Tenant ID é obrigatório.")
    else:
        token = _new_token()
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=int(exp_days))

        db.collection("invites").document(token).set(
            {
                "tenant_id": t_id,
                "email": inv_email,  # pode ser vazio
                "role": role,
                "createdAt": now,
                "createdBy": admin_email,
                "expiresAt": expires_at,
            }
        )

        invite_link = f"{base_url}/?invite={token}"
        st.success("Convite criado ✅")
        st.caption("Link do convite (abra em aba anônima para testar):")
        st.code(invite_link, language="text")


st.markdown("---")

# ---------------------------
# 3) Listar convites
# ---------------------------
st.subheader("3) Convites recentes")

c1, c2, c3 = st.columns([1, 1, 1])
limit = c1.slider("Quantidade", min_value=5, max_value=50, value=15, step=5)
status_filter = c2.selectbox("Status", ["Todos", "Pendentes", "Usados", "Expirados"], index=1)
tenant_filter = c3.text_input("Filtrar por tenant_id (opcional)").strip()

query = db.collection("invites").order_by("createdAt", direction="DESCENDING").limit(limit)
docs = list(query.stream())

now = datetime.now(timezone.utc)
rows = []

for doc in docs:
    d = doc.to_dict() or {}
    expires_at = d.get("expiresAt")
    used_at = d.get("usedAt")

    expired = False
    if isinstance(expires_at, datetime):
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        expired = now > expires_at

    if tenant_filter and d.get("tenant_id") != tenant_filter:
        continue

    if status_filter == "Pendentes" and (used_at or expired):
        continue
    if status_filter == "Usados" and not used_at:
        continue
    if status_filter == "Expirados" and not expired:
        continue

    rows.append(
        {
            "token": doc.id,
            "tenant_id": d.get("tenant_id", ""),
            "email": d.get("email", ""),
            "role": d.get("role", ""),
            "createdAt": _to_utc_str(d.get("createdAt")),
            "expiresAt": _to_utc_str(d.get("expiresAt")),
            "usedAt": _to_utc_str(used_at),
            "usedByUid": d.get("usedByUid", ""),
            "link": f"{base_url}/?invite={doc.id}",
        }
    )

st.dataframe(rows, use_container_width=True)
st.caption("Se você preencheu **email** no convite, ele só funciona para aquele email.")

