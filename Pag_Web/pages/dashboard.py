# Instalar si no tienes: pip install streamlit-autorefresh
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from data.influx import get_latest_values
from component.kpi_card import render_kpi_cards
from config import PARAMS

def render():
    st.title("Monitor de Calidad de Aire")
    st.caption("Laboratorio Mancera — actualización cada 30 s")

    st_autorefresh(interval=30_000)

    # Leer selección desde query params
    qp = st.query_params
    if "kpi" in qp:
        val = qp["kpi"]
        st.session_state["selected_kpi"] = None if val == "none" else val

    with st.spinner("Consultando sensores..."):
        data = get_latest_values()

    render_kpi_cards(data, PARAMS)
    st.divider()

    st.subheader("Visualización completa")
    grafana_url = "http://localhost:3000/public-dashboards/37fd3b15f7fa444f9a7162119265a78c"
    st.components.v1.iframe(grafana_url, height=800)