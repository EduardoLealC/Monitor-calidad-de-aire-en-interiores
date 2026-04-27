import streamlit as st
from pages import dashboard

st.set_page_config(
    page_title="Monitor de Aire",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",   # colapsa la sidebar
)

# Oculta completamente la sidebar y el botón de navegación
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)

dashboard.render()