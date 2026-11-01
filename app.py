import streamlit as st

st.set_page_config(page_title="Agente", layout="centered")

# Estilo compacto para encajar 4 columnas en iPhone 12 sin desplazamiento
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 0.4rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.3rem !important;
        padding-right: 0.3rem !important;
    }
    .card-discreta {
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        padding: 5px;
        text-align: center;
        color: #4a4a4a;
        margin-bottom: 4px;
    }
    .card-titulo {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #888888;
        margin-bottom: 1px;
    }
    .card-valores-fuerte {
        font-size: 15px;
        font-weight: 800;
        color: #1a1a1a;
    }
    .card-valores-suave {
        font-size: 14px;
        font-weight: 400;
        color: #555555;
    }
    .registro-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #f4f4f5;
        border: 1px solid #e4e4e7;
        border-radius: 5px;
        padding: 4px 6px;
        margin-bottom: 4px;
        font-size: 11px;
        color: #18181b;
        font-family: monospace;
        min-height: 26px;
    }
    .registro-texto {
        overflow-x: auto;
        white-space: nowrap;
        margin-right: 6px;
    }
    /* Reducción de separaciones para encajar 4 columnas en el ancho del teléfono */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
    }
    div[data-testid="column"] {
        width: 100% !important;
        min-width: 0px !important;
        flex: 1 1 0px !important;
        padding: 0px !important;
    }
    div.stButton > button {
        width: 100% !important;
        height: 30px !important;
        padding: 0px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dcdcdc !important;
        border-radius: 4px !important;
        margin: 0px !important;
    }
    div[data-testid="stTextInput"] input {
        height: 28px !important;
        padding: 2px 6px !important;
        font-size: 11px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Estado inicial
if "historial" not in st.session_state:
    st.session_state.historial = []

# Cajetines opcionales para números calientes y fríos de la ruleta
col_cal, col_fri = st.columns(2)
with col_cal:
    calientes = st.text_input("Calientes (opcional)", placeholder="Ej: 3, 17, 25", key="in_cal")
with col_fri:
    frios = st.text_input("Fríos (opcional)", placeholder="Ej: 0, 12, 30", key="in_fri")

# Tarjetas superiores de recomendaciones
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

# Visor de historial y botón de borrado
col_reg, col_del = st.columns([0.72, 0.28])

with col_reg:
    if st.session_state.historial:
        texto_registro = " - ".join(map(str, st.session_state.historial))
        st.markdown(f'<div class="registro-container"><div class="registro-texto"><b>Reg ({len(st.session_state.historial)}):</b> {texto_registro}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="registro-container" style="color: #999999;"><div class="registro-texto">Reg (0): Sin registros</div></div>', unsafe_allow_html=True)

with col_del:
    if st.button("⌫ Borrar", key="btn_del"):
        if len(st.session_state.historial) > 0:
            st.session_state.historial.pop()
            st.rerun()

# Botón Cero arriba
if st.button("0", key="btn_0", use_container_width=True):
    st.session_state.historial.append(0)
    st.rerun()

# Teclado ajustado a 4 columnas compactas en iPhone 12
for fila in range(0, 9):
    cols = st.columns(4)
    for col_idx in range(4):
        num = fila * 4 + col_idx + 1
        if num <= 36:
            with cols[col_idx]:
                if st.button(str(num), key=f"btn_{num}"):
                    st.session_state.historial.append(num)
                    st.rerun()
