import streamlit as st
from services.tenant_repo import (
    load_store_params, save_store_params,
    load_fixed_costs, save_fixed_costs
)
from services.guard import require_auth_and_tenant
from services.ui import sidebar_common, footer_signature

require_auth_and_tenant()
sidebar_common()

st.title("⚙️ Configurações da Loja")
st.caption("Aqui você define custos fixos e capacidade. (Por enquanto, salva só na sessão do navegador.)")

tenant_id = st.session_state["tenant_id"]

if "store_params" not in st.session_state:
    db_store = load_store_params(tenant_id)
    if db_store:
        st.session_state["store_params"] = db_store

if "fixed_costs" not in st.session_state:
    db_costs = load_fixed_costs(tenant_id)
    if db_costs:
        st.session_state["fixed_costs"] = db_costs
        
# Defaults
store_defaults = {
    "num_salas": 1,
    "dias_mes": 26,
    "horas_dia": 10.0,
    "ocupacao_pct": 70.0,  # 0 a 100
}
cost_defaults = {
    "aluguel": 0.0,
    "salarios": 0.0,
    "outros": 0.0,
}

store_params = st.session_state.get("store_params", store_defaults.copy())
fixed_costs = st.session_state.get("fixed_costs", cost_defaults.copy())

with st.form("config_form"):
    st.subheader("Capacidade")
    c1, c2, c3, c4 = st.columns(4)
    store_params["num_salas"] = c1.number_input("Nº de salas", min_value=1, step=1, value=int(store_params["num_salas"]))
    store_params["dias_mes"] = c2.number_input("Dias/mês", min_value=1, max_value=31, step=1, value=int(store_params["dias_mes"]))
    store_params["horas_dia"] = c3.number_input("Horas/dia", min_value=1.0, max_value=24.0, step=0.5, value=float(store_params["horas_dia"]))
    store_params["ocupacao_pct"] = c4.number_input("Ocupação média (%)", min_value=1.0, max_value=100.0, step=1.0, value=float(store_params["ocupacao_pct"]))

    st.subheader("Custos fixos (mensal)")
    k1, k2, k3 = st.columns(3)
    fixed_costs["aluguel"] = k1.number_input("Aluguel (R$)", min_value=0.0, step=100.0, value=float(fixed_costs["aluguel"]))
    fixed_costs["salarios"] = k2.number_input("Salários (R$)", min_value=0.0, step=100.0, value=float(fixed_costs["salarios"]))
    fixed_costs["outros"] = k3.number_input("Outros custos fixos (R$)", min_value=0.0, step=100.0, value=float(fixed_costs["outros"]))

    submitted = st.form_submit_button("Salvar configurações")

if submitted:
    st.session_state["store_params"] = store_params
    st.session_state["fixed_costs"] = fixed_costs

    save_store_params(tenant_id, store_params)
    save_fixed_costs(tenant_id, fixed_costs)

    st.success(f"Configurações salvas ✅ (loja: {tenant_id})")

# KPIs (preview)
if "store_params" in st.session_state and "fixed_costs" in st.session_state:
    sp = st.session_state["store_params"]
    fc = st.session_state["fixed_costs"]

    ocupacao = sp["ocupacao_pct"] / 100.0
    ociosidade_pct = 100.0 - sp["ocupacao_pct"]

    min_disponiveis = sp["num_salas"] * sp["dias_mes"] * sp["horas_dia"] * 60.0
    min_utilizados = min_disponiveis * ocupacao
    min_ociosos = min_disponiveis - min_utilizados

    custo_fixo_total = fc["aluguel"] + fc["salarios"] + fc["outros"]

    custo_min_capacidade = (custo_fixo_total / min_disponiveis) if min_disponiveis > 0 else 0.0
    custo_min_real = (custo_fixo_total / min_utilizados) if min_utilizados > 0 else 0.0
    custo_ociosidade_mes = custo_fixo_total * (ociosidade_pct / 100.0)

    st.markdown("---")
    st.subheader("KPIs (prévia)")

    a, b, c, d = st.columns(4)
    a.metric("Ociosidade (%)", f"{ociosidade_pct:.1f}%")
    b.metric("Minutos ociosos/mês", f"{min_ociosos:,.0f}".replace(",", "."))
    c.metric("R$ ociosidade/mês", f"R$ {custo_ociosidade_mes:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    d.metric("Custo/min (real)", f"R$ {custo_min_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    st.caption(f"Custo/min (capacidade): R$ {custo_min_capacidade:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

from services.ui import footer_signature
footer_signature()