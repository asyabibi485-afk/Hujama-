import streamlit as st
from datetime import date
from backend import (
    submit_booking,
    get_bookings,
    update_booking_status,
    get_ai_response,
    get_poster_copy,
    get_upcoming_hijama_dates,
    CONFIG,
)

st.set_page_config(
    page_title="Hijama Wellness Center",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- Figma-style UI --------------------
st.markdown("""
<style>
:root { --bg:#0d1017; --panel:#151a24; --panel2:#1b2130; --line:#2a3242; --text:#f7f8fb; --muted:#aab3c3; --accent:#c15b86; --accent2:#8d3f62; }
.stApp { background: radial-gradient(circle at 80% -10%, #2b1725 0, transparent 32%), var(--bg); color:var(--text); }
.block-container { max-width:1180px; padding:1.1rem 1rem 3rem; }
section[data-testid="stSidebar"] { background:#10141d; }
.hero { position:relative; overflow:hidden; border:1px solid #553047; border-radius:28px; padding:30px; margin-bottom:18px; background:linear-gradient(135deg,#24131d 0%,#733452 52%,#2b1824 100%); box-shadow:0 18px 50px rgba(0,0,0,.28); }
.hero:after { content:""; position:absolute; width:220px; height:220px; right:-70px; top:-90px; border-radius:50%; background:rgba(255,255,255,.08); }
.hero h1 { font-size:clamp(2rem,5vw,3.2rem); line-height:1.05; margin:0; letter-spacing:-1px; }
.hero p { color:#eee8ed; margin:.45rem 0 0; }
.eyebrow { text-transform:uppercase; letter-spacing:2px; font-size:.72rem; font-weight:800; color:#f0b4cd; margin-bottom:8px; }
.nav-wrap { position:sticky; top:0; z-index:20; background:rgba(13,16,23,.92); backdrop-filter:blur(14px); border:1px solid var(--line); border-radius:18px; padding:7px; margin-bottom:20px; }
.nav-scroll { overflow-x:auto; white-space:nowrap; scrollbar-width:thin; -webkit-overflow-scrolling:touch; padding-bottom:2px; }
.nav-scroll::-webkit-scrollbar { height:4px; }
.nav-scroll::-webkit-scrollbar-thumb { background:#454d5e; border-radius:10px; }
.nav-scroll .stButton { display:inline-block; min-width:max-content; margin-right:5px; }
.nav-scroll .stButton > button { border-radius:12px; border:1px solid transparent; background:transparent; color:#bac2d0; padding:.55rem .85rem; font-weight:700; }
.nav-scroll .stButton > button:hover { border-color:#4a5568; color:#fff; background:#1c2230; }
.nav-hint { color:#8993a5; font-size:.78rem; padding:4px 8px 0; }
.section-title { font-size:1.65rem; font-weight:800; margin:.2rem 0 .25rem; }
.section-sub { color:var(--muted); margin-bottom:1rem; }
.card { background:linear-gradient(180deg,#181e29,#131821); border:1px solid var(--line); border-radius:20px; padding:20px; height:100%; box-shadow:0 10px 25px rgba(0,0,0,.13); }
.card h3 { margin-top:0; }
.metric { font-size:1.8rem; font-weight:850; }
.muted { color:var(--muted); font-size:.88rem; }
.pill { display:inline-block; border:1px solid #5c3047; background:#241723; color:#efb0ca; border-radius:999px; padding:5px 10px; font-size:.76rem; font-weight:800; }
.calendar-card { background:linear-gradient(145deg,#1b1824,#251521); border:1px solid #5a3048; border-radius:18px; padding:15px; margin-bottom:10px; }
.calendar-card .day { font-size:1.1rem; font-weight:850; }
.poster { border-radius:28px; padding:32px; text-align:center; color:#fff; background:radial-gradient(circle at 12% 5%,#d68cad,transparent 28%),linear-gradient(135deg,#20111a,#813957,#1b1218); border:1px solid #9d4c70; box-shadow:0 18px 50px rgba(0,0,0,.25); }
.poster h2 { font-size:2rem; margin:.2rem 0; }
.hadith-card { background:rgba(10,11,16,.42); border:1px solid rgba(255,255,255,.18); border-radius:20px; padding:22px; margin:18px 0; }
.warning { background:#292316; border:1px solid #6c5a2c; border-radius:16px; padding:15px; }
.stButton > button, .stDownloadButton > button { border-radius:12px; font-weight:700; }
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"], .stDateInput input { border-radius:12px !important; }
div[data-testid="stForm"] { border:1px solid var(--line); border-radius:22px; padding:20px; background:#131821; }
 .role-shell { background:rgba(255,255,255,.045); border:1px solid var(--line); border-radius:20px; padding:10px; margin:0 auto 16px; max-width:560px; }
.role-label { color:#8f99aa; font-size:.68rem; font-weight:900; letter-spacing:1.8px; padding:2px 8px 8px; text-align:center; }
.bottom-nav { position:sticky; bottom:10px; z-index:30; margin-top:26px; padding:8px; border:1px solid var(--line); border-radius:22px; background:rgba(16,20,29,.94); backdrop-filter:blur(18px); box-shadow:0 16px 40px rgba(0,0,0,.28); }
.bottom-nav .stButton > button { min-height:48px; white-space:pre-line; line-height:1.05; font-size:.74rem; padding:.45rem .2rem; }
.admin-nav { background:rgba(255,255,255,.04); border:1px solid var(--line); border-radius:18px; padding:7px; margin-bottom:20px; }
.admin-nav .stButton > button { min-height:42px; }
.role-card { background:linear-gradient(145deg,#1b1f2a,#141821); border:1px solid var(--line); border-radius:24px; padding:24px; box-shadow:0 14px 40px rgba(0,0,0,.16); }
.admin-hero { background:linear-gradient(135deg,#121b2a,#1c3145); border:1px solid #29445d; border-radius:24px; padding:25px; margin-bottom:18px; }
.status-dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:#79d6a4; margin-right:7px; }
@media (max-width:700px) {
  .block-container { padding:.7rem .65rem 2.5rem; }
  .hero { padding:22px; border-radius:22px; }
  .hero h1 { font-size:2rem; }
  .nav-wrap { border-radius:15px; }
  .card { padding:16px; }
  .poster { padding:22px 15px; }
  .poster h2 { font-size:1.45rem; }
}
</style>
""", unsafe_allow_html=True)

PAGES = [
    ("🏠", "Home"),
    ("📅", "Book Appointment"),
    ("🕌", "Hijama Calendar"),
    ("🖼️", "Islamic Poster"),
    ("🤖", "AI Assistant"),
    ("🔐", "Admin"),
]

if "role" not in st.session_state:
    st.session_state.role = "Patient"
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False


def set_page(name):
    st.session_state.page = name


def render_header():
    st.markdown(f"""
    <div class="hero">
      <div class="eyebrow">Traditional Hijama • Wellness • Appointments</div>
      <h1>🩸 Hijama Wellness Center</h1>
      <p>Book appointments, view the Islamic Hijama calendar, and explore educational information.</p>
      <p>📍 {CONFIG['address']} &nbsp; • &nbsp; 📞 {CONFIG['phone1']} / {CONFIG['phone2']}</p>
    </div>
    """, unsafe_allow_html=True)


def render_role_switch():
    st.markdown('<div class="role-shell"><div class="role-label">APP MODE</div>', unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        if st.button("👤  Patient",key="role_patient",use_container_width=True,type="primary" if st.session_state.role=="Patient" else "secondary"):
            st.session_state.role="Patient"; st.session_state.page="Home"; st.session_state.admin_authenticated=False; st.rerun()
    with c2:
        if st.button("🔐  Admin",key="role_admin",use_container_width=True,type="primary" if st.session_state.role=="Admin" else "secondary"):
            st.session_state.role="Admin"; st.session_state.page="Dashboard"; st.rerun()
    st.markdown('</div>',unsafe_allow_html=True)

def render_patient_nav():
    pages=[("⌂","Home"),("＋","Book"),("☾","Calendar"),("✦","Poster"),("✧","Assistant")]
    mapping={"Book":"Book Appointment","Calendar":"Hijama Calendar","Poster":"Islamic Poster","Assistant":"AI Assistant"}
    st.markdown('<div class="bottom-nav">',unsafe_allow_html=True)
    for col,(icon,name) in zip(st.columns(5,gap="small"),pages):
        with col:
            target=mapping.get(name,name)
            if st.button(f"{icon}\n{name}",key=f"pnav_{name}",use_container_width=True,type="primary" if st.session_state.page==target else "secondary"):
                st.session_state.page=target; st.rerun()
    st.markdown('</div>',unsafe_allow_html=True)

def render_admin_nav():
    pages=[("▦","Dashboard"),("◷","Appointments"),("⚙","Settings")]
    st.markdown('<div class="admin-nav">',unsafe_allow_html=True)
    for col,(icon,name) in zip(st.columns(3,gap="small"),pages):
        with col:
            if st.button(f"{icon}  {name}",key=f"anav_{name}",use_container_width=True,type="primary" if st.session_state.page==name else "secondary"):
                st.session_state.page=name; st.rerun()
    st.markdown('</div>',unsafe_allow_html=True)

def render_poster_compact():
    try:
        tagline = get_poster_copy()
    except Exception:
        tagline = "Traditional Hijama & wellness appointment service."
    st.markdown(f"""
    <div class="poster">
      <div style="font-size:2.8rem">🌙 🩸</div>
      <h2>HIJAMA WELLNESS CENTER</h2>
      <p>{tagline}</p>
      <hr style="border-color:rgba(255,255,255,.2)">
      <p>👨 Muhammad Isreal — Male Practitioner</p>
      <p>👩 Shamim Akhtar — Female Practitioner</p>
      <p>📍 {CONFIG['address']}</p>
      <p><b>📞 {CONFIG['phone1']} &nbsp; {CONFIG['phone2']}</b></p>
    </div>
    """, unsafe_allow_html=True)


def home_page():
    st.markdown('<div class="section-title">Welcome</div><div class="section-sub">A simple mobile-first dashboard for your Hijama center.</div>', unsafe_allow_html=True)
    render_poster_compact()
    st.write("")
    cols = st.columns(3)
    items = [
        ("👨 Male Practitioner", "Muhammad Isreal", "For male clients"),
        ("👩 Female Practitioner", "Shamim Akhtar", "For female clients"),
        ("🕌 Sunnah Dates", "17 • 19 • 21", "Hijri dates commonly cited for Hijama"),
    ]
    for col, (title, value, sub) in zip(cols, items):
        with col:
            st.markdown(f'<div class="card"><h3>{title}</h3><div class="metric">{value}</div><div class="muted">{sub}</div></div>', unsafe_allow_html=True)
    st.write("")
    st.info("Tip: Open **Hijama Calendar** to see the next calculated 17th, 19th and 21st Hijri dates. Local moon-sighting may differ.")


def booking_page():
    st.markdown('<div class="section-title">📅 Book an Appointment</div><div class="section-sub">Choose a preferred date and practitioner. The center will review and confirm the request.</div>', unsafe_allow_html=True)
    with st.form("booking_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full name *", placeholder="Enter your full name")
            gender = st.selectbox("Gender *", ["Male", "Female"])
            phone = st.text_input("Phone number *", placeholder="e.g. 0787960263")
        with c2:
            preferred_date = st.date_input("Preferred Hijama date *", min_value=date.today(), value=date.today())
            preferred_time = st.selectbox("Preferred time", ["Morning", "Afternoon", "Evening", "Flexible"])
            practitioner = "Muhammad Isreal" if gender == "Male" else "Shamim Akhtar"
            st.text_input("Assigned practitioner", value=practitioner, disabled=True)
        notes = st.text_area("Symptoms / notes / preferred time", placeholder="Tell the practitioner anything important about your appointment.", height=120)
        consent = st.checkbox("I understand this is an appointment request and the center will confirm availability.")
        submitted = st.form_submit_button("📩 Submit Appointment Request", use_container_width=True, type="primary")
    if submitted:
        if not name.strip() or not phone.strip():
            st.error("Please enter your full name and phone number.")
            return
        if not consent:
            st.error("Please confirm the appointment-request consent box.")
            return
        try:
            result = submit_booking(name=name.strip(), gender=gender, phone=phone.strip(), preferred_date=preferred_date.isoformat(), preferred_time=preferred_time, practitioner=practitioner, notes=notes.strip())
            st.success("✅ Appointment request received successfully.")
            st.info(f"Booking ID: **{result['booking_id']}**  \nPractitioner: **{practitioner}**  \nStatus: **Pending**")
        except Exception as e:
            st.error(f"Could not save the appointment: {e}")


def calendar_page():
    st.markdown('<div class="section-title">🕌 Islamic Hijama Calendar</div><div class="section-sub">Upcoming 17th, 19th and 21st Hijri dates for planning Hijama appointments.</div>', unsafe_allow_html=True)
    st.markdown('<div class="warning"><b>Calendar note:</b> These Gregorian dates are calculated from the Hijri calendar. Local moon-sighting can shift the date by about one day, so confirm the local date before booking.</div>', unsafe_allow_html=True)
    dates = get_upcoming_hijama_dates(12)
    if dates:
        next_date = dates[0]
        st.success(f"🌙 **Next listed Hijama date:** {next_date['day']} — {next_date['hijri_date'].split(' ', 1)[1]} ({next_date['gregorian_date']})")
        cols = st.columns(3)
        for i, row in enumerate(dates[:12]):
            with cols[i % 3]:
                st.markdown(f'<div class="calendar-card"><div class="pill">{row["day"]} HIJRI</div><div class="day">🌙 {row["hijri_date"].split(" ", 1)[1]}</div><div class="muted">📅 {row["gregorian_date"]}</div></div>', unsafe_allow_html=True)
        st.caption("Showing the next 12 calculated Hijama dates.")
        st.link_button("📖 Read Sunan Abi Dawud 3861", "https://sunnah.com/abudawud/29/7")
    else:
        st.warning("Hijri date conversion is unavailable. Please install hijridate from requirements.txt.")
    st.write("")
    st.markdown('<div class="section-title">🩺 Symptoms & health concerns</div>', unsafe_allow_html=True)
    st.write("People may ask about Hijama for headaches, muscle or neck/back discomfort, and general wellbeing. These are **not promises of cure**. Hijama should not replace diagnosis or treatment from a qualified clinician.")
    cols = st.columns(4)
    for col, text in zip(cols, ["Headache / tension", "Neck & shoulder discomfort", "Back / muscle discomfort", "General wellness"]):
        with col:
            st.markdown(f'<div class="card"><b>🩺 {text}</b><div class="muted">Discuss symptoms with a qualified professional.</div></div>', unsafe_allow_html=True)
    st.write("")
    st.markdown('<div class="warning"><b>Important:</b> Seek urgent medical care for chest pain, severe breathing difficulty, fainting, major bleeding, stroke symptoms, severe infection, or other emergency symptoms. Tell the practitioner about medicines, pregnancy, bleeding disorders, anemia, diabetes, or other important medical conditions before Hijama.</div>', unsafe_allow_html=True)


def poster_page():
    st.markdown('<div class="section-title">🖼️ Islamic Hijama Poster</div><div class="section-sub">A clean poster layout suitable for sharing on your center page.</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="poster">
      <div style="font-size:3.2rem">🌙 🩸</div>
      <h2>HIJAMA • الحجامة</h2>
      <p style="font-size:1.2rem"><b>17 • 19 • 21</b> of the Hijri month</p>
      <div class="hadith-card">
        <p style="font-size:1.2rem;line-height:1.75">“If anyone has himself cupped on the 17th, 19th and 21st it will be a remedy for every disease.”</p>
        <p><b>— Sunan Abi Dawud 3861</b></p>
        <p style="color:#d6d9df;font-size:.9rem">Reported from Abu Hurayrah رضي الله عنه. Sunnah.com lists the hadith as Hasan according to al-Albani.</p>
      </div>
      <p>Traditional Islamic wellness • Appointment required</p>
      <p>👨 Muhammad Isreal — Male Practitioner</p>
      <p>👩 Shamim Akhtar — Female Practitioner</p>
      <p>📍 {CONFIG['address']}</p>
      <p><b>📞 {CONFIG['phone1']} &nbsp; {CONFIG['phone2']}</b></p>
      <p style="font-size:.82rem">Hijama is complementary care and does not replace medical diagnosis or emergency treatment.</p>
    </div>
    """, unsafe_allow_html=True)


def ai_page():
    st.markdown('<div class="section-title">🤖 Hijama Information Assistant</div><div class="section-sub">Educational information only — not diagnosis or prescribing.</div>', unsafe_allow_html=True)
    q = st.text_area("Ask a question", placeholder="Example: What should I do before a Hijama appointment?", height=110)
    if st.button("Ask Gemini", type="primary"):
        if not q.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Preparing information..."):
                st.markdown(get_ai_response(q.strip()))


def admin_login():
    st.markdown('<div class="section-title">🔐 Admin sign in</div><div class="section-sub">Private center management area. Patients cannot see appointment records.</div>',unsafe_allow_html=True)
    with st.container(border=True):
        password=st.text_input("Admin password",type="password",placeholder="Enter admin password")
        if st.button("Sign in to Admin",type="primary",use_container_width=True):
            if password==CONFIG["admin_password"]:
                st.session_state.admin_authenticated=True; st.session_state.page="Dashboard"; st.rerun()
            else: st.error("Incorrect admin password.")

def admin_dashboard():
    bookings=get_bookings(); pending=sum(b.get("status")=="Pending" for b in bookings); confirmed=sum(b.get("status")=="Confirmed" for b in bookings); completed=sum(b.get("status")=="Completed" for b in bookings)
    st.markdown('<div class="admin-hero"><div class="eyebrow">CENTER CONTROL</div><h2 style="margin:0">Admin Dashboard</h2><p style="margin:.4rem 0 0;color:#c5d0dc"><span class="status-dot"></span>Management mode is active</p></div>',unsafe_allow_html=True)
    for col,title,value in zip(st.columns(4),["Total","Pending","Confirmed","Completed"],[len(bookings),pending,confirmed,completed]):
        with col: st.markdown(f'<div class="card"><div class="muted">{title}</div><div class="metric">{value}</div></div>',unsafe_allow_html=True)
    st.write("")
    if bookings:
        st.markdown('<div class="section-title">Recent requests</div>',unsafe_allow_html=True)
        for b in bookings[:5]:
            st.markdown(f'<div class="card"><b>{b["name"]}</b><div class="muted">{b["booking_id"]} • {b["preferred_date"]} • {b["preferred_time"]}</div><p>{b["gender"]} • {b["practitioner"]} • <b>{b["status"]}</b></p></div>',unsafe_allow_html=True); st.write("")
    else: st.info("No appointment requests yet.")

def admin_appointments():
    st.markdown('<div class="section-title">◷ Appointments</div><div class="section-sub">Review, confirm, complete, or cancel patient requests.</div>',unsafe_allow_html=True)
    bookings=get_bookings()
    if not bookings: st.info("No appointment requests yet."); return
    statuses=["Pending","Confirmed","Completed","Cancelled"]
    for b in bookings:
        with st.container(border=True):
            a,c=st.columns([3,1])
            with a:
                st.markdown(f'### {b["booking_id"]} — {b["name"]}')
                st.write(f'**Gender:** {b["gender"]} | **Practitioner:** {b["practitioner"]}')
                st.write(f'**Phone:** {b["phone"]} | **Requested:** {b["preferred_date"]} ({b["preferred_time"]})')
                st.write(f'**Notes:** {b["notes"] or "—"}')
            with c:
                key=b["booking_id"]; status=st.selectbox("Status",statuses,index=statuses.index(b["status"]),key=f"status_{key}")
                if st.button("Save",key=f"update_{key}",use_container_width=True): update_booking_status(key,status); st.rerun()

def admin_settings():
    st.markdown('<div class="section-title">⚙ Admin Settings</div><div class="section-sub">Center information and account configuration.</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="role-card"><h3>Center profile</h3><p><b>Address</b><br>{CONFIG["address"]}</p><p><b>Phone</b><br>{CONFIG["phone1"]} / {CONFIG["phone2"]}</p><p><b>Male practitioner</b><br>Muhammad Isreal</p><p><b>Female practitioner</b><br>Shamim Akhtar</p></div>',unsafe_allow_html=True)
    st.write("")
    if st.button("Sign out of Admin",use_container_width=True): st.session_state.admin_authenticated=False; st.session_state.role="Patient"; st.session_state.page="Home"; st.rerun()


render_header()
render_role_switch()

if st.session_state.role == "Patient":
    render_patient_nav()
    if st.session_state.page == "Home": home_page()
    elif st.session_state.page == "Book Appointment": booking_page()
    elif st.session_state.page == "Hijama Calendar": calendar_page()
    elif st.session_state.page == "Islamic Poster": poster_page()
    elif st.session_state.page == "AI Assistant": ai_page()
else:
    if not st.session_state.admin_authenticated:
        admin_login()
    else:
        render_admin_nav()
        if st.session_state.page == "Dashboard": admin_dashboard()
        elif st.session_state.page == "Appointments": admin_appointments()
        elif st.session_state.page == "Settings": admin_settings()

st.divider()
st.caption("Hijama Wellness Center • Separate Patient and Admin interfaces. For urgent medical symptoms, seek appropriate medical care.")
