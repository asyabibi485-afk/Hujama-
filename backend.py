from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from typing import Dict, List

import streamlit as st

# ---------------------------
# Center configuration
# ---------------------------
DEFAULT_CONFIG = {
    "phone1": "0787960263",
    "phone2": "0784607516",
    "address": "Chaknore Tablighi Markaz, Jalalabad, Afghanistan",
    "admin_password": "CHANGE_ME",
    "google_sheet_name": "Hijama Appointment Requests",
    "google_worksheet": "Bookings",
    "gemini_model": "gemini-2.5-flash",
}

def _secret(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name, default)
        return str(value)
    except Exception:
        return os.getenv(name, default)

CONFIG = {
    "phone1": _secret("PHONE_1", DEFAULT_CONFIG["phone1"]),
    "phone2": _secret("PHONE_2", DEFAULT_CONFIG["phone2"]),
    "address": _secret("CENTER_ADDRESS", DEFAULT_CONFIG["address"]),
    "admin_password": _secret("ADMIN_PASSWORD", DEFAULT_CONFIG["admin_password"]),
    "google_sheet_name": _secret("GOOGLE_SHEET_NAME", DEFAULT_CONFIG["google_sheet_name"]),
    "google_worksheet": _secret("GOOGLE_WORKSHEET", DEFAULT_CONFIG["google_worksheet"]),
    "gemini_model": _secret("GEMINI_MODEL", DEFAULT_CONFIG["gemini_model"]),
}

HEADERS = [
    "booking_id",
    "created_at",
    "name",
    "gender",
    "phone",
    "preferred_date",
    "preferred_time",
    "practitioner",
    "notes",
    "status",
]

def _google_sheet():
    """Return a Google worksheet if Google Sheets credentials are configured."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        if "gcp_service_account" not in st.secrets:
            return None

        service_account_info = dict(st.secrets["gcp_service_account"])
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = Credentials.from_service_account_info(
            service_account_info, scopes=scopes
        )
        gc = gspread.authorize(credentials)

        try:
            sh = gc.open(CONFIG["google_sheet_name"])
        except gspread.SpreadsheetNotFound:
            sh = gc.create(CONFIG["google_sheet_name"])

        try:
            ws = sh.worksheet(CONFIG["google_worksheet"])
        except gspread.WorksheetNotFound:
            ws = sh.add_worksheet(title=CONFIG["google_worksheet"], rows=1000, cols=len(HEADERS))

        first_row = ws.row_values(1)
        if first_row != HEADERS:
            ws.update("A1:J1", [HEADERS])
        return ws
    except Exception:
        return None

def _local_file() -> str:
    # Local fallback only. Streamlit Community Cloud may reset local files.
    return os.path.join("/tmp", "hijama_bookings.json")

def _read_local() -> List[Dict]:
    path = _local_file()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _write_local(rows: List[Dict]) -> None:
    with open(_local_file(), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

def submit_booking(
    name: str,
    gender: str,
    phone: str,
    preferred_date: str,
    preferred_time: str,
    practitioner: str,
    notes: str,
) -> Dict:
    # Basic validation
    if gender not in ("Male", "Female"):
        raise ValueError("Invalid gender.")
    expected = "Muhammad Isreal" if gender == "Male" else "Shamim Akhtar"
    if practitioner != expected:
        practitioner = expected

    clean_phone = re.sub(r"[^\d+]", "", phone)
    if len(re.sub(r"\D", "", clean_phone)) < 7:
        raise ValueError("Please enter a valid phone number.")

    booking = {
        "booking_id": "HJ-" + uuid.uuid4().hex[:8].upper(),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "name": name[:120],
        "gender": gender,
        "phone": clean_phone[:30],
        "preferred_date": preferred_date,
        "preferred_time": preferred_time,
        "practitioner": practitioner,
        "notes": notes[:1000],
        "status": "Pending",
    }

    ws = _google_sheet()
    if ws is not None:
        ws.append_row([booking[h] for h in HEADERS], value_input_option="USER_ENTERED")
    else:
        rows = _read_local()
        rows.insert(0, booking)
        _write_local(rows)

    return booking

def get_bookings() -> List[Dict]:
    ws = _google_sheet()
    if ws is not None:
        records = ws.get_all_records()
        # newest first
        return list(reversed(records))
    return _read_local()

def update_booking_status(booking_id: str, status: str) -> None:
    if status not in ("Pending", "Confirmed", "Completed", "Cancelled"):
        raise ValueError("Invalid status.")

    ws = _google_sheet()
    if ws is not None:
        records = ws.get_all_records()
        for idx, record in enumerate(records, start=2):
            if str(record.get("booking_id", "")) == booking_id:
                ws.update_cell(idx, HEADERS.index("status") + 1, status)
                return
        raise ValueError("Booking not found.")

    rows = _read_local()
    found = False
    for row in rows:
        if row.get("booking_id") == booking_id:
            row["status"] = status
            found = True
            break
    if not found:
        raise ValueError("Booking not found.")
    _write_local(rows)



# Islamic/Hijri calendar helpers
def get_hijri_month_dates(year: int, month: int):
    """Return Gregorian dates for Hijri 17th, 19th and 21st.

    Uses hijridate's civil/tabular conversion. The displayed dates are
    approximate because local moon-sighting can differ by a day.
    """
    try:
        from hijridate import Hijri
        results = []
        for day in (17, 19, 21):
            try:
                g = Hijri(year, month, day).to_gregorian()
                results.append((day, g))
            except ValueError:
                continue
        return results
    except Exception:
        return []

def get_upcoming_hijama_dates(months: int = 12):
    """Return upcoming Hijri 17/19/21 dates starting around today."""
    from datetime import date
    try:
        from hijridate import Gregorian
        month_names = [
            "Muharram", "Safar", "Rabi al-Awwal", "Rabi al-Thani",
            "Jumada al-Awwal", "Jumada al-Thani", "Rajab", "Sha'ban",
            "Ramadan", "Shawwal", "Dhul-Qi'dah", "Dhul-Hijjah"
        ]
        today = date.today()
        h = Gregorian(today.year, today.month, today.day).to_hijri()
        rows = []
        y, m = h.year, h.month
        for _ in range(months):
            for day, g in get_hijri_month_dates(y, m):
                gd = date(g.year, g.month, g.day)
                if gd >= today:
                    rows.append({
                        "hijri_date": f"{day} {month_names[m-1]} {y} AH",
                        "gregorian_date": gd.isoformat(),
                        "day": day,
                    })
            m += 1
            if m == 13:
                m = 1
                y += 1
        return sorted(rows, key=lambda x: x["gregorian_date"])
    except Exception:
        return []


def get_ai_response(question: str) -> str:
    api_key = _secret("GEMINI_API_KEY", "")
    if not api_key:
        return (
            "### Gemini is not configured\n\n"
            "Add `GEMINI_API_KEY` to Streamlit Secrets to enable the AI assistant."
        )

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""
You are the educational information assistant for a Hijama appointment center.
Center: {CONFIG['address']}
Male practitioner: Muhammad Isreal
Female practitioner: Shamim Akhtar

Answer the user's question clearly and conservatively.
Do not diagnose disease, prescribe medicines, promise cures, or replace a doctor.
If the question describes severe or urgent symptoms, advise the person to seek
appropriate medical care.
When discussing Hijama, distinguish traditional/religious information from
medical evidence and avoid claiming that Hijama cures specific diseases.

User question:
{question}
"""
        response = client.models.generate_content(
            model=CONFIG["gemini_model"],
            contents=prompt,
        )
        return getattr(response, "text", None) or "No response was generated."
    except Exception as e:
        return (
            "### Gemini could not be reached\n\n"
            "The booking system is still available. Check your Gemini API key, "
            f"model setting, and quota.\n\nTechnical detail: `{e}`"
        )

@st.cache_data(ttl=3600)
def get_poster_copy() -> str:
    api_key = _secret("GEMINI_API_KEY", "")
    if not api_key:
        return "Traditional Hijama & wellness appointment service."

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=CONFIG["gemini_model"],
            contents=(
                "Write one short, respectful, non-medical marketing tagline "
                "for a Hijama appointment center poster. Do not promise cures. "
                "Return only the tagline, maximum 12 words."
            ),
        )
        text = getattr(response, "text", None)
        return text.strip() if text else "Book your Hijama appointment today."
    except Exception:
        return "Book your Hijama appointment today."
