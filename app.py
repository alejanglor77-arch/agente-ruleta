import streamlit as st

st.set_page_config(page_title="Agente", layout="centered")

# CSS para disposición fluida en fila ultra compacta
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 0.3rem !important;
        padding-bottom: 0.3rem !important;
        padding-left: 0.3rem !important;
        padding-right: 0.3rem !important;
    }
    
    /* Inputs de Calientes y Fríos súper discretos */
    div[data-testid="stTextInput"] {
        margin-bottom: 2px !important;
    }
    div[data-testid="stTextInput"] input {
        height: 26px !important;
        padding: 2px 4px !important;
        font-size: 11px !important;
    }
    div[data-testid="stTextInput"] label {
        font-size: 10px !important;
        margin-bottom: 0px !important;
        color: #777777 !important;
    }

    /* Tarjetas sobrias para Grupo A y B */
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
        letter-spacing: 0.5px;
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

    /* Visor de registro con botón de borrar */
    .registro-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #f4f4f5;
        border: 1px solid #e4e4e7;
        border-radius: 5px;
        padding: 4px 8px;
        margin-bottom: 6px;
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

    /* Teclado en modo FILA fluida y compacta */
    .teclado-filas {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
        justify-content: center;
        width: 100%;
        margin-top: 4px;
    }
    .btn-num-fila {
        flex: 1 0 18%; /* Permite 4-5 botones por fila según la pantalla */
        max-width: 23%;
        height: 32px;
        background-color: #ffffff;
        border: 1px solid #dcdcdc;
        border-radius: 5px;
        color: #333333;
        font-weight: 600;
        font-size: 13px;
        text-align: center;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
    }
    .btn-zero-fila {
        flex: 1 0 100%;
        max-width: 100%;
        height: 32px;
        background-color: #f4f4f5;
        border: 1px solid #dcdcdc;
        border-radius: 5px;
        color: #18181b;
        font-weight: 700;
        font-size: 14px;
        text-align: center;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2px;
        box-sizing: border-box;
    }
    </style>
""", unsafe_allow_html=True)

# Estado persistente del historial
if "historial" not in st.session_state:
    st.session_state.historial = []

# Procesamiento de clicks rápido desde el teclado en fila
query_params = st.query_params

if "num" in query_params:
    val = int(query_params["num"])
    st.session_state.historial.append(val)
    st.query_params.clear()
    st.rerun()

if "del" in query_params:
    if len(st.session_state.historial) > 0:
        st.session_state.historial.pop()
    st.query_params.clear()
    st.rerun()

# 1. Calientes y Fríos discretos arriba
col_cal, col_fri = st.columns(2)
with col_cal:
    st.text_input("Calientes (opcional)", placeholder="Ej: 3, 17...", key="in_cal")
with col_fri:
    st.text_input("Fríos (opcional)", placeholder="Ej: 0, 12...", key="in_fri")

# 2. Recomendación principal (Grupo A y Grupo B)
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

# 3. Visor de registro acumulativo + Botón ⌫ Borrar
if st.session_state.historial:
    texto_registro = " - ".join(map(str, st.session_state.historial))
    st.markdown(f"""
        <div class="registro-container">
            <div class="registro-texto"><b>Reg ({len(st.session_state.historial)}):</b> {texto_registro}</div>
            <a href="?del=1" target="_self" style="text-decoration:none; color:#333; font-weight:bold; background:#e4e4e7; padding:2px 6px; border-radius:4px; border:1px solid #d4d4d8;">⌫ Borrar</a>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="registro-container" style="color: #999999;">
            <div class="registro-texto">Reg (0): Sin registros</div>
        </div>
    """, unsafe_allow_html=True)

# 4. Teclado compacto organizado por filas adaptables
html_teclado = '<div class="teclado-filas">'
html_teclado += '<a href="?num=0" target="_self" class="btn-zero-fila">0</a>'

for n in range(1, 37):
    html_teclado += f'<a href="?num={n}" target="_self" class="btn-num-fila">{n}</a>'

html_teclado += '</div>'

st.markdown(html_teclado, unsafe_allow_html=True)
