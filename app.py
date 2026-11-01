import re
import streamlit as st

st.set_page_config(page_title="Agente", layout="centered")

# Estilo para FILAS fluidas, colores tenues y ajuste perfecto en iPhone
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
    </style>
""", unsafe_allow_html=True)

# Memoria de estado para el historial acumulado
if "historial" not in st.session_state:
    st.session_state.historial = []

# Procesamiento directo de los clicks del teclado en filas
query_params = st.query_params

if "press" in query_params:
    num_pulsado = int(query_params["press"])
    st.session_state.historial.append(num_pulsado)
    st.query_params.clear()
    st.rerun()

if "clear_last" in query_params:
    if len(st.session_state.historial) > 0:
        st.session_state.historial.pop()
    st.query_params.clear()
    st.rerun()

# Extraer números de los campos
def parse_numeros(texto):
    if not texto:
        return set()
    nums = re.findall(r'\b\d+\b', texto)
    return {int(n) for n in nums if 0 <= int(n) <= 36}

# 1. Calientes y Fríos discretos arriba (Desactivado autocompletado de datos personales)
col_cal, col_fri = st.columns(2)
with col_cal:
    in_calientes = st.text_input("Calientes (opcional)", placeholder="Ej: 3, 17...", key="in_cal", autocomplete="off")
with col_fri:
    in_frios = st.text_input("Fríos (opcional)", placeholder="Ej: 0, 12...", key="in_fri", autocomplete="off")

set_calientes = parse_numeros(in_calientes)
set_frios = parse_numeros(in_frios)

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

# 3. Visor del historial acumulativo con botón ⌫ Borrar
if st.session_state.historial:
    texto_registro = " - ".join(map(str, st.session_state.historial))
    st.markdown(f"""
        <div class="registro-container">
            <div class="registro-texto"><b>Reg ({len(st.session_state.historial)}):</b> {texto_registro}</div>
            <a href="?clear_last=1" target="_self" class="btn-del-style">⌫ Borrar</a>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="registro-container" style="color: #999999;">
            <div class="registro-texto">Reg (0): Sin registros</div>
        </div>
    """, unsafe_allow_html=True)

# 4. Teclado en FILAS adaptables con links de accionamiento directo
html_teclado = '<div class="teclado-filas">'

# Botón 0
clase_zero = "btn-zero-fila"
if 0 in set_calientes:
    clase_zero += " btn-caliente"
elif 0 in set_frios:
    clase_zero += " btn-frio"

html_teclado += f'<a href="?press=0" target="_self" class="{clase_zero}">0</a>'

# Botones 1 al 36 en filas
for n in range(1, 37):
    clase_btn = "btn-num-fila"
    if n in set_calientes:
        clase_btn += " btn-caliente"
    elif n in set_frios:
        clase_btn += " btn-frio"
    
    html_teclado += f'<a href="?press={n}" target="_self" class="{clase_btn}">{n}</a>'

html_teclado += '</div>'

st.markdown(html_teclado, unsafe_allow_html=True)
