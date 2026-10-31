import streamlit as st

# ------------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA (MODO ULTRA-RÁPIDO)
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Agente Ruleta Express",
    page_icon="⚡",
    layout="centered"
)

# Estilos CSS optimizados para lectura visual en 1 segundo
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 52px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
    }
    .box-fuerte {
        background-color: #d32f2f;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 12px;
    }
    .box-cobertura {
        background-color: #0288d1;
        color: white;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
    }
    .num-large {
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. DISPOSICIÓN FÍSICA REAL DE LA RULETA EUROPEA
# ------------------------------------------------------------------------------
RUEDA_OFICIAL = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
    5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]

# ------------------------------------------------------------------------------
# 3. MEMORIA DE SESIÓN
# ------------------------------------------------------------------------------
if "historial_sesion" not in st.session_state:
    st.session_state.historial_sesion = []
if "aciertos_sesion" not in st.session_state:
    st.session_state.aciertos_sesion = 0
if "total_historico_tiradas" not in st.session_state:
    st.session_state.total_historico_tiradas = 0
if "total_historico_aciertos" not in st.session_state:
    st.session_state.total_historico_aciertos = 0

# ------------------------------------------------------------------------------
# 4. LÓGICA DE CÁLCULO
# ------------------------------------------------------------------------------
def obtener_vecinos(num, radio=2):
    idx = RUEDA_OFICIAL.index(num)
    return [RUEDA_OFICIAL[(idx + i) % len(RUEDA_OFICIAL)] for i in range(-radio, radio + 1)]

def parsear_numeros(texto):
    if not texto:
        return []
    try:
        return [int(n.strip()) for n in texto.split(",") if n.strip().isdigit() and 0 <= int(n.strip()) <= 36]
    except:
        return []

def calcular_apuesta_rapida(historial, calientes_panel, frios_panel):
    if len(historial) < 2 and not calientes_panel:
        return None, None

    ventana = historial[-30:] if historial else []
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

    ultimo_num = historial[-1] if historial else (calientes_panel[0] if calientes_panel else 0)
    cobertura_inercia = [n for n in obtener_vecinos(ultimo_num, radio=2) if n not in apuesta_fuerte and n not in frios_panel]

    return sorted(apuesta_fuerte), sorted(cobertura_inercia)

# ------------------------------------------------------------------------------
# 5. ESTRUCTURA CON PESTAÑAS (JUEGO RÁPIDO VS ANÁLISIS FINAL)
# ------------------------------------------------------------------------------
tab_juego, tab_analisis, tab_config = st.tabs(["⚡ JUEGO RÁPIDO", "📊 RETIRADA Y ANÁLISIS", "⚙️ PANEL CASINO"])

# --- PESTAÑA 3: CONFIGURACIÓN INICIAL (PANEL CASINO) ---
with tab_config:
    st.subheader("Configuración del Panel del Casino")
    input_calientes = st.text_input("Calientes del Panel (separados por coma)", "3, 10, 26, 12, 35")
    input_frios = st.text_input("Fríos del Panel (separados por coma)", "7, 18, 29, 4, 21")

calientes_p = parsear_numeros(input_calientes)
frios_p = parsear_numeros(input_frios)

fuerte, cobertura = calcular_apuesta_rapida(st.session_state.historial_sesion, calientes_p, frios_p)

# --- PESTAÑA 1: JUEGO EN VIVO (SOLO LO IMPRESCINDIBLE) ---
with tab_juego:
    if fuerte:
        st.markdown(f"""
        <div class="box-fuerte">
            <span style="font-size: 14px; text-transform: uppercase;">🔥 APUESTA FUERTE (70%)</span><br>
            <span class="num-large">{", ".join(map(str, fuerte))}</span>
        </div>
        <div class="box-cobertura">
            <span style="font-size: 13px; text-transform: uppercase;">🛡️ COBERTURA (30%)</span><br>
            <span style="font-size: 22px; font-weight: bold;">{", ".join(map(str, cobertura))}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Introduce la primera tirada para generar las apuestas.")

    # Teclado Táctil Ultra-Directo
    def registrar_tiro(num):
        if fuerte and cobertura:
            if num in fuerte or num in cobertura:
                st.session_state.aciertos_sesion += 1
                st.session_state.total_historico_aciertos += 1
        st.session_state.historial_sesion.append(num)
        st.session_state.total_historico_tiradas += 1

    if st.button("🟢 0 (CERO)", key="btn_0"):
        registrar_tiro(0)
        st.rerun()

    cols = st.columns(3)
    for i in range(1, 37):
        col_idx = (i - 1) % 3
        if cols[col_idx].button(f"{i}", key=f"btn_{i}"):
            registrar_tiro(i)
            st.rerun()

# --- PESTAÑA 2: INFORME DE RETIRADA Y ANÁLISIS COMPLETO ---
with tab_analisis:
    st.title("📊 Informe de Retirada y Análisis")
    
    total_tiros = len(st.session_state.historial_sesion)
    aciertos = st.session_state.aciertos_sesion
    efectividad = (aciertos / total_tiros * 100) if total_tiros > 0 else 0.0

    st.metric("Tiradas en esta Sesión", total_tiros)
    st.metric("Aciertos Totales", aciertos)
    st.metric("Efectividad de la Sesión", f"{efectividad:.1f}%")

    st.divider()

    st.subheader("📜 Historial de Tiradas de la Sesión")
    st.write(st.session_state.historial_sesion)

    st.divider()

    st.subheader("💡 Resumen del Agente")
    if total_tiros > 0:
        st.write(f"Sesión finalizada tras **{total_tiros} tiradas**. El agente mantuvo la cobertura activa en los sectores de inercia y concentró el capital en las zonas térmicas dominantes.")
    
    if st.button("🔄 CERRAR SESIÓN Y EMPEZAR NUEVA"):
        st.session_state.historial_sesion = []
        st.session_state.aciertos_sesion = 0
        st.success("Sesión cerrada. Los datos históricos globales siguen guardados.")
        st.rerun()
