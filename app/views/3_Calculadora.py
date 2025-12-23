import streamlit as st
from services.guard import require_auth_and_tenant
from services.ui import sidebar_common, footer_signature

require_auth_and_tenant()
sidebar_common("calculator")

st.title("🧮 Calculadora")
st.caption("Calcula custo/minuto, custo do procedimento e mostra ociosidade.")

# ---------- Guards ----------
if "store_params" not in st.session_state or "fixed_costs" not in st.session_state:
    st.warning("Preencha primeiro as **Configurações**.")
    st.stop()

if "procedures" not in st.session_state or len(st.session_state["procedures"]) == 0:
    st.warning("Cadastre primeiro os **Procedimentos**.")
    st.stop()

sp = st.session_state["store_params"]
fc = st.session_state["fixed_costs"]
procedures = st.session_state["procedures"]

# ---------- Percentuais (0 a 100) ----------
aliquota_imposto_pct = float(sp.get("aliquota_imposto_pct", 0.0) or 0.0)
taxa_cartao_pct = float(sp.get("taxa_cartao_pct", 0.0) or 0.0)
comissao_pct = float(sp.get("comissao_pct", 0.0) or 0.0)

taxa_total_pct = aliquota_imposto_pct + taxa_cartao_pct + comissao_pct
taxa_total = taxa_total_pct / 100.0

# ---------- Capacidade / Ociosidade ----------
ocupacao = float(sp["ocupacao_pct"]) / 100.0
ociosidade_pct = 100.0 - float(sp["ocupacao_pct"])

min_disponiveis = float(sp["num_salas"]) * float(sp["dias_mes"]) * float(sp["horas_dia"]) * 60.0
min_utilizados = min_disponiveis * ocupacao
min_ociosos = min_disponiveis - min_utilizados

custo_fixo_total = float(fc["aluguel"]) + float(fc["salarios"]) + float(fc["outros"])

custo_min_capacidade = (custo_fixo_total / min_disponiveis) if min_disponiveis > 0 else 0.0
custo_min_real = (custo_fixo_total / min_utilizados) if min_utilizados > 0 else 0.0
custo_ociosidade_mes = custo_fixo_total * (ociosidade_pct / 100.0)

# ---------- KPIs topo ----------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Ociosidade (%)", f"{ociosidade_pct:.1f}%")
k2.metric("Minutos ociosos/mês", f"{min_ociosos:,.0f}".replace(",", "."))
k3.metric("R$ ociosidade/mês", f"R$ {custo_ociosidade_mes:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
k4.metric("Custo/min (real)", f"R$ {custo_min_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# ---------- Seleção de procedimento ----------
names = [p.get("nome", "Sem nome") for p in procedures]
idx = st.selectbox("Selecione o procedimento", range(len(names)), format_func=lambda i: names[i])

p = procedures[idx]
tempo_min = float(p.get("tempo_min", 0) or 0)
insumos = float(p.get("insumos", 0) or 0)
mod = float(p.get("mod", 0) or 0)  # ✅ NOVO
preco_atual = p.get("preco_atual", None)

# ---------- Custos ----------
custo_fixo_alocado = tempo_min * custo_min_real
custo_total = custo_fixo_alocado + insumos + mod

st.subheader("Resultado do procedimento")
r1, r2, r3, r4 = st.columns(4)
r1.metric("Custo fixo alocado", f"R$ {custo_fixo_alocado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
r2.metric("Insumos", f"R$ {insumos:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
r3.metric("MOD", f"R$ {mod:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
r4.metric("Custo total", f"R$ {custo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("### Percentuais configurados")
st.caption(
    f"Imposto: **{aliquota_imposto_pct:.2f}%** | "
    f"Cartão: **{taxa_cartao_pct:.2f}%** | "
    f"Comissão: **{comissao_pct:.2f}%** | "
    f"Total: **{taxa_total_pct:.2f}%**"
)

# ---------- Margens / Receita líquida ----------
if preco_atual not in (None, ""):
    try:
        preco = float(preco_atual)

        taxas_valor = preco * taxa_total
        receita_liquida = preco - taxas_valor

        lucro_liquido = receita_liquida - custo_total

        margem_bruta_pct = ((preco - custo_total) / preco) * 100.0 if preco > 0 else 0.0
        margem_liquida_pct = (lucro_liquido / preco) * 100.0 if preco > 0 else 0.0

        st.markdown("---")
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Preço (bruto)", f"R$ {preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        s2.metric("Taxas (imposto+cartão+comissão)", f"R$ {taxas_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        s3.metric("Receita líquida", f"R$ {receita_liquida:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        s4.metric("Lucro líquido", f"R$ {lucro_liquido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        st.caption(f"Margem bruta (sem taxas): {margem_bruta_pct:.1f}% | Margem líquida (com taxas): {margem_liquida_pct:.1f}%")

    except ValueError:
        st.warning("Preço atual inválido para cálculo. Corrija no cadastro de Procedimentos.")

st.markdown("---")
st.caption(f"Custo/min (capacidade): R$ {custo_min_capacidade:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
