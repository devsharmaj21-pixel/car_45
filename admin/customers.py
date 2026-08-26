import streamlit as st
from database import init_db, add_customer, get_all_customers, delete_customer
from theme import inject_css, sidebar_nav, page_header
from auth import require_admin

st.set_page_config(page_title="Customers | Car King Mauranipur", page_icon="👑", layout="wide")
init_db(); inject_css(); require_admin(); sidebar_nav()
page_header("👥 Customers", "Customer database manage karo.")

tab1, tab2 = st.tabs(["👥 All Customers", "➕ Add Customer"])

with tab2:
    st.markdown("<div class='ck-card'>", unsafe_allow_html=True)
    with st.form("cust_form", clear_on_submit=True):
        c1,c2 = st.columns(2)
        name  = c1.text_input("Full Name *")
        phone = c1.text_input("Phone *")
        email = c2.text_input("Email")
        addr  = c2.text_input("Address")
        notes = st.text_area("Notes")
        if st.form_submit_button("Add Customer", type="primary", use_container_width=True):
            if not name or not phone:
                st.error("Naam aur phone zaroori hai.")
            else:
                add_customer({"name":name,"phone":phone,"email":email,"address":addr,"notes":notes})
                st.success(f"Customer added: {name}"); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with tab1:
    search = st.text_input("🔍 Search by name or phone")
    custs  = get_all_customers(search=search)
    st.caption(f"{len(custs)} customer(s)")
    for cu in custs:
        st.markdown("<div class='ck-card'>", unsafe_allow_html=True)
        c1,c2,c3 = st.columns([2,3,1])
        c1.markdown(f"**{cu['name']}**\n\n📞 {cu['phone']}")
        if cu.get("email"):   c2.write(f"✉️ {cu['email']}")
        if cu.get("address"): c2.caption(f"📍 {cu['address']}")
        if cu.get("notes"):   c2.caption(f"📝 {cu['notes']}")
        if c3.button("🗑️ Delete", key=f"dc_{cu['id']}", use_container_width=True):
            delete_customer(cu["id"]); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
