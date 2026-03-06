import streamlit as st
from lojika.hiztegiya import translate

def erakutsi_login():
    # Diseinua (CSS klasetik hartuta)
    st.markdown(f'<div class="login-card">', unsafe_allow_html=True)
    st.title(translate("title"))
    
    # Google-rekin jarraitzeko botoia
    if st.button(translate("login_btn"), use_container_width=True):
        st.session_state.user_email = "mikel@gmail.com"  # Simulazioa
        st.session_state.autentifikatua = True
        st.rerun()

    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button(translate("login_btn").split()[0], use_container_width=True) # "Sartu" bezalakoa
    with col2:
        st.button("Register", type="secondary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)