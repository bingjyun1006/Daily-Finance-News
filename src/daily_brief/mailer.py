import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(report_url: str, date_str: str) -> None:
    gmail_address = os.environ.get("GMAIL_ADDRESS")
    gmail_app_password = os.environ.get("GMAIL_APP_PASSWORD")
    recipient_env = os.environ.get("RECIPIENT_EMAIL", gmail_address)

    if not gmail_address or not gmail_app_password:
        raise ValueError("Missing Gmail credentials. Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD.")

    recipients = [r.strip() for r in recipient_env.split(",") if r.strip()]

    subject = f"[金融早報] {date_str}"

    body_html = f"""<!DOCTYPE html>
<html>
<body style="font-family: sans-serif; background: #1a1a2e; color: #e0e0e0; padding: 32px; margin: 0;">
  <h2 style="color: #658DC6; margin-bottom: 8px;">📊 今日金融早報已出爐</h2>
  <p style="color: #aaa; margin-bottom: 24px;">{date_str}</p>
  <a href="{report_url}"
     style="display: inline-block; background: #658DC6; color: white;
            padding: 12px 28px; border-radius: 6px; text-decoration: none;
            font-size: 16px; font-weight: bold;">
    查看今日報告 →
  </a>
  <p style="color: #555; font-size: 12px; margin-top: 28px;">{report_url}</p>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmail_address
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(body_html, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_address, gmail_app_password)
        server.sendmail(gmail_address, recipients, msg.as_string())

    print(f"[Mail] Sent to {', '.join(recipients)}")
