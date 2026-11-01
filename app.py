import streamlit as st

st.set_page_config(page_title="Agente", layout="centered")

# Inyección de Viewport y CSS para ajustar la pantalla completa en móviles
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Contenedor principal sin márgenes que generen desplazamiento */
    .block-container {
        padding-top: 0.3rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.2rem !important;
        padding-right: 0.2rem !important;
        max-width: 100% !important;
    }
    
    /* Tarjetas y cajetines compactos */
    .card-discreta {
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        padding: 4px;
        text-align: center;
        color: #4a4a4a;
        margin-bottom: 3px;
    }
    .card-titulo {
        font-size: 9px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #888888;
        margin-bottom: 1px;
    }
    .card-valores-fuerte {
        font-size: 14px;
        font-weight: 800;
        color: #1a1a1a;
    }
    .card-valores-suave {
        font-size: 13px;
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
        padding: 3px 5px;
        margin-bottom: 3px;
        font-size: 11px;
        color: #18181b;
        font-family: monospace;
        min-height: 24px;
    }
    .registro-texto {
        overflow-x: auto;
        white-space: nowrap;
        margin-right: 4px;
    }

    /* Regla rígida de 4 columnas distribuidas proporcionalmente dentro del ancho del teléfono */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
        width: 100% !important;
    }
    div[data-testid="column"] {
        flex: 1 1 0px !important;
        min-width: 0px !important;
        padding: 0px !important;
    }
    
    /* Botones ajustados al ancho estricto de cada columna */
    div.stButton > button {
        width: 100% !important;
        height: 28px !important;
        padding: 0px !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dcdcdc !important;
        border-radius: 4px !important;
        margin: 0px !important;
    }
    
    /* Inputs de calientes y fríos ultra compactos */
    div[data-testid="stTextInput"] input {
        height: 26px !important;
        padding: 2px 4px !important;
        font-size: 10px !important;
    }
    div[data-testid="stTextInput"] label {
        font-size: 10px !important;
        margin-bottom: 0px !important;
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

# Teclado en 4 columnas encajadas proporcionalmente
for fila in range(0, 9):
    cols = st.columns(4)
    for col_idx in range(4):
        num = fila * 4 + col_idx + 1
        if num <= 36:
            with cols[col_idx]:
                if st.button(str(num), key=f"btn_{num}"):
                    st.session_state.historial.append(num)
                    st.rerun()
