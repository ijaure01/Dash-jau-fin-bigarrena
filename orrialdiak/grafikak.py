import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from lojika.hiztegiya import translate

def style_fig_elite(fig):
    PALETA_ELITE = ["#3d5a80", "#c9a050", "#98c1d9", "#566d7e", "#293241"]
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white", size=12),
        legend=dict(title=None, font=dict(color="#FFFFFF", size=12)),
        margin=dict(t=20, b=20, l=0, r=0),
        colorway=PALETA_ELITE,
        height=450
    )
    return fig

def erakutsi_grafikak(df):
    if df is None or df.empty:
        st.info("Ez dago daturik.")
        return

    # --- 1. DATUAK PRESTATU ---
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
    df['Month_Name'] = df['Date'].dt.month_name()
    df['Year'] = df['Date'].dt.year
    df['Day_of_Week'] = df['Date'].dt.day_name()

    hilabete_guztiak = ["January", "February", "March", "April", "May", "June", 
                        "July", "August", "September", "October", "November", "December"]
    
    if "f_urtea" not in st.session_state: st.session_state.f_urtea = datetime.now().year
    if "f_hilabeteak" not in st.session_state: st.session_state.f_hilabeteak = hilabete_guztiak

    df_filtratua = df[(df['Year'] == st.session_state.f_urtea) & (df['Month_Name'].isin(st.session_state.f_hilabeteak))]

    # --- 2. KPIak (GOIKO DISEINUA) ---
    guztira = f"$ {df_filtratua['Amount'].sum():,.2f}"
    egun_kop = len(df_filtratua['Date'].dt.date.unique()) if not df_filtratua.empty else 1
    batez_bestekoa = f"$ {(df_filtratua['Amount'].sum()/egun_kop):,.2f}"

    st.markdown(f"""
        <div style="display: flex; width: 100%; gap: 20px; margin-top: -30px; margin-bottom: 10px;">
            <div style="flex: 1; background-color: #313B45; padding: 20px; border-radius: 15px; border: 1px solid #c9a050; text-align: center;">
                <p style="color: #ffffff; font-size: 1.1rem; font-weight: bold; margin: 0; opacity: 0.8;">GASTUA GUZTIRA</p>
                <p style="color: #c9a050; font-size: 5vw; font-weight: bold; margin: 0; line-height: 1;">{guztira}</p>
            </div>
            <div style="flex: 1; background-color: #313B45; padding: 20px; border-radius: 15px; border: 1px solid #c9a050; text-align: center;">
                <p style="color: #ffffff; font-size: 1.1rem; font-weight: bold; margin: 0; opacity: 0.8;">EGUNEKO BATEZ BESTEKOA</p>
                <p style="color: #c9a050; font-size: 5vw; font-weight: bold; margin: 0; line-height: 1;">{batez_bestekoa}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- 3. IRAGAZKIAK ---
    _, col_f = st.columns([5, 1])
    with col_f:
        with st.popover("🔍 IRAGAZKIAK", use_container_width=True):
            urteak = sorted(df['Year'].dropna().unique(), reverse=True)
            st.selectbox("Urtea", urteak if urteak else [2026], key="f_urtea")
            st.multiselect("Hilabeteak", options=hilabete_guztiak, key="f_hilabeteak")
            if st.button("OK", use_container_width=True): st.rerun()

    # --- 4. CAROUSEL LOGIKA ---
    grafiko_izenak = ["banaketa", "bilakaera", "xehetasuna (sunburst)", "bolumena (treemap)", "intentsitatea (heatmap)", "top 5 taula"]
    if "grafiko_index" not in st.session_state: st.session_state.grafiko_index = 0
    uneko_izen = grafiko_izenak[st.session_state.grafiko_index]

    st.markdown(f"<h3 style='text-align: center; color: #c9a050; margin-bottom: 0;'>{uneko_izen.upper()}</h3>", unsafe_allow_html=True)

    col_gezia_l, col_grafika, col_gezia_r = st.columns([1, 8, 1])

    with col_gezia_l:
        st.markdown("<div style='height: 180px;'></div>", unsafe_allow_html=True)
        if st.button("«", key="prev_g", use_container_width=True):
            st.session_state.grafiko_index = (st.session_state.grafiko_index - 1) % len(grafiko_izenak)
            st.rerun()

    with col_grafika:
        if uneko_izen == "banaketa":
            fig = px.pie(df_filtratua, values='Amount', names='Category', hole=0.5)
            st.plotly_chart(style_fig_elite(fig), use_container_width=True)
        
        elif uneko_izen == "bilakaera":
            df_daily = df_filtratua.groupby('Date')['Amount'].sum().reset_index()
            fig = px.line(df_daily, x='Date', y='Amount', markers=True)
            fig.update_traces(line_color='#c9a050', fill='tozeroy', fillcolor='rgba(201, 160, 80, 0.2)')
            st.plotly_chart(style_fig_elite(fig), use_container_width=True)

        elif uneko_izen == "xehetasuna (sunburst)":
            # 1. Garbitu hosto hutsak: Notes hutsik badago, Plotly-k errorea ematen du
            df_sun = df_filtratua.copy()
            df_sun = df_sun[df_sun['Notes'].str.strip() != ""] # Hutsuneak kendu
            df_sun = df_sun.dropna(subset=['Notes'])         # Null balioak kendu

            if not df_sun.empty:
                # Oharrak bakarrak izatea ziurtatu index-a gehituz (hosto bikoiztuak ekiditeko)
                df_sun['Notes_Unique'] = df_sun['Notes'] + " (" + df_sun.index.astype(str) + ")"
                
                fig = px.sunburst(
                    df_sun, 
                    path=['Category', 'Notes_Unique'], 
                    values='Amount',
                    hover_data=['Notes'] # Hover-ean ohar garbia erakusteko
                )
                st.plotly_chart(style_fig_elite(fig), use_container_width=True)
            else:
                st.warning("Ez dago oharrik (Notes) grafika hau osatzeko.")

        elif uneko_izen == "bolumena (treemap)":
            # Logika bera Treemap-erako
            df_tree = df_filtratua.copy()
            df_tree = df_tree[df_tree['Notes'].str.strip() != ""]
            df_tree = df_tree.dropna(subset=['Notes'])

            if not df_tree.empty:
                df_tree['Notes_Unique'] = df_tree['Notes'] + " (" + df_tree.index.astype(str) + ")"
                
                fig = px.treemap(
                    df_tree, 
                    path=['Category', 'Notes_Unique'], 
                    values='Amount',
                    hover_data=['Notes']
                )
                st.plotly_chart(style_fig_elite(fig), use_container_width=True)
            else:
                st.warning("Ez dago oharrik (Notes) grafika hau osatzeko.")
            

        elif uneko_izen == "intentsitatea (heatmap)":
            # Asteko eguna eta kategoriaren arabera
            fig = px.density_heatmap(df_filtratua, x="Day_of_Week", y="Category", z="Amount", 
                                     color_continuous_scale=['#313B45', '#c9a050'])
            st.plotly_chart(style_fig_elite(fig), use_container_width=True)
            

        elif uneko_izen == "top 5 taula":
            st.markdown("<br>", unsafe_allow_html=True)
            top5_df = df_filtratua.nlargest(5, 'Amount')[['Date', 'Category', 'Notes', 'Amount']]
            st.table(top5_df.style.format({"Amount": "{:.2f} $"}))

    with col_gezia_r:
        st.markdown("<div style='height: 180px;'></div>", unsafe_allow_html=True)
        if st.button("»", key="next_g", use_container_width=True):
            st.session_state.grafiko_index = (st.session_state.grafiko_index + 1) % len(grafiko_izenak)
            st.rerun()