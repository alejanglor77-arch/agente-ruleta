import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Agente Ruleta Express Pro Evolutivo", layout="centered")

# Estilos CSS optimizados para iPhone 12 y visualización de rendimiento
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
        max-height: 190px;
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

# 2. SISTEMA DE BITÁCORA CON RENDIMIENTO Y CONTEXTO
ARCH_BITACORA = "libro_bitacora_ia.json"

def cargar_bitacora():
    if os.path.exists(ARCH_BITACORA):
        try:
            with open(ARCH_BITACORA, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_sesion_bitacora(sesion_historial, etiqueta_sede, calientes_panel, frios_panel, aciertos, fracasos):
    if not sesion_historial:
        return False
    
    bitacora = cargar_bitacora()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sede_limpia = etiqueta_sede.strip() if etiqueta_sede.strip() else "Mesa General"
    
    nueva_entrada = {
        "fecha": fecha_actual,
        "sede": sede_limpia,
        "total_tiradas": len(sesion_historial),
        "aciertos": aciertos,
        "fracasos": fracasos,
        "secuencia": sesion_historial,
        "calientes": calientes_panel,
        "frios": frios_panel
    }
    
    bitacora.append(nueva_entrada)
    if len(bitacora) > 100:
        bitacora = bitacora[-100:]
        
    with open(ARCH_BITACORA, "w", encoding="utf-8") as f:
        json.dump(bitacora, f, ensure_ascii=False, indent=4)
    return True

# 3. MEMORIA DE SESIÓN ACTUAL Y CONTADORES DE RENDIMIENTO
if "historial" not in st.session_state:
    st.session_state.historial = []
if "calientes" not in st.session_state:
    st.session_state.calientes = []
if "frios" not in st.session_state:
    st.session_state.frios = []
if "aciertos" not in st.session_state:
    st.session_state.aciertos = 0
if "fracasos" not in st.session_state:
    st.session_state.fracasos = 0
if "foco" not in st.session_state:
    st.session_state.foco = "reg"
if "ver_bitacora" not in st.session_state:
    st.session_state.ver_bitacora = False

# 4. CEREBRO ADAPTATIVO Y EVALUADOR DE ACIERTOS
def obtener_vecinos(num, radio=3):
    idx = RUEDA_OFICIAL.index(num)
    return [RUEDA_OFICIAL[(idx + i) % len(RUEDA_OFICIAL)] for i in range(-radio, radio + 1)]

def ordenar_por_rueda(lista_numeros):
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

    apuesta_fuerte_ordenada = ordenar_por_rueda(apuesta_fuerte)

    ultimo_num = historial[0] if historial else (calientes_panel[0] if calientes_panel else 0)
    vecinos_amplios = obtener_vecinos(ultimo_num, radio=4)
    cobertura_inercia = [n for n in vecinos_amplios if n not in apuesta_fuerte]
    cobertura_ordenada = ordenar_por_rueda(cobertura_inercia)

    return apuesta_fuerte_ordenada, cobertura_ordenada

def procesar_numero(num):
    if st.session_state.foco == "cal":
        if num not in st.session_state.calientes and len(st.session_state.calientes) < 5:
            st.session_state.calientes.insert(0, num)
    elif st.session_state.foco == "fri":
        if num not in st.session_state.frios and len(st.session_state.frios) < 5:
            st.session_state.frios.insert(0, num)
    else:
        # Evaluar acierto/fracaso con la predicción actual antes de meterlo
        fuerte_ant, cobertura_ant = calcular_agente(st.session_state.historial, st.session_state.calientes, st.session_state.frios)
        if fuerte_ant is not None:
            if num in fuerte_ant or num in cobertura_ant:
                st.session_state.aciertos += 1
            else:
                st.session_state.fracasos += 1
        st.session_state.historial.insert(0, num)

def borrar_ultimo():
    if st.session_state.foco == "cal" and st.session_state.calientes:
        st.session_state.calientes.pop(0)
    elif st.session_state.foco == "fri" and st.session_state.frios:
        st.session_state.frios.pop(0)
    elif st.session_state.foco == "reg" and st.session_state.historial:
        # Al borrar el último número registrado, ajustamos métricas si procede
        st.session_state.historial.pop(0)

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
        if st.button("💾", key="btn_save_bitacora", help="Guardar sesión y rendimiento"):
            if st.session_state.historial:
                if guardar_sesion_bitacora(st.session_state.historial, sede_actual, st.session_state.calientes, st.session_state.frios, st.session_state.aciertos, st.session_state.fracasos):
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

# --- INDICADOR DE RENDIMIENTO EN VIVO (ACIERTOS / FRACASOS) ---
total_apuestas = st.session_state.aciertos + st.session_state.fracasos
efectividad = (st.session_state.aciertos / total_apuestas * 100) if total_apuestas > 0 else 0
st.markdown(f"""
    <div style="background-color: #f4f4f5; border: 1px solid #d4d4d8; border-radius: 5px; padding: 4px 8px; font-size: 11px; margin-bottom: 4px; display: flex; justify-content: space-between;">
        <span>🎯 <b>Aciertos:</b> <span style="color: #2e7d32; font-weight: bold;">{st.session_state.aciertos}</span></span>
        <span>❌ <b>Fracasos:</b> <span style="color: #c62828; font-weight: bold;">{st.session_state.fracasos}</span></span>
        <span>📊 <b>Efectividad:</b> <span style="color: #0288d1; font-weight: bold;">{efectividad:.1f}%</span></span>
    </div>
""", unsafe_allow_html=True)

# --- VISOR DESPLEGABLE DEL LIBRO DE BITÁCORA CON RENDIMIENTO ---
if st.session_state.ver_bitacora:
    bitacora_datos = cargar_bitacora()
    st.markdown('<div class="bitacora-visor"><b>📖 LIBRO DE BITÁCORA (RENDIMIENTO Y HISTORIAL):</b><br>', unsafe_allow_html=True)
    if bitacora_datos:
        for idx, sesion in enumerate(reversed(bitacora_datos), 1):
            fecha = sesion.get("fecha", "Sin fecha")
            sede = sesion.get("sede", "Mesa General")
            total = sesion.get("total_tiradas", 0)
            aci = sesion.get("aciertos", 0)
            fra = sesion.get("fracasos", 0)
            t_ap = aci + fra
            ef_ses = (aci / t_ap * 100) if t_ap > 0 else 0
            
            secuencia = " - ".join(map(str, sesion.get("secuencia", [])))
            cals = ", ".join(map(str, sesion.get("calientes", []))) or "Ninguno"
            frs = ", ".join(map(str, sesion.get("frios", []))) or "Ninguno"
            
            st.markdown(f"<b>Sesión {idx}:</b> <span style='color:#d32f2f;'>{sede}</span> ({fecha})<br>"
                        f"🎯 Aciertos: <b style='color:#2e7d32;'>{aci}</b> | ❌ Fracasos: <b style='color:#c62828;'>{fra}</b> | Efectividad: <b>{ef_ses:.1f}%</b> (Tiradas: {total})<br>"
                        f"<span style='color: #0288d1;'>🔥 Calientes: [{cals}] | ❄️ Fríos: [{frs}]</span><br>"
                        f"<span style='color: #555;'>Tiradas: [{secuencia}]</span><br>---", unsafe_allow_html=True)
    else:
        st.markdown("<i>Aún no hay sesiones guardadas. Pulsa 💾 al terminar una partida.</i>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- CONTROL DE ALERTA NEURONAL AUTOMÁTICA POR RENDIMIENTO ---
# Analiza si hay suficientes datos globales en la bitácora para evaluar si se requiere mejora real
bitacora_check = cargar_bitacora()
total_global_aciertos = sum(s.get("aciertos", 0) for s in bitacora_check)
total_global_fracasos = sum(s.get("fracasos", 0) for s in bitacora_check)
total_global_apuestas = total_global_aciertos + total_global_fracasos

# Si hay historial acumulado y la efectividad histórica global baja del umbral de optimización (ej. < 45% con más de 20 jugadas)
if total_global_apuestas >= 20 and (total_global_aciertos / total_global_apuestas) < 0.45:
    st.markdown("""
        <div class="alerta-ia">
            <b>🧠 ALERTA NEURONAL DE EVOLUCIÓN (AUTOEVALUACIÓN):</b><br>
            El análisis de rendimiento global muestra margen de mejora en los sectores de cobertura.<br>
            👉 <b>Propuesta de Cambio Real:</b> Ajustar la inercia de radio o ponderación histórica para refinar los aciertos.
        </div>
    """, unsafe_allow_html=True)
    with st.expander("🛠️ Ver Instrucciones de Actualización de Parámetros"):
        st.markdown("""
        * **Paso 1:** Ve a la función de cálculo en el código.
        * **Paso 2:** Modifica temporalmente el peso histórico o amplía el radio de vecinos para reequilibrar los aciertos frente a los fracasos según el comportamiento de la mesa.
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
