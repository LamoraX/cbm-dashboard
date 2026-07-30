"""
CBM Dashboard — a single place to reach every Google Sheet in your index
plus the small calculators that used to live in its D/E columns.

Run locally:    streamlit run app.py
Deploy:         see README.md
"""

from datetime import date

import streamlit as st
import os

from sheets_data import CATEGORY_ORDER, SHEETS
from tools import duration_percentage, months_between, months_since, sitting_height

# --------------------------------------------------------------------------
# Page setup
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="CBM Dashboard",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .block-container {padding-top: 2.2rem; max-width: 1150px;}

        .cbm-title {font-size: 1.9rem; font-weight: 700; margin-bottom: 0.1rem;}
        .cbm-subtitle {color: var(--text-color-secondary, #9aa0a6); margin-bottom: 1.6rem;}

        .cbm-badge {
            display: inline-block; padding: 2px 10px; border-radius: 999px;
            font-size: 0.72rem; font-weight: 600; letter-spacing: 0.02em;
        }
        .cbm-badge-edit {background: rgba(108,92,231,0.18); color: #a29bfe;}
        .cbm-badge-view {background: rgba(255,193,7,0.16); color: #ffc107;}

        .cbm-card-title {font-size: 1.05rem; font-weight: 650; margin: 0.3rem 0 0.15rem 0;}
        .cbm-card-desc {font-size: 0.87rem; color: var(--text-color-secondary, #9aa0a6); min-height: 2.4em;}

        section[data-testid="stSidebar"] {border-right: 1px solid rgba(255,255,255,0.06);}
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------------------------------
# Auth gate — uses Streamlit's built-in st.login() (Authlib/OIDC under the
# hood). Falls back to open access if no [auth] block is configured, so the
# app still runs locally while you're building it.
# --------------------------------------------------------------------------
def require_auth() -> None:
    # Skip authentication when developing locally
    if os.getenv("LOCAL_DEV") == "1":
        st.sidebar.success("🛠️ Local development mode (authentication disabled)")
        return

    auth_configured = "auth" in st.secrets

    if not auth_configured:
        st.sidebar.warning(
            "No [auth] secrets found — running without login. "
            "Add secrets before hosting this publicly.",
            icon="⚠️",
        )
        return

    if not st.user.is_logged_in:
        st.markdown('<div class="cbm-title">🗂️ CBM Dashboard</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="cbm-subtitle">Sign in with the Google account this dashboard is registered to.</div>',
            unsafe_allow_html=True,
        )
        st.button("Log in with Google", on_click=st.login, type="primary")
        st.stop()

    allowed_emails = st.secrets.get("access", {}).get("allowed_emails", [])
    if allowed_emails and st.user.email not in allowed_emails:
        st.error(f"🚫 {st.user.email} isn't on the allow-list for this dashboard.")
        st.button("Log out", on_click=st.logout)
        st.stop()


require_auth()

# --------------------------------------------------------------------------
# Sidebar — identity + nav
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🗂️ CBM Dashboard")
    if "auth" in st.secrets and st.user.is_logged_in:
        st.caption(f"Signed in as **{st.user.name or st.user.email}**")
        st.button("Log out", on_click=st.logout, use_container_width=True)
        st.divider()

    page = st.radio(
        "Go to",
        ["📁 Sheets", "🧮 Tools"],
        label_visibility="collapsed",
    )

@st.dialog("📄 Sheet viewer", width="large")
def show_sheet_dialog(sheet: dict) -> None:
    """Big modal view of a sheet — opens full-size, closes via X / Esc / click-outside."""
    st.markdown(f"#### {sheet['name']}")
    st.caption(
        "If this stays blank, your workspace's sharing policy is blocking "
        "embeds — use Open in new tab instead."
    )
    st.link_button("Open in new tab ↗", sheet["url"])
    st.components.v1.iframe(sheet["url"], height=720, scrolling=True)


# --------------------------------------------------------------------------
# Page: Sheets
# --------------------------------------------------------------------------
if page == "📁 Sheets":
    st.markdown('<div class="cbm-title">Your Sheets</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="cbm-subtitle">Everything from your index, one click away. '
        "Click <b>View here</b> to open a sheet full-size, or <b>Open ↗</b> for a new tab.</div>",
        unsafe_allow_html=True,
    )

    grouped: dict[str, list[dict]] = {}
    for sheet in SHEETS:
        grouped.setdefault(sheet.get("category", "Other"), []).append(sheet)

    ordered_categories = [c for c in CATEGORY_ORDER if c in grouped] + [
        c for c in grouped if c not in CATEGORY_ORDER
    ]

    for category in ordered_categories:
        st.markdown(f"#### {category}")
        cards = grouped[category]
        cols = st.columns(3)

        for i, sheet in enumerate(cards):
            with cols[i % 3]:
                with st.container(border=True):
                    access = sheet.get("access", "edit")
                    badge_class = "cbm-badge-edit" if access == "edit" else "cbm-badge-view"
                    badge_label = "✏️ Edit access" if access == "edit" else "👁️ View only"

                    st.markdown(
                        f'<span class="cbm-badge {badge_class}">{badge_label}</span>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f'<div class="cbm-card-title">{sheet["name"]}</div>', unsafe_allow_html=True)
                    st.markdown(
                        f'<div class="cbm-card-desc">{sheet.get("description") or "&nbsp;"}</div>',
                        unsafe_allow_html=True,
                    )
                    b1, b2 = st.columns(2)
                    b1.link_button("Open ↗", sheet["url"], use_container_width=True)
                    if b2.button("🔍 View here", key=f"view_{sheet['name']}", use_container_width=True):
                        show_sheet_dialog(sheet)
        st.write("")

# --------------------------------------------------------------------------
# Page: Tools
# --------------------------------------------------------------------------
else:
    st.markdown('<div class="cbm-title">Tools</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="cbm-subtitle">The little calculators from columns D/E of the index sheet.</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["Sitting height", "Illness duration %", "Duration between dates"])

    with tab1:
        st.caption("sitting height = total height − stool height")
        c1, c2 = st.columns(2)
        total_h = c1.number_input("Total height (cm)", min_value=0.0, value=125.0, step=0.5)
        stool_h = c2.number_input("Stool height (cm)", min_value=0.0, value=47.5, step=0.5)
        st.metric("Sitting height (cm)", f"{sitting_height(total_h, stool_h):.1f}")

    with tab2:
        st.caption("percentage = (duration ÷ maximum duration) × 100")
        c1, c2 = st.columns(2)
        dur = c1.number_input("Duration with illness (months)", min_value=0.0, value=24.0, step=1.0)
        max_dur = c2.number_input("Maximum duration (months)", min_value=0.0, value=162.0, step=1.0)
        st.metric("Percentage", f"{duration_percentage(dur, max_dur):.1f}%")

        st.divider()
        st.caption("Or compute the duration automatically from an illness start date:")
        start = st.date_input("Illness start date", value=date(2021, 1, 5))
        auto_months = months_since(start)
        st.metric("Total duration so far (months)", auto_months)

    with tab3:
        st.caption("Complete months between any two dates — matches Excel's DATEDIF(x, y, \"M\")")
        c1, c2 = st.columns(2)
        date_x = c1.date_input("Date x", value=date.today(), key="date_x")
        date_y = c2.date_input("Date x+n", value=date.today(), key="date_y")
        st.metric("Total duration (months)", months_between(date_x, date_y))


from pathlib import Path
import streamlit as st

from reports.bpad_report_generator import generate_ppt, find_template, DEFAULT_TEMPLATE_DIR, DEFAULT_CREDS

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"

st.subheader("CBM Reports")

if st.button("Generate BPAD PPT"):
    try:
        template = find_template(DEFAULT_TEMPLATE_DIR)
        output_path = OUTPUT_DIR / "bpad_report_filled.pptx"
        saved = generate_ppt(
            template_path=template,
            output_path=output_path,
            creds_path=DEFAULT_CREDS,
        )
        with open(saved, "rb") as f:
            st.download_button(
                label="Download generated PPT",
                data=f,
                file_name=saved.name,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
        st.success("Report generated successfully.")
    except Exception as e:
        st.error(f"Failed to generate report: {e}")