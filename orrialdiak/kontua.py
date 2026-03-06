import streamlit as st
from lojika.hiztegiya import translate

def erakutsi_login():
    # KONTUZ: with st.sidebar blokea hemendik kendu dugu, 
    # orain dashboard.py-k kudeatzen duelako zentralizatuta.

    # Txartela beherago ezartzeko vh (viewport height)
    st.markdown("<div style='padding-top: 14vh;'></div>", unsafe_allow_html=True)

    main_container = st.container()

    with main_container:
        # Zutabeen bidez horizontalki erdiratu eta estutu
        _, col_center, _ = st.columns([1.5, 2.5, 1.5])

        with col_center:
            # Login txartelaren karratua hasi (diseinua.css-ko klasea)
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            
            # 1. Izenburua (Izenburu handia eta garbia)
            st.markdown(f'<div class="login-header">{translate("login_or_reg")}</div>', unsafe_allow_html=True)

            # 2. Google Botoia
            if st.button(translate("login_btn"), use_container_width=True, type="secondary"):
                # Simulazioa (Hemen joango da Google OAuth geroago)
                st.session_state.user_email = "mikel@gmail.com"
                st.session_state.autentifikatua = True
                st.rerun()

            # 3. Login Aukerak eta Toggle-a
            st.markdown(f"#### {translate('login_options')}")
            is_reg = st.toggle(translate("is_new_user"), key="reg_toggle")

            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

            # 4. Botoi Dinamikoak (Toggle-aren arabera aktibatu/desaktibatu)
            c1, c2 = st.columns(2)
            with c1:
                type_sartu = "primary" if not is_reg else "secondary"
                st.button(translate("login"), use_container_width=True, type=type_sartu, disabled=is_reg)
            with c2:
                type_reg = "primary" if is_reg else "secondary"
                st.button(translate("register"), use_container_width=True, type=type_reg, disabled=not is_reg)

            # 5. Footer testua
            st.markdown(f"""
                <p style='opacity: 0.5; font-size: 0.85rem; margin-top: 25px; text-align: center; line-height: 1.4;'>
                    {translate('login_footer')}
                </p>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True) # Karratuaren amaiera