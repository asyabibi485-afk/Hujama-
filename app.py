import streamlit as st
from datetime import date, timedelta
from hijri import gregorian_to_hijri, hijri_to_gregorian, HIJRI_MONTH_NAMES, month_length

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Hijama Sunnah Center",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded",
)

CENTER_NAME = "Hijama Sunnah Center"
CENTER_ADDRESS = "Chaknore Tablighi Markaz, Jalalabad, Afghanistan"
CENTER_PHONE = "0787960263"
MAPS_QUERY = "Chaknore Tablighi Markaz, Jalalabad, Afghanistan".replace(" ", "+")
MAPS_URL = f"https://www.google.com/maps/search/?api=1&query={MAPS_QUERY}"

RECOMMENDED_DAYS = [17, 19, 21]

# ----------------------------------------------------------------------
# Style
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }

    :root {
        --primary: #0f6b5c;
        --primary-dark: #0a4d42;
        --accent: #c9a13b;
        --bg-soft: #f4f7f6;
    }

    .main { background-color: var(--bg-soft); }

    .hj-hero {
        background: linear-gradient(135deg, var(--primary-dark), var(--primary));
        color: white;
        padding: 2.2rem 2rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
    }
    .hj-hero h1 { margin: 0; font-size: 2rem; }
    .hj-hero p { margin: 0.4rem 0 0 0; opacity: 0.9; }

    .hj-arabic {
        font-family: 'Amiri', serif;
        font-size: 1.4rem;
        direction: rtl;
        color: var(--accent);
        margin-top: 0.6rem;
    }

    .hj-hero h1, .hj-hero p { color: #ffffff !important; }

    .hj-card {
        background: white;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
        border-left: 5px solid var(--primary);
    }
    .hj-card h4 { color: var(--primary-dark) !important; margin: 0 0 0.5rem 0; }

    .hj-day-good {
        background: #e7f5ef;
        border: 1px solid var(--primary);
        border-radius: 10px;
        padding: 0.6rem 0.8rem;
        text-align: center;
        font-weight: 600;
        color: var(--primary-dark);
    }
    .hj-day-normal {
        background: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 0.6rem 0.8rem;
        text-align: center;
        color: #555;
    }
    .hj-badge {
        display: inline-block;
        background: var(--accent);
        color: white;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.4rem;
    }
    .hj-contact-box {
        background: var(--primary-dark);
        color: white;
        padding: 1.4rem;
        border-radius: 14px;
    }
    .hj-contact-box h3, .hj-contact-box p, .hj-contact-box b { color: #ffffff !important; }
    .hj-contact-box a { color: #ffe9b0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Sidebar navigation
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"### 🩸 {CENTER_NAME}")
    st.caption("Cupping (Hijama) therapy according to the Sunnah")
    st.divider()
    st.markdown("**Adjust Hijri date**")
    hijri_adjustment = st.slider(
        "Moonsighting adjustment (days)", -1, 1, 0,
        help="The tabular calendar can differ by a day from local moonsighting announcements. Adjust here if your center follows a different sighting.",
    )
    st.divider()
    st.markdown(f"📞 {CENTER_PHONE}")
    st.markdown(f"📍 {CENTER_ADDRESS}")

today = date.today()
h_year, h_month, h_day = gregorian_to_hijri(today, hijri_adjustment)

tab_home, tab_calendar, tab_hadith, tab_conditions, tab_poster, tab_assistant, tab_contact = st.tabs(
    [
        "🏠 Home",
        "📅 Hijama Calendar",
        "📖 Hadith on Hijama",
        "🩺 Conditions & Symptoms",
        "🖼️ Poster",
        "🤖 Ask the Assistant",
        "📍 Book / Contact",
    ]
)

# ----------------------------------------------------------------------
# HOME
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# POSTER (illustrated SVG, print-ready)
# ----------------------------------------------------------------------
def build_poster_svg() -> str:
    """A tasteful, illustrated (non-photographic) poster: a reclining patient
    receiving cupping therapy, the Sunnah-recommended days, commonly treated
    conditions, a hadith, and the center's contact details."""
    cups = [
        (300, 430, 32), (400, 410, 28), (500, 430, 32),
        (330, 520, 26), (470, 520, 26),
        (260, 610, 24), (400, 630, 28), (540, 610, 24),
    ]
    cup_svg = ""
    for cx, cy, r in cups:
        cup_svg += (
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#e9c46a" opacity="0.85"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#0a4d42" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.45}" fill="#0f6b5c" opacity="0.55"/>'
        )

    conditions_line = "Migraine  •  Back Pain  •  Joint Pain  •  Fatigue  •  Sciatica  •  High BP*"

    raw = f"""<svg viewBox="0 0 800 1600" xmlns="http://www.w3.org/2000/svg" font-family="Georgia, serif">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#0a4d42"/>
<stop offset="100%" stop-color="#0f6b5c"/>
</linearGradient>
<linearGradient id="skin" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#f3e3cf"/>
<stop offset="100%" stop-color="#e7cfae"/>
</linearGradient>
</defs>
<rect width="800" height="1600" fill="url(#bg)"/>
<rect x="24" y="24" width="752" height="1552" fill="none" stroke="#e9c46a" stroke-width="3" rx="18"/>
<text x="400" y="80" text-anchor="middle" font-size="26" fill="#e9c46a" font-family="'Amiri', serif" direction="rtl">الحجامة سنة نبوية</text>
<text x="400" y="135" text-anchor="middle" font-size="46" fill="#ffffff" font-weight="bold">🩸 HIJAMA</text>
<text x="400" y="171" text-anchor="middle" font-size="20" fill="#e9c46a" letter-spacing="2">SUNNAH CUPPING THERAPY</text>
<text x="400" y="200" text-anchor="middle" font-size="15" fill="#cfe3dc" font-style="italic">A patient receiving Hijama (cupping) on the back</text>
<g>
<!-- legs (patient lying face-down) -->
<rect x="300" y="780" width="85" height="280" rx="35" fill="url(#skin)" stroke="#c9a473" stroke-width="2"/>
<rect x="415" y="780" width="85" height="280" rx="35" fill="url(#skin)" stroke="#c9a473" stroke-width="2"/>
<ellipse cx="342" cy="1075" rx="38" ry="24" fill="url(#skin)" stroke="#c9a473" stroke-width="2"/>
<ellipse cx="458" cy="1075" rx="38" ry="24" fill="url(#skin)" stroke="#c9a473" stroke-width="2"/>
<!-- arms resting relaxed at the sides -->
<rect x="165" y="410" width="55" height="170" rx="27" fill="url(#skin)" stroke="#c9a473" stroke-width="2" transform="rotate(18 192 495)"/>
<rect x="155" y="555" width="50" height="140" rx="25" fill="url(#skin)" stroke="#c9a473" stroke-width="2" transform="rotate(-8 180 625)"/>
<rect x="580" y="410" width="55" height="170" rx="27" fill="url(#skin)" stroke="#c9a473" stroke-width="2" transform="rotate(-18 608 495)"/>
<rect x="595" y="555" width="50" height="140" rx="25" fill="url(#skin)" stroke="#c9a473" stroke-width="2" transform="rotate(8 620 625)"/>
<!-- head -->
<ellipse cx="400" cy="330" rx="55" ry="60" fill="url(#skin)" stroke="#c9a473" stroke-width="2"/>
<!-- back / torso, where the cups are placed -->
<path d="M230 460 Q220 380 290 350 Q340 320 400 320 Q460 320 510 350 Q580 380 570 460 L560 700 Q560 760 500 780 L300 780 Q240 760 240 700 Z" fill="url(#skin)" stroke="#c9a473" stroke-width="2"/>
{cup_svg}
</g>
<g>
<rect x="230" y="1130" width="340" height="56" rx="28" fill="#e9c46a"/>
<text x="400" y="1166" text-anchor="middle" font-size="20" fill="#0a4d42" font-weight="bold">Best days: 17th, 19th &amp; 21st (Hijri)</text>
</g>
<text x="400" y="1235" text-anchor="middle" font-size="17" fill="#e9c46a" font-weight="bold">Commonly used for:</text>
<text x="400" y="1265" text-anchor="middle" font-size="16" fill="#f4f7f6">{conditions_line}</text>
<text x="400" y="1290" text-anchor="middle" font-size="12" fill="#cfe3dc" font-style="italic">*Educational only — not a diagnosis. Always consult the practitioner first.</text>
<text x="400" y="1335" text-anchor="middle" font-size="15" fill="#e9c46a" font-weight="bold">Hadith</text>
<text x="400" y="1365" text-anchor="middle" font-size="17" fill="#f4f7f6" font-style="italic">"If there were something excellent to be used as a remedy,</text>
<text x="400" y="1390" text-anchor="middle" font-size="17" fill="#f4f7f6" font-style="italic">it would be cupping." — Sunan Abi Dawud / Ibn Majah</text>
<line x1="120" y1="1420" x2="680" y2="1420" stroke="#e9c46a" stroke-width="1.5"/>
<text x="400" y="1458" text-anchor="middle" font-size="24" fill="#ffffff" font-weight="bold">{CENTER_NAME}</text>
<text x="400" y="1488" text-anchor="middle" font-size="17" fill="#e9c46a">📞 {CENTER_PHONE}</text>
<text x="400" y="1514" text-anchor="middle" font-size="16" fill="#f4f7f6">{CENTER_ADDRESS}</text>
<text x="400" y="1546" text-anchor="middle" font-size="14" fill="#cfe3dc">👨‍⚕️ Muhammad Isreal (male)&#160;&#160;&#160;&#160;👩‍⚕️ Shamim Akhtar (female)</text>
</svg>"""

    # Collapse to a single line with no blank lines: Streamlit's markdown
    # parser treats a blank line inside an HTML block as the end of that
    # block, after which indented text gets rendered as a literal code
    # block instead of as SVG. Keeping this on one line avoids that.
    return " ".join(line.strip() for line in raw.splitlines() if line.strip())


with tab_home:
    st.markdown(
        f"""
        <div class="hj-hero">
            <h1>🩸 {CENTER_NAME}</h1>
            <p>Cupping therapy (Al-Hijama) performed according to the Sunnah of the Prophet ﷺ</p>
            <div class="hj-arabic">الحجامة سنة نبوية</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""<div class="hj-card"><h4>📅 Today (Hijri)</h4>
            <p style="font-size:1.3rem;font-weight:700;color:#0f6b5c;">
            {h_day} {HIJRI_MONTH_NAMES[h_month-1]} {h_year} AH</p>
            <p style="color:#777;">{today.strftime('%A, %d %B %Y')}</p></div>""",
            unsafe_allow_html=True,
        )
    with col2:
        is_recommended = h_day in RECOMMENDED_DAYS
        status = "✅ Recommended day for Hijama" if is_recommended else "Not a specially recommended Sunnah date"
        color = "#0f6b5c" if is_recommended else "#a35b00"
        st.markdown(
            f"""<div class="hj-card"><h4>🩸 Today's status</h4>
            <p style="font-size:1.05rem;font-weight:600;color:{color};">{status}</p>
            <p style="color:#777;">Sunnah days: 17th, 19th &amp; 21st of the Hijri month</p></div>""",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""<div class="hj-card"><h4>📞 Contact</h4>
            <p style="font-weight:600;color:#1f2a27;">{CENTER_PHONE}</p>
            <p style="color:#777;">{CENTER_ADDRESS}</p></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("### About Hijama")
    st.write(
        """
        Hijama (cupping) is a traditional therapy encouraged in the Sunnah, in which
        suction cups are used on specific points of the body — sometimes combined with
        light skin incisions (wet cupping) — to draw blood to the surface. It has long
        been used alongside other traditional and modern treatments to support general
        wellbeing.
        """
    )
    st.info(
        "⚠️ This app provides general educational and Sunnah-based information only. "
        "It is **not** a medical diagnosis tool. Always consult a qualified Hijama "
        "practitioner or physician before treatment, especially if you have an existing "
        "medical condition, are pregnant, or are on blood-thinning medication."
    )

    st.markdown("### 🖼️ Cupping Poster")
    teaser_col1, teaser_col2 = st.columns([1, 2])
    with teaser_col1:
        st.markdown(
            f'<div style="max-width:180px;">{build_poster_svg()}</div>',
            unsafe_allow_html=True,
        )
    with teaser_col2:
        st.write(
            "A print-ready poster showing where cups are placed and the Sunnah-"
            "recommended days, with your center's contact details."
        )
        st.caption("Open the **🖼️ Poster** tab above for the full-size version and download button.")

# ----------------------------------------------------------------------
# CALENDAR
# ----------------------------------------------------------------------
with tab_calendar:
    st.header("📅 Sunnah Hijama Calendar")
    st.write(
        "According to hadith, the best days to perform Hijama are the **17th, 19th, "
        "and 21st** of the Hijri (lunar) month. This calendar converts the Gregorian "
        "date to Hijri and highlights the upcoming recommended days."
    )

    st.markdown(f"#### {HIJRI_MONTH_NAMES[h_month-1]} {h_year} AH")

    days_in_month = month_length(h_year, h_month)
    cols = st.columns(7)
    for i, d in enumerate(range(1, days_in_month + 1)):
        g_date = hijri_to_gregorian(h_year, h_month, d, hijri_adjustment)
        col = cols[i % 7]
        css = "hj-day-good" if d in RECOMMENDED_DAYS else "hj-day-normal"
        label = f"{d}<br><span style='font-size:0.7rem;'>{g_date.strftime('%d %b')}</span>"
        col.markdown(f"<div class='{css}'>{label}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔜 Next recommended Hijama dates")

    upcoming = []
    check_date = today
    for _ in range(120):
        y, m, d = gregorian_to_hijri(check_date, hijri_adjustment)
        if d in RECOMMENDED_DAYS:
            upcoming.append((check_date, d, m, y))
        check_date += timedelta(days=1)
        if len(upcoming) >= 6:
            break

    ucols = st.columns(3)
    for idx, (g_date, d, m, y) in enumerate(upcoming):
        with ucols[idx % 3]:
            st.markdown(
                f"""<div class="hj-card" style="border-left-color:#c9a13b;">
                <b style="color:#1f2a27;">{g_date.strftime('%A, %d %B %Y')}</b><br>
                <span style="color:#0f6b5c;">{d} {HIJRI_MONTH_NAMES[m-1]} {y} AH</span>
                <span class="hj-badge">Sunnah day</span>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("### Notes on timing")
    st.markdown(
        """
        - The 17th, 19th and 21st of the lunar month are the days most commonly mentioned in hadith as best for Hijama.
        - Many practitioners prefer performing Hijama on an empty stomach, or 2–3 hours after a light meal.
        - Avoid Hijama during acute illness with high fever, during heavy menstrual bleeding, or without a qualified practitioner's advice if pregnant or on blood thinners.
        - This calendar is a *tabular* approximation of the Hijri calendar. Use the "Moonsighting adjustment" slider in the sidebar if it does not match your local moon-sighting announcement.
        """
    )

# ----------------------------------------------------------------------
# HADITH
# ----------------------------------------------------------------------
with tab_hadith:
    st.header("📖 Hadith on Hijama (Cupping)")
    st.caption("Summarized in plain English from well-known hadith collections. Please refer to the original collections for the exact wording.")

    hadiths = [
        {
            "text": "The Prophet ﷺ said that healing may be found in three things: a drink of honey, the incision of a cupping instrument, or a cauterization by fire — but he discouraged cauterization.",
            "source": "Sahih al-Bukhari",
        },
        {
            "text": "The Prophet ﷺ was cupped while fasting.",
            "source": "Sahih al-Bukhari",
        },
        {
            "text": "The Prophet ﷺ said that the best treatment his community could use was Hijama (cupping).",
            "source": "Sahih al-Bukhari",
        },
        {
            "text": "The Prophet ﷺ said that if there were something excellent to be used as a remedy, it would be cupping.",
            "source": "Sunan Abi Dawud / Sunan Ibn Majah",
        },
        {
            "text": "The Prophet ﷺ said that on the night of his Night Journey (Isra), every group of angels he passed told him to instruct his community to practice cupping.",
            "source": "Sunan al-Tirmidhi",
        },
        {
            "text": "The Prophet ﷺ recommended having Hijama done on the 17th, 19th or 21st of the (Hijri) month.",
            "source": "Sunan Abi Dawud / Sunan Ibn Majah",
        },
    ]

    for h in hadiths:
        st.markdown(
            f"""<div class="hj-card">
            <p style="font-size:1.02rem;color:#1f2a27;">"{h['text']}"</p>
            <p style="color:#0f6b5c;font-weight:600;">— {h['source']}</p>
            </div>""",
            unsafe_allow_html=True,
        )

    st.info(
        "These are paraphrased summaries for general awareness, not literal word-for-word "
        "translations. For rulings or exact wording, please consult the original hadith "
        "collections or a qualified scholar."
    )

# ----------------------------------------------------------------------
# CONDITIONS
# ----------------------------------------------------------------------
with tab_conditions:
    st.header("🩺 Conditions Traditionally Addressed with Hijama")
    st.warning(
        "⚠️ **This section is educational only and is not a medical diagnosis.** "
        "Hijama is a complementary/traditional therapy. For any serious, persistent, "
        "or worsening symptom, please see a licensed physician. Our practitioners can "
        "advise you further during your appointment."
    )

    conditions = {
        "Headache / Migraine": "Cupping is commonly applied at the back of the neck and shoulders. Practitioners often ask about frequency, triggers, and whether the pain is one- or two-sided.",
        "Back & Joint Pain": "Local cupping near the affected joint or along the lower back is commonly used for chronic muscular or joint pain.",
        "High Blood Pressure": "Some traditional practitioners use cupping at specific points; this should only be done under supervision and alongside your regular medical treatment — never as a replacement for prescribed medication.",
        "Fatigue / Low Energy": "General wet cupping on the upper back is traditionally used; practitioners typically also ask about sleep, diet, and stress levels.",
        "Sciatica": "Cupping along the lower back and leg is sometimes used together with stretching advice.",
        "Skin Conditions": "Localized cupping near the affected area is sometimes used; a practitioner will examine the skin first.",
    }

    for cond, desc in conditions.items():
        with st.expander(f"🔹 {cond}"):
            st.write(desc)

    st.markdown("### Simple symptom guide")
    symptom = st.selectbox(
        "Select your main symptom to see the general area of focus (for discussion with your practitioner — not a prescription):",
        list(conditions.keys()),
    )
    st.success(f"**{symptom}** — {conditions[symptom]}")
    st.caption("Bring this note with you to your appointment so the practitioner can assess you properly.")


with tab_poster:
    st.header("🖼️ Poster — Hijama Cupping Therapy")
    st.write(
        "An illustrated (non-photographic) poster you can display in the app, print, "
        "or share — showing where cups are typically placed, the Sunnah-recommended "
        "days, and your center's contact details."
    )

    poster_svg = build_poster_svg()

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f'<div style="max-width:420px;margin:auto;">{poster_svg}</div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown("#### Download")
        st.download_button(
            label="⬇️ Download poster (SVG)",
            data=poster_svg,
            file_name="hijama_poster.svg",
            mime="image/svg+xml",
        )
        st.caption(
            "SVG opens cleanly in Illustrator, Inkscape, Canva, or any browser, and "
            "prints sharply at any size (A3/A4 poster, flyer, banner, etc.)."
        )
        st.info(
            "This is a stylized illustration, not a real photo — kept simple and "
            "tasteful for public display."
        )

# ----------------------------------------------------------------------
# ASSISTANT (Gemini)
# ----------------------------------------------------------------------
with tab_assistant:
    st.header("🤖 Ask the Hijama Assistant")
    st.write(
        "This assistant can answer general questions about Hijama and help you decide "
        "whether to book with our **male** or **female** practitioner. It does not "
        "replace an in-person consultation."
    )

    configured_key = st.secrets.get("GEMINI_API_KEY", "")
    if configured_key:
        st.caption("✅ Assistant is ready — connected using the center's Gemini API key.")
    else:
        with st.expander("🔑 Gemini API setup", expanded=True):
            st.write(
                "No Gemini API key is configured for this app yet. You can either "
                "add one for everyone in **Secrets** (see README), or paste your own "
                "key below just for this session."
            )
            typed_key = st.text_input("Gemini API key", type="password", value=st.session_state.get("api_key", ""))
            if typed_key:
                st.session_state["api_key"] = typed_key

    patient_gender = st.radio("I am seeking treatment as a:", ["Male patient", "Female patient"], horizontal=True)
    doctor_label = "male practitioner, Muhammad Isreal" if patient_gender == "Male patient" else "female practitioner, Shamim Akhtar"
    badge_color = "#0f6b5c" if patient_gender == "Male patient" else "#a3557a"
    st.markdown(
        f"""<div style="background:{badge_color};color:#ffffff;padding:0.7rem 1rem;
        border-radius:10px;font-weight:600;margin-bottom:0.6rem;">
        You'll be matched with our {doctor_label} for in-person treatment.
        </div>""",
        unsafe_allow_html=True,
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask a question about Hijama, timing, or booking...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        api_key = st.secrets.get("GEMINI_API_KEY", "") or st.session_state.get("api_key", "")
        if not api_key:
            reply = "Please enter a Gemini API key in the box above so I can answer your question."
        else:
            try:
                import google.generativeai as genai

                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")

                system_context = (
                    "You are a helpful assistant for an Islamic Hijama (cupping) therapy "
                    f"center. The patient is a {patient_gender.lower()} who will be treated "
                    f"by our {doctor_label}. Answer questions about Hijama, Sunnah timing, "
                    "and general wellbeing in a warm, respectful tone. Do NOT give a medical "
                    "diagnosis or prescribe treatment — always recommend an in-person "
                    "consultation with the practitioner for anything specific. Keep answers "
                    "concise."
                )
                response = model.generate_content(f"{system_context}\n\nPatient question: {user_input}")
                reply = response.text
            except Exception as e:
                reply = f"Sorry, I couldn't reach the assistant right now ({e}). Please try again or contact the center directly at {CENTER_PHONE}."

        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)

# ----------------------------------------------------------------------
# BOOK / CONTACT
# ----------------------------------------------------------------------
with tab_contact:
    st.header("📍 Book an Appointment")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(
            f"""
            <div class="hj-contact-box">
            <h3>{CENTER_NAME}</h3>
            <p>📞 <b>{CENTER_PHONE}</b></p>
            <p>📍 {CENTER_ADDRESS}</p>
            <p><a href="{MAPS_URL}" target="_blank">Open location in Google Maps →</a></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("#### Practitioners")
        st.markdown(
            """<div style="background:#0f6b5c;color:#ffffff;padding:0.6rem 1rem;
            border-radius:10px;font-weight:600;margin-bottom:0.5rem;">
            👨‍⚕️ Muhammad Isreal — treats male patients</div>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """<div style="background:#a3557a;color:#ffffff;padding:0.6rem 1rem;
            border-radius:10px;font-weight:600;">
            👩‍⚕️ Shamim Akhtar — treats female patients</div>""",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("#### Request a booking")
        with st.form("booking_form"):
            name = st.text_input("Full name")
            gender = st.selectbox("Gender", ["Male", "Female"])
            phone = st.text_input("Your phone number")
            preferred_date = st.date_input("Preferred date", value=today)
            notes = st.text_area("Notes (symptom, preferred time, etc.)")
            submitted = st.form_submit_button("Prepare booking request")

            if submitted:
                if not name or not phone:
                    st.error("Please provide your name and phone number.")
                else:
                    practitioner = "Muhammad Isreal (male practitioner)" if gender == "Male" else "Shamim Akhtar (female practitioner)"
                    st.success("Booking request prepared. Please call or message the number below to confirm your appointment.")
                    st.markdown(
                        f"""
                        **Summary**
                        - Name: {name}
                        - Gender: {gender} → {practitioner}
                        - Phone: {phone}
                        - Preferred date: {preferred_date.strftime('%A, %d %B %Y')}
                        - Notes: {notes or '—'}

                        📞 Please confirm by calling **{CENTER_PHONE}**.
                        """
                    )

    st.markdown("---")
    st.caption(
        "This form does not submit automatically to the center's system — it prepares a "
        "summary for you to confirm by phone. Connect a messaging/CRM tool for direct "
        "automatic submission if needed."
    )
