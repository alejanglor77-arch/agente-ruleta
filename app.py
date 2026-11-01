import streamlit as st

st.set_page_config(page_title="Agente Ruleta Express", layout="centered")

# Estilos CSS estables e idénticos
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
        padding:
