import streamlit as st

def sidebar_common():
    with st.sidebar:
        role = st.session_state.get("role", "")
        tenant = st.session_state.get("tenant_id")

        if role == "admin" and tenant:
            st.caption(f"Admin | tenant: {tenant}")
        elif tenant:
            st.caption(f"Tenant: {tenant}")
        elif role == "admin":
            st.caption("Admin")

        if st.button("🚪 Sair"):
            # limpa sessão inteira
            for k in list(st.session_state.keys()):
                st.session_state.pop(k, None)
            st.rerun()

def footer_signature():
    st.markdown("---")
    st.markdown(
        """
        <div style="
            width:100%;
            text-align:center;
            padding: 8px 0 2px 0;
            font-size: 0.9rem;
            color: rgba(255,255,255,0.70);
        ">
            <strong>Pró-Corpo BI</strong> | Desenvolvido por <strong>Thales Basilio Santoro</strong> para <strong>360 Estética</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

