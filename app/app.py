from dotenv import load_dotenv
load_dotenv(override=True)

import os
import streamlit as st

st.set_page_config(page_title="Taxa de Sala 360", page_icon="🧮", layout="wide")
st.session_state["base_url"] = os.environ.get("APP_BASE_URL", "http://localhost:8501").rstrip("/")

# convite: só por link
invite_token = st.query_params.get("invite")
if invite_token:
    st.session_state["pending_invite"] = invite_token
    st.query_params.clear()
    st.switch_page("views/00_Convite.py")

from services.guard import require_auth_only, reset_tenant_scoped_state_if_needed
from services.user_tenant_repo import get_user_tenant
from services.permissions import is_admin_email

# ====== MENU DINÂMICO ======
pages = []

# não logado: mostra só "Login" (uma view simples)
# (aqui a gente só chama require_auth_only e ele já mostra a tela de login)
require_auth_only(allow_signup=False)

# se chegou aqui, está logado
uid = st.session_state["uid"]
email = st.session_state.get("email", "")

mapping = get_user_tenant(uid)
has_tenant = bool(mapping)

if has_tenant:
    tenant_id = mapping["tenant_id"]
    st.session_state["tenant_id"] = tenant_id
    reset_tenant_scoped_state_if_needed(tenant_id)

    role = mapping.get("role", "user")
    if is_admin_email(email):
        role = "admin"
    st.session_state["role"] = role

    pages += [
        st.Page("views/10_App.py", title="App", icon="🧮", url_path="home"),
        st.Page("views/1_Configuracoes.py", title="Configurações", icon="⚙️", url_path="configuracoes"),
        st.Page("views/2_Procedimentos.py", title="Procedimentos", icon="🧾", url_path="procedimentos"),
        st.Page("views/3_Calculadora.py", title="Calculadora", icon="🧮", url_path="calculadora"),
    ]
else:
    # sem tenant: só admin pode ver admin
    if st.session_state.get("role") != "admin":
        st.error("Seu usuário ainda não está vinculado a uma loja (tenant).")
        st.info("Use o link de convite enviado pelo administrador.")
        st.stop()

# admin no menu só pra admin
if st.session_state.get("role") == "admin":
    pages += [st.Page("views/0_Admin.py", title="Admin", icon="🛠️", url_path="admin")]

st.navigation(pages).run()
