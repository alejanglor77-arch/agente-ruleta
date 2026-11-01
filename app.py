import streamlit as st

st.set_page_config(page_title="Agente", layout="centered")

# Estilo para FILAS fluidas, selector táctil y teclado integrado
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

    /* Tarjetas de Calientes y Fríos visuales (llenadas desde tu teclado) */
    .cajetin-visual {
        background-color: #f4f4f5;
        border: 1px solid #d4d4d8;
        border-radius: 5px;
        padding: 4px 6px;
        font-size: 11px;
        color: #18181b;
        font-family: monospace;
        min-height: 24px;
        margin-bottom: 4px;
    }
    .cajetin-label {
        font-size: 9px;
        text-transform: uppercase;
        color: #71717a;
        font-weight: bold;
        margin-bottom: 2px;
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

    /* Teclado en FILAS fluidas */
    .teclado-filas {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
        justify-content: center;
        width: 100%;
        margin-top: 4px;
    }
    .btn-num-fila {
        flex: 1 0 18%;
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
        background-color: #ffffff;
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

    /* Resaltados de color tenue */
    .btn-caliente {
        background-color: #fff3e0 !important;
        border: 1px solid #ffe0b2 !important;
        color: #8c4a00 !important;
    }
    .btn-frio {
        background-color: #e3f2fd !important;
        border: 1px solid #bbdefb !important;
        color: #0d47a1 !important;
    }
    
    .btn-del-style {
        background: #e4e4e7;
        color: #333;
        font-weight: bold;
        border: 1px solid #d4d4d8;
        padding: 2px 6px;
        border-radius: 4px;
        text-decoration: none;
        font-size: 11px;
    }

    /* Ajuste de radio botones nativos de selección rápida */
    div[data-testid="stRadio"] > div {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-around !important;
        background-color: #f4f4f5;
        border-radius: 6px;
        padding: 2px;
        margin-bottom: 4px;
    }
    div[data-testid="stRadio"] label {
        font-size: 11px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# Estado persistente para Historial, Calientes y Fríos
if "historial" not in st.session_state:
    st.session_state.historial = []
if "calientes" not in st.session_state:
    st.session_state.calientes = []
if "frios" not in st.session_state:
    st.session_state.frios = []

# Procesamiento de entradas del teclado según el modo activo
query_params = st.query_params

if "press" in query_params:
    num_pulsado = int(query_params["press"])
    modo_actual = query_params.get("modo", "🎲 Registro")
    
    if modo_actual == "🔥 Calientes":
        if num_pulsado not in st.session_state.calientes and len(st.session_state.calientes) < 5:
            st.session_state.calientes.append(num_pulsado)
    elif modo_actual == "❄️ Fríos":
        if num_pulsado not in st.session_state.frios and len(st.session_state.frios) < 5:
            st.session_state.frios.append(num_pulsado)
    else:  # Registro de partida
        st.session_state.historial.append(num_pulsado)
        
    st.query_params.clear()
    st.rerun()

if "clear_act" in query_params:
    modo_actual = query_params.get("modo", "🎲 Registro")
    if modo_actual == "🔥 Calientes":
        if st.session_state.calientes:
            st.session_state.calientes.pop()
    elif modo_actual == "❄️ Fríos":
        if st.session_state.frios:
            st.session_state.frios.pop()
    else:
        if st.session_state.historial:
            st.session_state.historial.pop()
            
    st.query_params.clear()
    st.rerun()

# 1. Selector de Destino del Teclado (Sin usar teclado del móvil)
modo = st.radio("Destino de las pulsaciones:", ["🎲 Registro", "🔥 Calientes", "❄️ Fríos"], horizontal=True, label_visibility="collapsed")

# 2. Visor de Calientes y Fríos (Llenados con tu teclado)
col_cal_v, col_fri_v = st.columns(2)

with col_cal_v:
    txt_cal = ", ".join(map(str, st.session_state.calientes)) if st.session_state.calientes else "Ninguno"
    st.markdown(f'<div class="cajetin-visual"><div class="cajetin-label">Calientes ({len(st.session_state.calientes)}/5)</div><b>{txt_cal}</b></div>', unsafe_allow_html=True)

with col_fri_v:
    txt_fri = ", ".join(map(str, st.session_state.frios)) if st.session_state.frios else "Ninguno"
    st.markdown(f'<div class="cajetin-visual"><div class="cajetin-label">Fríos ({len(st.session_state.frios)}/5)</div><b>{txt_fri}</b></div>', unsafe_allow_html=True)

# 3. Recomendación principal (Grupo A y Grupo B)
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

# 4. Visor de registro acumulativo continuo
if st.session_state.historial:
    texto_registro = " - ".join(map(str, st.session_state.historial))
    st.markdown(f"""
        <div class="registro-container">
            <div class="registro-texto"><b>Reg ({len(st.session_state.historial)}):</b> {texto_registro}</div>
            <a href="?clear_act=1&modo={modo}" target="_self" class="btn-del-style">⌫ Borrar</a>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="registro-container" style="color: #999999;">
            <div class="registro-texto">Reg (0): Sin registros</div>
            <a href="?clear_act=1&modo={modo}" target="_self" class="btn-del-style">⌫ Borrar</a>
        </div>
    """, unsafe_allow_html=True)

# 5. Teclado en FILAS adaptables con direccionamiento y colores tenues
html_teclado = '<div class="teclado-filas">'

# Botón 0
clase_zero = "btn-zero-fila"
if 0 in st.session_state.calientes:
    clase_zero += " btn-caliente"
elif 0 in st.session_state.frios:
    clase_zero += " btn-frio"

html_teclado += f'<a href="?press=0&modo={modo}" target="_self" class="{clase_zero}">0</a>'

# Botones 1 al 36
for n in range(1, 37):
    clase_btn = "btn-num-fila"
    if n in st.session_state.calientes:
        clase_btn += " btn-caliente"
    elif n in st.session_state.frios:
        clase_btn += " btn-frio"
    
    html_teclado += f'<a href="?press={n}&modo={modo}" target="_self" class="{clase_btn}">{n}</a>'

html_teclado += '</div>'

st.markdown(html_teclado, unsafe_allow_html=True)
