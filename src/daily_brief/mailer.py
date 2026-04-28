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

    subject = "早安!野原一家加油!抽空來看今天的市場資訊~"

    body_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0; padding:0; background-color:#f2f2f0; font-family:'Helvetica Neue', Arial, sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f2f2f0; padding:40px 0;">
    <tr>
      <td align="center">
        <table width="560" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 2px 16px rgba(0,0,0,0.07);">

          <!-- Top accent bar -->
          <tr>
            <td style="background:linear-gradient(90deg,#b5b5a0 0%,#8c9e8c 100%); height:5px; font-size:0; line-height:0;">&nbsp;</td>
          </tr>

          <!-- Header -->
          <tr>
            <td style="padding:28px 40px 20px; border-bottom:1px solid #ebebeb;">
              <p style="margin:0; color:#999; font-size:11px; letter-spacing:2px; text-transform:uppercase;">Daily Financial News</p>
              <p style="margin:6px 0 0; color:#bbb; font-size:12px;">{date_str}</p>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:32px 40px 36px;">
              <p style="margin:0 0 6px; color:#2c2c2c; font-size:16px; font-weight:500;">野原先生請查收今天的早報如下~~</p>
              <p style="margin:0 0 28px; color:#888; font-size:13px; line-height:1.6;">&nbsp;</p>

              <table cellpadding="0" cellspacing="0">
                <tr>
                  <td style="background:#4a5568; border-radius:8px;">
                    <a href="{report_url}"
                       style="display:inline-block; padding:13px 30px; color:#ffffff; text-decoration:none;
                              font-size:14px; font-weight:600; letter-spacing:0.3px;">
                      查看今日報告 →
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#fafaf8; border-top:1px solid #ebebeb; padding:14px 40px;">
              <p style="margin:0; color:#c0c0b8; font-size:11px;">
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
