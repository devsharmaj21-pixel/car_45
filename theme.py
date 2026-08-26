import streamlit as st
import json, os
from streamlit.errors import StreamlitAPIException

PRIMARY      = "#6D28D9"
PRIMARY_DARK = "#4C1D95"
PRIMARY_LIGHT= "#EDE9FE"
SUCCESS      = "#16A34A"; SUCCESS_BG = "#DCFCE7"
WARNING      = "#D97706"; WARNING_BG = "#FEF3C7"
DANGER       = "#DC2626"; DANGER_BG  = "#FEE2E2"
INFO         = "#2563EB"; INFO_BG    = "#DBEAFE"
MUTED        = "#6B7280"; BORDER     = "#E5E7EB"
BG           = "#F5F3FF"; WHITE      = "#FFFFFF"
DARK         = "#1E1B2E"

STATUS_COLORS = {
    "Available":   (SUCCESS, SUCCESS_BG),
    "Reserved":    (WARNING, WARNING_BG),
    "Sold":        (DANGER,  DANGER_BG),
    "Under Review":(INFO,    INFO_BG),
    "New":         (INFO,    INFO_BG),
    "Contacted":   (WARNING, WARNING_BG),
    "Closed":      (SUCCESS, SUCCESS_BG),
    "Confirmed":   (SUCCESS, SUCCESS_BG),
    "Pending":     (WARNING, WARNING_BG),
    "Cancelled":   (DANGER,  DANGER_BG),
}

def inject_css():
    st.markdown(f"""
    <style>
      /* ── Base ── */
      .stApp {{ background:{BG}; }}
      .block-container {{ padding:1.5rem 2rem 2rem !important; max-width:1400px; }}

      /* ── Sidebar ── */
      section[data-testid="stSidebar"] {{
        background:{WHITE}; border-right:1px solid {BORDER};
        min-width:220px !important; max-width:240px !important;
      }}
      section[data-testid="stSidebar"] .stButton>button {{
        width:100%; text-align:left; background:transparent; border:none;
        color:{DARK}; font-weight:500; padding:.6rem 1rem;
        border-radius:10px; margin-bottom:2px; font-size:.9rem;
      }}
      section[data-testid="stSidebar"] .stButton>button:hover {{
        background:{PRIMARY_LIGHT}; color:{PRIMARY_DARK};
      }}

      /* ── Cards ── */
      .ck-card {{
        background:{WHITE}; border-radius:16px;
        border:1px solid {BORDER}; padding:1.2rem 1.4rem;
        margin-bottom:1rem;
      }}
      .ck-stat {{
        background:{WHITE}; border-radius:16px;
        border:1px solid {BORDER}; padding:1.1rem 1.2rem;
        height:100%;
      }}
      .ck-stat-icon {{
        width:44px; height:44px; border-radius:12px;
        display:inline-flex; align-items:center; justify-content:center;
        font-size:1.3rem; margin-bottom:.6rem;
      }}
      .ck-stat-val {{ font-size:1.55rem; font-weight:800; color:{DARK}; line-height:1.1; }}
      .ck-stat-label {{ color:{MUTED}; font-size:.84rem; margin-top:.1rem; }}
      .ck-stat-delta {{ color:{SUCCESS}; font-size:.76rem; margin-top:.35rem; font-weight:600; }}

      /* ── Panel (chart/table container) ── */
      .ck-panel {{
        background:{WHITE}; border-radius:16px;
        border:1px solid {BORDER}; padding:1.3rem 1.4rem;
        margin-bottom:1rem; height:100%;
      }}
      .ck-panel-title {{ font-weight:700; font-size:1rem; color:{DARK}; margin-bottom:.8rem; }}

      /* ── Hero banner ── */
      .ck-hero {{
        background:linear-gradient(120deg,{PRIMARY_DARK} 0%,{PRIMARY} 50%,#C2410C 100%);
        border-radius:18px; padding:2rem 2.5rem; color:white;
        margin-bottom:1.2rem; position:relative; overflow:hidden;
      }}
      .ck-hero-title {{ font-size:2rem; font-weight:800; margin-bottom:.25rem; }}
      .ck-hero-sub   {{ opacity:.88; font-size:.95rem; margin-bottom:1.2rem; }}

      /* ── Status pill ── */
      .ck-pill {{
        display:inline-block; padding:.18rem .7rem;
        border-radius:999px; font-size:.76rem; font-weight:700;
      }}

      /* ── Activity row ── */
      .ck-act {{ display:flex; gap:.7rem; padding:.55rem 0; border-bottom:1px solid {BORDER}; align-items:flex-start; }}
      .ck-act-icon {{ font-size:1.1rem; margin-top:.05rem; }}
      .ck-act-title {{ font-weight:600; font-size:.86rem; color:{DARK}; }}
      .ck-act-time  {{ color:#9CA3AF; font-size:.73rem; }}

      /* ── Quick action btn ── */
      .ck-qa {{
        background:{PRIMARY_LIGHT}; border-radius:14px;
        padding:1rem .8rem; text-align:center;
        color:{PRIMARY_DARK}; font-weight:700; font-size:.82rem;
        cursor:pointer; border:1px solid #DDD6FE;
      }}

      /* ── Table row ── */
      .ck-tr {{ padding:.45rem 0; border-bottom:1px solid {BORDER}; }}

      /* ── Inventory car card ── */
      .ck-car-card {{
        background:{WHITE}; border-radius:16px;
        border:1px solid {BORDER}; overflow:hidden;
        transition:box-shadow .2s; margin-bottom:1rem;
      }}
      .ck-car-card:hover {{ box-shadow:0 6px 28px rgba(109,40,217,.13); }}

      /* ── Metric override ── */
      div[data-testid="stMetric"] {{
        background:{WHITE}; border:1px solid {BORDER};
        border-radius:12px; padding:.7rem 1rem;
      }}

      /* ── Primary button ── */
      .stButton>button[kind="primary"],
      .stButton>button[data-testid*="primary"] {{
        background:{PRIMARY} !important; border-color:{PRIMARY} !important;
        border-radius:10px !important; font-weight:600 !important;
      }}
      .stButton>button[kind="primary"]:hover {{
        background:{PRIMARY_DARK} !important;
      }}

      /* ── Input ── */
      .stTextInput>div>div>input, .stSelectbox>div>div,
      .stNumberInput>div>div>input, .stTextArea>div>textarea {{
        border-radius:10px !important;
      }}

      /* ── Tab ── */
      .stTabs [data-baseweb="tab"] {{ font-weight:600; }}
      .stTabs [aria-selected="true"] {{ color:{PRIMARY} !important; }}
      .stTabs [data-baseweb="tab-highlight"] {{ background:{PRIMARY} !important; }}

      /* Hide streamlit default elements ── */
      #MainMenu {{ visibility:hidden; }}
      footer {{ visibility:hidden; }}
      header {{ visibility:hidden; }}
    </style>
    """, unsafe_allow_html=True)

def pill(status):
    color, bg = STATUS_COLORS.get(status, (MUTED, "#F3F4F6"))
    return f'<span class="ck-pill" style="color:{color};background:{bg};">{status}</span>'

def page_header(title, sub=""):
    sub_html = f'<p style="color:{MUTED};margin:0;font-size:.93rem;">{sub}</p>' if sub else ""
    st.markdown(f"""
    <div style="margin-bottom:1rem;">
      <h1 style="margin:0;color:{DARK};font-size:1.75rem;">{title}</h1>
      {sub_html}
    </div>""", unsafe_allow_html=True)

def switch_page(page):
    root = os.path.dirname(__file__)
    candidates = [
        os.path.join(root, page if page == "app.py" else os.path.join("pages", page)),
        os.path.join("..", "pages", page) if page != "app.py" else os.path.join("..", page),
    ]
    for target in candidates:
        try:
            st.switch_page(target)
            return
        except StreamlitAPIException:
            continue
    st.switch_page(candidates[0])

def load_settings():
    f = os.path.join(os.path.dirname(__file__), "settings.json")
    defaults = {f"partner_{i}_{k}":"" for i in range(1,4) for k in ["name","phone"]}
    defaults.update({"business_name":"Car King Mauranipur",
                     "tagline":"45+ Years Collective Expertise | Serving since 5+ Years"})
    if os.path.exists(f):
        import json
        with open(f) as fp:
            return {**defaults, **json.load(fp)}
    return defaults

def sidebar_nav():
    settings = load_settings()
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:.8rem 0 .4rem;">
          <div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.5rem;">
            <span style="font-size:1.6rem;">👑</span>
            <div>
              <div style="font-weight:800;font-size:1rem;color:{PRIMARY};line-height:1.2;">
                {settings['business_name']}</div>
              <div style="font-size:.68rem;color:{PRIMARY_DARK};">
                {settings['tagline']}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.caption("MAIN MENU")
        menu = [
            ("🏠  Dashboard",          "admin/dashboard.py"),
            ("🚘  Premium Inventory",  "admin/inventory.py"),
            ("➕  Add New Car",        "admin/add_car.py"),
            ("📥  Leads & Inquiries",  "admin/leads.py"),
            ("📅  Bookings",           "admin/bookings.py"),
            ("👥  Customers",          "admin/customers.py"),
            ("📊  Reports & Analytics","admin/reports.py"),
            ("⚙️  Settings",           "admin/settings.py"),
        ]
        for label, target in menu:
            route = target.replace("admin/", "pages/")
            if st.button(label, key=f"nav_{target}", use_container_width=True):
                switch_page(route.replace("pages/", ""))
        st.markdown("---")
        st.caption("OTHER")
        if st.button("🌐  View Public Site", key="nav_pub", use_container_width=True):
            switch_page("app.py")
        if st.button("🚪  Logout", key="nav_logout", use_container_width=True):
            st.session_state["admin_logged_in"] = False
            switch_page("app.py")
