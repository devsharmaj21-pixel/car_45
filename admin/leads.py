import streamlit as st
from database import init_db, add_lead, get_all_leads, update_lead_status, delete_lead, get_all_cars
from theme import inject_css, sidebar_nav, page_header, pill
from auth import require_admin

st.set_page_config(page_title="Leads | Car King Mauranipur", page_icon="👑", layout="wide")
init_db(); inject_css(); require_admin(); sidebar_nav()
page_header("📥 Leads & Inquiries", "Customer inquiries track karo aur follow-up karo.")

tab1, tab2 = st.tabs(["📋 All Leads", "➕ Add Lead"])

with tab2:
    st.markdown("<div class='ck-card'>", unsafe_allow_html=True)
    with st.form("lead_form", clear_on_submit=True):
        c1,c2 = st.columns(2)
        name  = c1.text_input("Customer Name *")
        phone = c1.text_input("Phone *")
        email = c2.text_input("Email")
        cars  = ["Not specified"] + [c["brand_model"] for c in get_all_cars()]
        car_i = c2.selectbox("Car Interested In", cars)
        msg   = st.text_area("Message / Notes")
        if st.form_submit_button("Add Lead", type="primary", use_container_width=True):
            if not name or not phone:
                st.error("Naam aur phone zaroori hai.")
            else:
                add_lead({"name":name,"phone":phone,"email":email,
                    "car_interested":"" if car_i=="Not specified" else car_i,"message":msg})
                st.success(f"Lead added: {name}"); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with tab1:
    sf = st.selectbox("Filter", ["All","New","Contacted","Closed"])
    leads = get_all_leads(status=sf)
    st.caption(f"{len(leads)} lead(s)")
    for lead in leads:
        st.markdown("<div class='ck-card'>", unsafe_allow_html=True)
        c1,c2,c3,c4 = st.columns([2.5,2,1.2,1.5])
        c1.markdown(f"**{lead['name']}**\n\n📞 {lead['phone']}" + (f"\n\n✉️ {lead['email']}" if lead.get("email") else ""))
        if lead.get("car_interested"): c2.write(f"🚗 {lead['car_interested']}")
        if lead.get("message"): c2.caption(lead["message"])
        c3.markdown(pill(lead["status"]), unsafe_allow_html=True)
        sts = ["New","Contacted","Closed"]
        ns = c4.selectbox("Status", sts, index=sts.index(lead["status"]) if lead["status"] in sts else 0,
                          key=f"ls_{lead['id']}", label_visibility="collapsed")
        if ns != lead["status"]:
            update_lead_status(lead["id"], ns); st.rerun()
        if c4.button("🗑️", key=f"dl_{lead['id']}", use_container_width=True):
            delete_lead(lead["id"]); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)