import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Agente Ruleta Express Pro Sectores", layout="centered")

# Estilos CSS optimizados para iPhone 12 y visualización de sectores continuos
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
        padding: 6px 8px;
        text-align: left;
        color: #4a4a4a;
        margin-bottom: 4px;
    }
    .card-titulo {
        font-size: 9px;
        text-transform: uppercase;
        color: #888888;
        font-weight: bold;
        margin-bottom: 2px;
    }
    .card-valores-fuerte {
        font-size: 14px;
        font-weight: 800;
        color: #d32f2f;
        letter-spacing: 0.5px;
    }
    .card-valores-suave {
        font-size: 13px;
        font-weight: 700;
        color: #0288d1;
        letter-spacing: 0.5px;
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

    .bitacora-visor {
        background-color: #f4f4f5;
        border: 1px solid #d4d4d8;
        border-radius: 6px;
        padding: 8px;
        font-size: 11px;
        color: #18181b;
        margin-bottom: 6px;
        max-height: 160px;
        overflow-y: auto;
    }

    .alerta-ia {
        background-color: #eff6ff;
        border: 1px solid #3b82f6;
        border-radius: 6px;
        padding: 6px 8px;
        font-size: 11px;
        color: #1e40af;
        margin-bottom: 4px;
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

# 1. DISPOSICIÓN FÍSICA REAL DE LA RULETA EUROPEA (CILINDRO OFICIAL)
RUEDA_OFICIAL = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
    5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]

# 2. SISTEMA DE BITÁCORA Y MEMORIA CON ETIQUETAS DE SEDE
ARCH_BITACORA = "libro_bitacora_ia.json"

def cargar_bitacora():
    if os.path.exists(ARCH_BITACORA):
        try:
            with open(ARCH_BITACORA, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_sesion_bitacora(sesion_historial, etiqueta_sede):
    if not sesion_historial:
        return False
    
    bitacora = cargar_bitacora()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sede_limpia = etiqueta_sede.strip() if etiqueta_sede.strip() else "Mesa General"
    
    nueva_entrada = {
        "fecha": fecha_actual,
        "sede": sede_limpia,
        "total_tiradas": len(sesion_historial),
        "secuencia": sesion_historial
    }
    
    bitacora.append(nueva_entrada)
    if len(bitacora) > 100:
        bitacora = bitacora[-100:]
        
    with open(ARCH_BITACORA, "w", encoding="utf-8") as f:
        json.dump(bitacora, f, ensure_ascii=False, indent=4)
    return True

# 3. MEMORIA DE SESIÓN ACTUAL
if "historial" not in st.session_state:
    st.session_state.historial = []
if "calientes" not in st.session_state:
    st.session_state.calientes = []
if "frios" not in st.session_state:
    st.session_state.frios = []
if "foco" not in st.session_state:
    st.session_state.foco = "reg"
if "ver_bitacora" not in st.session_state:
    st.session_state.ver_bitacora = False

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

# 4. CEREBRO ADAPTATIVO CON ORDENACIÓN POR SECTORES FÍSICOS CONTINUOS
def obtener_vecinos(num, radio=3):
    idx = RUEDA_OFICIAL.index(num)
    return [RUEDA_OFICIAL[(idx + i) % len(RUEDA_OFICIAL)] for i in range(-radio, radio + 1)]

def ordenar_por_rueda(lista_numeros):
    """Ordena una lista de números según su posición física estricta en el cilindro."""
    return [n for n in RUEDA_OFICIAL if n in lista_numeros]

def calcular_agente(historial, calientes_panel, frios_panel):
    if len(historial) < 2 and not calientes_panel:
        return None, None

    bitacora_pasada = cargar_bitacora()
    conteo_historico_global = {n: 0 for n in range(37)}
    for sesion in bitacora_pasada:
        for num in sesion.get("secuencia", []):
            conteo_historico_global[num] += 1

    ventana = historial[:30] if historial else []
    conteo_sesion = {n: ventana.count(n) for n in range(37)}
    ecos_detectados = [n for n, count in conteo_sesion.items() if count >= 2]

    puntuaciones = {}
    for num in RUEDA_OFICIAL:
        vecinos_cercanos = obtener_vecinos(num, radio=1)
        
        score = sum(conteo_sesion[v] * 2 for v in vecinos_cercanos)
        score += sum(conteo_historico_global[v] * 0.08 for v in vecinos_cercanos)
        score += sum(3 for v in vecinos_cercanos if v in calientes_panel)
        
        if any(v in ecos_detectados for v in vecinos_cercanos):
            score += 6

        for v in vecinos_cercanos:
            if v in frios_panel:
                if conteo_sesion[v] > 0:
                    score -= 1
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

    # Coherencia física: Ordenar el ataque fuerte estrictamente en el orden del cilindro
    apuesta_fuerte_ordenada = ordenar_por_rueda(apuesta_fuerte)

    # Cobertura de inercia contigua sin huecos alrededor del último número registrado
    ultimo_num = historial[0] if historial else (calientes_panel[0] if calientes_panel else 0)
    vecinos_amplios = obtener_vecinos(ultimo_num, radio=4)
    cobertura_inercia = [n for n in vecinos_amplios if n not in apuesta_fuerte]
    cobertura_ordenada = ordenar_por_rueda(cobertura_inercia)

    return apuesta_fuerte_ordenada, cobertura_ordenada

# --- INTERFAZ VERTICAL ---

sede_actual = st.text_input("📍 Sede / Mesa actual:", value="Online / Salón", placeholder="Ej. Centro Comercial, Online...", label_visibility="collapsed")

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

# 3. BLOQUE REGISTRO Y CONTROLES DE BITÁCORA
if st.button("🎲 Registro [✓]" if st.session_state.foco == "reg" else "🎲 Registro", key="btn_foco_reg", use_container_width=True):
    st.session_state.foco = "reg"
    st.rerun()

col_reg_v, col_del_v = st.columns([0.5, 0.5])
clase_reg = "registro-container caja-activa" if st.session_state.foco == "reg" else "registro-container"

with col_reg_v:
    if st.session_state.historial:
        texto_registro = " - ".join(map(str, st.session_state.historial))
        st.markdown(f'<div class="{clase_reg}"><div class="registro-texto"><b>Reg ({len(st.session_state.historial)}):</b> {texto_registro}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="{clase_reg}" style="color: #999999;"><div class="registro-texto">Reg (0): Sin registros</div></div>', unsafe_allow_html=True)

with col_del_v:
    col_sub1, col_sub2, col_sub3, col_sub4 = st.columns(4)
    with col_sub1:
        if st.button("⌫", key="btn_del_main", help="Borrar último"):
            borrar_ultimo()
            st.rerun()
    with col_sub2:
        if st.button("💾", key="btn_save_bitacora", help="Guardar sesión con sede"):
            if st.session_state.historial:
                if guardar_sesion_bitacora(st.session_state.historial, sede_actual):
                    st.success("¡Guardado!")
                    st.rerun()
    with col_sub3:
        if st.button("📖", key="btn_toggle_visor", help="Ver Libro de Bitácora"):
            st.session_state.ver_bitacora = not st.session_state.ver_bitacora
            st.rerun()
    with col_sub4:
        bitacora_actual = cargar_bitacora()
        if bitacora_actual:
            datos_json = json.dumps(bitacora_actual, ensure_ascii=False, indent=4)
            st.download_button(
                label="📥",
                data=datos_json,
                file_name=f"libro_bitacora_ia_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                help="Descargar archivo"
            )
        else:
            st.button("📥", disabled=True, help="Vacío")

# --- VISOR DESPLEGABLE DEL LIBRO DE BITÁCORA ---
if st.session_state.ver_bitacora:
    bitacora_datos = cargar_bitacora()
    st.markdown('<div class="bitacora-visor"><b>📖 LIBRO DE BITÁCORA (MULTISEDE):</b><br>', unsafe_allow_html=True)
    if bitacora_datos:
        for idx, sesion in enumerate(reversed(bitacora_datos), 1):
            fecha = sesion.get("fecha", "Sin fecha")
            sede = sesion.get("sede", "Mesa General")
            total = sesion.get("total_tiradas", 0)
            secuencia = " - ".join(map(str, sesion.get("secuencia", [])))
            st.markdown(f"<b>Sesión {idx}:</b> <span style='color:#d32f2f;'>{sede}</span> ({fecha}) | Tiradas: {total}<br><span style='color: #555;'>[{secuencia}]</span><br>---", unsafe_allow_html=True)
    else:
        st.markdown("<i>Aún no hay sesiones guardadas. Pulsa 💾 al terminar una partida.</i>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- CONTROL DE ALERTA NEURONAL ---
bitacora_check = cargar_bitacora()
if len(bitacora_check) >= 999:
    st.markdown("""
        <div class="alerta-ia">
            <b>🧠 ALERTA NEURONAL DEL AGENTE (DIAGNÓSTICO):</b><br>
            Analizadas las sesiones de la bitácora, propongo ajustar el parámetro del algoritmo.<br>
            👉 <b>Instrucción:</b> Ve a la función <code>calcular_agente()</code>.
        </div>
    """, unsafe_allow_html=True)
    with st.expander("🛠️ Ver Instrucciones de Borrado y Sustitución"):
        st.markdown("""
        * **Paso 1:** Busca esta línea exacta en tu código:
          `score += sum(conteo_historico_global[v] * 0.05 for v in vecinos_cercanos)`
        * **Paso 2:** Bórrala y cámbiala por la nueva propuesta.
        """)

# --- GRUPOS A Y B (ORDENADOS POR RUEDA FÍSICA SIN HUECOS) ---
fuerte, cobertura = calcular_agente(st.session_state.historial, st.session_state.calientes, st.session_state.frios)
txt_a = " - ".join(map(str, fuerte)) if fuerte else "—"
txt_b = " - ".join(map(str, cobertura)) if cobertura else "—"

st.markdown(f'<div class="card-discreta"><div class="card-titulo">Grupo A (Ataque Sectorial IA - Orden Rueda)</div><div class="card-valores-fuerte">{txt_a}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="card-discreta"><div class="card-titulo">Grupo B (Cobertura Sólida Contigua - Sin Huecos)</div><div class="card-valores-suave">{txt_b}</div></div>', unsafe_allow_html=True)

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
