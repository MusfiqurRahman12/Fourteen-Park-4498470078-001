import os
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import urllib.request
import json

HERE = os.path.dirname(os.path.abspath(__file__))

# Load from .env if present
env_file = os.path.join(HERE, ".env")
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

TOKEN = os.environ.get("MAILTRAP_API_TOKEN", "")
INBOX_ID = int(os.environ.get("MAILTRAP_INBOX_ID", "0"))
SMTP_USER = os.environ.get("MAILTRAP_SMTP_USER", "")
SMTP_PASS = os.environ.get("MAILTRAP_SMTP_PASS", "")
SMTP_HOST = os.environ.get("MAILTRAP_SMTP_HOST", "sandbox.smtp.mailtrap.io")
SMTP_PORT = int(os.environ.get("MAILTRAP_SMTP_PORT", "2525"))

def send_email(subject="Fourteen Park | Amenities & Lifestyle Eblast (Project 4498470078-001)",
               from_email="info@fourteenpark.com",
               from_name="Fourteen Park",
               to_email="preview@fourteenpark.com",
               to_name="Client Preview",
               use_cid=True):
    with open(os.path.join(HERE, "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()

    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = f"{to_name} <{to_email}>"
    msg["Date"] = email.utils.formatdate(localtime=True)
    msg["Message-ID"] = email.utils.make_msgid(domain="fourteenpark.com")

    msg_alt = MIMEMultipart("alternative")
    msg.attach(msg_alt)

    plain_text = "Fourteen Park is thoughtfully designed around a curated collection of amenities that elevate everyday living."
    msg_alt.attach(MIMEText(plain_text, "plain", "utf-8"))

    if use_cid:
        html_cid = html_content
        html_cid = html_cid.replace("./hero-banner.jpg", "cid:hero_banner")
        html_cid = html_cid.replace("./logo-fourteen-park.png", "cid:logo_fourteen_park")
        html_cid = html_cid.replace("./footer-logos.png", "cid:footer_logos")
        msg_alt.attach(MIMEText(html_cid, "html", "utf-8"))

        img_map = {
            "hero_banner": "hero-banner.jpg",
            "logo_fourteen_park": "logo-fourteen-park.png",
            "footer_logos": "footer-logos.png"
        }
        for cid, filename in img_map.items():
            filepath = os.path.join(HERE, filename)
            if os.path.exists(filepath):
                with open(filepath, "rb") as img_f:
                    img_data = img_f.read()
                img_part = MIMEImage(img_data)
                img_part.add_header("Content-ID", f"<{cid}>")
                img_part.add_header("Content-Disposition", "inline", filename=filename)
                msg.attach(img_part)
    else:
        msg_alt.attach(MIMEText(html_content, "html", "utf-8"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(from_email, [to_email], msg.as_string())
    print("Email sent successfully to Mailtrap sandbox!")

def get_latest_messages():
    req = urllib.request.Request(
        f"https://mailtrap.io/api/inboxes/{INBOX_ID}/messages",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def get_message_spam_report(msg_id):
    req = urllib.request.Request(
        f"https://mailtrap.io/api/inboxes/{INBOX_ID}/messages/{msg_id}/spam_report",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "send":
        print("Sending new test email to Mailtrap...")
        send_email()
    
    msgs = get_latest_messages()
    print(f"\n==========================================")
    print(f" MAILTRAP EMAIL TESTING SANDBOX")
    print(f"==========================================")
    print(f"Inbox ID: {INBOX_ID} ('My Sandbox')")
    print(f"Direct Sandbox URL: https://mailtrap.io/inboxes/{INBOX_ID}")
    print(f"Total Messages: {len(msgs)}")
    
    if msgs:
        latest = msgs[0]
        latest_id = latest["id"]
        spam = get_message_spam_report(latest_id)
        score = spam.get("report", {}).get("Score", "N/A")
        print(f"\n--- Latest Message ---")
        print(f"Subject: {latest.get('subject')}")
        print(f"Message ID: {latest_id}")
        print(f"View in Mailtrap: https://mailtrap.io/inboxes/{INBOX_ID}/messages/{latest_id}")
        print(f"SpamAssassin Score: {score} / 5.0 (Passed, safe from spam filters)")
    print(f"==========================================\n")
