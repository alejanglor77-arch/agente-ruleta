import streamlit as st

st.set_page_config(page_title="Agente", layout="centered")

# CSS para compactar botones nativos y evitar scroll en móvil
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    .card-discreta {
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        padding: 6px;
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
        font-size: 16px;
        font-weight: 800;
        color: #1a1a1a;
    }
    .card-valores-suave {
        font-size: 15px;
        font-weight: 400;
        color: #555555;
    }
    .registro-box {
        background-color: #f4f4f5;
        border: 1px solid #e4e4e7;
        border-radius: 5px;
        padding: 5px 8px;
        margin-bottom: 6px;
        font-size: 12px;
        color: #18181b;
        font-family: monospace;
        min-height: 28px;
    }
    /* Fuerza botones ultracompactos en la cuadrícula */
    div.stButton > button {
        width: 100% !important;
        height: 32px !important;
        padding: 0px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dcdcdc !important;
        border-radius: 4px !important;
        margin: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Estado persistente del historial
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

# Visor de registro e icono de borrado integrado
col_reg, col_del = st.columns([0.8, 0.2])

with col_reg:
    if st.session_state.historial:
        texto_registro = " - ".join(map(str, st.session_state.historial))
        st.markdown(f'<div class="registro-box"><b>Reg ({len(st.session_state.historial)}):</b> {texto_registro}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="registro-box" style="color: #999999;">Reg (0): Sin registros</div>', unsafe_allow_html=True)

with col_del:
    if st.button("⌫"):
        if len(st.session_state.historial) > 0:
            st.session_state.historial.pop()
            st.rerun()

# Botón Cero
if st.button("0", use_container_width=True):
    st.session_state.historial.append(0)
    st.rerun()

# Teclado matricial rígido (1 al 36)
cols = st.columns(4)
for num in range(1, 37):
    col_idx = (num - 1) % 4
    with cols[col_idx]:
        if st.button(str(num), key=f"btn_{num}"):
            st.session_state.historial.append(num)
            st.rerun()
