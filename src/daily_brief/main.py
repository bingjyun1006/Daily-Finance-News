import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from calendar_fetcher import fetch_weekly_calendar
from collector import fetch_market_data, fetch_rss_feeds, fetch_tw_movers, fetch_us_movers
from config import SITE_HASH, SITE_BASE_URL
from mailer import send_email
from processor import process_with_claude
from report import build_report

REPO_ROOT = Path(__file__).parent.parent.parent


def main() -> None:
    no_email = "--no-email" in sys.argv

    print("=== 金融早報機器人 ===")

    print("[1/6] 抓取市場指數與總經數據...")
    market_data = fetch_market_data()
    ok = sum(1 for v in market_data.values() if v["price"] != "N/A")
    print(f"      取得 {ok}/{len(market_data)} 個指標")

    print("[2/6] 抓取強弱勢個股...")
    tw_movers = fetch_tw_movers()
    us_movers = fetch_us_movers()
    print(f"      台股：漲{len(tw_movers['gainers'])}／跌{len(tw_movers['losers'])}  "
          f"美股：漲{len(us_movers['gainers'])}／跌{len(us_movers['losers'])}")

    print("[3/6] 抓取本週行事曆...")
    weekly_calendar = fetch_weekly_calendar()

    print("[4/6] 抓取 RSS 新聞...")
    articles = fetch_rss_feeds(max_items_per_source=10)
    sources = len(set(a["source"] for a in articles))
    print(f"      取得 {len(articles)} 則新聞，來自 {sources} 個來源")

    print("[5/6] Claude Haiku 過濾與分析...")
    processed = process_with_claude(market_data, articles, tw_movers, us_movers)

    print("[6/6] 生成 HTML 報告並存檔...")
    html = build_report(market_data, processed, tw_movers, us_movers, weekly_calendar)

    date_str = datetime.now().strftime("%Y-%m-%d")
    report_dir = REPO_ROOT / "docs" / "reports" / SITE_HASH
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{date_str}.html"
    report_path.write_text(html, encoding="utf-8")
    print(f"      已儲存：docs/reports/{SITE_HASH}/{date_str}.html")

    report_url = f"{SITE_BASE_URL}/reports/{SITE_HASH}/{date_str}.html"
    print(f"      報告網址：{report_url}")

    if not no_email:
        send_email(report_url, date_str)

    print("=== 完成 ===")


if __name__ == "__main__":
    main()
