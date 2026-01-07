import streamlit as st
from pathlib import Path

# Paleta dark premium
BRAND = {
    "bg": "#0B1220",          # fundo
    "panel": "#0F1A2E",       # sidebar / painéis
    "card": "#101E36",        # cards/metrics
    "border": "rgba(255,255,255,0.10)",
    "text": "rgba(255,255,255,0.88)",
    "muted": "rgba(255,255,255,0.65)",
    "primary": "#5B7CFF",     # azul “360”
    "primary2": "#7AA2FF",
}

def inject_brand_css():
    st.markdown(
        f"""
        <style>
        /* ====== Layout ====== */
        .stApp {{
            background: {BRAND["bg"]};
            color: {BRAND["text"]};
        }}

        .block-container {{
            padding-top: 2.0rem;
            padding-bottom: 2.5rem;
            max-width: 1200px;
        }}

        h1, h2, h3 {{
            letter-spacing: -0.02em;
            color: {BRAND["text"]};
        }}
        h1 {{ font-weight: 850; }}
        h2, h3 {{ font-weight: 750; }}

        .stCaption, [data-testid="stCaptionContainer"] {{
            color: {BRAND["muted"]} !important;
        }}

        [data-testid="stSidebar"] {{
            background: {BRAND["panel"]};
            border-right: 1px solid {BRAND["border"]};
        }}

        [data-testid="stMetric"] {{
            background: {BRAND["card"]};
            border: 1px solid {BRAND["border"]};
            border-radius: 16px;
            padding: 14px 14px;
        }}
        [data-testid="stMetric"] * {{
            color: {BRAND["text"]} !important;
        }}

        input, textarea, .stTextInput input, .stNumberInput input {{
            background: rgba(255,255,255,0.06) !important;
            border: 1px solid {BRAND["border"]} !important;
            color: {BRAND["text"]} !important;
            border-radius: 12px !important;
        }}

        [data-baseweb="select"] > div {{
            background: rgba(255,255,255,0.06) !important;
            border: 1px solid {BRAND["border"]} !important;
            border-radius: 12px !important;
            color: {BRAND["text"]} !important;
        }}

        .stButton>button {{
            background: linear-gradient(180deg, {BRAND["primary2"]}, {BRAND["primary"]});
            color: white !important;
            border-radius: 14px;
            padding: 0.70rem 1.00rem;
            font-weight: 800;
            border: 0px;
            box-shadow: 0 10px 30px rgba(91,124,255,0.18);
        }}
        .stButton>button:hover {{
            filter: brightness(1.05);
            transform: translateY(-1px);
        }}
        .stButton>button:active {{
            transform: translateY(0px);
            filter: brightness(0.98);
        }}

        a {{
            color: {BRAND["primary2"]} !important;
            font-weight: 650;
            text-decoration: none;
        }}
        a:hover {{ text-decoration: underline; }}

        hr {{
            border: none;
            border-top: 1px solid {BRAND["border"]};
            margin: 1.25rem 0;
        }}

        #MainMenu {{ visibility: hidden; }}
        header {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _logo_path() -> Path:
    """
    Retorna o caminho absoluto para app/assets/logo-360.png
    Funciona em local e no Cloud Run (desde que o arquivo esteja no repo).
    """
    # ui.py está em app/services/ui.py -> parents[1] = app/
    return Path(__file__).resolve().parents[1] / "assets" / "logo-360.png"


def sidebar_common(key_prefix: str):
    """Sidebar padrão com identidade visual + logout com key única por página."""
    inject_brand_css()

    with st.sidebar:
        # ✅ Logo
        lp = _logo_path()
        if lp.exists():
            st.image(str(lp), use_container_width=True)
            st.markdown("")
        else:
            # não quebra em prod se não tiver o arquivo
            st.markdown("")

        role = st.session_state.get("role", "user")
        tenant_id = st.session_state.get("tenant_id", "")

        if role == "admin":
            st.caption(f"🛠️ Admin | tenant: {tenant_id}")
        elif tenant_id:
            st.caption(f"🏷️ Tenant: {tenant_id}")
        else:
            st.caption("🏷️ Tenant: —")

        st.markdown("")

        if st.button("🚪 Sair", key=f"{key_prefix}_logout"):
            for k in list(st.session_state.keys()):
                st.session_state.pop(k, None)
            st.rerun()


def footer_signature():
    inject_brand_css()
    st.markdown("---")
    st.markdown(
        f"""
        <div style="
            width:100%;
            text-align:center;
            padding: 8px 0 2px 0;
            font-size: 0.9rem;
            color: {BRAND["muted"]};
        ">
            <strong style="color:{BRAND["text"]};">Pró-Corpo BI</strong>
            &nbsp;|&nbsp;
            <strong style="color:{BRAND["text"]};">360 Estética</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
