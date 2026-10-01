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


# Página estática servida por /app/static/ (precisa de server.enableStaticServing=true).
# Sair do Streamlit fecha o websocket -> o Cloud Run para de cobrar a instância.
SESSION_ENDED_URL = "/app/static/sessao-encerrada.html"

IDLE_WARNING_SECONDS = 90   # mostra o aviso
IDLE_TIMEOUT_SECONDS = 120  # redireciona


def inactivity_guard():
    """
    Redireciona para a página de sessão encerrada após IDLE_TIMEOUT_SECONDS sem
    atividade (mouse/teclado/scroll/toque), com aviso em IDLE_WARNING_SECONDS.
    Chamar em TODO rerun (app.py), inclusive na tela de login.
    """
    st.html(
        f"""
        <script>
        (function () {{
          // roda a cada rerun, mas instala os listeners uma única vez
          if (window.__idleGuard) return;
          window.__idleGuard = true;

          const WARN_MS = {IDLE_WARNING_SECONDS * 1000};
          const LIMIT_MS = {IDLE_TIMEOUT_SECONDS * 1000};
          const TARGET = "{SESSION_ENDED_URL}";
          let last = Date.now();
          let banner = null;

          function hideBanner() {{
            if (banner) {{ banner.remove(); banner = null; }}
          }}

          function showBanner(secondsLeft) {{
            if (!banner) {{
              banner = document.createElement("div");
              banner.setAttribute("role", "alert");
              banner.style.cssText = [
                "position:fixed", "left:50%", "bottom:24px", "transform:translateX(-50%)",
                "z-index:999999", "max-width:calc(100% - 32px)",
                "background:{BRAND['card']}", "border:1px solid rgba(91,124,255,0.35)",
                "border-radius:16px", "padding:14px 18px",
                "box-shadow:0 20px 60px rgba(0,0,0,0.45)",
                "color:{BRAND['text']}", "font-size:0.95rem", "line-height:1.4",
                "display:flex", "gap:14px", "align-items:center", "flex-wrap:wrap"
              ].join(";");
              // Montado via DOM: o st.html descarta scripts com tags HTML dentro de strings
              const msg = document.createElement("span");
              const btn = document.createElement("button");
              btn.type = "button";
              btn.textContent = "Continuar";
              btn.style.cssText = [
                "background:linear-gradient(180deg,{BRAND['primary2']},{BRAND['primary']})",
                "color:#fff", "border:0", "border-radius:12px", "padding:8px 14px",
                "font-weight:800", "cursor:pointer"
              ].join(";");
              btn.addEventListener("click", activity);
              banner.append(msg, btn);
              document.body.appendChild(banner);
            }}
            banner.firstChild.textContent =
              "⏳ Sua sessão será encerrada por inatividade em " + secondsLeft + " s.";
          }}

          function activity() {{
            last = Date.now();
            hideBanner();
          }}

          ["mousemove", "mousedown", "keydown", "scroll", "wheel", "touchstart"].forEach(function (ev) {{
            window.addEventListener(ev, activity, {{ passive: true, capture: true }});
          }});

          function check() {{
            const idle = Date.now() - last;
            if (idle >= LIMIT_MS) {{
              clearInterval(timer);
              window.location.replace(TARGET);
            }} else if (idle >= WARN_MS) {{
              showBanner(Math.ceil((LIMIT_MS - idle) / 1000));
            }}
          }}

          const timer = setInterval(check, 1000);
          // aba em segundo plano: timers são desacelerados; checa ao voltar
          document.addEventListener("visibilitychange", check);
        }})();
        </script>
        """,
        unsafe_allow_javascript=True,
    )


def redirect_to_session_ended(reason: str = "inatividade"):
    st.html(
        f'<script>window.location.replace("{SESSION_ENDED_URL}?motivo={reason}");</script>',
        unsafe_allow_javascript=True,
    )
    st.stop()


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

        /* ========= INPUTS (SUPER ROBUSTO) ========= */
        .stApp label {{
            color: rgba(255,255,255,0.72) !important;
            font-weight: 650 !important;
        }}

        .stApp div[data-baseweb="base-input"],
        .stApp div[data-baseweb="input"],
        .stApp div[data-baseweb="textarea"] {{
            background: rgba(255,255,255,0.10) !important;
            border-radius: 12px !important;
        }}

        .stApp div[data-baseweb="base-input"] > div,
        .stApp div[data-baseweb="base-input"] > div > div,
        .stApp div[data-baseweb="input"] > div,
        .stApp div[data-baseweb="input"] > div > div,
        .stApp div[data-baseweb="textarea"] > div,
        .stApp div[data-baseweb="textarea"] > div > div {{
            background: rgba(255,255,255,0.10) !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            border-radius: 12px !important;
        }}

        .stApp input,
        .stApp textarea {{
            background: transparent !important;
            color: rgba(255,255,255,0.92) !important;
            -webkit-text-fill-color: rgba(255,255,255,0.92) !important;
            caret-color: rgba(255,255,255,0.92) !important;
            border: none !important;
            outline: none !important;
        }}

        .stApp input::placeholder,
        .stApp textarea::placeholder {{
            color: rgba(255,255,255,0.45) !important;
            -webkit-text-fill-color: rgba(255,255,255,0.45) !important;
        }}

        /* Autofill do Chrome */
        .stApp input:-webkit-autofill,
        .stApp input:-webkit-autofill:hover,
        .stApp input:-webkit-autofill:focus,
        .stApp textarea:-webkit-autofill,
        .stApp textarea:-webkit-autofill:hover,
        .stApp textarea:-webkit-autofill:focus {{
            -webkit-text-fill-color: rgba(255,255,255,0.92) !important;
            transition: background-color 9999s ease-in-out 0s !important;
            box-shadow: 0 0 0px 1000px rgba(255,255,255,0.10) inset !important;
            border-radius: 12px !important;
        }}

        /* Botões +/- do number input */
        .stApp [data-testid="stNumberInput"] button {{
            background: rgba(255,255,255,0.10) !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            border-radius: 10px !important;
        }}
        .stApp [data-testid="stNumberInput"] button * {{
            color: rgba(255,255,255,0.92) !important;
        }}

        /* Selectbox */
        .stApp [data-baseweb="select"] > div,
        .stApp [data-baseweb="select"] > div > div {{
            background: rgba(255,255,255,0.10) !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            border-radius: 12px !important;
        }}
        .stApp [data-baseweb="select"] * {{
            color: rgba(255,255,255,0.92) !important;
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

        /* ========= Botões (inclui submit do form) ========= */
        .stButton>button,
        [data-testid="stFormSubmitButton"] button {{
          background: linear-gradient(180deg, #7AA2FF, #5B7CFF) !important;
          color: #ffffff !important;
          border-radius: 14px !important;
          padding: 0.70rem 1.00rem !important;
          font-weight: 800 !important;
          border: 0px !important;
          box-shadow: 0 10px 30px rgba(91,124,255,0.18) !important;
        }}

        .stButton>button:hover,
        [data-testid="stFormSubmitButton"] button:hover {{
          filter: brightness(1.05) !important;
          transform: translateY(-1px) !important;
        }}

        .stButton>button:active,
        [data-testid="stFormSubmitButton"] button:active {{
          transform: translateY(0px) !important;
          filter: brightness(0.98) !important;
        }}

        .stButton>button:focus-visible,
        [data-testid="stFormSubmitButton"] button:focus-visible {{
          outline: 2px solid rgba(122,162,255,0.55) !important;
          outline-offset: 2px !important;
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

        # ✅ Mensagem de boas práticas (fechar aba)
        st.markdown(
            f"""
            <div style="
                background: rgba(255,255,255,0.06);
                border: 1px solid {BRAND['border']};
                border-radius: 14px;
                padding: 10px 12px;
                margin: 10px 0 12px 0;
                color: {BRAND['muted']};
                font-size: 0.92rem;
                line-height: 1.35;
            ">
                ✅ Ao finalizar, clique em <b>Sair</b> e <b>feche a aba</b> para encerrar a sessão.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("🚪 Sair", key=f"{key_prefix}_logout"):
            for k in list(st.session_state.keys()):
                st.session_state.pop(k, None)

            # Sai do Streamlit (fecha o websocket) em vez de voltar ao login
            redirect_to_session_ended("logout")



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
