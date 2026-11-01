import streamlit as st

st.set_page_config(page_title="Agente", layout="centered")

# Estilo ultra compacto para evitar todo scroll en iPhone 12
st.markdown("""
    <style>
    /* Ocultar elementos sobrantes de la interfaz de Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    
    /* Tarjetas superiores sobrias y compactas */
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
    
    /* Visor de registro ultracompacto */
    .registro-box {
        background-color: #f4f4f5;
        border-radius: 5px;
        padding: 4px 8px;
        font-size: 11px;
        color: #333333;
        margin-bottom: 6px;
        font-family: monospace;
    }
    
    /* Teclado numérico ajustado a la pantalla de móvil */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 3px;
        width: 100%;
        box-sizing: border-box;
    }
    .btn-zero {
        grid-column: span 4;
        background-color: #ffffff;
        border: 1px solid #dcdcdc;
        color: #333333;
        padding: 5px 0;
        text-align: center;
        font-weight: 600;
        font-size: 13px;
        border-radius: 4px;
        text-decoration: none;
        display: block;
        margin-bottom: 3px;
    }
    .btn-num {
        background-color: #ffffff;
        border: 1px solid #dcdcdc;
        color: #333333;
        padding: 5px 0;
        text-align: center;
        font-weight: 600;
        font-size: 13px;
        border-radius: 4px;
        text-decoration: none;
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# Estado inicial del historial
if "historial" not in st.session_state:
    st.session_state.historial = []

# Captura de pulsaciones desde el teclado HTML
query_params = st.query_params
if "add_num" in query_params:
    num_pulsado = int(query_params["add_num"])
    st.session_state.historial.append(num_pulsado)
    st.query_params.clear()
    st.rerun()

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

# Generación del Teclado Rígido HTML Ultra Compacto
html_teclado = '<a href="?add_num=0" target="_self" class="btn-zero">0</a><div class="grid-container">'

for n in range(1, 37):
    html_teclado += f'<a href="?add_num={n}" target="_self" class="btn-num">{n}</a>'

html_teclado += "</div>"

st.markdown(html_teclado, unsafe_allow_html=True)
