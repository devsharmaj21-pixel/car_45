"""
database.py
SQLite (local) + Supabase (cloud) — dono support karta hai.
Local me SQLite use hoga, live deploy pe Supabase (data kabhi gayab nahi).
"""
import os, sqlite3
from datetime import datetime
import streamlit as st

_DB = os.path.join(os.path.dirname(__file__), "carking.db")

def _supabase_url():
    try:
        return st.secrets["supabase"]["database_url"]
    except Exception:
        return None

def _conn():
    url = _supabase_url()
    if url:
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            c = psycopg2.connect(url, cursor_factory=RealDictCursor)
            return c, "pg"
        except Exception:
            pass
    c = sqlite3.connect(_DB, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c, "sqlite"

def _q(sql, params=(), fetch="none"):
    c, mode = _conn()
    if mode == "sqlite":
        sql = sql.replace("%s","?").replace("ILIKE","LIKE").replace("SERIAL","INTEGER").replace("NUMERIC","REAL")
    cur = c.cursor()
    cur.execute(sql, params)
    res = None
    if fetch == "all":
        rows = cur.fetchall()
        res = [dict(r) for r in rows] if rows else []
    elif fetch == "one":
        r = cur.fetchone()
        res = dict(r) if r else None
    else:
        c.commit()
    cur.close(); c.close()
    return res

def init_db():
    _q("""CREATE TABLE IF NOT EXISTS cars (
        id SERIAL PRIMARY KEY, brand_model TEXT NOT NULL,
        variant TEXT DEFAULT '', category TEXT NOT NULL,
        year INTEGER NOT NULL, price NUMERIC NOT NULL,
        kms_driven INTEGER NOT NULL, registration_number TEXT DEFAULT '',
        fuel_type TEXT DEFAULT '', transmission TEXT DEFAULT '',
        owner_number TEXT DEFAULT '', status TEXT DEFAULT 'Available',
        description TEXT DEFAULT '', image_url TEXT DEFAULT '',
        image_url_2 TEXT DEFAULT '', image_url_3 TEXT DEFAULT '',
        created_at TEXT DEFAULT '')""")
    _q("""CREATE TABLE IF NOT EXISTS leads (
        id SERIAL PRIMARY KEY, name TEXT NOT NULL,
        phone TEXT NOT NULL, email TEXT DEFAULT '',
        car_interested TEXT DEFAULT '', message TEXT DEFAULT '',
        status TEXT DEFAULT 'New', created_at TEXT DEFAULT '')""")
    _q("""CREATE TABLE IF NOT EXISTS bookings (
        id SERIAL PRIMARY KEY, customer_name TEXT NOT NULL,
        phone TEXT NOT NULL, car_id INTEGER DEFAULT 0,
        car_details TEXT DEFAULT '', booking_date TEXT DEFAULT '',
        amount NUMERIC DEFAULT 0, status TEXT DEFAULT 'Confirmed',
        created_at TEXT DEFAULT '')""")
    _q("""CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY, name TEXT NOT NULL,
        phone TEXT NOT NULL, email TEXT DEFAULT '',
        address TEXT DEFAULT '', notes TEXT DEFAULT '',
        created_at TEXT DEFAULT '')""")
    _q("""CREATE TABLE IF NOT EXISTS activity_log (
        id SERIAL PRIMARY KEY, activity_type TEXT NOT NULL,
        description TEXT NOT NULL, created_at TEXT DEFAULT '')""")

def _log(atype, desc):
    _q("INSERT INTO activity_log(activity_type,description,created_at) VALUES(%s,%s,%s)",
       (atype, desc, datetime.now().isoformat()))

def get_recent_activity(n=6):
    return _q("SELECT * FROM activity_log ORDER BY created_at DESC LIMIT %s",(n,),fetch="all") or []

# ── CARS ──
def add_car(d):
    _q("""INSERT INTO cars(brand_model,variant,category,year,price,kms_driven,
        registration_number,fuel_type,transmission,owner_number,status,
        description,image_url,image_url_2,image_url_3,created_at)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
       (d["brand_model"],d.get("variant",""),d["category"],d["year"],d["price"],
        d["kms_driven"],d.get("registration_number",""),d.get("fuel_type",""),
        d.get("transmission",""),d.get("owner_number",""),d.get("status","Available"),
        d.get("description",""),d.get("image_url",""),d.get("image_url_2",""),
        d.get("image_url_3",""),datetime.now().isoformat()))
    _log("car_added", f"New car: {d['brand_model']} {d['year']}")

def get_all_cars(status=None, category=None, search=None):
    c,mode = _conn()
    sql = "SELECT * FROM cars WHERE 1=1"
    params = []
    if status and status != "All": sql += " AND status=%s"; params.append(status)
    if category and category != "All": sql += " AND category=%s"; params.append(category)
    if search:
        op = "LIKE" if mode=="sqlite" else "ILIKE"
        sql += f" AND (brand_model {op} %s OR registration_number {op} %s)"
        params += [f"%{search}%",f"%{search}%"]
    sql += " ORDER BY created_at DESC"
    if mode=="sqlite": sql=sql.replace("%s","?")
    cur=c.cursor(); cur.execute(sql,params)
    rows=[dict(r) for r in cur.fetchall()]
    cur.close(); c.close(); return rows

def get_car(cid):
    return _q("SELECT * FROM cars WHERE id=%s",(cid,),fetch="one")

def update_car(cid, d):
    c,mode = _conn()
    ph = "?" if mode=="sqlite" else "%s"
    fields=", ".join([f"{k}={ph}" for k in d.keys()])
    c.cursor().execute(f"UPDATE cars SET {fields} WHERE id={ph}", list(d.values())+[cid])
    c.commit(); c.close()

def delete_car(cid):
    _q("DELETE FROM cars WHERE id=%s",(cid,))

def car_stats():
    def cnt(w=""): r=_q(f"SELECT COUNT(*) as c FROM cars{' WHERE '+w if w else ''}",fetch="one"); return r["c"] if r else 0
    sr=_q("SELECT COALESCE(SUM(price),0) as s FROM cars WHERE status='Sold'",fetch="one")
    bc=_q("SELECT category,COUNT(*) as c FROM cars GROUP BY category ORDER BY c DESC",fetch="all") or []
    return {"total":cnt(),"available":cnt("status='Available'"),"reserved":cnt("status='Reserved'"),
            "sold":cnt("status='Sold'"),"under_review":cnt("status='Under Review'"),
            "total_sales":float(sr["s"]) if sr else 0,"by_category":bc}

# ── LEADS ──
def add_lead(d):
    _q("INSERT INTO leads(name,phone,email,car_interested,message,status,created_at) VALUES(%s,%s,%s,%s,%s,%s,%s)",
       (d["name"],d["phone"],d.get("email",""),d.get("car_interested",""),
        d.get("message",""),d.get("status","New"),datetime.now().isoformat()))
    _log("lead_added",f"New inquiry: {d['name']}")

def get_all_leads(status=None):
    sql="SELECT * FROM leads WHERE 1=1"
    params=[]
    if status and status!="All": sql+=" AND status=%s"; params.append(status)
    return _q(sql+" ORDER BY created_at DESC", params, fetch="all") or []

def update_lead_status(lid,status): _q("UPDATE leads SET status=%s WHERE id=%s",(status,lid))
def delete_lead(lid): _q("DELETE FROM leads WHERE id=%s",(lid,))

# ── BOOKINGS ──
def add_booking(d):
    _q("INSERT INTO bookings(customer_name,phone,car_id,car_details,booking_date,amount,status,created_at) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
       (d["customer_name"],d["phone"],d.get("car_id",0),d.get("car_details",""),
        d.get("booking_date",""),d.get("amount",0),d.get("status","Confirmed"),datetime.now().isoformat()))
    _log("booking_added",f"Booking: {d.get('car_details','')} → {d['customer_name']}")

def get_all_bookings(status=None):
    sql="SELECT * FROM bookings WHERE 1=1"; params=[]
    if status and status!="All": sql+=" AND status=%s"; params.append(status)
    return _q(sql+" ORDER BY created_at DESC",params,fetch="all") or []

def update_booking_status(bid,status): _q("UPDATE bookings SET status=%s WHERE id=%s",(status,bid))
def delete_booking(bid): _q("DELETE FROM bookings WHERE id=%s",(bid,))

# ── CUSTOMERS ──
def add_customer(d):
    _q("INSERT INTO customers(name,phone,email,address,notes,created_at) VALUES(%s,%s,%s,%s,%s,%s)",
       (d["name"],d["phone"],d.get("email",""),d.get("address",""),d.get("notes",""),datetime.now().isoformat()))

def get_all_customers(search=None):
    sql="SELECT * FROM customers WHERE 1=1"; params=[]
    if search:
        c,mode=_conn()
        op="LIKE" if mode=="sqlite" else "ILIKE"
        sql+=f" AND (name {op} %s OR phone {op} %s)"; params+=[f"%{search}%",f"%{search}%"]
    return _q(sql+" ORDER BY created_at DESC",params,fetch="all") or []

def delete_customer(cid): _q("DELETE FROM customers WHERE id=%s",(cid,))
