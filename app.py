import streamlit as st
from datetime import date, datetime
from backend import (
    submit_booking,
    get_bookings,
    update_booking_status,
    get_ai_response,
    get_poster_copy,
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

tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Home",
    "📅 Book Appointment",
    "🔐 Admin Requests",
    "🤖 AI Assistant",
])

with tab1:
    render_poster()
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

st.divider()
st.caption(
    "Hijama Wellness Center • Appointment requests are reviewed by the center. "
    "For urgent medical symptoms, seek appropriate medical care."
)
