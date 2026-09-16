import streamlit as st
from datetime import date, datetime
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
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root { --accent:#a84f77; --dark:#15151d; --card:#23232d; }
.stApp { background: #101116; }
.block-container { max-width: 1150px; padding-top: 1.5rem; }
.hero {
    padding: 28px; border-radius: 24px; margin-bottom: 22px;
    background: linear-gradient(135deg,#6f3151,#b65d82 55%,#351f2d);
    color: white; box-shadow: 0 12px 35px rgba(0,0,0,.25);
}
.hero h1 { font-size: clamp(2rem,5vw,3.5rem); margin:0 0 8px 0; }
.hero p { font-size:1.08rem; margin:6px 0; }
.info-card {
    background:#1d1d26; border:1px solid #343442; border-radius:18px;
    padding:18px; height:100%;
}
.small { color:#bdbdcc; font-size:.9rem; }
.poster {
    border-radius: 24px; padding: 30px; text-align:center; color:#fff;
    background: radial-gradient(circle at 15% 10%,#d58cac,transparent 30%),
                linear-gradient(135deg,#28131f,#7c3657,#21141b);
    border:1px solid #a84f77; box-shadow:0 12px 35px rgba(0,0,0,.25);
}
.poster h2 { font-size:2rem; margin-bottom:5px; }
.poster .phone { font-size:1.2rem; font-weight:700; }
.hadith-card { background:#171820; border:1px solid #6f3151; border-radius:20px; padding:24px; margin-top:18px; }
.hijri-date { background:#21141b; border:1px solid #5d3447; border-radius:14px; padding:14px; margin-bottom:10px; }
.warning { background:#2a2416; border:1px solid #665525; border-radius:14px; padding:14px; }
/* Mobile-friendly tab navigation: swipe horizontally to reach every tab. */
.stTabs [data-baseweb="tab-list"] {
    overflow-x: auto !important;
    flex-wrap: nowrap !important;
    scrollbar-width: thin;
    -webkit-overflow-scrolling: touch;
    gap: 4px;
    padding-bottom: 4px;
}
.stTabs [data-baseweb="tab"] {
    flex: 0 0 auto !important;
    white-space: nowrap !important;
}
@media (max-width: 700px) {
    .block-container { padding-left: .75rem; padding-right: .75rem; }
    .stTabs [data-baseweb="tab"] { font-size: .82rem; padding-left: .65rem; padding-right: .65rem; }
    .hero { padding: 20px; }
}
</style>
""", unsafe_allow_html=True)

def render_hero():
    st.markdown(f"""
    <div class="hero">
      <h1>🩸 Hijama Wellness Center</h1>
      <p>Traditional Hijama & wellness appointment service</p>
      <p>📍 {CONFIG['address']}</p>
      <p>📞 {CONFIG['phone1']} &nbsp; | &nbsp; {CONFIG['phone2']}</p>
    </div>
    """, unsafe_allow_html=True)

def render_poster():
    try:
        tagline = get_poster_copy()
    except Exception:
        tagline = "Book your Hijama appointment with our center."
    st.markdown(f"""
    <div class="poster">
      <div style="font-size:3rem">🩸</div>
      <h2>HIJAMA WELLNESS CENTER</h2>
      <p>{tagline}</p>
      <hr style="border-color:rgba(255,255,255,.25)">
      <p>👨 Muhammad Isreal — Male Practitioner</p>
      <p>👩 Shamim Akhtar — Female Practitioner</p>
      <p>📍 {CONFIG['address']}</p>
      <p class="phone">📞 {CONFIG['phone1']} &nbsp; {CONFIG['phone2']}</p>
    </div>
    """, unsafe_allow_html=True)

def islamic_calendar():
    st.subheader("🕌 Islamic Hijama Calendar")
    st.write(
        "The commonly cited Hijama dates in the hadith are the **17th, 19th and 21st of the Hijri month**. "
        "The Gregorian dates below are calculated from the Hijri calendar; local moon-sighting can differ by about a day, so confirm locally before booking."
    )

    dates = get_upcoming_hijama_dates(12)
    if dates:
        next_date = dates[0]
        st.success(
            f"🌙 **Next listed Hijama date:** {next_date['day']} — {next_date['hijri_date'].split(' ', 1)[1]} "
            f"({next_date['gregorian_date']})"
        )
        cols = st.columns(3)
        for i, row in enumerate(dates[:12]):
            with cols[i % 3]:
                st.markdown(
                    f'<div class="hijri-date"><b>🌙 {row["day"]} {row["hijri_date"].split(" ", 1)[1]}</b><br>'
                    f'📅 {row["gregorian_date"]}</div>',
                    unsafe_allow_html=True,
                )
        st.caption("Showing the next 12 calculated 17th, 19th and 21st Hijri dates.")
        st.link_button("📖 Read the hadith — Sunan Abi Dawud 3861", "https://sunnah.com/abudawud/29/7")
    else:
        st.warning("Hijri date conversion is unavailable. Please install the hijridate package from requirements.txt.")

    st.markdown("### 🩺 Symptoms & health concerns")
    st.write("People commonly ask about Hijama for headaches, muscle or neck/back discomfort, and general wellbeing. These are **not promises of cure**. Medical evidence for cupping varies by condition, and Hijama should not replace diagnosis or treatment from a qualified clinician.")
    st.markdown("""
    - Headache or tension-type pain
    - Neck, shoulder or back muscle discomfort
    - General relaxation/wellness requests
    - Questions about traditional Islamic healing practices
    """)
    st.markdown('<div class="warning"><b>Important:</b> Seek urgent medical care for chest pain, severe breathing difficulty, fainting, major bleeding, stroke symptoms, severe infection, or other emergency symptoms. Tell the practitioner about medicines, pregnancy, bleeding disorders, anemia, diabetes, or other important medical conditions before Hijama.</div>', unsafe_allow_html=True)


def islamic_poster():
    st.subheader("🕌 Islamic Hijama Poster")
    st.markdown("""
    <div class="poster">
      <div style="font-size:3rem">🌙 🩸</div>
      <h2>HIJAMA • الحجامة</h2>
      <p style="font-size:1.15rem"><b>17 • 19 • 21</b> of the Hijri month</p>
      <div class="hadith-card">
        <p style="font-size:1.2rem;line-height:1.7">“If anyone has himself cupped on the 17th, 19th and 21st it will be a remedy for every disease.”</p>
        <p><b>— Sunan Abi Dawud 3861</b></p>
        <p class="small">Reported from Abu Hurayrah رضي الله عنه. The hadith is graded Hasan by al-Albani on Sunnah.com.</p>
      </div>
      <hr style="border-color:rgba(255,255,255,.25)">
      <p>Traditional Islamic wellness • Appointment required</p>
      <p>👨 Muhammad Isreal — Male Practitioner</p>
      <p>👩 Shamim Akhtar — Female Practitioner</p>
      <p>📍 {address}</p>
      <p class="phone">📞 {phone1} &nbsp; {phone2}</p>
      <p style="font-size:.85rem">Hijama is complementary care and does not replace medical diagnosis or emergency treatment.</p>
    </div>
    """.format(address=CONFIG['address'], phone1=CONFIG['phone1'], phone2=CONFIG['phone2']), unsafe_allow_html=True)

def booking_form():
    st.subheader("📅 Book an Appointment")
    st.caption("Submit your preferred date. The center will review and confirm your appointment.")

    with st.form("booking_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full name *", placeholder="Enter your full name")
            gender = st.selectbox("Gender *", ["Male", "Female"])
            phone = st.text_input("Phone number *", placeholder="e.g. 0787960263")
        with c2:
            preferred_date = st.date_input(
                "Preferred Hijama date *",
                min_value=date.today(),
                value=date.today(),
            )
            preferred_time = st.selectbox(
                "Preferred time",
                ["Morning", "Afternoon", "Evening", "Flexible"],
            )
            practitioner = (
                "Muhammad Isreal" if gender == "Male" else "Shamim Akhtar"
            )
            st.text_input("Assigned practitioner", value=practitioner, disabled=True)

        notes = st.text_area(
            "Symptoms / notes / preferred time",
            placeholder="Tell the practitioner anything important about your appointment.",
            height=130,
        )
        consent = st.checkbox(
            "I understand this is an appointment request and the center will confirm availability."
        )
        submitted = st.form_submit_button(
            "📩 Submit Appointment Request",
            use_container_width=True,
            type="primary",
        )

    if submitted:
        if not name.strip() or not phone.strip():
            st.error("Please enter your full name and phone number.")
            return
        if not consent:
            st.error("Please confirm the appointment-request consent box.")
            return
        try:
            result = submit_booking(
                name=name.strip(),
                gender=gender,
                phone=phone.strip(),
                preferred_date=preferred_date.isoformat(),
                preferred_time=preferred_time,
                practitioner=practitioner,
                notes=notes.strip(),
            )
            st.success("✅ Appointment request received successfully.")
            st.info(
                f"Booking ID: **{result['booking_id']}**  \n"
                f"Practitioner: **{practitioner}**  \n"
                f"Status: **Pending**"
            )
        except Exception as e:
            st.error(f"Could not save the appointment: {e}")

def admin_panel():
    st.subheader("🔐 Admin — Appointment Requests")
    password = st.text_input("Admin password", type="password")
    if not password:
        st.caption("Enter the admin password configured in Streamlit Secrets.")
        return

    if password != CONFIG["admin_password"]:
        st.error("Incorrect admin password.")
        return

    st.success("Admin access granted.")
    bookings = get_bookings()

    if not bookings:
        st.info("No appointment requests yet.")
        return

    st.write(f"**{len(bookings)} appointment request(s)**")
    for b in bookings:
        with st.container(border=True):
            a, c = st.columns([3, 1])
            with a:
                st.markdown(f"### {b['booking_id']} — {b['name']}")
                st.write(
                    f"**Gender:** {b['gender']}  |  "
                    f"**Practitioner:** {b['practitioner']}"
                )
                st.write(
                    f"**Phone:** {b['phone']}  |  "
                    f"**Requested:** {b['preferred_date']} ({b['preferred_time']})"
                )
                st.write(f"**Notes:** {b['notes'] or '—'}")
                st.caption(f"Received: {b['created_at']}")
            with c:
                status = st.selectbox(
                    "Status",
                    ["Pending", "Confirmed", "Completed", "Cancelled"],
                    index=["Pending", "Confirmed", "Completed", "Cancelled"].index(
                        b["status"]
                    ),
                    key=f"status_{b['booking_id']}",
                )
                if st.button(
                    "Update",
                    key=f"update_{b['booking_id']}",
                    use_container_width=True,
                ):
                    update_booking_status(b["booking_id"], status)
                    st.rerun()

def ai_assistant():
    st.subheader("🤖 Hijama Information Assistant")
    st.caption(
        "Educational information only. The AI does not replace a qualified medical "
        "professional and should not be used to diagnose or prescribe treatment."
    )
    q = st.text_area(
        "Ask a question",
        placeholder="Example: What should I do before a Hijama appointment?",
        height=100,
    )
    if st.button("Ask Gemini", type="primary"):
        if not q.strip():
            st.warning("Please enter a question.")
            return
        with st.spinner("Preparing information..."):
            answer = get_ai_response(q.strip())
        st.markdown(answer)

render_hero()

st.caption("📱 On a phone, swipe the tab bar left/right to reach all sections.")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Home",
    "📅 Book",
    "🔐 Admin",
    "🤖 AI",
    "🕌 Islamic Calendar",
    "🖼️ Poster",
])

with tab1:
    render_poster()
    st.info("🕌 Sunnah scheduling: commonly cited Hijama dates are the 17th, 19th and 21st of each Hijri month. See the Islamic Calendar tab for upcoming dates.")
    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="info-card"><h3>👨 Male Practitioner</h3><b>Muhammad Isreal</b><p class="small">For male clients</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="info-card"><h3>👩 Female Practitioner</h3><b>Shamim Akhtar</b><p class="small">For female clients</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="info-card"><h3>📞 Contact</h3><b>{CONFIG["phone1"]}</b><br><b>{CONFIG["phone2"]}</b><p class="small">{CONFIG["address"]}</p></div>', unsafe_allow_html=True)

with tab2:
    booking_form()

with tab3:
    admin_panel()

with tab4:
    ai_assistant()

with tab5:
    islamic_calendar()

with tab6:
    islamic_poster()

st.divider()
st.caption(
    "Hijama Wellness Center • Appointment requests are reviewed by the center. "
    "For urgent medical symptoms, seek appropriate medical care."
)
