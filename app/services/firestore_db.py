import os
import streamlit as st
from google.cloud import firestore

@st.cache_resource
def get_db() -> firestore.Client:
    project_id = os.environ.get("GCP_PROJECT_ID")
    database_id = os.environ.get("FIRESTORE_DATABASE", "(default)")

    if not project_id:
        raise RuntimeError("GCP_PROJECT_ID não definido no .env")

    # Usa GOOGLE_APPLICATION_CREDENTIALS automaticamente (ADC)
    return firestore.Client(project=project_id, database=database_id)
