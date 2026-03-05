import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import gspread
from google.oauth2.service_account import Credentials
import plotly.express as px

# --- 1. KONFIGURAZIOA ---
st.set_page_config(page_title="Finantza Analisia 2026", layout="wide")

# Konexioa secrets.toml-eko datuekin
conn = st.connection("gsheets", type=GSheetsConnection)

# Saioaren egoera hasieratu
if "autentifikatua" not in st.session_state:
    st.session_state.autentifikatua = False
if "orrialdea" not in st.session_state:
    st.session_state.orrialdea = "Grafikak"

# --- 2. LOGIN DISEINUA ---
def erakutsi_login():
    st.markdown("""
        <style>
        .login-card {
            background-color: #1d1e24;
            padding: 2.5rem;
            border-radius: 12px;
            border: 1px solid #31333f;
            text-align: center;
            max-width: 500px;
            margin: auto;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.title("Sartu edo Erregistratu Finantza Dashboard-era")
    
    if st.button("🚀 Jarraitu Google bidez", use_container_width=True):
        st.session_state.user_email = "mikel@gmail.com" 
        st.session_state.autentifikatua = True
        st.rerun()

    st.write("---")
    st.write("**Login Aukerak**")
    reg_mode = st.toggle("Erregistratu berria baldin bauk")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sartu", type="primary" if not reg_mode else "secondary", use_container_width=True):
            st.session_state.user_email = "erabiltzaile_test@gmail.com"
            st.session_state.autentifikatua = True
            st.rerun()
    with col2:
        st.button("Erregistratu", type="primary" if reg_mode else "secondary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. APLIKAZIOAREN LOGIKA ---
if not st.session_state.autentifikatua:
    erakutsi_login()
else:
    # Sidebar
    with st.sidebar:
        st.subheader(f"Kaixo, {st.session_state.user_email}")
        if st.button("📊 Grafikak", use_container_width=True, 
                     type="primary" if st.session_state.orrialdea == "Grafikak" else "secondary"):
            st.session_state.orrialdea = "Grafikak"
        if st.button("📑 Taula", use_container_width=True,
                     type="primary" if st.session_state.orrialdea == "Taula" else "secondary"):
            st.session_state.orrialdea = "Taula"
        st.divider()
        if st.button("Saioa itxi"):
            st.session_state.autentifikatua = False
            st.rerun()

    # --- DATUAK KARGATU ETA SORTU ---
    email_orria = st.session_state.user_email
    
    try:
        # Saia gaitezen orria irakurtzen
        df = conn.read(worksheet=email_orria, ttl=0)
    except Exception:
        # Orria ez bada existitzen, gspread erabiliz sortu
        try:
            creds_dict = st.secrets["connections"]["gsheets"]
            scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
            client = gspread.authorize(creds)
            sh = client.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
            
            sh.add_worksheet(title=email_orria, rows="100", cols="20")
            df = pd.DataFrame(columns=["Date", "Category", "Notes", "Amount"])
            conn.update(worksheet=email_orria, data=df)
            st.toast(f"Orri berria sortu dugu: {email_orria}")
        except Exception as e:
            st.error(f"Ezin izan dugu orria sortu: {e}")
            df = pd.DataFrame(columns=["Date", "Category", "Notes", "Amount"])

    # --- DATU MOTAK BEREZITU (Data erroreak ekiditeko) ---
    # Behartu datuak mota egokian egon daitezen editorean sartu aurretik
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0.0)
    # Kategoria zutabea testu gisa ziurtatu
    df['Category'] = df['Category'].astype(str).replace('nan', '')

    # --- GRAFIKAK ORRIALDEA ---
    if st.session_state.orrialdea == "Grafikak":
        st.markdown(f"<h1 style='text-align: center;'>Gastuen Bilakaera</h1>", unsafe_allow_html=True)
        
        # Garbitu datu hutsak grafikoa ez puskatzeko
        df_valid = df.dropna(subset=['Category', 'Amount'])
        df_valid = df_valid[df_valid['Amount'] > 0]
        
        if df_valid.empty:
            st.info("Ez dago datu nahikorik grafikatzeko. Sartu gastu batzuk 'Taula' atalean.")
        else:
            df_sum = df_valid.groupby("Category")["Amount"].sum().reset_index()
            fig = px.pie(df_sum, values='Amount', names='Category', hole=.5,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(showlegend=True, paper_bgcolor='rgba(0,0,0,0)', 
                              plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, use_container_width=True)
            
            # Geziak (Nabigazio simulazioa)
            gc1, gc2, gc3 = st.columns([1, 2, 1])
            with gc1: st.button("«", use_container_width=True, key="prev")
            with gc3: st.button("»", use_container_width=True, key="next")

    # --- TAULA ORRIALDEA ---
    elif st.session_state.orrialdea == "Taula":
        st.markdown(f"## Datuen Taula - {email_orria}")
        
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Date": st.column_config.DateColumn("Data", required=True),
                # Hemen dago aldaketa: SelectboxColumn kendu dugu edozer idatzi ahal izateko
                "Category": st.column_config.TextColumn("Kategoria", help="Idatzi nahi duzun kategoria"),
                "Amount": st.column_config.NumberColumn("Kopurua", format="$%.2f", min_value=0)
            }
        )
        
        if st.button("💾 Gorde Aldaketak", use_container_width=True):
            # Gorde aurretik datak testu formatura pasatu Sheets-entzat
            df_to_save = edited_df.copy()
            if not df_to_save.empty:
                df_to_save['Date'] = df_to_save['Date'].dt.strftime('%Y-%m-%d')
            
            conn.update(worksheet=email_orria, data=df_to_save)
            st.cache_data.clear()
            st.success(f"Datuak ondo gordeta!")
            st.balloons()