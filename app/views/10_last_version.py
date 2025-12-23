import streamlit as st
from services.guard import require_auth_and_tenant
from services.ui import sidebar_common, footer_signature

require_auth_and_tenant()
sidebar_common("last")

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

footer_signature()
