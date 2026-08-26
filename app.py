import streamlit as st, json, os
from database import init_db, get_all_cars
from theme import load_settings

st.set_page_config(page_title="Car King Mauranipur | Premium Cars",
                   page_icon="👑", layout="wide",
                   initial_sidebar_state="collapsed")
init_db()

st.markdown("""
<style>
*{margin:0;padding:0;box-sizing:border-box;}
[data-testid="collapsedControl"]{display:none!important;}
section[data-testid="stSidebar"]{display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}
header,footer,#MainMenu{display:none!important;}
</style>""", unsafe_allow_html=True)

settings  = load_settings()
cars_raw  = get_all_cars(status="Available")
cars_data = [{"id":c["id"],"brand_model":c["brand_model"],"category":c["category"],
              "year":c["year"],"price":c["price"],"kms_driven":c["kms_driven"],
              "fuel_type":c.get("fuel_type",""),"transmission":c.get("transmission",""),
              "owner_number":c.get("owner_number",""),"registration_number":c.get("registration_number",""),
              "description":c.get("description",""),"image_url":c.get("image_url",""),
              "status":c.get("status","Available")} for c in cars_raw]

phones = [{"name":settings.get(f"partner_{i}_name",""),
           "phone":settings.get(f"partner_{i}_phone","")}
          for i in range(1,4) if settings.get(f"partner_{i}_phone","")]

import json as _j
cars_js  = _j.dumps(cars_data,  ensure_ascii=False)
phones_js = _j.dumps(phones,    ensure_ascii=False)

st.page_link("pages/admin_login.py", label="🔐 Admin Login", icon="🔐")

st.components.v1.html(f"""<!DOCTYPE html><html lang='hi'><head>
<meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Car King Mauranipur</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Segoe UI',sans-serif;background:#07071a;overflow-x:hidden;}}
.nav-btn,.cta.secondary{{display:none;}}
/* NAVBAR */
.nav{{position:fixed;top:0;left:0;width:100%;z-index:999;
  background:rgba(10,9,18,.9);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid rgba(180,100,255,.22);
  display:flex;align-items:center;justify-content:space-between;padding:.9rem 2.5rem;}}
.brand-block{{display:flex;flex-direction:column;gap:.12rem;}}
.nav-brand{{font-size:1.25rem;font-weight:900;
  background:linear-gradient(90deg,#FFD700,#FF8C00,#FF69B4,#FFD700);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:.02em;}}
.nav-tag{{color:rgba(255,255,255,.54);font-size:.68rem;}}
.nav-meta{{display:flex;gap:1rem;align-items:center;color:rgba(255,255,255,.72);font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;}}
.nav-meta span{{padding:.38rem .8rem;border:1px solid rgba(255,255,255,.08);border-radius:999px;background:rgba(255,255,255,.02);box-shadow:inset 0 0 20px rgba(255,255,255,.02);}}
.nav-btn{{background:linear-gradient(135deg,#5B21B6,#7C3AED);color:#fff;border:none;
  padding:.62rem 1.2rem;border-radius:999px;font-weight:700;cursor:pointer;font-size:.8rem;
  text-decoration:none;box-shadow:0 8px 24px rgba(109,40,217,.55);transition:all .2s;}}
.nav-btn:hover{{transform:translateY(-2px);box-shadow:0 12px 32px rgba(109,40,217,.75);}}
/* HERO */
.hero{{position:relative;width:min(1320px,94vw);height:calc(100vh - 82px);min-height:620px;
  margin:72px auto 0;display:flex;align-items:center;justify-content:center;overflow:hidden;
  border:1px solid rgba(255,255,255,.12);border-radius:30px;background:rgba(17,12,32,.82);
  box-shadow:0 32px 80px rgba(25,12,46,.72), inset 0 0 40px rgba(255,255,255,.02), 0 0 0 1px rgba(255,255,255,.02);}}
.hero::before{{content:'';position:absolute;inset:0;background:linear-gradient(120deg, rgba(255,255,255,.03), transparent 28%, transparent 72%, rgba(255,255,255,.05));pointer-events:none;}}
.hero-bg{{position:absolute;inset:0;
  background:linear-gradient(135deg,#12091f 0%,#240b43 24%,#1a0f33 48%,#120d22 100%);
  box-shadow:inset 0 0 180px rgba(138,87,255,.2);}}
.hero-bg::before{{content:'';position:absolute;inset:0;
  background:radial-gradient(circle at 18% 20%, rgba(255,188,76,.18), transparent 18%),
    radial-gradient(circle at 78% 14%, rgba(255,105,180,.18), transparent 18%),
    radial-gradient(circle at 54% 78%, rgba(71,99,255,.15), transparent 26%),
    radial-gradient(circle at 50% 48%, rgba(255,255,255,.03), transparent 50%);}}
.hero-glow{{position:absolute;inset:8% 4% auto auto;width:38vw;height:38vw;max-width:460px;max-height:460px;border-radius:50%;
 background:radial-gradient(circle, rgba(255,182,34,.18), rgba(255,102,168,.12) 34%, transparent 68%);filter:blur(34px);}}
.beams{{position:absolute;inset:0;overflow:hidden;}}
.beam{{position:absolute;top:0;width:2px;height:100%;filter:blur(12px);animation:bp ease-in-out infinite alternate;opacity:.9;}}
.beam:nth-child(1){{left:12%;background:linear-gradient(#0000,#b060ff,#0000);animation-duration:3.2s;}}
.beam:nth-child(2){{left:32%;background:linear-gradient(#0000,#ff6090,#0000);animation-duration:4.1s;animation-delay:.7s;}}
.beam:nth-child(3){{left:52%;background:linear-gradient(#0000,#ffb030,#0000);animation-duration:3.7s;animation-delay:1.4s;}}
.beam:nth-child(4){{left:68%;background:linear-gradient(#0000,#30c0ff,#0000);animation-duration:4.5s;animation-delay:.3s;}}
.beam:nth-child(5){{left:86%;background:linear-gradient(#0000,#b060ff,#0000);animation-duration:3.9s;animation-delay:1.1s;}}
@keyframes bp{{from{{opacity:.22;transform:scaleY(.85);}}to{{opacity:1;transform:scaleY(1.15);}}}}
#ptcl{{position:absolute;inset:0;pointer-events:none;}}
.pt{{position:absolute;border-radius:50%;animation:fu linear infinite;}}
@keyframes fu{{0%{{transform:translateY(100vh) scale(0);opacity:0;}}8%{{opacity:1;}}90%{{opacity:.7;}}100%{{transform:translateY(-80px) scale(1.4);opacity:0;}}}}
.hero-inner{{position:relative;z-index:10;width:100%;display:grid;grid-template-columns:1.12fr .88fr;gap:2rem;align-items:center;padding:2rem 1.8rem 1.3rem;}}
.hero-copy{{animation:fid .9s ease both;position:relative;z-index:2;}}
.eyebrow{{color:#d4b4ff;font-size:.7rem;letter-spacing:.24em;font-weight:800;margin-bottom:1rem;text-transform:uppercase;}}
@keyframes fid{{from{{opacity:0;transform:translateY(-35px);}}to{{opacity:1;transform:translateY(0);}}}}
.crown{{font-size:4.2rem;display:block;margin-bottom:.6rem;animation:cp 3s ease-in-out infinite;}}
@keyframes cp{{0%,100%{{transform:scale(1) rotate(-6deg);filter:drop-shadow(0 0 18px rgba(255,215,0,.9));}}50%{{transform:scale(1.18) rotate(6deg);filter:drop-shadow(0 0 36px rgba(255,215,0,.95)) drop-shadow(0 0 80px rgba(255,140,0,.75));}}}}
.ht{{font-size:clamp(2.8rem,5vw,5.6rem);font-weight:900;line-height:.9;letter-spacing:-2px;
  background:linear-gradient(135deg,#FFD700 0%,#FF8C00 20%,#FF1493 36%,#9400D3 52%,#1E90FF 68%,#00FFAA 82%,#FFD700 100%);
  background-size:300% 300%;-webkit-background-clip:text;
  -webkit-text-fill-color:transparent;background-clip:text;animation:tr 5s ease infinite;text-shadow:0 0 22px rgba(255,190,82,.22);}}
.ht span{{display:block;}}
@keyframes tr{{0%{{background-position:0% 50%;}}50%{{background-position:100% 50%;}}100%{{background-position:0% 50%;}}}}
.hsub{{font-size:clamp(.9rem,1.4vw,1.12rem);color:rgba(255,255,255,.82);max-width:560px;
  margin:.9rem 0 1rem;line-height:1.6;}}
.hero-badges{{display:flex;gap:.7rem;flex-wrap:wrap;padding-top:.7rem;}}
.hero-badges span{{display:inline-flex;align-items:center;justify-content:center;padding:.55rem .88rem;border-radius:12px;
  font-size:.72rem;font-weight:800;color:#f5e9ff;letter-spacing:.12em;text-transform:uppercase;
  background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);backdrop-filter:blur(10px);}}
.badges{{display:flex;gap:.6rem;justify-content:flex-start;flex-wrap:wrap;}}
.badge{{padding:.38rem .9rem;border-radius:999px;font-size:.78rem;font-weight:700;border:1px solid rgba(255,255,255,.12);backdrop-filter:blur(8px);animation:bp2 3.5s ease-in-out infinite;}}
.badge:nth-child(1){{color:#FFD700;background:rgba(255,215,0,.08);}}
.badge:nth-child(2){{color:#FF69B4;background:rgba(255,105,180,.08);animation-delay:.5s;}}
.badge:nth-child(3){{color:#00CED1;background:rgba(0,206,209,.08);animation-delay:1s;}}
@keyframes bp2{{0%,100%{{transform:scale(1);}}50%{{transform:scale(1.06);}}}}
.cta-row{{display:flex;align-items:center;gap:1rem;flex-wrap:wrap;margin-top:1.5rem;}}
.cta{{display:inline-flex;align-items:center;justify-content:center;padding:.9rem 1.5rem;border-radius:14px;text-decoration:none;font-weight:800;transition:all .2s;}}
.cta.primary{{background:linear-gradient(135deg,#f59e0b,#f97316);color:#fff;box-shadow:0 12px 32px rgba(245,158,11,.35);}}
.cta.secondary{{background:rgba(255,255,255,.06);color:#fff;border:1px solid rgba(255,255,255,.12);}}
.cta:hover{{transform:translateY(-2px);}}
.hero-stats{{display:flex;gap:1.2rem;flex-wrap:wrap;margin-top:2rem;}}
.hero-stats div{{min-width:120px;padding:1rem 1.2rem;border:1px solid rgba(255,255,255,.08);border-radius:16px;background:linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.02));backdrop-filter:blur(6px);box-shadow:inset 0 0 20px rgba(255,255,255,.03);}}
.hero-stats strong{{display:block;color:#fff;font-size:1.4rem;font-weight:900;}}
.hero-stats span{{color:rgba(255,255,255,.7);font-size:.72rem;}}
.hero-showcase{{position:relative;display:flex;align-items:center;justify-content:center;min-height:520px;animation:fid .9s ease .25s both;}}
.showcase-panel{{position:relative;width:min(430px,88%);background:linear-gradient(180deg,rgba(255,255,255,.11),rgba(255,255,255,.02));
  border:1px solid rgba(255,255,255,.12);border-radius:28px;padding:1.25rem 1.3rem;backdrop-filter:blur(12px);box-shadow:0 30px 80px rgba(59,22,122,.42), inset 0 0 28px rgba(255,255,255,.04);}}
.showcase-panel::before{{content:'';position:absolute;inset:-1px;border-radius:28px;padding:1px;background:linear-gradient(135deg,rgba(255,214,102,.85),rgba(192,132,252,.55),rgba(59,130,246,.52));-webkit-mask:linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none;}}
.panel-top{{display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;}}
.label{{font-size:.7rem;text-transform:uppercase;letter-spacing:.16em;color:#d8c5ff;}}
.status{{padding:.35rem .7rem;border-radius:999px;background:rgba(34,197,94,.12);color:#86efac;border:1px solid rgba(134,239,172,.22);font-size:.68rem;font-weight:700;}}
.car-name{{font-size:2.6rem;font-weight:900;line-height:1;color:#fff;letter-spacing:-.06em;}}
.car-meta{{margin-top:.6rem;font-size:.9rem;color:rgba(255,255,255,.66);}}
.car-visual{{display:flex;align-items:center;justify-content:center;height:170px;font-size:7.5rem;margin:1rem 0 1.2rem;filter:drop-shadow(0 10px 30px rgba(255,186,59,.55));animation:floatCar 3.8s ease-in-out infinite;}}
@keyframes floatCar{{0%,100%{{transform:translateY(0) rotate(0deg);}}50%{{transform:translateY(-10px) rotate(-1deg);}}}}
.spec-row{{display:flex;justify-content:space-between;align-items:center;padding-top:.7rem;border-top:1px solid rgba(255,255,255,.08);font-size:1rem;font-weight:800;color:#fff;}}
.spec-row span:last-child{{color:#ffd166;}}
.mini-card{{position:absolute;padding:.7rem 1rem;border-radius:14px;background:rgba(16,14,33,.72);border:1px solid rgba(255,255,255,.08);color:#fff;font-weight:700;font-size:.78rem;backdrop-filter:blur(10px);box-shadow:0 8px 18px rgba(0,0,0,.2);}}
.card-1{{top:18%;left:1%;transform:rotate(-12deg);background:linear-gradient(145deg, rgba(109,40,217,.78), rgba(17,24,39,.8));}}
.card-2{{right:4%;bottom:16%;transform:rotate(10deg);background:linear-gradient(145deg, rgba(59,130,246,.72), rgba(17,24,39,.8));}}
.card-3{{left:18%;bottom:4%;transform:rotate(-8deg);background:linear-gradient(145deg, rgba(245,158,11,.75), rgba(17,24,39,.8));}}
.scroll-hint{{position:absolute;bottom:210px;left:50%;transform:translateX(-50%);color:rgba(255,255,255,.35);font-size:.74rem;text-align:center;animation:fid .9s ease .9s both;}}
.arr{{font-size:1.4rem;display:block;animation:ab 1.6s ease-in-out infinite;}}
@keyframes ab{{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(9px);}}}}
/* SLIDING CARS */
.cstrip{{position:absolute;bottom:0;width:100%;height:195px;overflow:hidden;
  -webkit-mask-image:linear-gradient(90deg,#0000,#fff 8%,#fff 92%,#0000);
  mask-image:linear-gradient(90deg,#0000,#fff 8%,#fff 92%,#0000);}}
.ctrack{{display:flex;align-items:flex-end;height:100%;
  animation:sl 20s linear infinite;width:max-content;}}
.cs{{font-size:6.5rem;margin:0 2.2rem;
  animation:cb .55s ease-in-out infinite alternate;
  filter:drop-shadow(0 0 28px rgba(160,80,255,.9)) drop-shadow(0 0 55px rgba(255,150,50,.5));}}
.cs:nth-child(2n){{font-size:7.5rem;animation-delay:.27s;
  filter:drop-shadow(0 0 28px rgba(255,100,150,.9)) drop-shadow(0 0 55px rgba(100,200,255,.5));}}
.cs:nth-child(3n){{animation-delay:.14s;font-size:7rem;
  filter:drop-shadow(0 0 28px rgba(255,215,0,.9)) drop-shadow(0 0 55px rgba(150,50,255,.5));}}
@keyframes sl{{0%{{transform:translateX(0);}}100%{{transform:translateX(-50%);}}}}
@keyframes cb{{0%{{transform:translateY(0);}}100%{{transform:translateY(-16px);}}}}
.road{{position:absolute;bottom:0;width:100%;height:5px;
  background:linear-gradient(90deg,#ff6b00,#ff00aa,#aa00ff,#0088ff,#00ffaa,#ffff00,#ff6b00);
  background-size:400% 100%;animation:rs 3s linear infinite;
  box-shadow:0 0 25px rgba(255,150,50,.9),0 0 50px rgba(180,50,255,.6);}}
@keyframes rs{{from{{background-position:0 50%;}}to{{background-position:400% 50%;}}}}
/* FLAGSHIP DEALERSHIP SECTIONS */
.flagship-band{{padding:1.2rem 2.5rem 0;}}
.band-inner{{max-width:1440px;margin:0 auto;background:linear-gradient(135deg,rgba(255,210,87,.12),rgba(167,139,250,.1),rgba(59,130,246,.08));
  border:1px solid rgba(255,255,255,.08);border-radius:22px;padding:1rem 1.2rem;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;}}
.band-copy{{display:flex;align-items:center;gap:1rem;flex-wrap:wrap;}}
.band-copy .mark{{background:linear-gradient(135deg,#f59e0b,#f97316);color:#fff;padding:.56rem .9rem;border-radius:12px;font-size:.72rem;font-weight:900;letter-spacing:.16em;text-transform:uppercase;}}
.band-copy .line{{font-size:1.1rem;font-weight:800;color:#fff;letter-spacing:.04em;}}
.band-copy .line span{{background:linear-gradient(90deg,#FFD700,#FF8C00,#FF69B4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}}
.band-chips{{display:flex;gap:.6rem;flex-wrap:wrap;}}
.band-chips span{{padding:.45rem .8rem;border-radius:999px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);color:rgba(255,255,255,.7);font-size:.7rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;}}
.feature-grid{{max-width:1440px;margin:2rem auto 0;padding:0 2.5rem;display:grid;grid-template-columns:repeat(4, minmax(0,1fr));gap:1rem;}}
.feature-card{{background:linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.02));
  border:1px solid rgba(180,100,255,.18);border-radius:22px;padding:1.4rem 1.2rem;position:relative;overflow:hidden;}}
.feature-card::before{{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,215,0,.08),transparent 40%,rgba(168,85,247,.12));pointer-events:none;}}
.feature-icon{{position:relative;z-index:1;font-size:2rem;margin-bottom:.8rem;display:inline-flex;align-items:center;justify-content:center;width:58px;height:58px;border-radius:16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);}}
.feature-title{{position:relative;z-index:1;font-size:1.1rem;font-weight:800;color:#fff;margin-bottom:.35rem;}}
.feature-copy{{position:relative;z-index:1;color:rgba(255,255,255,.64);font-size:.82rem;line-height:1.6;}}
.featured-wrap{{max-width:1440px;margin:2rem auto 0;padding:0 2.5rem 0;}}
.featured-header{{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;}}
.featured-title{{font-size:clamp(1.5rem,2.6vw,2.2rem);font-weight:900;background:linear-gradient(90deg,#FFD700,#FF8C00,#FF69B4,#9400D3);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}}
.featured-sub{{color:rgba(255,255,255,.48);font-size:.9rem;}}
.featured-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1rem;}}
.featured-card{{background:linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.02));border:1px solid rgba(180,100,255,.18);border-radius:22px;overflow:hidden;cursor:pointer;transition:all .25s ease;}}
.featured-card:hover{{transform:translateY(-8px);border-color:rgba(255,215,0,.44);box-shadow:0 18px 42px rgba(109,40,217,.24);}}
.featured-image{{height:210px;position:relative;overflow:hidden;}}
.featured-image img{{width:100%;height:100%;object-fit:cover;display:block;}}
.featured-image .fallback{{width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,rgba(109,40,217,.25),rgba(32,50,90,.28));font-size:4rem;}}
.featured-body{{padding:1rem 1rem 1.1rem;}}
.featured-model{{font-size:1.08rem;font-weight:800;color:#fff;margin-bottom:.2rem;}}
.featured-meta{{font-size:.75rem;color:rgba(255,255,255,.5);margin-bottom:.7rem;letter-spacing:.04em;}}
.featured-price{{font-size:1.4rem;font-weight:900;background:linear-gradient(90deg,#FFD700,#FF8C00);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}}
.featured-row{{display:flex;justify-content:space-between;align-items:center;gap:.6rem;margin-top:.7rem;}}
.featured-tag{{padding:.24rem .7rem;border-radius:999px;font-size:.68rem;font-weight:800;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.03);color:rgba(255,255,255,.72);}}
.featured-btn{{padding:.5rem .9rem;border-radius:10px;background:linear-gradient(135deg,#6D28D9,#9333EA);color:#fff;border:none;font-weight:700;cursor:pointer;font-size:.76rem;}}
@media (max-width: 1100px){{
  .feature-grid{{grid-template-columns:repeat(2,minmax(0,1fr));}}
  .featured-grid{{grid-template-columns:repeat(2,minmax(0,1fr));}}
}}
@media (max-width: 760px){{
  .feature-grid{{grid-template-columns:1fr;}}
  .featured-grid{{grid-template-columns:1fr;}}
  .band-inner{{padding:1rem;}}
  .flagship-band{{padding:1rem 1rem 0;}}
  .featured-wrap{{padding:0 1rem;}}
  .feature-grid{{padding:0 1rem;}}
}}
/* CARS SECTION */
.cars-sec{{background:#0b0b20;padding:5rem 2.5rem 4rem;}}
.stitle{{text-align:center;font-size:clamp(1.6rem,3.5vw,2.4rem);font-weight:900;margin-bottom:.4rem;
  background:linear-gradient(90deg,#FFD700,#FF8C00,#FF1493,#9400D3);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}}
.ssub{{text-align:center;color:rgba(255,255,255,.4);margin-bottom:2.5rem;font-size:.9rem;}}
.fbar{{display:flex;gap:.7rem;flex-wrap:wrap;justify-content:center;margin-bottom:2.5rem;}}
.si{{padding:.6rem 1.5rem;border-radius:999px;border:2px solid rgba(255,255,255,.18);
  background:rgba(255,255,255,.04);color:rgba(255,255,255,.7);font-weight:600;
  outline:none;font-size:.86rem;min-width:250px;transition:border-color .2s;}}
.si:focus{{border-color:#9333EA;}}
.si::placeholder{{color:rgba(255,255,255,.3);}}
.fb{{padding:.52rem 1.2rem;border-radius:999px;border:2px solid rgba(255,255,255,.18);
  background:rgba(255,255,255,.04);color:rgba(255,255,255,.65);
  font-weight:600;cursor:pointer;font-size:.82rem;transition:all .2s;}}
.fb:hover,.fb.on{{background:linear-gradient(135deg,#6D28D9,#9333EA);
  border-color:transparent;color:#fff;box-shadow:0 4px 16px rgba(109,40,217,.5);transform:translateY(-2px);}}
.cgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(285px,1fr));
  gap:1.5rem;max-width:1440px;margin:0 auto;}}
.ccard{{background:linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.02));
  border:1px solid rgba(180,100,255,.2);border-radius:20px;overflow:hidden;
  cursor:pointer;transition:all .3s;animation:cin .5s ease both;}}
.ccard:hover{{transform:translateY(-9px);border-color:rgba(200,120,255,.65);
  box-shadow:0 22px 60px rgba(109,40,217,.3),0 0 35px rgba(255,150,50,.1);}}
@keyframes cin{{from{{opacity:0;transform:translateY(28px);}}to{{opacity:1;transform:translateY(0);}}}}
.cimg{{width:100%;height:200px;object-fit:cover;}}
.cnoimg{{width:100%;height:200px;
  background:linear-gradient(135deg,rgba(109,40,217,.18),rgba(147,51,234,.08));
  display:flex;align-items:center;justify-content:center;font-size:4rem;}}
.cbody{{padding:1.1rem 1.2rem 1.3rem;}}
.cname{{font-size:1.05rem;font-weight:800;color:#fff;margin-bottom:.22rem;}}
.ccat{{font-size:.74rem;color:rgba(255,255,255,.36);margin-bottom:.6rem;}}
.cprice{{font-size:1.5rem;font-weight:900;
  background:linear-gradient(90deg,#FFD700,#FF8C00);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:.55rem;}}
.specs{{display:flex;flex-wrap:wrap;gap:.38rem;margin-bottom:.65rem;}}
.sp{{padding:.17rem .62rem;border-radius:999px;font-size:.71rem;font-weight:600;
  background:rgba(255,255,255,.07);color:rgba(255,255,255,.58);border:1px solid rgba(255,255,255,.1);}}
.cpill{{display:inline-block;padding:.17rem .72rem;border-radius:999px;font-size:.72rem;font-weight:700;}}
.pav{{background:rgba(22,163,74,.18);color:#4ade80;border:1px solid rgba(74,222,128,.28);}}
.prv{{background:rgba(217,119,6,.18);color:#fbbf24;border:1px solid rgba(251,191,36,.28);}}
.cbtn{{width:100%;padding:.68rem;border-radius:12px;
  background:linear-gradient(135deg,#6D28D9,#9333EA);
  color:#fff;border:none;font-weight:700;cursor:pointer;font-size:.85rem;
  margin-top:.48rem;transition:all .2s;}}
.cbtn:hover{{background:linear-gradient(135deg,#5B21B6,#7C3AED);transform:translateY(-2px);}}
.nocars{{text-align:center;padding:4rem;color:rgba(255,255,255,.32);font-size:1rem;}}
/* CONTACT */
.con-sec{{background:linear-gradient(135deg,#180030,#0a1628,#280055);
  padding:4.5rem 2.5rem;text-align:center;}}
.con-title{{font-size:clamp(1.4rem,3vw,2.1rem);font-weight:900;color:#fff;margin-bottom:.4rem;}}
.con-sub{{color:rgba(255,255,255,.48);margin-bottom:2.5rem;font-size:.9rem;}}
.pgrid{{display:flex;gap:1.4rem;justify-content:center;flex-wrap:wrap;}}
.pcard{{background:rgba(255,255,255,.055);border:1px solid rgba(180,100,255,.28);
  border-radius:18px;padding:1.5rem 2rem;min-width:205px;transition:all .3s;}}
.pcard:hover{{transform:translateY(-6px);border-color:rgba(255,215,0,.5);
  box-shadow:0 12px 35px rgba(255,215,0,.12);}}
.pname{{color:rgba(255,255,255,.48);font-size:.76rem;margin-bottom:.4rem;text-transform:uppercase;letter-spacing:.5px;}}
.pnum{{font-size:1.22rem;font-weight:900;
  background:linear-gradient(90deg,#FFD700,#FF8C00);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:.6rem;}}
.wa{{display:inline-block;padding:.36rem .95rem;border-radius:999px;
  background:rgba(37,211,102,.13);border:1px solid rgba(37,211,102,.38);
  color:#25d366;font-size:.74rem;font-weight:700;text-decoration:none;transition:all .2s;margin-right:.4rem;}}
.ca{{display:inline-block;padding:.36rem .95rem;border-radius:999px;
  background:rgba(109,40,217,.18);border:1px solid rgba(109,40,217,.42);
  color:#c084fc;font-size:.74rem;font-weight:700;text-decoration:none;transition:all .2s;}}
/* MODAL */
.mov{{position:fixed;inset:0;background:rgba(0,0,0,.88);z-index:2000;
  display:none;align-items:center;justify-content:center;backdrop-filter:blur(10px);}}
.mov.open{{display:flex;}}
.mbox{{background:linear-gradient(145deg,#180a2e,#0f1835);
  border:1px solid rgba(180,100,255,.38);border-radius:24px;padding:2rem;
  max-width:560px;width:92%;max-height:88vh;overflow-y:auto;animation:min .28s ease;}}
@keyframes min{{from{{opacity:0;transform:scale(.84);}}to{{opacity:1;transform:scale(1);}}}}
.mimg{{width:100%;height:225px;object-fit:cover;border-radius:14px;margin-bottom:1rem;}}
.mname{{font-size:1.5rem;font-weight:900;color:#fff;margin-bottom:.3rem;}}
.mprice{{font-size:2rem;font-weight:900;
  background:linear-gradient(90deg,#FFD700,#FF8C00);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:1rem;}}
.msg{{display:grid;grid-template-columns:1fr 1fr;gap:.6rem;margin-bottom:1rem;}}
.ms{{background:rgba(255,255,255,.05);border-radius:10px;padding:.62rem;border:1px solid rgba(255,255,255,.07);}}
.msl{{color:rgba(255,255,255,.38);font-size:.69rem;margin-bottom:.18rem;}}
.msv{{color:#fff;font-weight:700;font-size:.87rem;}}
.mdesc{{color:rgba(255,255,255,.5);font-size:.83rem;line-height:1.65;margin-bottom:1rem;}}
.mcl{{float:right;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.12);
  color:rgba(255,255,255,.7);padding:.33rem .88rem;border-radius:8px;cursor:pointer;font-size:.8rem;}}
.foot{{background:#07071a;text-align:center;padding:1.3rem;
  color:rgba(255,255,255,.18);font-size:.72rem;border-top:1px solid rgba(180,100,255,.1);}}
</style></head><body>
<nav class='nav'>
  <div class='brand-block'>
    <div class='nav-brand'>👑 Car King Mauranipur</div>
    <div class='nav-tag'>45+ Years Collective Expertise | Serving since 5+ Years</div>
  </div>
  <div class='nav-meta'>
    <span>Luxury Collection</span>
    <span>Premium Verified</span>
  </div>
  <a class='nav-btn' href='/admin_login' target='_top'>🔐 Admin Login</a>
</nav>
<section class='hero'>
  <div class='hero-bg'></div>
  <div class='hero-glow'></div>
  <div class='beams'>
    <div class='beam'></div><div class='beam'></div><div class='beam'></div>
    <div class='beam'></div><div class='beam'></div>
  </div>
  <div id='ptcl'></div>
  <div class='hero-inner'>
    <div class='hero-copy'>
      <div class='eyebrow'>PREMIUM PERFORMANCE • EXCLUSIVE COLLECTION</div>
      <div class='crown'>👑</div>
      <div class='ht'>Car King<br><span>Mauranipur</span></div>
      <div class='hsub'>Luxury cars for discerning buyers — premium inventory, trusted service, and a showroom experience built for serious sales.</div>
      <div class='badges'>
        <span class='badge'>🚗 Premium Cars</span>
        <span class='badge'>⭐ 98% Satisfaction</span>
        <span class='badge'>👥 5000+ Customers</span>
      </div>
      <div class='cta-row'>
        <a class='cta primary' href='#cs'>Explore Collection</a>
        <a class='cta secondary' href='/admin_login' target='_top'>Admin Access</a>
      </div>
      <div class='hero-stats'>
        <div><strong>5000+</strong><span>Happy Drivers</span></div>
        <div><strong>45+</strong><span>Years Expertise</span></div>
        <div><strong>98%</strong><span>Customer Delight</span></div>
      </div>
    </div>
    <div class='hero-showcase'>
      <div class='showcase-panel'>
        <div class='panel-top'>
          <span class='label'>Luxury Garage</span>
          <span class='status'>Live Inventory</span>
        </div>
        <div class='car-name'>BMW X7</div>
        <div class='car-meta'>2024 • Automatic • 7 Seater</div>
        <div class='car-visual'>🏎️</div>
        <div class='spec-row'>
          <span>₹1.89 Cr</span>
          <span>Hybrid</span>
        </div>
      </div>
      <div class='mini-card card-1'>Range Rover</div>
      <div class='mini-card card-2'>Mercedes</div>
      <div class='mini-card card-3'>Audi</div>
    </div>
  </div>
  <div class='scroll-hint'>Hamare Cars Dekho<br><span class='arr'>⬇</span></div>
  <div class='cstrip'><div class='ctrack'>
    <span class='cs'>🚗</span><span class='cs'>🏎️</span><span class='cs'>🚙</span>
    <span class='cs'>🚕</span><span class='cs'>🏎️</span><span class='cs'>🚗</span>
    <span class='cs'>🚙</span><span class='cs'>🏎️</span><span class='cs'>🚗</span><span class='cs'>🚕</span>
    <span class='cs'>🚗</span><span class='cs'>🏎️</span><span class='cs'>🚙</span>
    <span class='cs'>🚕</span><span class='cs'>🏎️</span><span class='cs'>🚗</span>
    <span class='cs'>🚙</span><span class='cs'>🏎️</span><span class='cs'>🚗</span><span class='cs'>🚕</span>
  </div><div class='road'></div></div>
</section>
<section class='flagship-band'>
  <div class='band-inner'>
    <div class='band-copy'>
      <div class='mark'>Flagship</div>
      <div class='line'>Luxury that moves you <span>before the first test drive</span></div>
    </div>
    <div class='band-chips'>
      <span>Certified</span>
      <span>Finance</span>
      <span>Delivery</span>
      <span>Test Drive</span>
    </div>
  </div>
</section>
<section class='feature-grid'>
  <div class='feature-card'>
    <div class='feature-icon'>✅</div>
    <div class='feature-title'>Certified Quality</div>
    <div class='feature-copy'>Every car is inspected for confidence, clarity, and premium ownership experience.</div>
  </div>
  <div class='feature-card'>
    <div class='feature-icon'>💳</div>
    <div class='feature-title'>Flexible Finance</div>
    <div class='feature-copy'>Simple loan support and tailored plans for personal, family, and premium purchases.</div>
  </div>
  <div class='feature-card'>
    <div class='feature-icon'>🚚</div>
    <div class='feature-title'>Fast Delivery</div>
    <div class='feature-copy'>Seamless handover and trusted process from selection to driveway delivery.</div>
  </div>
  <div class='feature-card'>
    <div class='feature-icon'>🏁</div>
    <div class='feature-title'>Test Drive Ready</div>
    <div class='feature-copy'>Drive the exact car you love and discover the fit before you commit.</div>
  </div>
</section>
<section class='featured-wrap'>
  <div class='featured-header'>
    <div>
      <div class='featured-title'>Featured Collection</div>
      <div class='featured-sub'>Hand-picked premium inventory from our live showroom</div>
    </div>
  </div>
  <div class='featured-grid' id='featured-grid'></div>
</section>
<section class='cars-sec' id='cs'>
  <div class='stitle'>🚘 Hamare Premium Cars</div>
  <div class='ssub'>Sabse behtareen selection — sirf aapke liye</div>
  <div class='fbar'>
    <input type='text' class='si' id='srch' placeholder='🔍  Model ya Brand search karo...' oninput='fc()'>
    <button class='fb on' onclick='sf("All",this)'>All</button>
    <button class='fb' onclick='sf("SUV",this)'>🚙 SUV</button>
    <button class='fb' onclick='sf("Sedan",this)'>🚗 Sedan</button>
    <button class='fb' onclick='sf("Hatchback",this)'>🚕 Hatchback</button>
    <button class='fb' onclick='sf("Luxury",this)'>🏎️ Luxury</button>
    <button class='fb' onclick='sf("Others",this)'>Others</button>
  </div>
  <div class='cgrid' id='cg'></div>
  <div class='nocars' id='nc' style='display:none'>😔 Koi car nahi mili. Jald hi nayi cars aayengi!</div>
</section>
<section class='con-sec'>
  <div class='con-title'>📞 Koi Car Pasand Aayi? Abhi Contact Karo!</div>
  <div class='con-sub'>Hamare experts aapki madad karenge — Test Drive bhi available hai</div>
  <div class='pgrid' id='pg'></div>
</section>
<div class='foot'>© 2024 Car King Mauranipur &nbsp;|&nbsp; Premium Used Cars &nbsp;|&nbsp; All Rights Reserved</div>
<div class='mov' id='mo' onclick='cm(event)'><div class='mbox' id='mb'>
  <button class='mcl' onclick="document.getElementById('mo').classList.remove('open')">✕ Close</button>
  <div id='mc'></div>
</div></div>
<script>
const CARS={cars_js}, PH={phones_js};
let CF='All';
const pc=['#FFD700','#FF69B4','#9400D3','#00CED1','#FF6B00','#1E90FF'];
const p=document.getElementById('ptcl');
for(let i=0;i<65;i++){{const d=document.createElement('div');d.className='pt';
  const s=Math.random()*6+2;
  d.style.cssText=`width:${{s}}px;height:${{s}}px;left:${{Math.random()*100}}%;
    background:${{pc[i%pc.length]}};animation-duration:${{Math.random()*9+6}}s;
    animation-delay:${{Math.random()*9}}s;box-shadow:0 0 ${{s*3}}px ${{pc[i%pc.length]}};
    opacity:${{Math.random()*.7+.3}};`;p.appendChild(d);}}
const pg=document.getElementById('pg');
if(PH.length===0){{pg.innerHTML='<p style="color:rgba(255,255,255,.3)">Settings me partner numbers add karo</p>';}}
else PH.forEach(x=>{{const n=x.phone.replace(/[^0-9]/g,'');
  pg.innerHTML+=`<div class='pcard'><div class='pname'>${{x.name}}</div>
    <div class='pnum'>📞 ${{x.phone}}</div>
    <a class='wa' href='https://wa.me/91${{n}}' target='_blank'>💬 WhatsApp</a>
    <a class='ca' href='tel:${{x.phone}}'>📲 Call</a></div>`;
}});
function renderFeatured(){{
  const featured = CARS.slice(0,4);
  const box = document.getElementById('featured-grid');
  if(!box || !featured.length) return;
  box.innerHTML = featured.map((c)=>`<div class='featured-card' onclick='om(${{c.id}})'>
    <div class='featured-image'>
      ${{c.image_url?`<img src='${{c.image_url}}' alt='${{c.brand_model}}' onerror="this.style.display='none';this.nextElementSibling.style.display='flex';">`:'<div class="fallback">🚗</div>'}}
      <div class='fallback' style='display:none;'>🚗</div>
    </div>
    <div class='featured-body'>
      <div class='featured-model'>${{c.brand_model}}</div>
      <div class='featured-meta'>${{c.year}} • ${{c.fuel_type || 'Petrol'}} • ${{c.transmission || 'Automatic'}}</div>
      <div class='featured-price'>₹${{Number(c.price).toLocaleString('en-IN')}}</div>
      <div class='featured-row'>
        <span class='featured-tag'>${{c.category || 'Premium'}}</span>
        <button class='featured-btn' onclick='event.stopPropagation();om(${{c.id}})'>View</button>
      </div>
    </div>
  </div>`).join('');
}}
function render(cars){{
  const g=document.getElementById('cg'),nc=document.getElementById('nc');
  if(!cars.length){{g.innerHTML='';nc.style.display='block';return;}}
  nc.style.display='none';
  g.innerHTML=cars.map((c,i)=>`<div class='ccard' style='animation-delay:${{i*.06}}s' onclick='om(${{c.id}})'>
    ${{c.image_url?`<img src='${{c.image_url}}' class='cimg' onerror="this.outerHTML='<div class=cnoimg>🚗</div>'">`:'<div class="cnoimg">🚗</div>'}}
    <div class='cbody'><div class='cname'>${{c.brand_model}}</div>
    <div class='ccat'>${{c.category}}${{c.registration_number?' • '+c.registration_number:''}}</div>
    <div class='cprice'>₹${{Number(c.price).toLocaleString('en-IN')}}</div>
    <div class='specs'>
      <span class='sp'>📅 ${{c.year}}</span>
      <span class='sp'>🛣️ ${{Number(c.kms_driven).toLocaleString('en-IN')}} km</span>
      ${{c.fuel_type?`<span class='sp'>⛽ ${{c.fuel_type}}</span>`:''}}
      ${{c.transmission?`<span class='sp'>🔧 ${{c.transmission}}</span>`:''}}
      ${{c.owner_number?`<span class='sp'>👤 ${{c.owner_number}}</span>`:''}}
    </div>
    <span class='cpill ${{c.status==="Available"?"pav":"prv"}}'>${{c.status}}</span>
    <button class='cbtn' onclick='event.stopPropagation();contact()'>📞 Contact Karo</button>
    </div></div>`).join('');
  renderFeatured();
}}
function sf(cat,btn){{CF=cat;document.querySelectorAll('.fb').forEach(b=>b.classList.remove('on'));btn.classList.add('on');fc();}}
function fc(){{const q=document.getElementById('srch').value.toLowerCase();
  const filtered = CARS.filter(c=>(CF==='All'||c.category===CF)&&(!q||c.brand_model.toLowerCase().includes(q)||c.category.toLowerCase().includes(q)||(c.registration_number||'').toLowerCase().includes(q)));
  render(filtered);}}
function gc(){{document.querySelector('.con-sec').scrollIntoView({{behavior:'smooth'}});}}
function contact(){{
  if(PH.length){{
    const number=PH[0].phone.replace(/[^0-9]/g,'');
    window.open(`https://wa.me/91${{number}}`,'_blank','noopener');
    return;
  }}
  gc();
}}
function om(id){{const c=CARS.find(x=>x.id===id);if(!c)return;
  document.getElementById('mc').innerHTML=`
    ${{c.image_url?`<img src='${{c.image_url}}' class='mimg' onerror="this.style.display='none'">`:''}}<div class='mname'>${{c.brand_model}}</div>
    <span class='cpill ${{c.status==="Available"?"pav":"prv"}}' style='margin-bottom:.6rem;display:inline-block'>${{c.status}}</span>
    <div class='mprice'>₹${{Number(c.price).toLocaleString('en-IN')}}</div>
    <div class='msg'>
      <div class='ms'><div class='msl'>Year</div><div class='msv'>${{c.year}}</div></div>
      <div class='ms'><div class='msl'>Kms Driven</div><div class='msv'>${{Number(c.kms_driven).toLocaleString('en-IN')}} km</div></div>
      <div class='ms'><div class='msl'>Fuel</div><div class='msv'>${{c.fuel_type||'—'}}</div></div>
      <div class='ms'><div class='msl'>Transmission</div><div class='msv'>${{c.transmission||'—'}}</div></div>
      <div class='ms'><div class='msl'>Owner</div><div class='msv'>${{c.owner_number||'—'}}</div></div>
      <div class='ms'><div class='msl'>Category</div><div class='msv'>${{c.category}}</div></div>
    </div>
    ${{c.description?`<div class='mdesc'>${{c.description}}</div>`:''}}
    <button class='cbtn' onclick="contact();document.getElementById('mo').classList.remove('open')">📞 Abhi Contact Karo</button>`;
  document.getElementById('mo').classList.add('open');}}
function cm(e){{if(e.target===document.getElementById('mo'))document.getElementById('mo').classList.remove('open');}}
render(CARS);
</script></body></html>""", height=5200, scrolling=True)
