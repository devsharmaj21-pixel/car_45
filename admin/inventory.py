import streamlit as st
from database import init_db, get_all_cars, get_car, update_car, delete_car
from theme import inject_css, sidebar_nav, page_header, pill
from auth import require_admin

st.set_page_config(page_title="Inventory | Car King Mauranipur", page_icon="👑", layout="wide")
init_db(); inject_css(); require_admin(); sidebar_nav()
page_header("🚘 Premium Inventory", "Cars dekho, edit karo, delete karo.")

f1,f2,f3,f4 = st.columns([2.5,1.2,1.2,1])
search   = f1.text_input("🔍 Search", placeholder="Model, brand ya registration number...")
sf       = f2.selectbox("Status", ["All","Available","Reserved","Sold","Under Review"])
cf       = f3.selectbox("Category", ["All","SUV","Sedan","Hatchback","Luxury","Others"])
view     = f4.selectbox("View", ["Grid","Table"])

cars = get_all_cars(status=sf, category=cf, search=search)
st.caption(f"{len(cars)} car(s) found")

if "edit_id" not in st.session_state: st.session_state.edit_id = None

if st.session_state.edit_id:
    car = get_car(st.session_state.edit_id)
    if car:
        with st.expander(f"✏️ Edit: {car['brand_model']}", expanded=True):
            with st.form("edit_form"):
                e1,e2,e3 = st.columns(3)
                nb = e1.text_input("Brand & Model", value=car["brand_model"])
                np = e1.number_input("Price (₹)", value=int(car["price"]), step=10000)
                cats = ["SUV","Sedan","Hatchback","Luxury","Others"]
                nc = e2.selectbox("Category", cats, index=cats.index(car["category"]) if car["category"] in cats else 0)
                sts = ["Available","Reserved","Sold","Under Review"]
                ns = e2.selectbox("Status", sts, index=sts.index(car["status"]) if car["status"] in sts else 0)
                ny = e3.number_input("Year", value=int(car["year"]), step=1)
                nk = e3.number_input("Kms Driven", value=int(car["kms_driven"]), step=500)
                nd = st.text_area("Description", value=car.get("description",""))
                b1,b2 = st.columns(2)
                save   = b1.form_submit_button("💾 Save", type="primary", use_container_width=True)
                cancel = b2.form_submit_button("✖ Cancel", use_container_width=True)
                if save:
                    update_car(car["id"], {"brand_model":nb,"price":np,"category":nc,
                        "status":ns,"year":ny,"kms_driven":nk,"description":nd})
                    st.session_state.edit_id = None; st.success("Updated!"); st.rerun()
                if cancel:
                    st.session_state.edit_id = None; st.rerun()

st.write("")
if not cars:
    st.info("Koi car nahi mili. Filters change karo ya nayi car add karo.")
elif view == "Grid":
    cols = st.columns(3)
    for i, car in enumerate(cars):
        with cols[i%3]:
            st.markdown("<div class='ck-car-card'>", unsafe_allow_html=True)
            if car.get("image_url"):
                st.image(car["image_url"], use_container_width=True)
            else:
                st.markdown('<div style="height:150px;background:#F3F0FB;border-radius:10px 10px 0 0;display:flex;align-items:center;justify-content:center;font-size:3rem;">🚗</div>', unsafe_allow_html=True)
            st.markdown(f"<div style='padding:.8rem 1rem;'>", unsafe_allow_html=True)
            st.markdown(f"**{car['brand_model']}**")
            st.markdown(pill(car["status"]), unsafe_allow_html=True)
            st.write(f"₹{car['price']:,.0f} | {car['year']} | {car['kms_driven']:,} km")
            b1,b2 = st.columns(2)
            if b1.button("✏️ Edit",   key=f"e{car['id']}", use_container_width=True):
                st.session_state.edit_id = car["id"]; st.rerun()
            if b2.button("🗑️ Delete", key=f"d{car['id']}", use_container_width=True):
                delete_car(car["id"]); st.rerun()
            st.markdown("</div></div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='ck-panel'>", unsafe_allow_html=True)
    hc = st.columns([2.5,1,.8,1.3,1.3,1.2,1.4])
    for h,c in zip(["Car","Category","Year","Price","Kms","Status","Actions"],hc):
        c.markdown(f"**{h}**")
    st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
    for car in cars:
        rc = st.columns([2.5,1,.8,1.3,1.3,1.2,1.4])
        rc[0].write(car["brand_model"])
        rc[1].write(car["category"])
        rc[2].write(car["year"])
        rc[3].write(f"₹{car['price']:,.0f}")
        rc[4].write(f"{car['kms_driven']:,} km")
        rc[5].markdown(pill(car["status"]), unsafe_allow_html=True)
        with rc[6]:
            b1,b2 = st.columns(2)
            if b1.button("✏️", key=f"te{car['id']}"):
                st.session_state.edit_id = car["id"]; st.rerun()
            if b2.button("🗑️", key=f"td{car['id']}"):
                delete_car(car["id"]); st.rerun()
        st.markdown(f"<hr style='margin:3px 0;border-color:#F0EEFA;'>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
