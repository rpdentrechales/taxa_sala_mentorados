from dotenv import load_dotenv
load_dotenv(override=True)

import os
import streamlit as st

# ⚠️ PRIMEIRO st.*
st.set_page_config(
    page_title="Taxa de Sala 360",
    page_icon="🧮",
    layout="wide"
)

# Base URL para gerar link correto (Admin)
st.session_state["base_url"] = os.environ.get("APP_BASE_URL", "http://localhost:8501").rstrip("/")

# Se tiver invite, salva token e manda para a página única de convite
invite_token = st.query_params.get("invite")
if invite_token:
    st.session_state["pending_invite"] = invite_token
    st.query_params.clear()
    st.switch_page("pages/00_Convite.py")

from services.guard import require_auth_and_tenant
from services.ui import sidebar_common

# Garante login + tenant (criar conta não aparece aqui)
require_auth_and_tenant()
sidebar_common()

# ---------- HOME ----------
st.title("🧮 Taxa de Sala 360")
st.caption("MVP (Firestore + login + convites).")

has_config = "store_params" in st.session_state and "fixed_costs" in st.session_state
has_procs = "procedures" in st.session_state and len(st.session_state.get("procedures", [])) > 0

col1, col2, col3 = st.columns(3)
col1.metric("Configurações", "OK" if has_config else "Pendente")
col2.metric("Procedimentos", "OK" if has_procs else "Pendente")
col3.metric("Pronto p/ calcular", "SIM" if (has_config and has_procs) else "NÃO")

st.markdown("---")
st.subheader("Como usar")
st.write(
    """
1) Vá em **Configurações** e preencha custos fixos + capacidade (salas, dias, horas, ocupação).
2) Vá em **Procedimentos** e cadastre os procedimentos da loja.
3) Vá em **Calculadora** e selecione um procedimento para ver os custos e KPIs (incluindo ociosidade).
"""
)

st.info("Agora navegue pelas páginas no menu lateral 👈")
