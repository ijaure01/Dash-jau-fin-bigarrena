import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from lojika.hiztegiya import translate
from lojika.sheets_manager import kargatu_edo_sortu_orria

# --- 1. KONFIGURAZIO NAGUSIA ---
st.set_page_config(page_title="Finantza Dashboard 2026", layout="wide")

# Konexioa
conn = st.connection("gsheets", type=GSheetsConnection)

# CSS kargatu
try:
    with open("diseinua/diseinua.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# --- 2. SESSION STATE ---
if "autentifikatua" not in st.session_state:
    st.session_state.autentifikatua = False
if "orrialdea" not in st.session_state:
    st.session_state.orrialdea = "Grafikak"
if "lang" not in st.session_state:
    st.session_state.lang = "eu"

# --- 3. SIDEBAR UNIFORMEA (Guztientzat) ---
with st.sidebar:
    st.title(translate("title"))
    
    # 🌍 HIZKUNTZA (Beti agertuko da, baita loginean ere)
    hizk_aukera = {"Euskara": "eu", "Español": "es", "English": "en"}
    current_lang_name = [k for k, v in hizk_aukera.items() if v == st.session_state.lang][0]
    
    hautatutako_hizk = st.selectbox("Hizkuntza", list(hizk_aukera.keys()), 
                                    index=list(hizk_aukera.keys()).index(current_lang_name))
    
    if hizk_aukera[hautatutako_hizk] != st.session_state.lang:
        st.session_state.lang = hizk_aukera[hautatutako_hizk]
        st.rerun()
    
    # 👤 NABIGAZIOA (Bakarrik saioa hasita badago)
    if st.session_state.autentifikatua:
        st.divider()
        st.subheader(f"👤 {st.session_state.user_email}")
        
        if st.button(translate("menu_charts"), width='stretch', 
                     type="primary" if st.session_state.orrialdea == "Grafikak" else "secondary"):
            st.session_state.orrialdea = "Grafikak"
            st.rerun()
            
        if st.button(translate("menu_table"), width='stretch',
                     type="primary" if st.session_state.orrialdea == "Taula" else "secondary"):
            st.session_state.orrialdea = "Taula"
            st.rerun()
            
        st.divider()
        if st.button(translate("logout"), type="secondary", width='stretch'):
            st.session_state.autentifikatua = False
            st.rerun()

# --- 4. EDUKI NAGUSIA (Logika) ---
if not st.session_state.autentifikatua:
    # 🔑 LOGIN ORRIALDEA
    from orrialdiak.kontua import erakutsi_login
    erakutsi_login() # Gogoratu orrialde honetako 'with st.sidebar' kendu behar duzula!
else:
    # 📊 DATUAK ETA DASHBOARD-A
    email_orria = st.session_state.user_email
    df = kargatu_edo_sortu_orria(conn, email_orria)

    if st.session_state.orrialdea == "Grafikak":
        from orrialdiak.grafikak import erakutsi_grafikak
        erakutsi_grafikak(df)
        
    elif st.session_state.orrialdea == "Taula":
        from orrialdiak.taula import erakutsi_taula
        erakutsi_taula(df, conn, email_orria)