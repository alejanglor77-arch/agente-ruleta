import streamlit as st

st.set_page_config(page_title="Agente", layout="centered")

# Estilo para FILAS fluidas y tonos tenues
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

    /* Teclado en filas adaptables HTML */
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

    /* Estilos directos de color tenue */
    .btn-caliente {
        background-color: #fff3e0 !important;
        border: 1px solid #ffe0b2 !important;
        color: #8c4a00 !important;
        font-weight: 800 !important;
    }
    .btn-frio {
        background-color: #e3f2fd !important;
        border: 1px solid #bbdefb !important;
        color: #0d47a1 !important;
        font-weight: 800 !important;
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

# Procesar parámetros de URL (Pulsación de tecla HTML)
query_params = st.query_params

if "press" in query_params:
    num = int(query_params["press"])
    if st.session_state.foco == "cal":
        if num not in st.session_state.calientes and len(st.session_state.calientes) < 5:
            st.session_state.calientes.insert(0, num)
    elif st.session_state.foco == "fri":
        if num not in st.session_state.frios and len(st.session_state.frios) < 5:
            st.session_state.frios.insert(0, num)
    else:
        st.session_state.historial.insert(0, num)
    st.query_params.clear()
    st.rerun()

# 2. Selector de Foco (Checks superiores)
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

# 4. Tarjetas limpias
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
        if st.session_state.foco == "cal" and st.session_state.calientes:
            st.session_state.calientes.pop(0)
        elif st.session_state.foco == "fri" and st.session_state.frios:
            st.session_state.frios.pop(0)
        elif st.session_state.foco == "reg" and st.session_state.historial:
            st.session_state.historial.pop(0)
        st.rerun()

# 6. Teclado HTML (Coloreado directo garantizado)
html_teclado = '<div class="teclado-filas">'

# Botón 0
clase_zero = "btn-zero-fila"
if 0 in st.session_state.calientes:
    clase_zero += " btn-caliente"
elif 0 in st.session_state.frios:
    clase_zero += " btn-frio"

html_teclado += f'<a href="?press=0" target="_self" class="{clase_zero}">0</a>'

# Botones 1 al 36
for n in range(1, 37):
    clase_btn = "btn-num-fila"
    if n in st.session_state.calientes:
        clase_btn += " btn-caliente"
    elif n in st.session_state.frios:
        clase_btn += " btn-frio"
    
    html_teclado += f'<a href="?press={n}" target="_self" class="{clase_btn}">{n}</a>'

html_teclado += '</div>'

st.markdown(html_teclado, unsafe_allow_html=True)
