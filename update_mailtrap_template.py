import json
import urllib.request

TOKEN = None
for line in open(".env", encoding="utf-8"):
    if line.startswith("MAILTRAP_API_TOKEN="):
        TOKEN = line.split("=", 1)[1].strip()

URL = "https://mailtrap.io/api/accounts/2849014/email_templates/78025"
HDR = {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"}

html = open("index.html", encoding="utf-8").read()
for a, b in {
    "./hero-banner.jpg": "https://iili.io/n03T7mg.jpg",
    "./cta-button.png": "https://iili.io/n12Rbyb.png",
    "./footer-bottom.png": "https://iili.io/n125JnV.png",
}.items():
    html = html.replace(a, b)

payload = {"email_template": {
    "name": "Fourteen Park - Amenities & Lifestyle Eblast (Final)",
    "subject": "Fourteen Park | Midtown Atlanta",
    "body_html": html,
}}
req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers=HDR, method="PATCH")
print("PATCH", urllib.request.urlopen(req).status)

got = json.loads(urllib.request.urlopen(urllib.request.Request(URL, headers=HDR)).read())
body = got.get("data", got)["body_html"]
i = body.find("n125JnV")
print("footer image wrapped in link:", 'href="https://FourteeenPark.com"' in body[i - 450:i])
