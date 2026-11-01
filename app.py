import re
import streamlit as st

st.set_page_config(page_title="Agente", layout="centered")

# Estilo ultra compacto para filas y tonos tenues
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

    /* Regla rígida para filas continuas y compactas */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 3px !important;
    }
    div[data-testid="column"] {
        flex: 1 1 0px !important;
        min-width: 0px !important;
        padding: 0px !important;
    }

    /* Botones principales para el teclado numérico */
    div.stButton > button {
        width: 100% !important;
        height: 32px !important;
        padding: 0px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dcdcdc !important;
        border-radius: 5px !important;
        margin: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Estado persistente del historial acumulativo
if "historial" not in st.session_state:
    st.session_state.historial = []

# Función para extraer números de calientes y fríos
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

# Aplicar colores tenues de forma limpia mediante CSS inyectado
css_colores = "<style>"
if 0 in set_calientes:
    css_colores += "div.stButton > button[key='btn_0'] { background-color: #fff3e0 !important; border: 1px solid #ffe0b2 !important; color: #8c4a00 !important; }"
elif 0 in set_frios:
    css_colores += "div.stButton > button[key='btn_0'] { background-color: #e3f2fd !important; border: 1px solid #bbdefb !important; color: #0d47a1 !important; }"

for num in range(1, 37):
    if num in set_calientes:
        css_colores += f"div.stButton > button[key='btn_{num}'] {{ background-color: #fff3e0 !important; border: 1px solid #ffe0b2 !important; color: #8c4a00 !important; }}"
    elif num in set_frios:
        css_colores += f"div.stButton > button[key='btn_{num}'] {{ background-color: #e3f2fd !important; border: 1px solid #bbdefb !important; color: #0d47a1 !important; }}"
css_colores += "</style>"
st.markdown(css_colores, unsafe_allow_html=True)

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

# 3. Visor del historial acumulado y botón de borrado
col_reg, col_del = st.columns([0.75, 0.25])

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

# 4. Botón 0 arriba
if st.button("0", key="btn_0", use_container_width=True):
    st.session_state.historial.append(0)
    st.rerun()

# 5. Teclado distribuido por filas compactas de 4 columnas
for fila in range(0, 9):
    cols = st.columns(4)
    for col_idx in range(4):
        num = fila * 4 + col_idx + 1
        if num <= 36:
            with cols[col_idx]:
                if st.button(str(num), key=f"btn_{num}"):
                    st.session_state.historial.append(num)
                    st.rerun()
