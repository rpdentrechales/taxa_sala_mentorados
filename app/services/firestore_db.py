import os
import streamlit as st
from google.cloud import firestore
import google.auth

@st.cache_resource
def get_db() -> firestore.Client:
    project_id = os.environ.get("GCP_PROJECT_ID")
    database_id = os.environ.get("FIRESTORE_DATABASE", "(default)")

    # ✅ Em Cloud Run (ADC), dá pra descobrir o project automaticamente
    if not project_id:
        _, project_id = google.auth.default()

    if not project_id:
        raise RuntimeError("Não foi possível resolver o Project ID (defina GCP_PROJECT_ID).")

    return firestore.Client(project=project_id, database=database_id)
