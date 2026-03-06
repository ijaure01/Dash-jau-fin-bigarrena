import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from lojika.hiztegiya import translate
from lojika.sheets_manager import kargatu_edo_sortu_orria

# --- 1. KONFIGURAZIO NAGUSIA ---
st.set_page_config(page_title="Finantza Dashboard 2026", layout="wide")

# Konexioa definitu (fitxategi nagusian egitea hobe da behin bakarrik)
conn = st.connection("gsheets", type=GSheetsConnection)

# CSS kargatu (diseinua/diseinua.css fitxategitik)
try:
    with open("diseinua/diseinua.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("CSS fitxategia ez da aurkitu 'diseinua/diseinua.css' bidean.")

# --- 2. SAIOAREN HASIERATZEA (Session State) ---
if "autentifikatua" not in st.session_state:
    st.session_state.autentifikatua = False
if "orrialdea" not in st.session_state:
    st.session_state.orrialdea = "Grafikak"
if "lang" not in st.session_state:
    st.session_state.lang = "eu"

# --- 3. LOGIKA NAGUSIA ---
if not st.session_state.autentifikatua:
    # Kontua (Login) orria erakutsi
    from orrialdiak.kontua import erakutsi_login
    erakutsi_login()
else:
    # Sidebar-a eta Hizkuntza hautatzailea
    with st.sidebar:
        st.title(translate("title"))
        
        # Hizkuntza hautatzailea
        hizk_aukera = {"Euskara": "eu", "Español": "es", "English": "en"}
        # Uneko hizkuntza index-a aurkitu selectbox-erako
        current_lang_name = [k for k, v in hizk_aukera.items() if v == st.session_state.lang][0]
        hautatutako_hizk = st.selectbox("Hizkuntza", list(hizk_aukera.keys()), 
                                        index=list(hizk_aukera.keys()).index(current_lang_name))
        
        if hizk_aukera[hautatutako_hizk] != st.session_state.lang:
            st.session_state.lang = hizk_aukera[hautatutako_hizk]
            st.rerun()
        
        st.divider()
        st.subheader(f"👤 {st.session_state.user_email}")
        
        # Nabigazio Menua
        if st.button(translate("menu_charts"), use_container_width=True, 
                     type="primary" if st.session_state.orrialdea == "Grafikak" else "secondary"):
            st.session_state.orrialdea = "Grafikak"
            st.rerun()
            
        if st.button(translate("menu_table"), use_container_width=True,
                     type="primary" if st.session_state.orrialdea == "Taula" else "secondary"):
            st.session_state.orrialdea = "Taula"
            st.rerun()
            
        st.divider()
        if st.button(translate("logout"), type="secondary", use_container_width=True):
            st.session_state.autentifikatua = False
            st.rerun()

    # DATUAK KARGATU (Hemen kudeatzen dugu orriaren sorkuntza automatikoa)
    email_orria = st.session_state.user_email
    df = kargatu_edo_sortu_orria(conn, email_orria)

    # --- 4. ORRIALDE ESPEZIFIKOA KARGATU ---
    # Garrantzitsua: Funtzio bakoitzari behar dituen datuak pasatu behar dizkiogu
    if st.session_state.orrialdea == "Grafikak":
        from orrialdiak.grafikak import erakutsi_grafikak
        erakutsi_grafikak(df)
        
    elif st.session_state.orrialdea == "Taula":
        from orrialdiak.taula import erakutsi_taula
        # Taulari 'conn' eta 'email_orria' pasatzen dizkiogu Gorde ahal izateko
        erakutsi_taula(df, conn, email_orria)