"""
Build preview_local.html from index.html (single source of truth).
Swaps the live asset base URL for the local ./ftp-upload/ folder so the email can be
previewed offline before anything is uploaded. Run after every edit to index.html:

    python build_preview.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LIVE_BASE = "https://assets.tangocrew.com/Kolter/14park/4498470078-001/"
LOCAL_BASE = "ftp-upload/"

with open(os.path.join(HERE, "index.html"), encoding="utf-8") as f:
    html = f.read()

count = html.count(LIVE_BASE)
html = html.replace(LIVE_BASE, LOCAL_BASE)
html = html.replace("<title>Fourteen Park | Midtown Atlanta</title>",
                    "<title>Fourteen Park | Midtown Atlanta (LOCAL PREVIEW - do not send)</title>")

with open(os.path.join(HERE, "preview_local.html"), "w", encoding="utf-8") as f:
    f.write(html)

print(f"preview_local.html written ({count} asset URLs mapped to {LOCAL_BASE})")
