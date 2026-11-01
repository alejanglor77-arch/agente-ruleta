import streamlit as st

st.set_page_config(page_title="Agente", layout="centered")

# Estilo discreto sin colores llamativos
st.markdown("""
    <style>
    /* Estilo tenue para las tarjetas */
    .card-discreta {
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        color: #4a4a4a;
        margin-bottom: 10px;
    }
    .card-titulo {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #888888;
        margin-bottom: 4px;
    }
    .card-valores-fuerte {
        font-size: 19px;
        font-weight: 800;
        color: #1a1a1a;
    }
    .card-valores-suave {
        font-size: 17px;
        font-weight: 400;
        color: #555555;
    }
    /* Estilo para la lista de registro comprobante */
    .registro-box {
        background-color: #f4f4f5;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 13px;
        color: #333333;
        margin-bottom: 15px;
        font-family: monospace;
    }
    /* Botones compactos y neutros */
    div.stButton > button {
        width: 100%;
        padding: 8px 0px;
        font-size: 15px;
        font-weight: 500;
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #dcdcdc;
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

# MUESTRA DE REGISTRO EN TIEMPO REAL (Justo antes del teclado)
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

st.divider()

# Botón Cero arriba
if st.button("0", use_container_width=True):
    st.session_state.historial.append(0)

# Teclado compacto ordenado (1 al 36) en 4 columnas
cols = st.columns(4)
for num in range(1, 37):
    col_idx = (num - 1) % 4
    with cols[col_idx]:
        if st.button(str(num), key=f"num_{num}"):
            st.session_state.historial.append(num)
