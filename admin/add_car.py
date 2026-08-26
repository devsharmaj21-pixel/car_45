import streamlit as st
from database import init_db, add_car
from cloudinary_utils import upload_image, is_configured
from theme import inject_css, sidebar_nav, page_header
from auth import require_admin

st.set_page_config(page_title="Add New Car | Car King Mauranipur", page_icon="👑", layout="wide")
init_db(); inject_css(); require_admin(); sidebar_nav()

page_header("➕ Add New Car", "Naye car ki details bharo — images Cloudinary pe safe store hongi.")

if not is_configured():
    st.warning("⚠️ Cloudinary setup nahi hai. secrets.toml me keys daalo (free).")

with st.form("add_car_form", clear_on_submit=True):
    st.markdown("<div class='ck-card'>", unsafe_allow_html=True)
    st.markdown("##### 🚗 Basic Details")
    c1,c2,c3 = st.columns(3)
    brand_model  = c1.text_input("Brand & Model *", placeholder="e.g. BMW X5 xDrive40i")
    variant      = c2.text_input("Variant", placeholder="e.g. xDrive40i")
    category     = c3.selectbox("Category *", ["SUV","Sedan","Hatchback","Luxury","Others"])

    c4,c5,c6 = st.columns(3)
    year       = c4.number_input("Year *", min_value=1990, max_value=2027, value=2023, step=1)
    price      = c5.number_input("Price (₹) *", min_value=0, value=500000, step=10000)
    kms_driven = c6.number_input("Kms Driven *", min_value=0, value=10000, step=500)

    st.markdown("##### 📋 More Details")
    c7,c8,c9 = st.columns(3)
    reg_no      = c7.text_input("Registration Number", placeholder="e.g. MP04AB1234")
    fuel_type   = c8.selectbox("Fuel Type", ["Petrol","Diesel","CNG","Electric","Hybrid"])
    transmission= c9.selectbox("Transmission", ["Manual","Automatic"])

    c10,c11 = st.columns(2)
    owner_number = c10.selectbox("Owner Number", ["1st Owner","2nd Owner","3rd Owner","4th+ Owner"])
    status       = c11.selectbox("Status", ["Available","Reserved","Sold","Under Review"])

    description = st.text_area("Description", placeholder="Car ki condition, features, extras...")

    st.markdown("##### 📸 Car Images (up to 3)")
    i1,i2,i3 = st.columns(3)
    img1 = i1.file_uploader("Main Image", type=["jpg","jpeg","png","webp"], key="img1")
    img2 = i2.file_uploader("Image 2", type=["jpg","jpeg","png","webp"], key="img2")
    img3 = i3.file_uploader("Image 3", type=["jpg","jpeg","png","webp"], key="img3")
    st.markdown("</div>", unsafe_allow_html=True)

    submitted = st.form_submit_button("✅ Add Car to Inventory", type="primary", use_container_width=True)

    if submitted:
        if not brand_model or price <= 0:
            st.error("Brand & Model aur Price zaroori hai.")
        else:
            with st.spinner("Car add ho rahi hai..."):
                add_car({
                    "brand_model": brand_model, "variant": variant,
                    "category": category, "year": int(year),
                    "price": float(price), "kms_driven": int(kms_driven),
                    "registration_number": reg_no, "fuel_type": fuel_type,
                    "transmission": transmission, "owner_number": owner_number,
                    "status": status, "description": description,
                    "image_url":   upload_image(img1) if img1 else "",
                    "image_url_2": upload_image(img2) if img2 else "",
                    "image_url_3": upload_image(img3) if img3 else "",
                })
            st.success(f"🎉 {brand_model} inventory me add ho gayi!")
            st.balloons()
