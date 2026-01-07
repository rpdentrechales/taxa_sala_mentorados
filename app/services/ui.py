import streamlit as st
from pathlib import Path

# Paleta dark premium
BRAND = {
    "bg": "#0B1220",
    "panel": "#0F1A2E",
    "card": "#101E36",
    "border": "rgba(255,255,255,0.10)",
    "text": "rgba(255,255,255,0.92)",
    "muted": "rgba(255,255,255,0.70)",
    "primary": "#5B7CFF",
    "primary2": "#7AA2FF",
}


def _logo_path() -> Path:
    # ui.py está em app/services/ui.py -> parents[1] = app/
    return Path(__file__).resolve().parents[1] / "assets" / "logo-360.png"


def inject_brand_css():
    """
    CSS precisa ser re-injetado em TODO rerun (não use flag em session_state),
    senão "pisca" / muda tema ao clicar.
    """
    st.markdown(
        f"""
        <style>
        /* ========= Base ========= */
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

        /* captions / textos secundários */
        .stCaption, [data-testid="stCaptionContainer"] {{
            color: {BRAND["muted"]} !important;
        }}

        /* ========= Sidebar ========= */
        [data-testid="stSidebar"] {{
            background: {BRAND["panel"]};
            border-right: 1px solid {BRAND["border"]};
        }}

        /* ========= Sidebar NAV (st.navigation) ========= */
        [data-testid="stSidebarNav"] {{
            padding-top: 0.5rem;
        }}

        [data-testid="stSidebarNav"] a {{
            color: {BRAND["text"]} !important;
            border-radius: 12px;
            margin: 6px 0;
            padding: 10px 12px;
            text-decoration: none !important;
        }}

        [data-testid="stSidebarNav"] a span {{
            color: {BRAND["text"]} !important;
            font-weight: 700;
            opacity: 0.95;
        }}

        [data-testid="stSidebarNav"] a:hover {{
            background: rgba(255,255,255,0.06) !important;
        }}

        [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: rgba(91,124,255,0.20) !important;
            border: 1px solid rgba(91,124,255,0.35) !important;
        }}

        /* ========= Cards / Metrics ========= */
        [data-testid="stMetric"] {{
            background: {BRAND["card"]};
            border: 1px solid {BRAND["border"]};
            border-radius: 16px;
            padding: 14px 14px;
        }}
        [data-testid="stMetric"] * {{
            color: {BRAND["text"]} !important;
        }}

        /* ========= Inputs (corrigido BaseWeb) ========= */

        /* Labels */
        [data-testid="stNumberInput"] label,
        [data-testid="stTextInput"] label,
        [data-testid="stTextArea"] label,
        [data-testid="stSelectbox"] label,
        [data-testid="stMultiSelect"] label {{
            color: {BRAND["muted"]} !important;
            font-weight: 650;
        }}

        /* Wrapper BaseWeb INPUT (isso estava branco!) */
        div[data-baseweb="input"] > div {{
            background: rgba(255,255,255,0.06) !important;
            border: 1px solid {BRAND["border"]} !important;
            border-radius: 12px !important;
        }}

        /* Input (texto/numero) */
        div[data-baseweb="input"] input {{
            background: transparent !important;
            color: {BRAND["text"]} !important;
            -webkit-text-fill-color: {BRAND["text"]} !important;
            caret-color: {BRAND["text"]} !important;
        }}

        /* Placeholder */
        div[data-baseweb="input"] input::placeholder {{
            color: rgba(255,255,255,0.45) !important;
            -webkit-text-fill-color: rgba(255,255,255,0.45) !important;
        }}

        /* Wrapper BaseWeb TEXTAREA */
        div[data-baseweb="textarea"] > div {{
            background: rgba(255,255,255,0.06) !important;
            border: 1px solid {BRAND["border"]} !important;
            border-radius: 12px !important;
        }}
        div[data-baseweb="textarea"] textarea {{
            background: transparent !important;
            color: {BRAND["text"]} !important;
            -webkit-text-fill-color: {BRAND["text"]} !important;
            caret-color: {BRAND["text"]} !important;
        }}
        div[data-baseweb="textarea"] textarea::placeholder {{
            color: rgba(255,255,255,0.45) !important;
            -webkit-text-fill-color: rgba(255,255,255,0.45) !important;
        }}

        /* Botões +/- do number input */
        [data-testid="stNumberInput"] button {{
            background: rgba(255,255,255,0.06) !important;
            border: 1px solid {BRAND["border"]} !important;
            border-radius: 10px !important;
        }}
        [data-testid="stNumberInput"] button * {{
            color: {BRAND["text"]} !important;
        }}

        /* Selectbox baseweb */
        [data-baseweb="select"] > div {{
            background: rgba(255,255,255,0.06) !important;
            border: 1px solid {BRAND["border"]} !important;
            border-radius: 12px !important;
            color: {BRAND["text"]} !important;
        }}
        [data-baseweb="select"] * {{
            color: {BRAND["text"]} !important;
        }}

        /* ========= Botões (CTA) ========= */
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

        /* ========= Separador ========= */
        hr {{
            border: none;
            border-top: 1px solid {BRAND["border"]};
            margin: 1.25rem 0;
        }}

        /* ========= Remove menu/toolbar (opcional) ========= */
        #MainMenu {{ visibility: hidden; }}
        header {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        </style>
        """,
        unsafe_allow_html=True,
    )



def sidebar_common(key_prefix: str):
    inject_brand_css()

    with st.sidebar:
        lp = _logo_path()
        if lp.exists():
            st.image(str(lp), use_container_width=True)
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
            padding: 10px 0 2px 0;
            font-size: 0.9rem;
            color: {BRAND["muted"]};
        ">
            <strong style="color:{BRAND["text"]};">Pró-Corpo BI</strong>
            &nbsp;|&nbsp;
            Desenvolvido por <strong style="color:{BRAND["text"]};">Thales Basilio Santoro</strong>
            para <strong style="color:{BRAND["text"]};">360 Estética</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
