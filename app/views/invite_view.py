import streamlit as st
from app.services.guard import require_auth_only, accept_invite_for_current_user
from app.services.ui import footer_signature

def render_invite():
    st.title("🎟️ Ativar acesso")

    token = st.query_params.get("invite") or st.session_state.get("pending_invite")
    if not token:
        st.error("Este link de convite é inválido (sem token).")
        footer_signature()
        st.stop()

    require_auth_only(allow_signup=True)

    footer_signature()

    ok = accept_invite_for_current_user(token)
    if ok:
        st.success("Acesso ativado ✅")
        st.rerun()
