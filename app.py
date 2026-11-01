import streamlit as st
import json
import os

st.set_page_config(page_title="Agente Ruleta Express Pro", layout="centered")

# Estilos CSS optimizados para iPhone 12
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

# 2. SISTEMA DE MEMORIA ACUMULATIVA (APRENDIZAJE GRATIS EN ARCHIVO LOCAL)
ARCH_MEMORIA = "historial_aprendido.json"

def cargar_memoria_historica():
    if os.path.exists(ARCH_MEMORIA):
        try:
            with open(ARCH_MEMORIA, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_en_memoria(sesion_historial):
    if not sesion_historial:
        return
    historico = cargar_memoria_historica()
    historico.append(sesion_historial)
    # Guardamos las últimas 50 sesiones para que el cerebro crezca sin sobrecargar
    if len(historico) > 50:
        historico = historico[-50:]
    with open(ARCH_MEMORIA, "w") as f:
        json.dump(historico, f)

# 3. MEMORIA DE SESIÓN ACTUAL
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

# 4. CEREBRO ADAPTATIVO CON APRENDIZAJE HISTÓRICO
def obtener_vecinos(num, radio=3): # Radio ampliado para mayor solidez física
    idx = RUEDA_OFICIAL.index(num)
    return [RUEDA_OFICIAL[(idx + i) % len(RUEDA_OFICIAL)] for i in range(-radio, radio + 1)]

def calcular_agente(historial, calientes_panel, frios_panel):
    if len(historial) < 2 and not calientes_panel:
        return None, None

    # Cargamos el aprendizaje histórico de sesiones pasadas
    memoria_pasada = cargar_memoria_historica()
    conteo_historico_global = {n: 0 for n in range(37)}
    for sesion in memoria_pasada:
        for num in sesion:
            conteo_historico_global[num] += 1

    # Ventana de sesión actual
    ventana = historial[:30] if historial else []
    conteo_sesion = {n: ventana.count(n) for n in range(37)}
    
    ecos_detectados = [n for n, count in conteo_sesion.items() if count >= 2]

    puntuaciones = {}
    for num in RUEDA_OFICIAL:
        vecinos_cercanos = obtener_vecinos(num, radio=1)
        
        # Ponderación basada en frecuencia actual + peso acumulado de sesiones pasadas (Aprendizaje)
        score = sum(conteo_sesion[v] * 2 for v in vecinos_cercanos)
        score += sum(conteo_historico_global[v] * 0.1 for v in vecinos_cercanos) # Feedback neuronal histórico
        
        score += sum(3 for v in vecinos_cercanos if v in calientes_panel)
        
        if any(v in ecos_detectados for v in vecinos_cercanos):
            score += 6 # Alerta de eco reforzada

        # Adaptabilidad de fríos
        for v in vecinos_cercanos:
            if v in frios_panel:
                if conteo_sesion[v] > 0:
                    score -= 1 # Ciclo cambiado, flexibilizamos
                else:
                    score -= 4

        puntuaciones[num] = score

    ordenados = sorted(puntuaciones, key=puntuaciones.get, reverse=True)
    max_score = puntuaciones[ordenados[0]]
    
    apuesta_fuerte = []
    for n in ordenados:
        if n in frios_panel and conteo_sesion[n] == 0:
            continue
        if len(apuesta_fuerte) < 5 or (len(apuesta_fuerte) < 8 and puntuaciones[n] >= max_score * 0.6):
            apuesta_fuerte.append(n)

    # Bloque continuo ordenado en la rueda (Cero huecos)
    apuesta_fuerte_ordenada_rueda = [n for n in RUEDA_OFICIAL if n in apuesta_fuerte]

    # COBERTURA SÓLIDA GRUPO B (Radio de 3 posiciones para que no sean solo 2 números)
    ultimo_num = historial[0] if historial else (calientes_panel[0] if calientes_panel else 0)
    cobertura_inercia = [n for n in obtener_vecinos(ultimo_num, radio=3) if n not in apuesta_fuerte]

    return apuesta_fuerte_ordenada_rueda, sorted(cobertura_inercia)

# --- INTERFAZ VERTICAL ---

# 1. BLOQUE CALIENTES
if st.button("🔥 Calientes [✓]" if st.session_state.foco == "cal" else "🔥 Calientes", key="btn_foco_cal", use_container_width=True):
    st.session_state.foco = "cal"
    st.rerun()

clase_cal = "caja-interactiva caja-activa" if st.session_state.foco == "cal" else "caja-interactiva"
txt_cal = ", ".join(map(str, st.session_state.calientes)) if st.session_state.calientes else "Vacío"
st.markdown(f'<div class="{clase_cal}"><div class="caja-label">Calientes</div><b>{txt_cal}</b></div>', unsafe_allow_html=True)

# 2. BLOQUE FRÍOS
if st.button("❄️ Fríos [✓]" if st.session_state.foco == "fri" else "❄️ Fríos", key="btn_foco_fri", use_container_width=True):
    st.session_state.foco = "fri"
    st.rerun()

clase_fri = "caja-interactiva caja-activa" if st.session_state.foco == "fri" else "caja-interactiva"
txt_fri = ", ".join(map(str, st.session_state.frios)) if st.session_state.frios else "Vacío"
st.markdown(f'<div class="{clase_fri}"><div class="caja-label">Fríos</div><b>{txt_fri}</b></div>', unsafe_allow_html=True)

# 3. BLOQUE REGISTRO Y BOTÓN DE GUARDAR SESIÓN (APRENDIZAJE)
if st.button("🎲 Registro [✓]" if st.session_state.foco == "reg" else "🎲 Registro", key="btn_foco_reg", use_container_width=True):
    st.session_state.foco = "reg"
    st.rerun()

col_reg_v, col_del_v = st.columns([0.6, 0.4])
clase_reg = "registro-container caja-activa" if st.session_state.foco == "reg" else "registro-container"

with col_reg_v:
    if st.session_state.historial:
        texto_registro = " - ".join(map(str, st.session_state.historial))
        st.markdown(f'<div class="{clase_reg}"><div class="registro-texto"><b>Reg ({len(st.session_state.historial)}):</b> {texto_registro}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="{clase_reg}" style="color: #999999;"><div class="registro-texto">Reg (0): Sin registros</div></div>', unsafe_allow_html=True)

with col_del_v:
    col_sub_del1, col_sub_del2 = st.columns(2)
    with col_sub_del1:
        if st.button("⌫", key="btn_del_main", help="Borrar último"):
            borrar_ultimo()
            st.rerun()
    with col_sub_del2:
        if st.button("💾", key="btn_save_session", help="Guardar sesión para que la IA aprenda"):
            if st.session_state.historial:
                guardar_en_memoria(st.session_state.historial)
                st.success("¡Aprendido!")
                st.rerun()

# --- GRUPOS A Y B ---
fuerte, cobertura = calcular_agente(st.session_state.historial, st.session_state.calientes, st.session_state.frios)
txt_a = ", ".join(map(str, fuerte)) if fuerte else "—"
txt_b = ", ".join(map(str, cobertura)) if cobertura else "—"

st.markdown(f'<div class="card-discreta"><div class="card-titulo">Grupo A (Ataque Continuo IA)</div><div class="card-valores-fuerte">{txt_a}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="card-discreta"><div class="card-titulo">Grupo B (Cobertura Sólida Rebote)</div><div class="card-valores-suave">{txt_b}</div></div>', unsafe_allow_html=True)

# --- TECLADO EN 2 COLUMNAS (0 AL 36) ---
if st.button("0", key="btn_0", use_container_width=True):
    procesar_numero(0)
    st.rerun()

for i in range(1, 37, 2):
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        if st.button(str(i), key=f"btn_{i}"):
            procesar_numero(i)
            st.rerun()
    if i + 1 <= 36:
        with col_n2:
            if st.button(str(i + 1), key=f"btn_{i+1}"):
                procesar_numero(i + 1)
                st.rerun()
