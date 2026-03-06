import streamlit as st

PALETAK = {
    "Elite Gold": {
        "main": "#c9a050",      # Urrea
        "bg_card": "#313B45",   # Karratuen hondoa
        "sidebar": "#0e1117",
        "chart_list": ["#3d5a80", "#c9a050", "#98c1d9", "#566d7e", "#293241"]
    },
    "Lavender Aroma": {
        "main": "#967bb6",      # Lila
        "bg_card": "#3d344d",   # More iluna
        "sidebar": "#1a1625",
        "chart_list": ["#b19cd9", "#967bb6", "#5d4d7a", "#dcd0ff", "#4b3d60"]
    },
    "Ocean Breeze": {
        "main": "#00a2ed",      # Urdin argia
        "bg_card": "#1a2a33",   # Urdin-grisaxka
        "sidebar": "#0b141a",
        "chart_list": ["#0077be", "#00a2ed", "#5dade2", "#2e86c1", "#1b4f72"]
    }
}

def get_theme():
    # Session state-n gordeko dugu aukeratutako paleta
    p_name = st.session_state.get("tema_izena", "Elite Gold")
    return PALETAK[p_name]

def injektatu_estiloa():
    theme = get_theme()
    # CSS dinamikoa injektatzen dugu aldagaiak erabiliz
    st.markdown(f"""
        <style>
        :root {{
            --main-color: {theme['main']};
            --bg-card: {theme['bg_card']};
        }}
        [data-testid="stSidebar"] {{ background-color: {theme['sidebar']}; }}
        
        /* KPI karratuak eta beste elementuak */
        .kpi-card {{
            background-color: var(--bg-card);
            border: 1px solid var(--main-color);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }}
        .kpi-text {{ color: var(--main-color); font-weight: bold; }}
        
        /* Streamlit botoiak */
        .stButton>button {{
            border-radius: 8px;
            border: 1px solid var(--main-color);
            color: white;
        }}
        .stButton>button:hover {{
            border-color: white;
            color: var(--main-color);
        }}
        </style>
    """, unsafe_allow_html=True)