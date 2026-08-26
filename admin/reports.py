import streamlit as st, pandas as pd
import plotly.graph_objects as go
from database import init_db, get_all_cars, get_all_leads, get_all_bookings, car_stats
from theme import inject_css, sidebar_nav, page_header, PRIMARY
from auth import require_admin

st.set_page_config(page_title="Reports | Car King Mauranipur", page_icon="👑", layout="wide")
init_db(); inject_css(); require_admin(); sidebar_nav()
page_header("📊 Reports & Analytics", "Business ka poora overview ek jagah.")

stats = car_stats()
leads = get_all_leads()
books = get_all_bookings()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Cars",     stats["total"])
c2.metric("Total Leads",    len(leads))
c3.metric("Total Bookings", len(books))
c4.metric("Total Sales",    f"₹{stats['total_sales']:,.0f}")

st.write("")
l,r = st.columns(2)

with l:
    st.markdown("<div class='ck-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='ck-panel-title'>Inventory by Status</div>", unsafe_allow_html=True)
    sd = {"Available":stats["available"],"Reserved":stats["reserved"],
          "Sold":stats["sold"],"Under Review":stats["under_review"]}
    if sum(sd.values()):
        fig = go.Figure(go.Bar(x=list(sd.keys()), y=list(sd.values()),
            marker_color=["#16A34A","#D97706","#DC2626","#2563EB"]))
        fig.update_layout(height=280, margin=dict(l=10,r=10,t=10,b=10),
            plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    else:
        st.info("Data nahi hai.")
    st.markdown("</div>", unsafe_allow_html=True)

with r:
    st.markdown("<div class='ck-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='ck-panel-title'>Leads by Status</div>", unsafe_allow_html=True)
    if leads:
        df = pd.DataFrame(leads)
        vc = df["status"].value_counts()
        fig2 = go.Figure(go.Pie(labels=vc.index, values=vc.values, hole=0.55,
            marker=dict(colors=["#2563EB","#D97706","#16A34A"])))
        fig2.update_layout(height=280, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
    else:
        st.info("Koi lead nahi hai.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='ck-panel'>", unsafe_allow_html=True)
st.markdown("<div class='ck-panel-title'>Category-wise Inventory</div>", unsafe_allow_html=True)
if stats["by_category"]:
    df2 = pd.DataFrame(stats["by_category"])
    fig3 = go.Figure(go.Bar(x=df2["category"], y=df2["c"], marker_color=PRIMARY))
    fig3.update_layout(height=260, margin=dict(l=10,r=10,t=10,b=10),
        plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})
st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.markdown("<div class='ck-panel'>", unsafe_allow_html=True)
st.markdown("<div class='ck-panel-title'>⬇️ Export Data</div>", unsafe_allow_html=True)
e1,e2,e3 = st.columns(3)
cars = get_all_cars()
if cars:
    e1.download_button("⬇️ Download Inventory", pd.DataFrame(cars).to_csv(index=False),
                       "inventory.csv", "text/csv", use_container_width=True)
if leads:
    e2.download_button("⬇️ Download Leads", pd.DataFrame(leads).to_csv(index=False),
                       "leads.csv", "text/csv", use_container_width=True)
if books:
    e3.download_button("⬇️ Download Bookings", pd.DataFrame(books).to_csv(index=False),
                       "bookings.csv", "text/csv", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
