# 🩸 Hijama Sunnah Center — Streamlit App

An app for a Hijama (cupping therapy) center: Sunnah-based Hijri calendar
with recommended treatment days, hadith about Hijama, general condition
information, a Gemini-powered assistant that matches patients with a male
or female practitioner, and a booking/contact page.

- **Center:** Hijama Sunnah Center
- **Address:** Chaknore Tablighi Markaz, Jalalabad, Afghanistan
- **Phone:** 0787960263

## Features

- 📅 Hijri calendar (pure Python, no external calendar package) highlighting
  the 17th, 19th and 21st of each lunar month — the days mentioned in
  hadith as best for Hijama
- 📖 Hadith about Hijama (summarized, with sources)
- 🩺 General condition/symptom reference (educational only, not a diagnosis)
- 🤖 Gemini-powered chat assistant that routes male patients to the male
  practitioner and female patients to the female practitioner
- 📍 Contact and Google Maps link, plus a simple booking form

## Add your logo

Drop your center's logo/photo into `assets/logo.png` and, if you want it
shown in the app, add this near the top of `app.py`:

```python
st.image("assets/logo.png", width=120)
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Gemini API key

Get a free key at <https://aistudio.google.com/app/apikey>.

The app looks for the key in Streamlit's **secrets** first. If none is
configured, it falls back to letting a visitor paste their own key for
just that session.

**Run locally with your own key:**

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# then edit .streamlit/secrets.toml and paste your real key in
streamlit run app.py
```

`.streamlit/secrets.toml` is already in `.gitignore`, so your real key
never gets committed or pushed to GitHub.

**Deploy on Streamlit Community Cloud with one shared key for everyone:**

1. Deploy the app first (see below).
2. In the Streamlit Cloud dashboard, open your app → **Settings → Secrets**.
3. Paste:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
4. Save — the app restarts automatically and the assistant page will show
   "✅ Assistant is ready" for every visitor, with no key prompt.

## Deploy to GitHub + Streamlit Community Cloud

1. **Create a GitHub repo** and push this folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Hijama Sunnah Center app"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to <https://share.streamlit.io>
   - Sign in with GitHub
   - Click **"New app"**
   - Select your repository, branch `main`, and main file `app.py`
   - Click **Deploy**

3. Your app will be live at a URL like:
   `https://<your-app-name>.streamlit.app`

4. (Optional) Add the `GEMINI_API_KEY` secret as described above so
   visitors don't need their own key.

## Project structure

```
hujama_app/
├── app.py              # Main Streamlit app
├── hijri.py            # Pure-Python Gregorian↔Hijri conversion
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml     # App theme
└── assets/
    └── (place your logo/photos here)
```

## Notes

- The Hijri calendar here is a **tabular (arithmetic) approximation**.
  It can differ by a day from local moonsighting announcements — use the
  "Moonsighting adjustment" slider in the sidebar to correct it for your
  region if needed.
- The address shown links to a Google Maps **search** for "Chaknore
  Tablighi Markaz, Jalalabad, Afghanistan" rather than a fixed pin, since
  no exact coordinates were provided. Swap in exact coordinates in
  `app.py` (`MAPS_URL`) if you have them.
- All medical/condition content is educational only and clearly marked
  as not a substitute for a qualified practitioner's assessment.
