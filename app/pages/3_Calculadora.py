import streamlit as st

st.title("🧮 Calculadora")
st.caption("Calcula custo/minuto, custo do procedimento e mostra ociosidade. (MVP: dados da sessão)")

if "store_params" not in st.session_state or "fixed_costs" not in st.session_state:
    st.warning("Preencha primeiro as **Configurações**.")
    st.stop()

if "procedures" not in st.session_state or len(st.session_state["procedures"]) == 0:
    st.warning("Cadastre primeiro os **Procedimentos**.")
    st.stop()

sp = st.session_state["store_params"]
fc = st.session_state["fixed_costs"]
procedures = st.session_state["procedures"]

ocupacao = sp["ocupacao_pct"] / 100.0
ociosidade_pct = 100.0 - sp["ocupacao_pct"]

min_disponiveis = sp["num_salas"] * sp["dias_mes"] * sp["horas_dia"] * 60.0
min_utilizados = min_disponiveis * ocupacao
min_ociosos = min_disponiveis - min_utilizados

custo_fixo_total = fc["aluguel"] + fc["salarios"] + fc["outros"]

custo_min_capacidade = (custo_fixo_total / min_disponiveis) if min_disponiveis > 0 else 0.0
custo_min_real = (custo_fixo_total / min_utilizados) if min_utilizados > 0 else 0.0
custo_ociosidade_mes = custo_fixo_total * (ociosidade_pct / 100.0)

# KPIs topo
k1, k2, k3, k4 = st.columns(4)
k1.metric("Ociosidade (%)", f"{ociosidade_pct:.1f}%")
k2.metric("Minutos ociosos/mês", f"{min_ociosos:,.0f}".replace(",", "."))
k3.metric("R$ ociosidade/mês", f"R$ {custo_ociosidade_mes:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
k4.metric("Custo/min (real)", f"R$ {custo_min_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# seleção de procedimento
names = [p.get("nome", "Sem nome") for p in procedures]
idx = st.selectbox("Selecione o procedimento", range(len(names)), format_func=lambda i: names[i])

p = procedures[idx]
tempo_min = float(p.get("tempo_min", 0))
insumos = float(p.get("insumos", 0))
preco_atual = p.get("preco_atual", None)

custo_fixo_alocado = tempo_min * custo_min_real
custo_total = custo_fixo_alocado + insumos

st.subheader("Resultado do procedimento")
r1, r2, r3 = st.columns(3)
r1.metric("Custo fixo alocado", f"R$ {custo_fixo_alocado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
r2.metric("Custo de insumos", f"R$ {insumos:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
r3.metric("Custo total", f"R$ {custo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

if preco_atual not in (None, ""):
    try:
        preco = float(preco_atual)
        margem = ((preco - custo_total) / preco) * 100.0 if preco > 0 else 0.0
        st.caption(f"Preço atual: R$ {preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + f" | Margem estimada: {margem:.1f}%")
    except ValueError:
        pass

st.markdown("---")
st.caption(f"Custo/min (capacidade): R$ {custo_min_capacidade:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

from services.ui import footer_signature
footer_signature()