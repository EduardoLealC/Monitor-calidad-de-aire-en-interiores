import streamlit as st
import streamlit.components.v1 as components
import json
import math


def _build_params_js(data: dict, params: dict) -> str:
    fields = list(params.keys())
    payload = {
        f: {
            "label":     params[f]["label"],
            "unit":      params[f]["unit"],
            "oms":       params[f]["oms"],
            "epa":       params[f]["epa"],
            "desc":      params[f]["description"],
            "tips":      params[f]["tips"],
            "value":     data.get(f),
            "alertLow":  params[f].get("alert_low"),
            "alertHigh": params[f].get("alert_high"),
        }
        for f in fields
    }
    return json.dumps(payload)


def render_kpi_cards(data: dict, params: dict):
    params_js = _build_params_js(data, params)
    n_rows = math.ceil(len(params) / 4)
    total_h = n_rows * 170 + 260

    html = f"""
    <style>
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        font-family: system-ui, sans-serif;
    }}

    body {{
        background: transparent;
    }}

    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 10px;
        padding: 4px 2px;
    }}

    .kpi-card {{
        background: #1e1e1e;
        border-radius: 12px;
        padding: 16px 14px;
        cursor: pointer;
        transition: 0.15s;
        border-left: 3px solid rgba(255,255,255,0.1);
    }}

    .kpi-card:hover {{
        background: #252525;
    }}

    .kpi-card.alert {{
        border-left-color: #E24B4A;
    }}

    .kpi-card.ok {{
        border-left-color: #1D9E75;
    }}

    .kpi-card.nodata {{
        opacity: 0.5;
        cursor: default;
    }}

    .kpi-label {{
        font-size: 11px;
        color: #888;
        margin-bottom: 10px;
    }}

    .kpi-value {{
        font-size: 20px;
        color: #fff;
        margin-bottom: 8px;
    }}

    .kpi-unit {{
        font-size: 12px;
        color: #666;
    }}

    .kpi-badge {{
        display: inline-flex;
        font-size: 11px;
        padding: 3px 8px;
        border-radius: 999px;
    }}

    .kpi-badge.alert {{
        background: #2a1111;
        color: #e87878;
    }}

    .kpi-badge.ok {{
        background: #0e2418;
        color: #5cc98a;
    }}

    .kpi-badge.nodata {{
        background: #222;
        color: #666;
    }}

    /* MODAL */
    .modal {{
        display: none;
        position: fixed;
        z-index: 999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.65);
        backdrop-filter: blur(3px);
    }}

    .modal.show {{
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .modal-content {{
        width: 520px;
        max-width: 92%;
        background: #1e1e1e;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
        padding: 18px;
        animation: pop 0.15s ease-out;
    }}

    @keyframes pop {{
        from {{ transform: scale(0.96); opacity: 0; }}
        to {{ transform: scale(1); opacity: 1; }}
    }}

    .detail-header {{
        display:flex;
        justify-content:space-between;
        margin-bottom:12px;
    }}

    .detail-title {{
        color:#fff;
        font-size:14px;
        font-weight:500;
    }}

    .detail-close {{
        color:#888;
        cursor:pointer;
        font-size:12px;
    }}

    .detail-close:hover {{
        color:#ccc;
    }}

    .detail-body {{
        display:grid;
        gap:10px;
    }}

    .detail-info {{
        background:#252525;
        padding:12px;
        border-radius:10px;
    }}

    .detail-info-label {{
        font-size:11px;
        color:#666;
        margin-bottom:4px;
    }}

    .detail-info-val {{
        font-size:13px;
        color:#ccc;
    }}

    .tips {{
        margin-top:10px;
    }}

    .tips li {{
        font-size:12px;
        color:#888;
        margin-top:6px;
        list-style:none;
    }}

    </style>

    <div class="kpi-grid" id="grid"></div>

    <div class="modal" id="modal">
        <div class="modal-content" id="modal-content"></div>
    </div>

    <script>
    const PARAMS = {params_js};

    function getStatus(p) {{
        if (p.value == null) return "nodata";
        if (p.alertLow != null && p.value < p.alertLow) return "alert";
        if (p.alertHigh != null && p.value > p.alertHigh) return "alert";
        return "ok";
    }}

    function formatValue(p) {{
        if (p.value == null) return "—";
        return p.value.toFixed ? p.value.toFixed(1) + " " + p.unit : p.value + " " + p.unit;
    }}

    function openModal(field) {{
        const p = PARAMS[field];

        document.getElementById("modal-content").innerHTML =
            '<div class="detail-header">' +
                '<div class="detail-title">' + p.label + '</div>' +
                '<div class="detail-close" onclick="closeModal()">Cerrar</div>' +
            '</div>' +
            '<div class="detail-body">' +
                '<div class="detail-info">' +
                    '<div class="detail-info-label">Descripción</div>' +
                    '<div class="detail-info-val">' + p.desc + '</div>' +
                '</div>' +
                '<div class="detail-info">' +
                    '<div class="detail-info-label">Umbral OMS</div>' +
                    '<div class="detail-info-val">' + p.oms + '</div>' +
                '</div>' +
                '<div class="detail-info">' +
                    '<div class="detail-info-label">Umbral EPA</div>' +
                    '<div class="detail-info-val">' + p.epa + '</div>' +
                '</div>' +
            '</div>';

        document.getElementById("modal").classList.add("show");
    }}

    function closeModal() {{
        document.getElementById("modal").classList.remove("show");
    }}

    function render() {{
        const grid = document.getElementById("grid");
        grid.innerHTML = "";

        Object.keys(PARAMS).forEach(f => {{
            const p = PARAMS[f];
            const status = getStatus(p);

            const card = document.createElement("div");
            card.className = "kpi-card " + status;

            if (status !== "nodata") {{
                card.onclick = () => openModal(f);
            }}

            card.innerHTML =
                '<div class="kpi-label">' + p.label + '</div>' +
                '<div class="kpi-value">' + formatValue(p) + '</div>' +
                '<div class="kpi-badge ' + status + '">' + status.toUpperCase() + '</div>';

            grid.appendChild(card);
        }});
    }}

    render();
    </script>
    """

    components.html(html, height=total_h, scrolling=False)