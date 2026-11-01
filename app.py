import streamlit as st

st.set_page_config(page_title="Agente", layout="centered")

# Ocultar cabeceras y definir la cuadrícula CSS indestructible
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
    .registro-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
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
    .registro-texto {
        overflow-x: auto;
        white-space: nowrap;
        margin-right: 8px;
    }
    
    /* Cuadrícula fija de 4 columnas en HTML */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 3px;
        width: 100%;
        box-sizing: border-box;
    }
    .btn-kbd {
        background-color: #ffffff;
        border: 1px solid #dcdcdc;
        color: #333333;
        padding: 6px 0;
        text-align: center;
        font-weight: 600;
        font-size: 13px;
        border-radius: 4px;
        cursor: pointer;
        width: 100%;
        box-sizing: border-box;
    }
    .btn-kbd:active {
        background-color: #e4e4e7;
    }
    .btn-zero {
        grid-column: span 4;
        margin-bottom: 3px;
    }
    .btn-undo-style {
        background-color: #e4e4e7;
        border: 1px solid #d4d4d8;
        color: #333333;
        padding: 2px 8px;
        font-size: 11px;
        font-weight: bold;
        border-radius: 4px;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Estado persistente del historial
if "historial" not in st.session_state:
    st.session_state.historial = []

# Procesar acciones recibidas mediante parámetros URL sin resetear el estado
query_params = st.query_params

if "val" in query_params:
    num_pulsado = int(query_params["val"])
    st.session_state.historial.append(num_pulsado)
    st.query_params.clear()
    st.rerun()

if "act" in query_params and query_params["act"] == "undo":
    if len(st.session_state.historial) > 0:
        st.session_state.historial.pop()
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

# Visor de registro con avance continuo y botón de borrado
if st.session_state.historial:
    texto_registro = " - ".join(map(str, st.session_state.historial))
    st.markdown(f"""
        <div class="registro-container">
            <div class="registro-texto"><b>Reg ({len(st.session_state.historial)}):</b> {texto_registro}</div>
            <a href="?act=undo" target="_self" style="text-decoration:none;"><button class="btn-undo-style">⌫ Borrar</button></a>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="registro-container" style="color: #999999;">
            <div class="registro-texto">Reg (0): Sin registros</div>
        </div>
    """, unsafe_allow_html=True)

# Teclado en HTML puro para forzar las 4 columnas en iPhone 12 sin desordenar
html_teclado = '<a href="?val=0" target="_self" style="text-decoration:none;"><button class="btn-kbd btn-zero">0</button></a><div class="grid-container">'

for n in range(1, 37):
    html_teclado += f'<a href="?val={n}" target="_self" style="text-decoration:none;"><button class="btn-kbd">{n}</button></a>'

html_teclado += "</div>"

st.markdown(html_teclado, unsafe_allow_html=True)
