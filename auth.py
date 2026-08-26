import streamlit as st
from theme import switch_page

def require_admin():
    if not st.session_state.get("admin_logged_in"):
        st.error("🔐 Admin login required.")
        if st.button("→ Login Page", type="primary"):
            switch_page("admin_login.py")
        st.stop()

def do_logout():
    st.session_state["admin_logged_in"] = False
