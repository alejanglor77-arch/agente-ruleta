import streamlit as st

st.set_page_config(page_title="Agente", layout="centered")

# Estilo para pantalla sin scroll en iPhone 12
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
        color: #888888;
        margin-bottom: 1px;
    }
    .card-valores {
        font-size: 14px;
        font-weight: bold;
        color: #1a1a1a;
    }

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
    }

    /* Filas nativas ultra compactas */
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

# 1. Memoria persistente
if "historial" not in st.session_state:
    st.session_state.historial = []
if "calientes" not in st.session_state:
    st.session_state.calientes = []
if "frios" not in st.session_state:
    st.session_state.frios = []
if "foco" not in st.session_state:
    st.session_state.foco = "reg"

def procesar_numero(num):
    if st.session_state.foco == "cal":
        if num not in st.session_state.calientes and len(st.session_state.calientes) < 5:
            st.session_state.calientes.insert(0, num)
    elif st.session_state.foco == "fri":
        if num not in st.session_state.frios and len(st.session_state.frios) < 5:
            st.session_state.frios.insert(0, num)
    else:
        st.session_state.historial.insert(0, num)

def borrar_ultimo():
    if st.session_state.foco == "cal" and st.session_state.calientes:
        st.session_state.calientes.pop(0)
    elif st.session_state.foco == "fri" and st.session_state.frios:
        st.session_state.frios.pop(0)
    elif st.session_state.foco == "reg" and st.session_state.historial:
        st.session_state.historial.pop(0)

# 2. Selector de Foco (Checks arriba)
col_sel_cal, col_sel_fri, col_sel_reg = st.columns(3)

with col_sel_cal:
    if st.button("🔥 Calientes [✓]" if st.session_state.foco == "cal" else "🔥 Calientes", key="btn_foco_cal"):
        st.session_state.foco = "cal"
        st.rerun()

with col_sel_fri:
    if st.button("❄️ Fríos [✓]" if st.session_state.foco == "fri" else "❄️ Fríos", key="btn_foco_fri"):
        st.session_state.foco = "fri"
        st.rerun()

with col_sel_reg:
    if st.button("🎲 Registro [✓]" if st.session_state.foco == "reg" else "🎲 Registro", key="btn_foco_reg"):
        st.session_state.foco = "reg"
        st.rerun()

# 3. Visores
col_cal_v, col_fri_v = st.columns(2)

clase_cal = "caja-interactiva caja-activa" if st.session_state.foco == "cal" else "caja-interactiva"
clase_fri = "caja-interactiva caja-activa" if st.session_state.foco == "fri" else "caja-interactiva"

with col_cal_v:
    txt_cal = ", ".join(map(str, st.session_state.calientes)) if st.session_state.calientes else "Vacío"
    st.markdown(f'<div class="{clase_cal}"><div class="caja-label">Calientes</div><b>{txt_cal}</b></div>', unsafe_allow_html=True)

with col_fri_v:
    txt_fri = ", ".join(map(str, st.session_state.frios)) if st.session_state.frios else "Vacío"
    st.markdown(f'<div class="{clase_fri}"><div class="caja-label">Fríos</div><b>{txt_fri}</b></div>', unsafe_allow_html=True)

# 4. Tarjetas totalmente vacías de inicio
col_a, col_b = st.columns(2)
with col_a:
    st.markdown('<div class="card-discreta"><div class="card-titulo">Grupo A</div><div class="card-valores">—</div></div>', unsafe_allow_html=True)
with col_b:
    st.markdown('<div class="card-discreta"><div class="card-titulo">Grupo B</div><div class="card-valores">—</div></div>', unsafe_allow_html=True)

# 5. Visor de Registro y Borrado
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

# 6. Coloreado tenue inyectado directo
css_colores = "<style>"
for n in range(37):
    if n in st.session_state.calientes:
        css_colores += f"div.stButton > button[key='btn_{n}'] {{ background-color: #fff3e0 !important; border: 1px solid #ffe0b2 !important; color: #8c4a00 !important; font-weight: bold !important; }}"
    elif n in st.session_state.frios:
        css_colores += f"div.stButton > button[key='btn_{n}'] {{ background-color: #e3f2fd !important; border: 1px solid #bbdefb !important; color: #0d47a1 !important; font-weight: bold !important; }}"
css_colores += "</style>"
st.markdown(css_colores, unsafe_allow_html=True)

# 7. Teclado nativo estable (Sin recargas externas)
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
