import streamlit as st

st.set_page_config(page_title="Agente Ruleta Express", layout="centered")

# Estilos CSS limpios y cajetines interactivos como selectores
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 0.2rem !important;
        padding-bottom: 0.2rem !important;
        padding-left: 0.3rem !important;
        padding-right: 0.3rem !important;
    }

    .card-discreta {
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        padding: 4px 6px;
        text-align: left;
        color: #4a4a4a;
        margin-bottom: 3px;
    }
    .card-titulo {
        font-size: 9px;
        text-transform: uppercase;
        color: #888888;
        font-weight: bold;
    }
    .card-valores-fuerte {
        font-size: 13px;
        font-weight: 800;
        color: #d32f2f;
    }
    .card-valores-suave {
        font-size: 12px;
        font-weight: 700;
        color: #0288d1;
    }

    .caja-interactiva {
        background-color: #ffffff;
        border: 1px solid #d4d4d8;
        border-radius: 5px;
        padding: 4px 6px;
        font-size: 11px;
        color: #18181b;
        font-family: monospace;
        min-height: 26px;
        margin-bottom: 3px;
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
    }

    .registro-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #ffffff;
        border: 1px solid #d4d4d8;
        border-radius: 5px;
        padding: 4px 8px;
        margin-bottom: 4px;
        font-size: 11px;
        color: #18181b;
        font-family: monospace;
        min-height: 26px;
    }
    .registro-texto {
        overflow-x: auto;
        white-space: nowrap;
    }

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

    /* Botones de números limpios y compactos */
    div.stButton > button {
        width: 100% !important;
        height: 28px !important;
        padding: 0px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dcdcdc !important;
        border-radius: 4px !important;
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

# 3. LÓGICA DEL AGENTE
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

# 4. LOS PROPIOS CAJETINES ACTÚAN COMO SELECTOR (SIN BOTONES SUPERIORES FEOS)
clase_cal = "caja-interactiva caja-activa" if st.session_state.foco == "cal" else "caja-interactiva"
txt_cal = ", ".join(map(str, st.session_state.calientes)) if st.session_state.calientes else "Vacío (Pulsa para activar)"
if st.button(f"🔥 Calientes: {txt_cal}", key="btn_foco_cal", use_container_width=True):
    st.session_state.foco = "cal"
    st.rerun()

clase_fri = "caja-interactiva caja-activa" if st.session_state.foco == "fri" else "caja-interactiva"
txt_fri = ", ".join(map(str, st.session_state.frios)) if st.session_state.frios else "Vacío (Pulsa para activar)"
if st.button(f"❄️ Fríos: {txt_fri}", key="btn_foco_fri", use_container_width=True):
    st.session_state.foco = "fri"
    st.rerun()

# 5. GRUPOS A Y B VERTICALES
fuerte, cobertura = calcular_agente(st.session_state.historial, st.session_state.calientes, st.session_state.frios)
txt_a = ", ".join(map(str, fuerte)) if fuerte else "—"
txt_b = ", ".join(map(str, cobertura)) if cobertura else "—"

st.markdown(f'<div class="card-discreta"><div class="card-titulo">Grupo A (Ataque 70%)</div><div class="card-valores-fuerte">{txt_a}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="card-discreta"><div class="card-titulo">Grupo B (Cobertura 30%)</div><div class="card-valores-suave">{txt_b}</div></div>', unsafe_allow_html=True)

# 6. REGISTRO Y BORRADO (EL REGISTRO TAMBIÉN ACTÚA COMO SELECTOR)
col_reg_v, col_del_v = st.columns([0.75, 0.25])
clase_reg = "registro-container caja-activa" if st.session_state.foco == "reg" else "registro-container"

with col_reg_v:
    texto_reg_lbl = f"Reg ({len(st.session_state.historial)}): " + (" - ".join(map(str, st.session_state.historial)) if st.session_state.historial else "Sin registros")
    if st.button(texto_reg_lbl, key="btn_foco_reg", use_container_width=True):
        st.session_state.foco = "reg"
        st.rerun()

with col_del_v:
    if st.button("⌫ Borrar", key="btn_del_main", use_container_width=True):
        borrar_ultimo()
        st.rerun()

# 7. TECLADO EN 2 COLUMNAS (NÚMEROS DEL 0 AL 36)
if st.button("0 (CERO)", key="btn_0", use_container_width=True):
    procesar_numero(0)
    st.rerun()

for i in range(1, 37, 2):
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        if st.button(str(i), key=f"btn_{i}", use_container_width=True):
            procesar_numero(i)
            st.rerun()
    if i + 1 <= 36:
        with col_n2:
            if st.button(str(i + 1), key=f"btn_{i+1}", use_container_width=True):
                procesar_numero(i + 1)
                st.rerun()
