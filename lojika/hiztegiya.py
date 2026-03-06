import streamlit as st

# Hiztegi nagusia
TRANSLATIONS = {
    "eu": {
        "title": "Finantza Dashboard-a",
        "login_btn": "🚀 Jarraitu Google bidez",
        "menu_charts": "📊 Grafikak",
        "menu_table": "📑 Taula",
        "logout": "Saioa itxi",
        "save": "Gorde Aldaketak",
        "date": "Data",
        "category": "Kategoria",
        "amount": "Kopurua",
        "notes": "Oharrak"
    },
    "es": {
        "title": "Dashboard Financiero",
        "login_btn": "🚀 Continuar con Google",
        "menu_charts": "📊 Gráficos",
        "menu_table": "📑 Tabla",
        "logout": "Cerrar sesión",
        "save": "Guardar cambios",
        "date": "Fecha",
        "category": "Categoría",
        "amount": "Cantidad",
        "notes": "Notas"
    },
    "en": {
        "title": "Financial Dashboard",
        "login_btn": "🚀 Continue with Google",
        "menu_charts": "📊 Charts",
        "menu_table": "📑 Table",
        "logout": "Logout",
        "save": "Save Changes",
        "date": "Date",
        "category": "Category",
        "amount": "Amount",
        "notes": "Notes"
    }
}

def translate(key):
    lang = st.session_state.get("lang", "eu")
    return TRANSLATIONS[lang].get(key, key)