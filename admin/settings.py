import streamlit as st, json, os
from database import init_db
from theme import inject_css, sidebar_nav, page_header
from auth import require_admin

st.set_page_config(page_title="Settings | Car King Mauranipur", page_icon="👑", layout="wide")
init_db(); inject_css(); require_admin(); sidebar_nav()
page_header("⚙️ Settings", "Business details aur partner contact numbers.")

SF = os.path.join(os.path.dirname(__file__), "..", "settings.json")

def load():
    d = {"business_name":"Car King Mauranipur",
         "tagline":"45+ Years Collective Expertise | Serving since 5+ Years"}
    for i in range(1,4): d[f"partner_{i}_name"]=""; d[f"partner_{i}_phone"]=""
    if os.path.exists(SF):
        with open(SF) as f: return {**d, **json.load(f)}
    return d

def save(d):
    with open(SF,"w") as f: json.dump(d, f, indent=2)

s = load()
tab1, tab2 = st.tabs(["🏢 Business Info", "👥 Partner Numbers"])

with tab1:
    st.markdown("<div class='ck-card'>", unsafe_allow_html=True)
    with st.form("biz_form"):
        bname = st.text_input("Business Name", value=s["business_name"])
        tag   = st.text_input("Tagline",       value=s["tagline"])
        if st.form_submit_button("💾 Save", type="primary", use_container_width=True):
            s["business_name"] = bname; s["tagline"] = tag
            save(s); st.success("Saved!")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='ck-card'>", unsafe_allow_html=True)
    st.markdown("**Teeno Partners ke Mobile Numbers** — customers ko WhatsApp/Call buttons me dikhenge.")
    with st.form("partners_form"):
        for i in range(1,4):
            st.markdown(f"**Partner {i}**")
            p1,p2 = st.columns(2)
            p1.text_input(f"Partner {i} Name",   value=s.get(f"partner_{i}_name",""),  key=f"pn{i}")
            p2.text_input(f"Partner {i} Mobile",  value=s.get(f"partner_{i}_phone",""), key=f"pp{i}", placeholder="10-digit number")
        if st.form_submit_button("💾 Save Partner Numbers", type="primary", use_container_width=True):
            for i in range(1,4):
                s[f"partner_{i}_name"]  = st.session_state[f"pn{i}"]
                s[f"partner_{i}_phone"] = st.session_state[f"pp{i}"]
            save(s); st.success("Partner numbers saved!"); st.rerun()
    st.markdown("---")
    st.markdown("**Current Partners:**")
    any_saved = False
    for i in range(1,4):
        n = s.get(f"partner_{i}_name",""); p = s.get(f"partner_{i}_phone","")
        if n or p:
            st.markdown(f"**{n or f'Partner {i}'}** — 📞 {p or 'Not added'}")
            any_saved = True
    if not any_saved: st.info("Abhi koi partner number save nahi hua.")
    st.markdown("</div>", unsafe_allow_html=True)
