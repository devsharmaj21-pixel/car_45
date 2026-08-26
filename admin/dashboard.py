import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from database import init_db, car_stats, get_all_cars, get_recent_activity
from theme import inject_css, sidebar_nav, page_header, pill, load_settings, switch_page, PRIMARY, BORDER, MUTED, DARK
from auth import require_admin

st.set_page_config(page_title="Dashboard | Car King Mauranipur",
                   page_icon="👑", layout="wide")
init_db(); inject_css(); require_admin(); sidebar_nav()

settings = load_settings()
stats    = car_stats()

# ── Header ──
h1, h2 = st.columns([5,1])
with h1: page_header("Dashboard", "Welcome back, Admin! Here's what's happening with your inventory.")
with h2:
    if st.button("➕ Add New Car", type="primary", use_container_width=True):
        switch_page("add_car.py")

# ── Hero Banner ──
st.markdown(f"""
<div class='ck-hero'>
  <div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;'>
    <div>
      <div class='ck-hero-title'>👑 {settings['business_name']}</div>
      <div class='ck-hero-sub'>{settings['tagline']}</div>
      <div style='display:flex;gap:.6rem;flex-wrap:wrap;'>
        <span style='background:rgba(255,255,255,.18);padding:.28rem .85rem;border-radius:999px;font-size:.8rem;'>🚗 {stats['available']} Cars Available</span>
        <span style='background:rgba(255,255,255,.18);padding:.28rem .85rem;border-radius:999px;font-size:.8rem;'>⭐ 98% Satisfaction</span>
        <span style='background:rgba(255,255,255,.18);padding:.28rem .85rem;border-radius:999px;font-size:.8rem;'>👥 5000+ Customers</span>
      </div>
    </div>
    <div style='font-size:5rem;opacity:.6;'>🏎️</div>
  </div>
</div>""", unsafe_allow_html=True)

# ── Stat Cards ──
def stat_card(icon, bg, val, label, delta=""):
    delta_html = f'<div class="ck-stat-delta">↑ {delta}</div>' if delta else ""
    st.markdown(f"""<div class='ck-stat'>
      <div class='ck-stat-icon' style='background:{bg};'>{icon}</div>
      <div class='ck-stat-val'>{val}</div>
      <div class='ck-stat-label'>{label}</div>
      {delta_html}
    </div>""", unsafe_allow_html=True)

c1,c2,c3,c4,c5 = st.columns(5)
with c1: stat_card("🚗","#EDE9FE", stats["available"], "Total Cars Available", "Live count")
with c2: stat_card("⭐","#FFEDD5", "98%", "Customer Satisfaction", "2% vs last month")
with c3: stat_card("✅","#DCFCE7", "45+", "Years of Expertise")
with c4: stat_card("👥","#DBEAFE", "5000+", "Happy Customers")
with c5:
    sales = stats["total_sales"]
    val = f"₹{sales/1e7:.2f} Cr" if sales >= 1e7 else f"₹{sales:,.0f}"
    stat_card("₹","#EDE9FE", val, "Total Sales")

st.write("")

# ── Charts Row ──
left, mid, right = st.columns([2.1, 1.3, 1.3])

with left:
    st.markdown("<div class='ck-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='ck-panel-title'>📈 Inventory Overview</div>", unsafe_allow_html=True)
    all_cars = get_all_cars()
    if all_cars:
        df = pd.DataFrame(all_cars)
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        df["date"] = df["created_at"].dt.date
        daily = df.groupby("date").size().cumsum().reset_index(name="n")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily["date"], y=daily["n"],
            mode="lines+markers", line=dict(color=PRIMARY, width=3),
            fill="tozeroy", fillcolor="rgba(109,40,217,0.08)",
            marker=dict(size=6, color=PRIMARY)))
        fig.update_layout(height=260, margin=dict(l=10,r=10,t=10,b=10),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#F0EEFA"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    else:
        st.info("Koi car nahi hai abhi — Add New Car se shuru karo!")
    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("Added",   stats["total"])
    m2.metric("Sold",    stats["sold"])
    m3.metric("Available", stats["available"])
    m4.metric("Reserved",  stats["reserved"])
    m5.metric("Review",    stats["under_review"])
    st.markdown("</div>", unsafe_allow_html=True)

with mid:
    st.markdown("<div class='ck-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='ck-panel-title'>🍩 Top Categories</div>", unsafe_allow_html=True)
    bc = stats["by_category"]
    if bc:
        labels = [x["category"] for x in bc]
        values = [x["c"] for x in bc]
        colors = ["#6D28D9","#2563EB","#16A34A","#D97706","#9CA3AF"]
        fig2 = go.Figure(go.Pie(labels=labels, values=values, hole=0.62,
            marker=dict(colors=colors[:len(labels)]), textinfo="none"))
        fig2.update_layout(height=210, margin=dict(l=0,r=0,t=0,b=0), showlegend=False,
            annotations=[dict(text=f"<b>{stats['total']}</b><br>Total", showarrow=False, font_size=15)])
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        t = stats["total"] or 1
        for cat, clr in zip(bc, colors):
            pct = round(cat["c"]/t*100)
            st.markdown(f"""<div style='display:flex;justify-content:space-between;
              font-size:.82rem;padding:2px 0;color:{DARK};'>
              <span><span style='color:{clr};'>●</span> {cat['category']}</span>
              <span>{cat['c']} ({pct}%)</span></div>""", unsafe_allow_html=True)
    else:
        st.info("Cars add karo categories dikhne ke liye.")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='ck-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='ck-panel-title'>🔔 Recent Activity</div>", unsafe_allow_html=True)
    acts = get_recent_activity(7)
    icons = {"car_added":"🚗","lead_added":"📥","booking_added":"📅","car_sold":"💰"}
    if acts:
        for a in acts:
            icon = icons.get(a["activity_type"],"🔔")
            try:
                diff = datetime.now() - datetime.fromisoformat(a["created_at"])
                mins = int(diff.total_seconds()//60)
                t = f"{mins} min ago" if mins < 60 else f"{mins//60} hr ago"
            except Exception:
                t = ""
            st.markdown(f"""<div class='ck-act'>
              <div class='ck-act-icon'>{icon}</div>
              <div><div class='ck-act-title'>{a['description']}</div>
              <div class='ck-act-time'>{t}</div></div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("Koi activity nahi hai abhi.")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ── Latest Inventory + Quick Actions ──
bot_l, bot_r = st.columns([2.4, 1])

with bot_l:
    st.markdown("<div class='ck-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='ck-panel-title'>🚘 Latest Inventory</div>", unsafe_allow_html=True)
    latest = get_all_cars()[:6]
    if latest:
        hcols = st.columns([2.5,1,.8,1.3,1.3,1.3])
        for h,c in zip(["Car Details","Category","Year","Price","Kms","Status"],hcols):
            c.markdown(f"<span style='font-size:.78rem;font-weight:700;color:{MUTED};'>{h}</span>", unsafe_allow_html=True)
        for car in latest:
            st.markdown(f"<hr style='margin:4px 0;border-color:{BORDER};'>", unsafe_allow_html=True)
            rc = st.columns([2.5,1,.8,1.3,1.3,1.3])
            rc[0].markdown(f"**{car['brand_model']}**  \n<span style='color:#9CA3AF;font-size:.74rem;'>{car.get('registration_number','')}</span>", unsafe_allow_html=True)
            rc[1].write(car["category"])
            rc[2].write(car["year"])
            rc[3].write(f"₹{car['price']:,.0f}")
            rc[4].write(f"{car['kms_driven']:,} km")
            rc[5].markdown(pill(car["status"]), unsafe_allow_html=True)
    else:
        st.info("Inventory khali hai — pehli car add karo!")
    st.markdown("</div>", unsafe_allow_html=True)

with bot_r:
    st.markdown("<div class='ck-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='ck-panel-title'>⚡ Quick Actions</div>", unsafe_allow_html=True)
    qa1, qa2 = st.columns(2)
    with qa1:
        if st.button("➕\nAdd Car", use_container_width=True):    switch_page("add_car.py")
        if st.button("📅\nBookings", use_container_width=True):   switch_page("bookings.py")
    with qa2:
        if st.button("🚘\nInventory", use_container_width=True):  switch_page("inventory.py")
        if st.button("👥\nCustomers", use_container_width=True):  switch_page("customers.py")
    if st.button("📊 Reports & Analytics", use_container_width=True): switch_page("reports.py")
    if st.button("📥 Leads & Inquiries",   use_container_width=True): switch_page("leads.py")
    st.markdown("</div>", unsafe_allow_html=True)
