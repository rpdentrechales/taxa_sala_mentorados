import streamlit as st
import pandas as pd
from services.tenant_repo import load_procedures, save_procedures

st.title("🧾 Procedimentos")
st.caption("Cada loja cadastra seus próprios procedimentos. (MVP: salva só na sessão)")

tenant_id = st.session_state.get("tenant_id", "loja_demo")

if "procedures_loaded" not in st.session_state or st.session_state.get("procedures_loaded_for") != tenant_id:
    st.session_state["procedures"] = load_procedures(tenant_id)
    st.session_state["procedures_loaded"] = True
    st.session_state["procedures_loaded_for"] = tenant_id

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
    edited = edited.dropna(subset=["nome", "tempo_min", "insumos"], how="any")
    items = edited.to_dict(orient="records")
    st.session_state["procedures"] = items
    save_procedures(tenant_id, items)
    st.success(f"Procedimentos salvos ✅ (loja: {tenant_id})")

if col2.button("Limpar tudo"):
    st.session_state["procedures"] = []
    save_procedures(tenant_id, [])
    st.warning(f"Procedimentos removidos (loja: {tenant_id})")
