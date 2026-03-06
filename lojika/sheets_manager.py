import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

def kargatu_edo_sortu_orria(conn, email_orria):
    try:
        # 1. Saiatu irakurtzen (ttl=0 katxerik ez izateko)
        df = conn.read(worksheet=email_orria, ttl=0)
        return df
    except Exception:
        # 2. Orria ez badago, gspread bidez sortu
        try:
            creds_dict = st.secrets["connections"]["gsheets"]
            scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
            client = gspread.authorize(creds)
            
            sh = client.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
            sh.add_worksheet(title=email_orria, rows="100", cols="20")
            
            # Hasten dugu orria goiburuekin
            df_husa = pd.DataFrame(columns=["Date", "Category", "Notes", "Amount"])
            conn.update(worksheet=email_orria, data=df_husa)
            return df_husa
        except Exception as e:
            st.error(f"Errorea orria kudeatzean: {e}")
            return pd.DataFrame(columns=["Date", "Category", "Notes", "Amount"])