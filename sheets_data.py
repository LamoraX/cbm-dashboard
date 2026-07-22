"""
Registry of your Google Sheets, pulled from Index_sheet_CBM.xlsx.

This is the ONLY file you need to touch to add, remove, or re-describe a
sheet. Each entry is a plain dict:

    {
        "name": "Display name",
        "description": "One-line note (from column B of your index)",
        "url": "https://docs.google.com/spreadsheets/d/.../edit",
        "access": "edit" | "view",   # sets the badge colour + icon
        "category": "Clinical" | "Admin" | "Tools",  # groups cards on the page
    }

`access` couldn't be read from the spreadsheet (Google Sheets doesn't store
your permission level in the file itself), so everything below defaults to
"edit" — flip the ones that are actually view-only for you to "view".
"""

SHEETS = [
    {
        "name": "New MRI Scheduler 2025",
        "description": "MRI scheduling",
        "url": "https://docs.google.com/spreadsheets/d/1tP7mp3awLFEIf8FdPVS_CC41r2ircZRSHPQI2xBPXY0/edit?gid=821713699#gid=821713699",
        "access": "edit",
        "category": "Clinical",
    },
    {
        "name": "CBM-MONTHLY-AUDIT",
        "description": "What investigations are done — update on the same day",
        "url": "https://docs.google.com/spreadsheets/d/1cVRT47xWPxIB7WzruwSTKiGSpBLALpSOkcBMiHQNWqA/edit?gid=1980041451#gid=1980041451",
        "access": "edit",
        "category": "Clinical",
    },
    {
        "name": "ADBS Monthly Forms and Stationary Requirements",
        "description": "Request stationary",
        "url": "https://docs.google.com/spreadsheets/d/19qWhCUmBWFne18ua6CyGAL2NMkmIRI2uFkFw5rcSKmI/edit?gid=1572856938#gid=1572856938",
        "access": "edit",
        "category": "Admin",
    },
    {
        "name": "BPAD Cohort",
        "description": "",
        "url": "https://docs.google.com/spreadsheets/d/1hlBd1_FYmBG1jb4mEycgHd0DrFTjAdMKzzJ70rBtSK8/edit?gid=477551608#gid=477551608",
        "access": "edit",
        "category": "Clinical",
    },
    {
        "name": "SCZ and BPAD Status",
        "description": "For making PPTs",
        "url": "https://docs.google.com/spreadsheets/d/1tE4uXTSaO6rHk_W3GXU55FEwUfMw_CLdnMTXQJCWYx8/edit?gid=1218074150#gid=1218074150",
        "access": "edit",
        "category": "Clinical",
    },
    {
        "name": "Clinical-Lab Linking Sheet",
        "description": "Get Family / D-number",
        "url": "https://docs.google.com/spreadsheets/d/1aSxKutdxbB1TPjlp7dldkYU3eci0hIpoW5QnVzLNvBg/edit?gid=861885384#gid=861885384",
        "access": "edit",
        "category": "Clinical",
    },
    {
        "name": "Verified Numbers",
        "description": "",
        "url": "https://docs.google.com/spreadsheets/d/1dqNHa13Lns1e9nlnoWxs8kqa_5UrFhVwvWtejAHaUGE/edit?gid=397338218",
        "access": "view",
        "category": "Admin",
    },
]

# Order categories appear in on the page
CATEGORY_ORDER = ["Clinical", "Admin", "Other"]
