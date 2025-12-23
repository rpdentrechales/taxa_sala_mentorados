# app/pages/00_Convite.py
import streamlit as st
from services.guard import require_auth_only, accept_invite_for_current_user
from services.ui import footer_signature

st.title("🎟️ Ativar acesso")

invite_token = st.session_state.get("pending_invite") or st.query_params.get("invite")
if not invite_token:
    st.error("Este link de convite é inválido (sem token).")
    footer_signature()
    st.stop()

require_auth_only(allow_signup=True)

# footer aparece na tela antes do redirect (e também se der erro antes)
footer_signature()

accept_invite_for_current_user(invite_token)
