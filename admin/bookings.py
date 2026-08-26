import streamlit as st
from datetime import date
from database import init_db, add_booking, get_all_bookings, update_booking_status, delete_booking, get_all_cars
from theme import inject_css, sidebar_nav, page_header, pill
from auth import require_admin

st.set_page_config(page_title="Bookings | Car King Mauranipur", page_icon="👑", layout="wide")
init_db(); inject_css(); require_admin(); sidebar_nav()
page_header("📅 Bookings", "Car bookings manage karo.")

tab1, tab2 = st.tabs(["📅 All Bookings", "➕ New Booking"])

with tab2:
    st.markdown("<div class='ck-card'>", unsafe_allow_html=True)
    with st.form("booking_form", clear_on_submit=True):
        c1,c2 = st.columns(2)
        cname = c1.text_input("Customer Name *")
        phone = c1.text_input("Phone *")
        cars  = get_all_cars()
        opts  = {f"{c['brand_model']} ({c['year']}) — ₹{c['price']:,.0f}":c for c in cars}
        sel   = c2.selectbox("Select Car *", ["-- Select --"] + list(opts.keys()))
        bdate = c2.date_input("Booking Date", value=date.today())
        amount= st.number_input("Token Amount (₹)", min_value=0, value=0, step=1000)
        if st.form_submit_button("Confirm Booking", type="primary", use_container_width=True):
            if not cname or not phone or sel == "-- Select --":
                st.error("Naam, phone aur car select karo.")
            else:
                car = opts[sel]
                add_booking({"customer_name":cname,"phone":phone,"car_id":car["id"],
                    "car_details":car["brand_model"],"booking_date":str(bdate),"amount":amount})
                st.success(f"Booking confirmed for {cname}!"); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with tab1:
    sf = st.selectbox("Filter", ["All","Confirmed","Pending","Cancelled"])
    bks = get_all_bookings(status=sf)
    st.caption(f"{len(bks)} booking(s)")
    for b in bks:
        st.markdown("<div class='ck-card'>", unsafe_allow_html=True)
        c1,c2,c3,c4 = st.columns([2,2,1.2,1.5])
        c1.markdown(f"**{b['customer_name']}**\n\n📞 {b['phone']}")
        c2.write(f"🚗 {b.get('car_details','')}")
        c2.caption(f"📅 {b.get('booking_date','')} | 💰 ₹{b.get('amount',0):,.0f}")
        c3.markdown(pill(b["status"]), unsafe_allow_html=True)
        sts = ["Confirmed","Pending","Cancelled"]
        ns = c4.selectbox("", sts, index=sts.index(b["status"]) if b["status"] in sts else 0,
                          key=f"bs_{b['id']}", label_visibility="collapsed")
        if ns != b["status"]:
            update_booking_status(b["id"], ns); st.rerun()
        if c4.button("🗑️", key=f"db_{b['id']}", use_container_width=True):
            delete_booking(b["id"]); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
