# 🩸 Hijama Wellness Center — Appointment System

A mobile-friendly Streamlit Hijama appointment application with:
- Client appointment form
- Automatic practitioner selection by gender
- Persistent Google Sheets booking storage
- Admin appointment dashboard
- Booking status management
- Gemini educational information assistant
- Gemini-generated short poster tagline
- Optional Gradio frontend using the same backend

## Center details

- Male practitioner: Muhammad Isreal
- Female practitioner: Shamim Akhtar
- Contact: 0787960263
- Additional contact: 0784607516
- Address: Chaknore Tablighi Markaz, Jalalabad, Afghanistan

## 1. GitHub files

Upload these files to your GitHub repository:

- app.py
- backend.py
- gradio_app.py
- requirements.txt
- .gitignore
- README.md

Do NOT upload `.streamlit/secrets.toml`.

## 2. Configure Google Sheets persistence

The app first tries Google Sheets. If Google credentials are not configured, it falls back to a temporary local JSON file for development.

For Streamlit Community Cloud, use Google Sheets so appointment requests are persistent.

High-level steps:
1. Create a Google Cloud project.
2. Create a service account.
3. Enable Google Sheets API and Google Drive API.
4. Create a Google Sheet named `Hijama Appointment Requests`.
5. Share that Sheet with the service account's `client_email` as Editor.
6. Put the service-account fields in Streamlit Secrets under `[gcp_service_account]`.

## 3. Configure Gemini

Create a Gemini API key and add it to Streamlit Secrets:

GEMINI_API_KEY = "your-key"

The model is configurable:

GEMINI_MODEL = "gemini-2.5-flash"

If Google changes model availability for your account, change this value in Secrets without changing the application code.

## 4. Streamlit Secrets

In Streamlit Community Cloud:
Manage app → Settings → Secrets

Paste the contents of your local `secrets.toml` (with your real values).

Never commit the real secrets file to GitHub.

## 5. Deploy

Streamlit Community Cloud:
1. Push the repository to GitHub.
2. Create App.
3. Select the repository and branch.
4. Main file: `app.py`.
5. Add the Secrets.
6. Deploy.

## 6. Admin

Open the deployed app → `🔐 Admin Requests` → enter your ADMIN_PASSWORD.

Every submitted request gets a unique ID such as `HJ-AB12CD34`.

## 7. Optional Gradio app

Install dependencies and run:

python gradio_app.py

The Gradio interface uses the same `backend.py`.

For production, use the Streamlit application as the main public app and keep Gradio as an optional testing/secondary frontend.

## Medical safety

The Gemini assistant is deliberately configured for educational information. It should not diagnose conditions, prescribe medicines, or promise that Hijama cures a disease. Appointment booking does not replace professional medical evaluation.

## Important persistence note

Streamlit Community Cloud instances are not a suitable place to treat a local file as permanent appointment storage. Configure Google Sheets (or another hosted database) for real client bookings.
