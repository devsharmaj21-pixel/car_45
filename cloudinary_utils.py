import streamlit as st

def is_configured():
    try:
        st.secrets["cloudinary"]["cloud_name"]
        return True
    except Exception:
        return False

def upload_image(file, folder="car_king_mauranipur"):
    if not file:
        return ""
    try:
        import cloudinary, cloudinary.uploader
        cloudinary.config(
            cloud_name=st.secrets["cloudinary"]["cloud_name"],
            api_key=st.secrets["cloudinary"]["api_key"],
            api_secret=st.secrets["cloudinary"]["api_secret"],
            secure=True,
        )
        result = cloudinary.uploader.upload(file, folder=folder)
        return result.get("secure_url", "")
    except KeyError:
        st.error("⚠️ Cloudinary keys missing — secrets.toml check karo.")
        return ""
    except Exception as e:
        st.error(f"⚠️ Image upload failed: {e}")
        return ""
