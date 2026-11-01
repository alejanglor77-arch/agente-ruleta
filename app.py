import streamlit as st

st.set_page_config(page_title="PRUEBA VISTA", layout="centered")

# Estilo discreto y compacto
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

    /* Indicadores visuales de foco */
    .caja-interactiva {
        background-color: #ffffff;
        border: 1px solid #d4d4d8;
        border-radius: 5px;
        padding: 4px 6px;
        font-size: 11px;
        color: #18181b;
        font-family: monospace;
        min-height: 28px;
        margin-bottom: 4px;
    }
    .caja-activa {
        border: 2px solid #18181b !important;
        background-color: #f4f4f5 !important;
    }
    .caja-label {
        font-size: 9px;
        text-transform: uppercase;
        color: #71717a;
        font-weight: bold;
        margin-bottom: 1px;
    }

    .registro-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #ffffff;
        border: 1px solid #d4d4d8;
        border-radius: 5px;
        padding: 4px 8px;
        margin-bottom: 6px;
        font-size: 11px;
        color: #18181b;
        font-family: monospace;
        min-height: 28px;
    }
    .registro-texto {
        overflow-x: auto;
        white-space: nowrap;
        margin-right: 6px;
    }

    /* Ajuste para mantener 4 columnas juntas */
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

    /* Estilo de botones nativos compactos */
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

# 1. Estado persistente del servidor
if "historial" not in st.session_state:
    st.session_state.historial = []
if "calientes" not in st.session_state:
    st.session_state.calientes = []
if "frios" not in st.session_state:
    st.session_state.frios = []
if "foco" not in st.session_state:
    st.session_state.foco = "reg"

# Funciones de procesamiento con inserción al principio (MÁS RECIENTE A LA IZQUIERDA)
def procesar_numero(num):
    if st.session_state.foco == "cal":
        if num not in st.session_state.calientes and len(st.session_state.calientes) < 5:
            st.session_state.calientes.insert(0, num)
    elif st.session_state.foco == "fri":
        if num not in st.session_state.frios and len(st.session_state.frios) < 5:
            st.session_state.frios.insert(0, num)
    else:
        # En el registro, el número recién tecleado entra en la primera posición (índice 0)
        st.session_state.historial.insert(0, num)

def borrar_ultimo():
    if st.session_state.foco == "cal":
        if st.session_state.calientes:
            st.session_state.calientes.pop(0)
    elif st.session_state.foco == "fri":
        if st.session_state.frios:
            st.session_state.frios.pop(0)
    else:
        if st.session_state.historial:
            st.session_state.historial.pop(0)

# 2. Selección de cajetín mediante botones nativos
col_sel_cal, col_sel_fri, col_sel_reg = st.columns(3)

with col_sel_cal:
    lbl_cal = "🔥 Calientes [✓]" if st.session_state.foco == "cal" else "🔥 Calientes"
    if st.button(lbl_cal, key="btn_foco_cal"):
        st.session_state.foco = "cal"
        st.rerun()

with col_sel_fri:
    lbl_fri = "❄️ Fríos [✓]" if st.session_state.foco == "fri" else "❄️ Fríos"
    if st.button(lbl_fri, key="btn_foco_fri"):
        st.session_state.foco = "fri"
        st.rerun()

with col_sel_reg:
    lbl_reg = "🎲 Registro [✓]" if st.session_state.foco == "reg" else "🎲 Registro"
    if st.button(lbl_reg, key="btn_foco_reg"):
        st.session_state.foco = "reg"
        st.rerun()

# 3. Visores interactivos
col_cal_v, col_fri_v = st.columns(2)

clase_cal = "caja-interactiva caja-activa" if st.session_state.foco == "cal" else "caja-interactiva"
clase_fri = "caja-interactiva caja-activa" if st.session_state.foco == "fri" else "caja-interactiva"

with col_cal_v:
    txt_cal = ", ".join(map(str, st.session_state.calientes)) if st.session_state.calientes else "Vacío"
    st.markdown(f'<div class="{clase_cal}"><div class="caja-label">Calientes (máx 5)</div><b>{txt_cal}</b></div>', unsafe_allow_html=True)

with col_fri_v:
    txt_fri = ", ".join(map(str, st.session_state.frios)) if st.session_state.frios else "Vacío"
    st.markdown(f'<div class="{clase_fri}"><div class="caja-label">Fríos (máx 5)</div><b>{txt_fri}</b></div>', unsafe_allow_html=True)

# Tarjetas del Grupo A y B
col_a, col_b = st.columns(2)
with col_a:
    st.markdown('<div class="card-discreta"><div class="card-titulo">Grupo A</div><div class="card-valores-fuerte">3, 20, 35</div></div>', unsafe_allow_html=True)
with col_b:
    st.markdown('<div class="card-discreta"><div class="card-titulo">Grupo B</div><div class="card-valores-suave">9, 22, 31</div></div>', unsafe_allow_html=True)

# Visor de Registro y Borrado
col_reg_v, col_del_v = st.columns([0.75, 0.25])

clase_reg = "registro-container caja-activa" if st.session_state.foco == "reg" else "registro-container"

with col_reg_v:
    if st.session_state.historial:
        texto_registro = " - ".join(map(str, st.session_state.historial))
        st.markdown(f'<div class="{clase_reg}"><div class="registro-texto"><b>Reg ({len(st.session_state.historial)}):</b> {texto_registro}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="{clase_reg}" style="color: #999999;"><div class="registro-texto">Reg (0): Sin registros</div></div>', unsafe_allow_html=True)

with col_del_v:
    if st.button("⌫ Borrar", key="btn_del_main"):
        borrar_ultimo()
        st.rerun()

# Dynamic Styling Script para colorear botones de calientes y fríos
css_colores = "<style>"
if 0 in st.session_state.calientes:
    css_colores += "div.stButton > button[key='btn_0'] { background-color: #fff3e0 !important; border: 1px solid #ffe0b2 !important; color: #8c4a00 !important; }"
elif 0 in st.session_state.frios:
    css_colores += "div.stButton > button[key='btn_0'] { background-color: #e3f2fd !important; border: 1px solid #bbdefb !important; color: #0d47a1 !important; }"

for num in range(1, 37):
    if num in st.session_state.calientes:
        css_colores += f"div.stButton > button[key='btn_{num}'] {{ background-color: #fff3e0 !important; border: 1px solid #ffe0b2 !important; color: #8c4a00 !important; }}"
    elif num in st.session_state.frios:
        css_colores += f"div.stButton > button[key='btn_{num}'] {{ background-color: #e3f2fd !important; border: 1px solid #bbdefb !important; color: #0d47a1 !important; }}"
css_colores += "</style>"
st.markdown(css_colores, unsafe_allow_html=True)

# 4. Teclado funcional
if st.button("0", key="btn_0", use_container_width=True):
    procesar_numero(0)
    st.rerun()

for fila in range(0, 9):
    cols = st.columns(4)
    for col_idx in range(4):
        num = fila * 4 + col_idx + 1
        if num <= 36:
            with cols[col_idx]:
                if st.button(str(num), key=f"btn_{num}"):
                    procesar_numero(num)
                    st.rerun()
