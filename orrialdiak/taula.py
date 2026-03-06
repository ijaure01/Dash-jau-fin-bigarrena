import streamlit as st
import pandas as pd
from lojika.hiztegiya import translate

def erakutsi_taula(df, conn, email_orria):
    #st.markdown(f"### 📑 {translate('menu_table')}: {email_orria}")
    
    # --- 1. DATUAK PRESTATU ---
    if df is None or df.empty:
        # ID zutabea gehitzen dugu hasieratik
        df = pd.DataFrame(columns=["ID", "Date", "Category", "Notes", "Amount"])
    
    # Ziurtatu ID zutabea badagoela (lehengo datuekin bateragarri izateko)
    if "ID" not in df.columns:
        df.insert(0, "ID", range(1, len(df) + 1))

    # Streamlit-ek RangeIndex bat behar du errenkada berriak onartzeko
    df = df.reset_index(drop=True)

    # Bihurketa seguruak
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0.0)
    
    # --- 2. DATA EDITOR ---
    # 
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        width='stretch',
        key="taula_editorea",
        column_order=("Date", "Category", "Notes", "Amount"),
        column_config={
            
            "Date": st.column_config.DateColumn(
                translate("date"), 
                format="YYYY-MM-DD",
                required=True
            ),
            "Category": st.column_config.TextColumn(translate("category")),
            "Amount": st.column_config.NumberColumn(translate("amount"), format="$%.2f", min_value=0),
            "Notes": st.column_config.TextColumn(translate("notes"))
        }
    )

    # --- 3. GORDE ETA AUTO-INDEXATU ---
    st.divider()
    if st.button(f"💾 {translate('save')}", width='stretch', type="primary"):
        with st.spinner("Gordetzen..."):
            try:
                df_to_save = edited_df.copy()
                
                # --- ID-AK AUTOMATIKOKI BETE ---
                # ID-a NaN duten errenkadak (berriak) aurkitu eta zenbakiak jarri
                existing_ids = pd.to_numeric(df_to_save["ID"], errors='coerce').dropna()
                max_id = int(existing_ids.max()) if not existing_ids.empty else 0
                
                for i in range(len(df_to_save)):
                    if pd.isna(df_to_save.iloc[i, df_to_save.columns.get_loc("ID")]):
                        max_id += 1
                        df_to_save.iloc[i, df_to_save.columns.get_loc("ID")] = max_id

                # --- DATA FORMATUA (YYYY/MM/DD) ---
                if not df_to_save.empty:
                    # Web-ean YYYY-MM-DD ikusten dugu, baina Sheets-era YYYY/MM/DD bidali
                    df_to_save['Date'] = df_to_save['Date'].dt.strftime('%Y/%m/%d')
                
                # Google Sheets-era bidali
                conn.update(worksheet=email_orria, data=df_to_save)
                
                st.cache_data.clear()
                st.success("✅ Datuak ondo gordeta!")
                st.balloons()
                st.rerun() # Berriz kargatu ID berriak taulan ikusteko
                
            except Exception as e:
                st.error(f"Errorea gordetzean: {e}")



