# CBM Dashboard

A single Streamlit page for every sheet in `Index_sheet_CBM.xlsx`, plus the
small calculators that lived in its D/E columns — deployable for free on
Streamlit Community Cloud, locked down with Google sign-in.

```
cbm-dashboard/
├── app.py                          # the app
├── sheets_data.py                  # ← edit this to add/remove/re-tag sheets
├── tools.py                        # calculator logic
├── requirements.txt
├── .gitignore
├── .streamlit/
│   ├── config.toml                 # theme
│   └── secrets.toml.example        # template — copy, never commit the real one
└── README.md
```

## 1. Run it locally first

```bash
cd cbm-dashboard
python -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt
streamlit run app.py
```

Without any secrets configured, the app runs with a visible "no login"
warning in the sidebar so you can build/test freely. Auth only switches on
once `.streamlit/secrets.toml` has an `[auth]` block (step 3 below).

## 2. Push to GitHub

```bash
git init
git add .
git commit -m "CBM dashboard"
git branch -M main
git remote add origin https://github.com/<you>/cbm-dashboard.git
git push -u origin main
```

`secrets.toml` is git-ignored on purpose — only `secrets.toml.example` gets
committed. Real secrets are pasted into Streamlit Cloud directly (step 4).

## 3. Create a Google OAuth client

1. Go to the [Google Cloud Console](https://console.cloud.google.com/) →
   **APIs & Services → Credentials**.
2. **Create Credentials → OAuth client ID → Web application.**
3. Under **Authorized redirect URIs**, add:
   - `http://localhost:8501/oauth2callback` (for local testing)
   - `https://YOUR-APP-NAME.streamlit.app/oauth2callback` (your deployed
     app's URL — you'll get this in step 4; you can add it after)
4. Copy the **Client ID** and **Client secret** — you'll need them next.

If prompted, configure the OAuth consent screen as **Internal** (if your
Google account is on a Workspace domain) or **External** with your own
email added as a test user — either works fine for a single-user dashboard.

## 4. Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** →
   pick your GitHub repo, branch `main`, file `app.py`.
2. Deploy once (it'll run with the "no login" warning — that's expected).
3. Note the app's URL, then go back to Google Cloud Console and add
   `https://YOUR-APP-NAME.streamlit.app/oauth2callback` to the redirect URIs.
4. In Streamlit Cloud: your app → **Settings → Secrets**, paste in:

```toml
[auth]
redirect_uri = "https://YOUR-APP-NAME.streamlit.app/oauth2callback"
cookie_secret = "a-long-random-string"
client_id = "your-client-id.apps.googleusercontent.com"
client_secret = "your-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

[access]
allowed_emails = ["you@gmail.com"]
```

Save — the app reboots and the login screen appears. Only emails in
`allowed_emails` get past it.

## Editing the sheet list

Everything on the "Sheets" page comes from `sheets_data.py`. Each entry:

```python
{
    "name": "Display name",
    "description": "One-line note",
    "url": "https://docs.google.com/spreadsheets/d/.../edit",
    "access": "edit",       # or "view" — just controls the badge shown
    "category": "Clinical", # groups cards; add new categories freely
}
```

Add a dict, remove one, or flip `access` any time — no other code needs to
change. Commit and push, and Streamlit Cloud redeploys automatically.

## A note on the "Embed here" toggle

Each card can expand to load the sheet in an iframe right on the page. This
works because Google Sheets checks *your* logged-in Google session in the
browser, same as opening the tab directly — the dashboard itself never
touches your Sheets data or credentials. If your Google Workspace admin has
restricted iframe embedding, the embed will stay blank; **Open ↗** always
works as the fallback.
