import streamlit as st

st.set_page_config(page_title="Agente", layout="centered")

# CSS para forzar el teclado matricial perfecto en iPhone
st.markdown("""
    <style>
    .card-discreta {
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        color: #4a4a4a;
        margin-bottom: 8px;
    }
    .card-titulo {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #888888;
        margin-bottom: 2px;
    }
    .card-valores-fuerte {
        font-size: 18px;
        font-weight: 800;
        color: #1a1a1a;
    }
    .card-valores-suave {
        font-size: 16px;
        font-weight: 400;
        color: #555555;
    }
    .registro-box {
        background-color: #f4f4f5;
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 12px;
        color: #333333;
        margin-bottom: 10px;
        font-family: monospace;
    }
    /* Estructura fija de teclado para móvil */
    .grid-teclado {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 4px;
        width: 100%;
        margin-top: 5px;
    }
    /* Redefinición estricta de botones de Streamlit */
    div.element-container:has(button) {
        margin: 0 !important;
        padding: 0 !important;
    }
    div.stButton > button {
        width: 100% !important;
        height: 38px !important;
        padding: 0px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dcdcdc !important;
        border-radius: 4px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Estado inicial del historial
if "historial" not in st.session_state:
    st.session_state.historial = []

# Tarjetas superiores sobrias
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
        <div class="card-discreta">
            <div class="card-titulo">Grupo A</div>
            <div class="card-valores-fuerte">3, 20, 35</div>
        </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
        <div class="card-discreta">
            <div class="card-titulo">Grupo B</div>
            <div class="card-valores-suave">9, 22, 31</div>
        </div>
    """, unsafe_allow_html=True)

# Visor de registro en tiempo real
if st.session_state.historial:
    ultimos = st.session_state.historial[-20:]
    texto_registro = " - ".join(map(str, ultimos))
    st.markdown(f"""
        <div class="registro-box">
            <b>Reg ({len(st.session_state.historial)}):</b> {texto_registro}
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="registro-box" style="color: #999999;">
            Reg (0): Sin registros
        </div>
    """, unsafe_allow_html=True)

# Botón Cero arriba
if st.button("0", use_container_width=True):
    st.session_state.historial.append(0)

# Teclado compacto ordenado (1 al 36) en 4 columnas estrictas
cols = st.columns(4)
for num in range(1, 37):
    col_idx = (num - 1) % 4
    with cols[col_idx]:
        if st.button(str(num), key=f"num_{num}"):
            st.session_state.historial.append(num)
