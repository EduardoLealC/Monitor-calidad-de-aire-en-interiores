import streamlit as st
from config import PARAMS

def render_kpi_detail():
    field = st.session_state.get("selected_kpi")
    if not field:
        return

    p = PARAMS[field]

    with st.expander(f"Detalle: {p['label']}  —  haz clic para cerrar", expanded=True):
        st.markdown(f"### {p['label']} `({p['unit']})`")
        st.markdown("**Descripción**")
        st.info(p["description"])

        col1, col2 = st.columns(2)
        col1.markdown(f"**OMS (2021):** {p['oms']}")
        col2.markdown(f"**🇺🇸 EPA:** {p['epa']}")

        low  = p.get("alert_low")
        high = p.get("alert_high")
        rango_str = (
            f"{low} – {high} {p['unit']}" if low and high
            else f"< {high} {p['unit']}" if high
            else f"> {low} {p['unit']}" if low
            else "—"
        )
        st.markdown(f"**Umbral de alerta:** `{rango_str}`")

        st.markdown("**Recomendaciones para mejorar:**")
        for tip in p["tips"]:
            st.markdown(f"- {tip}")

        if st.button("✖ Cerrar", key="close_detail"):
            st.session_state["selected_kpi"] = None
            st.rerun()