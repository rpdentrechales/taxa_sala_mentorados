import streamlit as st
import pandas as pd

st.title("🧾 Procedimentos")
st.caption("Cada loja cadastra seus próprios procedimentos. (MVP: salva só na sessão)")

if "procedures" not in st.session_state:
    st.session_state["procedures"] = []

# transforma lista em DataFrame editável
df = pd.DataFrame(st.session_state["procedures"])
if df.empty:
    df = pd.DataFrame(columns=["nome", "tempo_min", "insumos", "preco_atual"])

st.subheader("Tabela de procedimentos (edite e salve)")
edited = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "nome": st.column_config.TextColumn("Nome", required=True),
        "tempo_min": st.column_config.NumberColumn("Tempo (min)", min_value=1, step=1, required=True),
        "insumos": st.column_config.NumberColumn("Insumos (R$)", min_value=0.0, step=10.0, required=True),
        "preco_atual": st.column_config.NumberColumn("Preço atual (R$)", min_value=0.0, step=50.0),
    }
)

col1, col2 = st.columns(2)
if col1.button("Salvar tabela"):
    # limpa linhas vazias
    edited = edited.dropna(subset=["nome", "tempo_min", "insumos"], how="any")
    st.session_state["procedures"] = edited.to_dict(orient="records")
    st.success("Procedimentos salvos na sessão ✅")

if col2.button("Limpar tudo"):
    st.session_state["procedures"] = []
    st.warning("Procedimentos removidos da sessão.")
