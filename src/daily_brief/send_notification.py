import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from config import SITE_HASH, SITE_BASE_URL
from mailer import send_email, send_failure_email

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "report"
    if mode == "failure":
        send_failure_email()
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
        url = f"{SITE_BASE_URL}/reports/{SITE_HASH}/{date_str}.html"
        send_email(url, date_str)
