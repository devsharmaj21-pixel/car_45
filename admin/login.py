import streamlit as st
from theme import inject_css, switch_page

st.set_page_config(page_title="Admin Login | Car King Mauranipur",
                   page_icon="🔐", layout="centered",
                   initial_sidebar_state="collapsed")
inject_css()
st.markdown("""
<style>
[data-testid="collapsedControl"]{display:none!important;}
section[data-testid="stSidebar"]{display:none!important;}
</style>""", unsafe_allow_html=True)

_, col, _ = st.columns([1, 2, 1])
with col:
    st.markdown("""
    <div style="text-align:center;padding:2rem 0 1.5rem;">
      <div style="font-size:3rem;">👑</div>
      <div style="font-size:1.5rem;font-weight:800;color:#6D28D9;">Car King Mauranipur</div>
      <div style="color:#6B7280;font-size:.88rem;margin-top:.3rem;">Admin Panel Login</div>
    </div>""", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="ck-card">', unsafe_allow_html=True)
        username = st.text_input("👤 Username", placeholder="Enter username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter password")

        if st.button("Login →", type="primary", use_container_width=True):
            try:
                cu = st.secrets["admin"]["username"]
                cp = st.secrets["admin"]["password"]
            except Exception:
                cu, cp = "admin", "carking2024"

            if username == cu and password == cp:
                st.session_state["admin_logged_in"] = True
                st.success("✅ Login successful!")
                switch_page("dashboard.py")
            else:
                st.error("❌ Galat username ya password.")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Wapas Public Site Pe", use_container_width=True):
            switch_page("app.py")
