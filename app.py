import streamlit as st

st.set_page_config(page_title="Agente Ruleta Express", layout="centered")

# CSS Ajustado para 2 columnas (Lectura 100% clara en iPhone, scroll vertical fluido)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    .card-discreta {
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        color: #4a4a4a;
        margin-bottom: 6px;
    }
    .card-titulo {
        font-size: 11px;
        text-transform: uppercase;
        color: #888888;
        margin-bottom: 2px;
        font-weight: bold;
    }
    .card-valores-fuerte {
        font-size: 18px;
        font-weight: 800;
        color: #d32f2f;
    }
    .card-valores-suave {
        font-size: 16px;
        font-weight: 700;
        color: #0288d1;
    }

    .caja-interactiva {
        background-color: #ffffff;
        border: 1px solid #d4d4d8;
        border-radius: 6px;
        padding: 6px;
        font-size: 12px;
        color: #18181b;
        font-family: monospace;
        min-height: 32px;
        margin-bottom: 6px;
    }
    .caja-activa {
        border: 2px solid #18181b !important;
        background-color: #f4f4f5 !important;
    }
    .caja-label {
        font-size: 10px;
        text-transform: uppercase;
        color: #71717a;
        font-weight: bold;
        margin-bottom: 2px;
    }

    .registro-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #ffffff;
        border: 1px solid #d4d4d8;
        border-radius: 6px;
        padding: 6px 10px;
        margin-bottom: 8px;
        font-size: 12px;
        color: #18181b;
        font-family: monospace;
        min-height: 34px;
    }
    .registro-texto {
        overflow-x: auto;
        white-space: nowrap;
    }

    /* Permitir que las columnas se adapten de forma natural */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        gap: 6px !important;
    }
    div[data-testid="column"] {
        flex: 1 1 0px !important;
        min-width: 0px !important;
        padding: 0px !important;
    }

    div.stButton > button {
        width: 100% !important;
        height: 44px !important;
        padding: 0px !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        background-color: #ffffff !important;
        color: #111111 !important;
        border: 1px solid #cccccc !important;
        border-radius: 8px !important;
        margin-bottom: 2px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 1. DISPOSICIÓN FÍSICA REAL DE LA RULETA EUROPEA
RUEDA_OFICIAL = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
    5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]

# 2. MEMORIA DE SESIÓN
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

# 3. MOTOR INTELIGENTE DEL AGENTE
def obtener_vecinos(num, radio=2):
    idx = RUEDA_OFICIAL.index(num)
    return [RUEDA_OFICIAL[(idx + i) % len(RUEDA_OFICIAL)] for i in range(-radio, radio + 1)]

def calcular_agente(historial, calientes_panel, frios_panel):
    if len(historial) < 2 and not calientes_panel:
        return None, None

    ventana = historial[:30] if historial else []
    conteo_sesion = {n: ventana.count(n) for n in range(37)}
    
    puntuaciones = {}
    for num in RUEDA_OFICIAL:
        vecinos_cercanos = obtener_vecinos(num, radio=1)
        score = sum(conteo_sesion[v] * 2 for v in vecinos_cercanos)
        score += sum(3 for v in vecinos_cercanos if v in calientes_panel)
        score -= sum(4 for v in vecinos_cercanos if v in frios_panel)
        puntuaciones[num] = score

    ordenados = sorted(puntuaciones, key=puntuaciones.get, reverse=True)
    max_score = puntuaciones[ordenados[0]]
    
    apuesta_fuerte = []
    for n in ordenados:
        if n in frios_panel:
            continue
        if len(apuesta_fuerte) < 3 or (len(apuesta_fuerte) < 6 and puntuaciones[n] >= max_score * 0.7):
            apuesta_fuerte.append(n)

    ultimo_num = historial[0] if historial else (calientes_panel[0] if calientes_panel else 0)
    cobertura_inercia = [n for n in obtener_vecinos(ultimo_num, radio=2) if n not in apuesta_fuerte and n not in frios_panel]

    return sorted(apuesta_fuerte), sorted(cobertura_inercia)

# 4. CONTROLES SUPERIORES (CONTROLES Y VISORES)
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

col_cal_v, col_fri_v = st.columns(2)

clase_cal = "caja-interactiva caja-activa" if st.session_state.foco == "cal" else "caja-interactiva"
clase_fri = "caja-interactiva caja-activa" if st.session_state.foco == "fri" else "caja-interactiva"

with col_cal_v:
    txt_cal = ", ".join(map(str, st.session_state.calientes)) if st.session_state.calientes else "Vacío"
    st.markdown(f'<div class="{clase_cal}"><div class="caja-label">Calientes</div><b>{txt_cal}</b></div>', unsafe_allow_html=True)

with col_fri_v:
    txt_fri = ", ".join(map(str, st.session_state.frios)) if st.session_state.frios else "Vacío"
    st.markdown(f'<div class="{clase_fri}"><div class="caja-label">Fríos</div><b>{txt_fri}</b></div>', unsafe_allow_html=True)

# 5. GRUPO A Y GRUPO B
fuerte, cobertura = calcular_agente(st.session_state.historial, st.session_state.calientes, st.session_state.frios)

txt_a = ", ".join(map(str, fuerte)) if fuerte else "—"
txt_b = ", ".join(map(str, cobertura)) if cobertura else "—"

col_a, col_b = st.columns(2)
with col_a:
    st.markdown(f'<div class="card-discreta"><div class="card-titulo">Grupo A (Ataque 70%)</div><div class="card-valores-fuerte">{txt_a}</div></div>', unsafe_allow_html=True)
with col_b:
    st.markdown(f'<div class="card-discreta"><div class="card-titulo">Grupo B (Cobertura 30%)</div><div class="card-valores-suave">{txt_b}</div></div>', unsafe_allow_html=True)

# 6. HISTORIAL Y BORRADO
col_reg_v, col_del_v = st.columns([0.7, 0.3])
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

# 7. TECLADO EN 2 COLUMNAS GRANDES (BOTONES ANCHOS Y ACCESIBLES)
if st.button("0 (CERO)", key="btn_0", use_container_width=True):
    procesar_numero(0)
    st.rerun()

for fila in range(0, 18):
    cols = st.columns(2)
    for col_idx in range(2):
        num = fila * 2 + col_idx + 1
        if num <= 36:
            with cols[col_idx]:
                if st.button(str(num), key=f"btn_{num}"):
                    procesar_numero(num)
                    st.rerun()
