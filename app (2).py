import streamlit as st
import pandas as pd
from io import BytesIO

# ---------------------------------------------------------
# Sahifa sozlamalari
# ---------------------------------------------------------
st.set_page_config(
    page_title="Farg‘ona Travel",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Och havorang dizayn
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --blue-50: #f0f9ff;
        --blue-100: #e0f2fe;
        --blue-200: #bae6fd;
        --blue-500: #0ea5e9;
        --blue-600: #0284c7;
        --blue-700: #0369a1;
        --ink: #0f2942;
        --muted: #5b7185;
        --white: #ffffff;
    }

    * { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(180deg, #f5fbff 0%, #eef8fd 100%); color: var(--ink); }
    [data-testid="stHeader"] { background: rgba(245, 251, 255, .85); }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #dff3ff 0%, #c9ebfb 100%); border-right: 1px solid #b8e2f5; }
    [data-testid="stSidebar"] * { color: var(--ink) !important; }
    [data-testid="stSidebar"] .stButton > button { background: white; color: var(--blue-700) !important; border: 1px solid var(--blue-200); }

    .brand { display:flex; align-items:center; gap:10px; padding: 4px 0 18px; }
    .brand-mark { width:42px; height:42px; display:flex; align-items:center; justify-content:center; border-radius:14px; background: linear-gradient(135deg, #0284c7, #38bdf8); color:white; font-size:22px; box-shadow: 0 8px 18px rgba(2,132,199,.25); }
    .brand-title { font-size: 1.18rem; font-weight: 800; color: var(--ink); }
    .brand-subtitle { font-size: .72rem; color: var(--muted); margin-top:2px; }

    .hero { position:relative; overflow:hidden; min-height:245px; padding:38px 42px; border-radius:28px; color:white; background: linear-gradient(120deg, #0369a1 0%, #0284c7 42%, #38bdf8 100%); box-shadow: 0 18px 40px rgba(2,132,199,.20); margin-bottom:24px; }
    .hero:after { content:''; position:absolute; width:300px; height:300px; border-radius:50%; right:-80px; top:-120px; background:rgba(255,255,255,.13); }
    .hero h1 { position:relative; z-index:1; font-size:2.35rem; line-height:1.15; max-width:680px; margin:0 0 12px; font-weight:800; }
    .hero p { position:relative; z-index:1; max-width:650px; margin:0; font-size:1.04rem; line-height:1.7; opacity:.93; }
    .hero-badge { position:relative; z-index:1; display:inline-block; padding:7px 13px; border-radius:30px; background:rgba(255,255,255,.18); font-size:.78rem; font-weight:600; margin-bottom:16px; }

    .section-title { color: var(--ink); font-size:1.45rem; font-weight:800; margin: 18px 0 12px; }
    .section-subtitle { color:var(--muted); margin-top:-6px; margin-bottom:18px; }
    div[data-testid="stMetric"] { background:rgba(255,255,255,.92); border:1px solid #cceaf8; border-radius:18px; padding:16px 18px; box-shadow: 0 5px 16px rgba(14,116,144,.06); }
    div[data-testid="stMetricLabel"] { color:var(--muted); }
    div[data-testid="stMetricValue"] { color:var(--blue-700); font-weight:800; }

    .spot-card { background:rgba(255,255,255,.96); border:1px solid #cceaf8; border-radius:19px; padding:19px; min-height:150px; box-shadow:0 5px 16px rgba(14,116,144,.06); margin-bottom:14px; }
    .spot-card:hover { border-color:#7dd3fc; box-shadow:0 10px 24px rgba(14,116,144,.12); }
    .spot-title { color:var(--ink); font-size:1.02rem; font-weight:700; line-height:1.35; margin-bottom:7px; }
    .spot-meta { color:var(--muted); font-size:.86rem; line-height:1.65; }
    .tag { display:inline-block; color:#0369a1; background:#e0f2fe; border-radius:20px; padding:4px 9px; margin:7px 4px 0 0; font-size:.72rem; font-weight:600; }
    .route-step { display:flex; gap:14px; align-items:flex-start; background:white; border:1px solid #cceaf8; border-radius:17px; padding:17px; margin-bottom:10px; box-shadow:0 4px 13px rgba(14,116,144,.05); }
    .step-number { flex:0 0 34px; width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; background:linear-gradient(135deg,#0284c7,#38bdf8); font-weight:800; }
    .info-box { background:#e0f2fe; border:1px solid #bae6fd; border-radius:17px; padding:17px 19px; color:#075985; }
    .footer { text-align:center; color:#6b8497; font-size:.78rem; padding:28px 0 8px; }
    .stButton > button { border-radius:11px; border:1px solid #b9e3f6; font-weight:600; min-height:42px; }
    .stButton > button[kind="primary"] { background:linear-gradient(135deg,#0284c7,#0ea5e9); color:white; border:none; }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { border-radius:11px; border-color:#b9e3f6; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Ma'lumotlar
# ---------------------------------------------------------
SPOTS = [
    {"name":"Xudoyorxon o‘rdasi", "city":"Qo‘qon", "tags":["Tarixiy","Madaniy"], "time":2.0, "cost":30000, "cluster":"G‘arb", "lat":40.5286, "lon":70.9428, "description":"Qo‘qon xonligi tarixini aks ettiruvchi muhtasham saroy majmuasi."},
    {"name":"Jome masjidi va amaliy san’at muzeyi", "city":"Qo‘qon", "tags":["Tarixiy","Me’moriy"], "time":1.5, "cost":20000, "cluster":"G‘arb", "lat":40.5270, "lon":70.9420, "description":"Qadimiy me’morchilik va mahalliy amaliy san’at namunalari maskani."},
    {"name":"Norbo‘tabiy madrasasi", "city":"Qo‘qon", "tags":["Ziyorat","Tarixiy"], "time":1.0, "cost":0, "cluster":"G‘arb", "lat":40.5261, "lon":70.9436, "description":"Qo‘qon tarixining muhim yodgorliklaridan biri bo‘lgan madrasa."},
    {"name":"Daxmai Shohon maqbarasi", "city":"Qo‘qon", "tags":["Tarixiy","Ziyorat"], "time":1.0, "cost":15000, "cluster":"G‘arb", "lat":40.5254, "lon":70.9470, "description":"Tarixiy hukmdorlar xotirasi bilan bog‘liq ziyoratgoh."},
    {"name":"Yodgorlik ipak fabrikasi", "city":"Marg‘ilon", "tags":["Hunarmandchilik","Madaniy"], "time":2.0, "cost":40000, "cluster":"Markaz", "lat":40.4731, "lon":71.7246, "description":"An’anaviy ipak ishlab chiqarish jarayonini ko‘rish mumkin bo‘lgan maskan."},
    {"name":"Hunarmandlar markazi", "city":"Marg‘ilon", "tags":["Hunarmandchilik","Madaniy"], "time":1.5, "cost":15000, "cluster":"Markaz", "lat":40.4720, "lon":71.7235, "description":"Mahalliy ustalar ijodi va hunarmandchilik mahsulotlari markazi."},
    {"name":"Pir Siddiq majmuasi", "city":"Marg‘ilon", "tags":["Ziyorat","Tarixiy"], "time":1.0, "cost":0, "cluster":"Markaz", "lat":40.4750, "lon":71.7260, "description":"Marg‘ilondagi qadimiy ziyorat va tarixiy majmua."},
    {"name":"Al-Farg‘oniy markaziy bog‘i", "city":"Farg‘ona", "tags":["Ekoturizm","Dam olish"], "time":2.0, "cost":30000, "cluster":"Markaz", "lat":40.3864, "lon":71.7864, "description":"Oila bilan sayr qilish va hordiq chiqarish uchun qulay yashil maskan."},
    {"name":"Farg‘ona o‘lkashunoslik muzeyi", "city":"Farg‘ona", "tags":["Tarixiy","Madaniy"], "time":1.5, "cost":15000, "cluster":"Markaz", "lat":40.3880, "lon":71.7870, "description":"Viloyat tarixi, tabiati va madaniyatiga oid boy kolleksiya."},
    {"name":"Rishton kulolchilik markazi", "city":"Rishton", "tags":["Hunarmandchilik","Madaniy"], "time":2.5, "cost":50000, "cluster":"G‘arb", "lat":40.3562, "lon":71.2847, "description":"Mashhur Rishton kulolchilik maktabi bilan yaqindan tanishing."},
    {"name":"Shohimardon ko‘llari", "city":"Farg‘ona tumani", "tags":["Ekoturizm","Dam olish"], "time":6.0, "cost":200000, "cluster":"Janub", "lat":39.9910, "lon":71.8040, "description":"Tog‘lar bag‘ridagi go‘zal ko‘llar va tabiat manzaralari."},
    {"name":"Vodil chinorlari va ziyoratgohi", "city":"Farg‘ona tumani", "tags":["Ekoturizm","Ziyorat","Gastronomiya"], "time":2.5, "cost":80000, "cluster":"Janub", "lat":40.2300, "lon":71.7200, "description":"Qadimiy chinorlar, ziyorat va milliy taomlarni birlashtirgan yo‘nalish."},
    {"name":"Oltiariq uzumzorlari", "city":"Oltiariq", "tags":["Agroturizm","Ekoturizm","Gastronomiya"], "time":2.5, "cost":60000, "cluster":"G‘arb", "lat":40.3900, "lon":71.4800, "description":"Uzumzorlar, dehqonchilik an’analari va agroturizm tajribasi."},
    {"name":"Quva qadimiy shahristoni", "city":"Quva", "tags":["Tarixiy","Ziyorat"], "time":2.0, "cost":15000, "cluster":"Sharq", "lat":40.5220, "lon":72.0720, "description":"Qadimiy shahar xarobalari va Al-Farg‘oniy merosi bilan bog‘liq maskan."},
    {"name":"Chimen sanatoriysi va buloqlari", "city":"Farg‘ona tumani", "tags":["Sog‘lomlashtirish","Dam olish"], "time":3.5, "cost":120000, "cluster":"Janub", "lat":40.2100, "lon":71.6900, "description":"Tabiiy buloqlar va sog‘lomlashtirish xizmatlari bilan mashhur maskan."},
]

df = pd.DataFrame(SPOTS)
TAG_OPTIONS = sorted({tag for item in SPOTS for tag in item["tags"]})
CITY_OPTIONS = sorted(df["city"].unique())
CLUSTER_ORDER = {"G‘arb":0, "Markaz":1, "Sharq":2, "Janub":3}

# ---------------------------------------------------------
# Hisoblash funksiyalari
# ---------------------------------------------------------
def recommend(interests, budget, hours, travel_time, travel_cost, cities=None):
    candidates = []
    for item in SPOTS:
        if cities and item["city"] not in cities:
            continue
        score = len(set(interests).intersection(item["tags"]))
        if score > 0:
            copy = item.copy()
            copy["score"] = score
            candidates.append(copy)
    candidates.sort(key=lambda x: (-x["score"], x["cost"], x["time"]))
    selected, total_time, total_cost = [], 0.0, 0
    for item in candidates:
        extra_time = travel_time if selected else 0
        extra_cost = travel_cost if selected else 0
        if total_time + item["time"] + extra_time <= hours and total_cost + item["cost"] + extra_cost <= budget:
            selected.append(item)
            total_time += item["time"] + extra_time
            total_cost += item["cost"] + extra_cost
    selected.sort(key=lambda x: (CLUSTER_ORDER.get(x["cluster"],99), -x["score"], x["name"]))
    return selected, total_time, total_cost


def format_money(value):
    return f"{int(value):,}".replace(",", " ") + " so‘m"


def spot_card(item, favorite=False):
    tags = " ".join(f'<span class="tag">{tag}</span>' for tag in item["tags"])
    cost = "Bepul" if item["cost"] == 0 else format_money(item["cost"])
    st.markdown(
        f"""
        <div class="spot-card">
            <div class="spot-title">{item['name']}</div>
            <div class="spot-meta">📍 {item['city']} · 🧭 {item['cluster']} · ⏱️ {item['time']:.1f} soat · 💰 {cost}</div>
            <div class="spot-meta" style="margin-top:7px;">{item['description']}</div>
            <div>{tags}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# ---------------------------------------------------------
# Sidebar navigatsiya va sozlamalar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">✈</div>
            <div><div class="brand-title">Farg‘ona Travel</div><div class="brand-subtitle">Sayohatni oson rejalashtiring</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    page = st.radio("Asosiy menyu", ["Bosh sahifa", "Marshrut rejalashtirgich", "Turistik obyektlar", "Sevimlilar", "Ilova haqida"], format_func=lambda x: {"Bosh sahifa":"🏠  Bosh sahifa", "Marshrut rejalashtirgich":"🧭  Marshrut rejalashtirgich", "Turistik obyektlar":"📍  Turistik obyektlar", "Sevimlilar":"💙  Sevimlilar", "Ilova haqida":"ℹ️  Ilova haqida"}[x])
    st.divider()
    st.caption("Foydalanuvchi sozlamalari")
    user_name = st.text_input("Ismingiz", placeholder="Masalan: Azizbek")
    st.caption("15 ta tanlangan turistik obyekt")

# ---------------------------------------------------------
# Bosh sahifa
# ---------------------------------------------------------
if page == "Bosh sahifa":
    greeting = f"Assalomu alaykum, {user_name}!" if user_name else "Farg‘onani birga kashf etamiz!"
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-badge">FARG‘ONA VILOYATI · SAYOHAT PLATFORMASI</div>
            <h1>{greeting}</h1>
            <p>Qiziqishlaringiz, bo‘sh vaqtingiz va byudjetingizga mos chiroyli sayohat marshrutini yarating.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-title">Platforma imkoniyatlari</div>', unsafe_allow_html=True)
    a, b, c, d = st.columns(4)
    a.metric("Turistik obyektlar", "15 ta")
    b.metric("Shahar va tumanlar", f"{len(CITY_OPTIONS)} ta")
    c.metric("Qiziqish turlari", f"{len(TAG_OPTIONS)} ta")
    d.metric("Bepul obyektlar", f"{int((df['cost'] == 0).sum())} ta")

    st.markdown('<div class="section-title">Qanday ishlaydi?</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Uch qadamda o‘zingizga mos yo‘nalishni toping.</div>', unsafe_allow_html=True)
    x, y, z = st.columns(3)
    with x:
        st.markdown('<div class="spot-card"><div class="spot-title">1. Qiziqishingizni tanlang</div><div class="spot-meta">Tarix, madaniyat, tabiat, hunarmandchilik yoki gastronomiyadan birini tanlang.</div></div>', unsafe_allow_html=True)
    with y:
        st.markdown('<div class="spot-card"><div class="spot-title">2. Imkoniyatingizni belgilang</div><div class="spot-meta">Byudjet, vaqt va tashrif hududlarini kiriting.</div></div>', unsafe_allow_html=True)
    with z:
        st.markdown('<div class="spot-card"><div class="spot-title">3. Marshrutni oling</div><div class="spot-meta">Tizim eng mos obyektlarni saralab, tayyor yo‘nalish yaratadi.</div></div>', unsafe_allow_html=True)

    if st.button("🧭 Marshrut tuzishni boshlash", type="primary", use_container_width=True):
        st.info("Chap menyudan ‘Marshrut rejalashtirgich’ bo‘limini tanlang.")

# ---------------------------------------------------------
# Marshrut rejalashtirgich
# ---------------------------------------------------------
elif page == "Marshrut rejalashtirgich":
    st.markdown('<div class="section-title">Sizning shaxsiy marshrutingiz</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Quyidagi maydonlarni to‘ldiring — tizim sizga eng mos yo‘nalishni tavsiya qiladi.</div>', unsafe_allow_html=True)
    left, right = st.columns([1.05, 1.95])
    with left:
        interests = st.multiselect("Qiziqishlaringiz", TAG_OPTIONS, default=["Tarixiy", "Madaniy"])
        budget = st.number_input("Maksimal byudjet (so‘m)", min_value=0, max_value=10_000_000, value=150_000, step=10_000)
        hours = st.slider("Safar davomiyligi (soat)", 1.0, 24.0, 8.0, 0.5)
        cities = st.multiselect("Hududlar (ixtiyoriy)", CITY_OPTIONS)
        with st.expander("Qo‘shimcha yo‘l sozlamalari"):
            travel_time = st.number_input("Manzillar orasidagi yo‘l (soat)", 0.0, 5.0, 0.5, 0.5)
            travel_cost = st.number_input("Har bir yo‘l uchun kira (so‘m)", 0, 1_000_000, 15_000, 5_000)
    with right:
        if not interests:
            st.warning("Kamida bitta qiziqish turini tanlang.")
        else:
            route, total_time, total_cost = recommend(interests, budget, hours, travel_time, travel_cost, cities or None)
            k1, k2, k3 = st.columns(3)
            k1.metric("Manzillar", len(route))
            k2.metric("Jami vaqt", f"{total_time:.1f} soat")
            k3.metric("Jami xarajat", format_money(total_cost))
            st.markdown("#### Tavsiya etilgan yo‘nalish")
            if not route:
                st.error("Ushbu cheklovlar bilan mos marshrut topilmadi. Byudjet yoki vaqtni oshirib ko‘ring.")
            else:
                for i, item in enumerate(route, 1):
                    cost = "Bepul" if item["cost"] == 0 else format_money(item["cost"])
                    st.markdown(f'<div class="route-step"><div class="step-number">{i}</div><div><div class="spot-title">{item["name"]}</div><div class="spot-meta">📍 {item["city"]} · {item["cluster"]} · ⏱️ {item["time"]:.1f} soat · 💰 {cost}</div><div class="spot-meta">Moslik bali: {item["score"]}</div></div></div>', unsafe_allow_html=True)
                route_df = pd.DataFrame([{"№":i, "Obyekt":x["name"], "Shahar/tuman":x["city"], "Yo‘nalish":x["cluster"], "Vaqt (soat)":x["time"], "Xarajat (so‘m)":x["cost"], "Moslik":x["score"]} for i,x in enumerate(route,1)])
                csv = route_df.to_csv(index=False).encode("utf-8-sig")
                st.download_button("⬇️ CSV yuklab olish", csv, "fargona_marshrut.csv", "text/csv", use_container_width=True)

# ---------------------------------------------------------
# Barcha turistik obyektlar
# ---------------------------------------------------------
elif page == "Turistik obyektlar":
    st.markdown('<div class="section-title">Farg‘onaning turistik obyektlari</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Barcha manzillarni qidiring, saralang va batafsil ko‘rib chiqing.</div>', unsafe_allow_html=True)
    q1, q2, q3 = st.columns([1.5, 1, 1])
    with q1:
        search = st.text_input("Qidirish", placeholder="Obyekt yoki shahar nomi...")
    with q2:
        tag_filter = st.selectbox("Qiziqish turi", ["Barchasi"] + TAG_OPTIONS)
    with q3:
        price_filter = st.selectbox("Narx bo‘yicha", ["Barchasi", "Bepul", "Pullik"])
    filtered = df.copy()
    if search:
        mask = filtered.apply(lambda r: search.lower() in (r["name"] + " " + r["city"] + " " + r["description"]).lower(), axis=1)
        filtered = filtered[mask]
    if tag_filter != "Barchasi":
        filtered = filtered[filtered["tags"].apply(lambda x: tag_filter in x)]
    if price_filter == "Bepul":
        filtered = filtered[filtered["cost"] == 0]
    elif price_filter == "Pullik":
        filtered = filtered[filtered["cost"] > 0]
    st.caption(f"{len(filtered)} ta obyekt topildi")
    for start in range(0, len(filtered), 2):
        cols = st.columns(2)
        for col, (_, row) in zip(cols, filtered.iloc[start:start+2].iterrows()):
            with col:
                item = row.to_dict()
                spot_card(item)
                if st.button("💙 Sevimlilarga qo‘shish", key=f"fav_{item['name']}", use_container_width=True):
                    if item["name"] not in st.session_state.favorites:
                        st.session_state.favorites.append(item["name"])
                        st.success("Sevimlilarga qo‘shildi")
                    else:
                        st.info("Bu obyekt allaqachon saqlangan")

# ---------------------------------------------------------
# Sevimlilar
# ---------------------------------------------------------
elif page == "Sevimlilar":
    st.markdown('<div class="section-title">Sevimli obyektlaringiz</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Siz saqlagan manzillar shu yerda ko‘rinadi.</div>', unsafe_allow_html=True)
    if not st.session_state.favorites:
        st.markdown('<div class="info-box">Hozircha sevimli obyektlar yo‘q. “Turistik obyektlar” bo‘limidan istalgan manzilni saqlang.</div>', unsafe_allow_html=True)
    else:
        fav_df = df[df["name"].isin(st.session_state.favorites)]
        for _, row in fav_df.iterrows():
            spot_card(row.to_dict(), True)
        if st.button("Sevimlilarni tozalash"):
            st.session_state.favorites = []
            st.rerun()

# ---------------------------------------------------------
# Ilova haqida
# ---------------------------------------------------------
elif page == "Ilova haqida":
    st.markdown('<div class="section-title">Farg‘ona Travel haqida</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Farg‘ona viloyatining tarixiy, madaniy va tabiiy boyliklarini kashf etish uchun raqamli yordamchi.</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box"><b>Bizning maqsadimiz</b><br>Sayohatchilarga vaqt va byudjetiga mos, qulay va mazmunli marshrutni tez topishga yordam berish.</div>', unsafe_allow_html=True)
    st.markdown("### Platforma nimalarni taklif qiladi?")
    st.write("• Qiziqishlarga asoslangan shaxsiy tavsiyalar")
    st.write("• Byudjet va vaqt cheklovlarini hisobga oluvchi marshrut")
    st.write("• Turistik obyektlar bo‘yicha qidiruv va filtrlar")
    st.write("• Sevimli manzillarni saqlash")
    st.write("• Marshrutni CSV formatida yuklab olish")
    st.warning("Eslatma: narxlar va tashrif vaqtlari taxminiy. Safardan oldin ma’lumotlarni aniqlashtirish tavsiya etiladi.")

st.markdown('<div class="footer">Farg‘ona Travel · Sayohatingizni chiroyli rejalashtiring</div>', unsafe_allow_html=True)
