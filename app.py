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

    /* Teclado en FILAS fluidas (manteniendo la estructura exacta que funcionaba) */
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
        display: flex;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
        cursor: pointer;
        user-select: none;
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
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2px;
        box-sizing: border-box;
        cursor: pointer;
        user-select: none;
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
        padding: 2px 8px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 11px;
    }
    </style>

    <script>
    function pressNum(val) {
        const url = new URL(window.location.href);
        url.searchParams.set('add_val', val);
        window.location.href = url.toString();
    }
    function pressDel() {
        const url = new URL(window.location.href);
        url.searchParams.set('del_act', '1');
        window.location.href = url.toString();
    }
    </script>
""", unsafe_allow_html=True)

# Estado interno persistente para acumular la secuencia completa
if "historial" not in st.session_state:
    st.session_state.historial = []

# Procesar capturas de pulsación manteniendo el historial intacto
query_params = st.query_params

if "add_val" in query_params:
    st.session_state.historial.append(int(query_params["add_val"]))
    st.query_params.clear()
    st.rerun()

if "del_act" in query_params:
    if len(st.session_state.historial) > 0:
        st.session_state.historial.pop()
    st.query_params.clear()
    st.rerun()

# Extraer calientes y fríos para colorear teclas
def parse_numeros(texto):
    if not texto:
        return set()
    nums = re.findall(r'\b\d+\b', texto)
    return {int(n) for n in nums if 0 <= int(n) <= 36}

# 1. Calientes y Fríos discretos arriba
col_cal, col_fri = st.columns(2)
with col_cal:
    in_calientes = st.text_input("Calientes (opcional)", placeholder="Ej: 3, 17...", key="in_cal")
with col_fri:
    in_frios = st.text_input("Fríos (opcional)", placeholder="Ej: 0, 12...", key="in_fri")

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

# 3. Visor de registro continuo + Botón ⌫ Borrar
if st.session_state.historial:
    texto_registro = " - ".join(map(str, st.session_state.historial))
    st.markdown(f"""
        <div class="registro-container">
            <div class="registro-texto"><b>Reg ({len(st.session_state.historial)}):</b> {texto_registro}</div>
            <div class="btn-del-style" onclick="pressDel()">⌫ Borrar</div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="registro-container" style="color: #999999;">
            <div class="registro-texto">Reg (0): Sin registros</div>
        </div>
    """, unsafe_allow_html=True)

# 4. Teclado en FILAS adaptables con sombreado tenue y registro acumulativo
html_teclado = '<div class="teclado-filas">'

# Botón 0
clase_zero = "btn-zero-fila"
if 0 in set_calientes:
    clase_zero += " btn-caliente"
elif 0 in set_frios:
    clase_zero += " btn-frio"

html_teclado += f'<div onclick="pressNum(0)" class="{clase_zero}">0</div>'

# Botones 1 al 36 en filas
for n in range(1, 37):
    clase_btn = "btn-num-fila"
    if n in set_calientes:
        clase_btn += " btn-caliente"
    elif n in set_frios:
        clase_btn += " btn-frio"
    
    html_teclado += f'<div onclick="pressNum({n})" class="{clase_btn}">{n}</div>'

html_teclado += '</div>'

st.markdown(html_teclado, unsafe_allow_html=True)
