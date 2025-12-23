# app/services/guard.py
from __future__ import annotations

from datetime import datetime, timezone
import streamlit as st

from services.auth import sign_in_with_password, sign_up_with_password, verify_id_token
from services.permissions import is_admin_email
from services.user_tenant_repo import get_user_tenant, set_user_tenant
from services.invite_repo import get_invite, mark_invite_used


# -------------------------
# UI / Auth
# -------------------------
def login_screen(allow_signup: bool = False):
    st.title("🔐 Acesso")

    if allow_signup:
        st.caption("Você recebeu um convite. Entre ou crie sua conta para continuar.")
        mode = st.radio("O que você quer fazer?", ["Entrar", "Criar conta"], horizontal=True)
    else:
        st.caption("Entre com seu email e senha.")
        mode = "Entrar"

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")

        if allow_signup and mode == "Criar conta":
            password2 = st.text_input("Confirmar senha", type="password")
        submitted = st.form_submit_button("Continuar")

    if submitted:
        try:
            if allow_signup and mode == "Criar conta":
                if password != password2:
                    st.error("As senhas não coincidem.")
                    return
                data = sign_up_with_password(email, password)
                st.success("Conta criada ✅")
            else:
                data = sign_in_with_password(email, password)

            st.session_state["id_token"] = data["idToken"]
            st.rerun()
        except Exception as e:
            st.error(f"Erro: {e}")


def require_auth_only(allow_signup: bool = False):
    """
    Garante usuário logado e define uid/email/role.
    Não exige tenant (ideal para Admin e Convite).
    """
    id_token = st.session_state.get("id_token")
    if not id_token:
        login_screen(allow_signup=allow_signup)
        st.stop()

    try:
        decoded = verify_id_token(id_token)
    except Exception:
        st.session_state.pop("id_token", None)
        st.warning("Sessão expirada. Faça login novamente.")
        st.rerun()

    uid = decoded["uid"]
    email = (decoded.get("email", "") or "").strip()

    st.session_state["uid"] = uid
    st.session_state["email"] = email
    st.session_state["role"] = "admin" if is_admin_email(email) else "user"


# -------------------------
# Tenant-scoped session
# -------------------------
def reset_tenant_scoped_state_if_needed(tenant_id: str):
    """
    Evita 'vazar' dados do tenant anterior no session_state.
    Sempre que trocar de tenant, limpa dados da loja em memória.
    """
    prev = st.session_state.get("_active_tenant_id")
    if prev != tenant_id:
        for k in [
            "store_params",
            "fixed_costs",
            "procedures",
            "procedures_loaded",
            "procedures_loaded_for",
        ]:
            st.session_state.pop(k, None)

        st.session_state["_active_tenant_id"] = tenant_id


def require_auth_and_tenant():
    """
    Para Home e páginas do app (Config/Procedimentos/Calculadora):
    exige login + vínculo com tenant.
    """
    require_auth_only(allow_signup=False)

    uid = st.session_state["uid"]
    mapping = get_user_tenant(uid)

    if not mapping:
        st.error("Seu usuário ainda não está vinculado a nenhuma loja (tenant).")
        st.info("Use o link de convite enviado pelo administrador.")
        st.stop()

    tenant_id = mapping["tenant_id"]
    st.session_state["tenant_id"] = tenant_id

    # role vindo do banco, mas admin pode ser forçado por allowlist
    role = mapping.get("role", "user")
    if is_admin_email(st.session_state.get("email", "")):
        role = "admin"
    st.session_state["role"] = role

    reset_tenant_scoped_state_if_needed(tenant_id)


# -------------------------
# Invite onboarding (página Convite)
# -------------------------
def accept_invite_for_current_user(invite_token: str):
    """
    Consome o convite e vincula o usuário logado ao tenant.
    Use somente na página 00_Convite.py.
    """
    uid = st.session_state.get("uid")
    email = (st.session_state.get("email") or "").strip().lower()

    inv = get_invite(invite_token)
    if not inv:
        st.error("Convite inválido.")
        st.stop()

    if inv.get("usedAt"):
        st.error("Convite já utilizado.")
        st.stop()

    # expiração
    expires_at = inv.get("expiresAt")
    if expires_at:
        if isinstance(expires_at, datetime) and expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires_at:
            st.error("Convite expirado.")
            st.stop()

    # email travado (se existir)
    invite_email = (inv.get("email") or "").strip().lower()
    if invite_email and invite_email != email:
        st.error("Esse convite não é para este email.")
        st.stop()

    tenant_id = inv["tenant_id"]
    role = inv.get("role", "user")

    set_user_tenant(uid, tenant_id, email=email, role=role)
    mark_invite_used(invite_token, uid)

    # limpa e volta
    st.session_state.pop("pending_invite", None)
    st.query_params.clear()
    st.success("Acesso ativado ✅")
    st.switch_page("app.py")
