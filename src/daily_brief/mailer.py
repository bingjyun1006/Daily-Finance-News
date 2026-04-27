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

    subject = f"Daily Financial News | {date_str}"

    body_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0; padding:0; background-color:#f0f2f7; font-family:'Helvetica Neue', Arial, sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0f2f7; padding:40px 0;">
    <tr>
      <td align="center">
        <table width="560" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 2px 12px rgba(0,0,0,0.08);">

          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg,#4a6fa5 0%,#658DC6 100%); padding:32px 40px;">
              <p style="margin:0; color:rgba(255,255,255,0.75); font-size:12px; letter-spacing:2px; text-transform:uppercase;">Market Intelligence</p>
              <h1 style="margin:6px 0 0; color:#ffffff; font-size:22px; font-weight:600; letter-spacing:0.5px;">Daily Financial News</h1>
              <p style="margin:6px 0 0; color:rgba(255,255,255,0.7); font-size:13px;">{date_str}</p>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:36px 40px;">
              <p style="margin:0 0 6px; color:#333333; font-size:16px; font-weight:500;">早安！新的一天加油～</p>
              <p style="margin:0 0 28px; color:#666666; font-size:14px; line-height:1.6;">請抽空閱讀新一份市場資訊 :)</p>

              <table cellpadding="0" cellspacing="0">
                <tr>
                  <td style="background:linear-gradient(135deg,#4a6fa5 0%,#658DC6 100%); border-radius:8px;">
                    <a href="{report_url}"
                       style="display:inline-block; padding:14px 32px; color:#ffffff; text-decoration:none;
                              font-size:15px; font-weight:600; letter-spacing:0.3px;">
                      查看今日報告 →
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#f8f9fb; border-top:1px solid #eaedf2; padding:16px 40px;">
              <p style="margin:0; color:#aab0bc; font-size:11px;">
                {report_url}
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
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


def send_failure_email() -> None:
    gmail_address = os.environ.get("GMAIL_ADDRESS")
    gmail_app_password = os.environ.get("GMAIL_APP_PASSWORD")
    recipient_env = os.environ.get("RECIPIENT_EMAIL", gmail_address)

    if not gmail_address or not gmail_app_password:
        print("[Mail] Missing credentials, cannot send failure notification")
        return

    recipients = [r.strip() for r in recipient_env.split(",") if r.strip()]

    body_html = """<!DOCTYPE html>
<html>
<body style="font-family:sans-serif;background:#f0f2f7;padding:32px;margin:0;">
  <table width="560" cellpadding="0" cellspacing="0"
         style="background:#fff;border-radius:12px;overflow:hidden;
                box-shadow:0 2px 12px rgba(0,0,0,0.08);margin:0 auto;">
    <tr>
      <td style="background:linear-gradient(135deg,#c0392b,#e74c3c);padding:28px 36px;">
        <h2 style="margin:0;color:#fff;font-size:18px;">⚠️ 金融早報產生失敗</h2>
      </td>
    </tr>
    <tr>
      <td style="padding:28px 36px;">
        <p style="margin:0;color:#555;font-size:14px;line-height:1.7;">
          今日的 GitHub Actions workflow 執行失敗，早報未能產生。<br>
          請至 GitHub Actions 頁面查看錯誤詳情。
        </p>
      </td>
    </tr>
  </table>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "⚠️ 金融早報產生失敗"
    msg["From"] = gmail_address
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(body_html, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_address, gmail_app_password)
        server.sendmail(gmail_address, recipients, msg.as_string())

    print(f"[Mail] Failure notification sent to {', '.join(recipients)}")
