import os
import requests
import streamlit as st
import firebase_admin
from firebase_admin import auth as fb_auth
from firebase_admin import credentials

@st.cache_resource
def init_firebase_admin():
    # Usa GOOGLE_APPLICATION_CREDENTIALS (ADC) — no seu caso já está OK
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    return True

def sign_in_with_password(email: str, password: str) -> dict:
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise RuntimeError("FIREBASE_WEB_API_KEY não definido no .env")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=payload, timeout=15)

    data = r.json()
    if r.status_code != 200:
        # mensagem legível
        msg = data.get("error", {}).get("message", "Erro ao autenticar")
        raise ValueError(msg)

    return data  # contém idToken, refreshToken, localId (uid), email...

def verify_id_token(id_token: str) -> dict:
    init_firebase_admin()
    return fb_auth.verify_id_token(id_token)

def sign_up_with_password(email: str, password: str) -> dict:
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise RuntimeError("FIREBASE_WEB_API_KEY não definido no .env")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=payload, timeout=15)

    data = r.json()
    if r.status_code != 200:
        msg = data.get("error", {}).get("message", "Erro ao criar conta")
        raise ValueError(msg)

    return data
