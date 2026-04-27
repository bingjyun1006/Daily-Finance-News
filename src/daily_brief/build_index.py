import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import SITE_HASH, SITE_BASE_URL

REPO_ROOT = Path(__file__).parent.parent.parent
REPORTS_DIR = REPO_ROOT / "docs" / "reports" / SITE_HASH


def build_index() -> None:
    report_files = sorted(REPORTS_DIR.glob("*.html"), reverse=True)

    links = [(f.stem, f"{SITE_BASE_URL}/reports/{SITE_HASH}/{f.name}")
             for f in report_files]

    html = _render(links)
    output = REPO_ROOT / "docs" / "index.html"
    output.write_text(html, encoding="utf-8")
    print(f"[Index] Generated with {len(links)} report(s)")


def _render(links: list[tuple[str, str]]) -> str:
    if links:
        latest_date = links[0][0]
        latest_url = links[0][1]
        latest_html = f"""
    <a href="{latest_url}" class="latest-btn">查看最新報告 ({latest_date}) →</a>"""
    else:
        latest_html = "<p class='empty'>尚無報告</p>"

    rows = ""
    for date, url in links:
        rows += f"""
      <a href="{url}" class="row">
        <span class="row-date">{date}</span>
        <span class="row-arrow">→</span>
      </a>"""

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Daily Financial News</title>
  <style>
    :root {{
      --bg: #0d1117; --surface: #161b22; --border: #30363d;
      --text: #e6edf3; --text-sub: #adbac7; --text-dim: #768390;
      --blue: #658DC6; --amber: #e3b341;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'PingFang TC', 'Segoe UI', sans-serif;
      background: var(--bg); color: var(--text);
      min-height: 100vh; padding: 40px 16px;
    }}
    .container {{ max-width: 560px; margin: 0 auto; }}
    .header {{ margin-bottom: 32px; }}
    .header h1 {{ font-size: 1.4em; font-weight: 700; color: var(--text); }}
    .header p {{ font-size: 0.82em; color: var(--text-dim); margin-top: 6px; }}
    .latest-btn {{
      display: inline-block; margin: 20px 0 32px;
      background: var(--blue); color: #fff; text-decoration: none;
      padding: 11px 24px; border-radius: 8px;
      font-size: 0.9em; font-weight: 600;
    }}
    .archive-title {{
      font-size: 0.75em; font-weight: 700; color: var(--text-dim);
      text-transform: uppercase; letter-spacing: 0.08em;
      margin-bottom: 10px;
    }}
    .list {{
      border: 1px solid var(--border); border-radius: 10px; overflow: hidden;
    }}
    .row {{
      display: flex; align-items: center; justify-content: space-between;
      padding: 12px 18px; border-bottom: 1px solid var(--border);
      text-decoration: none; color: var(--text);
      transition: background 0.15s;
    }}
    .row:last-child {{ border-bottom: none; }}
    .row:hover {{ background: var(--surface); }}
    .row-date {{ font-size: 0.88em; font-variant-numeric: tabular-nums; }}
    .row-arrow {{ color: var(--text-dim); font-size: 0.8em; }}
    .empty {{ color: var(--text-dim); font-size: 0.88em; padding: 20px 0; }}
    .footer {{
      text-align: center; color: var(--text-dim);
      font-size: 0.7em; margin-top: 36px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Daily Financial News</h1>
      <p>每日自動生成 · 台股 &amp; 美股市場解析</p>
    </div>
    {latest_html}
    {"<div class='archive-title'>所有報告</div><div class='list'>" + rows + "</div>" if links else ""}
    <div class="footer">由 Claude Haiku 自動生成 · TWSE + yfinance + RSS</div>
  </div>
</body>
</html>"""


if __name__ == "__main__":
    build_index()
