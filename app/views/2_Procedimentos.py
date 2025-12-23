import streamlit as st
import pandas as pd
from services.tenant_repo import load_procedures, save_procedures
from services.guard import require_auth_and_tenant
from services.ui import sidebar_common, footer_signature

require_auth_and_tenant()
sidebar_common()

st.title("🧾 Procedimentos")
st.caption("Cada loja cadastra seus próprios procedimentos.")

tenant_id = st.session_state["tenant_id"]

# Carrega do Firestore (1x por tenant)
if "procedures" not in st.session_state or st.session_state.get("procedures_loaded_for") != tenant_id:
    st.session_state["procedures"] = load_procedures(tenant_id) or []
    st.session_state["procedures_loaded"] = True
    st.session_state["procedures_loaded_for"] = tenant_id

# Lista -> DataFrame editável
df = pd.DataFrame(st.session_state["procedures"])

# garante colunas (inclui MOD)
if df.empty:
    df = pd.DataFrame(columns=["nome", "tempo_min", "insumos", "mod", "preco_atual"])
else:
    # garante que procedimentos antigos tenham mod
    if "mod" not in df.columns:
        df["mod"] = 0.0

# ordem das colunas
df = df.reindex(columns=["nome", "tempo_min", "insumos", "mod", "preco_atual"])

st.subheader("Tabela de procedimentos (edite e salve)")

edited = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "nome": st.column_config.TextColumn("Nome", required=True),
        "tempo_min": st.column_config.NumberColumn("Tempo (min)", min_value=1, step=1, required=True),
        "insumos": st.column_config.NumberColumn("Insumos (R$)", min_value=0.0, step=10.0, required=True),
        "mod": st.column_config.NumberColumn("MOD (R$)", min_value=0.0, step=10.0),
        "preco_atual": st.column_config.NumberColumn("Preço atual (R$)", min_value=0.0, step=50.0),
    }
)

col1, col2 = st.columns(2)

if col1.button("Salvar tabela"):
    # remove linhas inválidas
    edited2 = edited.copy()

    # normaliza tipos / defaults
    if "mod" not in edited2.columns:
        edited2["mod"] = 0.0

    edited2["mod"] = edited2["mod"].fillna(0.0)
    edited2["preco_atual"] = edited2.get("preco_atual", pd.Series([None] * len(edited2))).where(
        pd.notnull(edited2.get("preco_atual")), None
    )

    edited2 = edited2.dropna(subset=["nome", "tempo_min", "insumos"], how="any")

    items = edited2.to_dict(orient="records")

    st.session_state["procedures"] = items
    save_procedures(tenant_id, items)
    st.success(f"Procedimentos salvos ✅ (loja: {tenant_id})")

if col2.button("Limpar tudo"):
    st.session_state["procedures"] = []
    save_procedures(tenant_id, [])
    st.warning(f"Procedimentos removidos (loja: {tenant_id})")

footer_signature()
