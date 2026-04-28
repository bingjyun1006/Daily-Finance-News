from datetime import datetime

from jinja2 import Template

from config import MARKET_INDICES, US_TICKER_CN_NAMES

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>金融早報 {{ date }}</title>
  <style>
    :root {
      --bg:         #0d1117;
      --surface:    #161b22;
      --surface2:   #1c2128;
      --border:     #30363d;
      --border2:    #21262d;
      --text:       #e6edf3;
      --text-sub:   #adbac7;
      --text-dim:   #768390;
      --blue:       #58a6ff;
      --blue-link:  #658DC6;
      --blue-dim:   #1f4a8a;
      --green:      #56d364;
      --green-dim:  #1a4731;
      --red:        #ff7b72;
      --amber:      #e3b341;
      --purple:     #d2a8ff;
      --teal:       #39d353;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'PingFang TC', 'Microsoft JhengHei', 'Segoe UI', sans-serif;
      max-width: 780px; margin: 0 auto; padding: 16px;
      background: var(--bg); color: var(--text);
      font-size: 18px; line-height: 1.55;
    }

    /* ── HEADER ── */
    .header {
      background: linear-gradient(135deg, #161b22 0%, #0d1117 60%, #111827 100%);
      border: 1px solid var(--border);
      border-top: 2px solid var(--blue);
      padding: 22px 26px 18px;
      border-radius: 12px;
      margin-bottom: 14px;
      position: relative; overflow: hidden;
    }
    .header::before {
      content: ''; position: absolute; top: 0; right: 0;
      width: 200px; height: 200px;
      background: radial-gradient(circle at top right, rgba(88,166,255,0.06) 0%, transparent 70%);
      pointer-events: none;
    }
    .header-top { display: flex; justify-content: space-between; align-items: flex-start; }
    .header-brand h1 { font-size: 1.25em; font-weight: 700; letter-spacing: 0.04em; color: var(--text); }
    .header-brand .meta { color: var(--text-sub); font-size: 0.75em; margin-top: 3px; }
    .header-badge {
      background: var(--blue-dim); color: var(--blue);
      font-size: 0.68em; font-weight: 600;
      padding: 3px 10px; border-radius: 20px;
      letter-spacing: 0.06em; text-transform: uppercase;
      border: 1px solid rgba(88,166,255,0.3); white-space: nowrap;
    }
    .quote-block { margin-top: 16px; padding-top: 14px; border-top: 1px solid var(--border2); }
    .quote-en { font-size: 1.05em; font-weight: 500; color: var(--text); line-height: 1.45; font-style: italic; }
    .quote-zh { font-size: 0.78em; color: var(--text-sub); margin-top: 4px; }
    .quote-source { font-size: 0.72em; color: var(--text-dim); margin-top: 3px; }

    /* ── CARD ── */
    .card {
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 10px; padding: 16px 20px; margin-bottom: 12px;
    }
    .section-title {
      font-size: 0.9em; font-weight: 700; color: var(--text-sub);
      text-transform: uppercase; letter-spacing: 0.08em;
      margin-bottom: 12px; display: flex; align-items: center; gap: 7px;
    }
    .section-title::before {
      content: ''; display: inline-block; width: 3px; height: 12px;
      background: var(--blue); border-radius: 2px; flex-shrink: 0;
    }
    .section-title.green::before  { background: var(--green); }
    .section-title.amber::before  { background: var(--amber); }
    .section-title.purple::before { background: var(--purple); }
    .section-title.teal::before   { background: var(--teal); }

    /* ── INNER LAYOUT HELPERS ── */
    .inner-divider { border-top: 1px solid var(--border2); margin: 12px 0 10px; }
    .inner-header {
      font-size: 0.72em; font-weight: 700; color: var(--text-dim);
      text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;
    }

    /* ── NARRATIVE ── */
    .narrative-summary {
      font-size: 0.9em; font-weight: 600; color: var(--amber);
      margin-bottom: 10px; line-height: 1.5;
    }
    .narrative-row { display: flex; gap: 10px; align-items: baseline; padding: 4px 0; }
    .narrative-label {
      font-size: 0.72em; font-weight: 700; color: var(--text-dim);
      text-transform: uppercase; letter-spacing: 0.07em;
      min-width: 58px; flex-shrink: 0; padding-top: 2px;
    }
    .narrative-body { font-size: 0.86em; color: var(--text); line-height: 1.6; }

    /* ── HIGHLIGHTS ── */
    .highlight {
      padding: 6px 0; border-bottom: 1px solid var(--border2);
      font-size: 0.86em; line-height: 1.55; color: var(--text);
      display: flex; gap: 8px;
    }
    .highlight:last-child { border-bottom: none; }
    .highlight::before { content: "▸"; color: var(--blue); flex-shrink: 0; margin-top: 1px; }

    /* ── MARKET TABLE ── */
    .market-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .market-group-title {
      font-size: 0.82em; font-weight: 600; color: var(--text-sub);
      text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 8px;
    }
    table { width: 100%; border-collapse: collapse; }
    td, th { padding: 5px 6px; text-align: left; border-bottom: 1px solid var(--border2); font-size: 0.82em; }
    th { font-weight: 600; color: var(--text-dim); font-size: 0.7em; text-transform: uppercase; }
    tr:last-child td { border-bottom: none; }
    .up  { color: var(--green); font-weight: 600; }
    .dn  { color: var(--red);   font-weight: 600; }
    .na  { color: var(--text-dim); }
    td:first-child { color: var(--text); }

    /* ── MOVERS 3-COL ── */
    .movers-3col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }
    .movers-col-title {
      font-size: 0.76em; font-weight: 700; margin-bottom: 7px;
      padding-bottom: 5px; border-bottom: 1px solid var(--border);
    }
    .movers-sub {
      font-size: 0.7em; font-weight: 700;
      text-transform: uppercase; letter-spacing: 0.07em;
      color: var(--text-dim); margin: 8px 0 4px;
    }
    .mover-item { padding: 4px 0; border-bottom: 1px solid var(--border2); }
    .mover-item:last-child { border-bottom: none; }
    .mover-row { display: flex; align-items: baseline; gap: 4px; flex-wrap: wrap; }
    .mover-name { font-weight: 600; font-size: 0.78em; color: var(--text); }
    .mover-cn   { font-size: 0.72em; color: var(--text-dim); }
    .mover-pct  { font-weight: 700; font-size: 0.8em; margin-left: auto; }
    .mover-news { font-size: 0.72em; color: var(--text-sub); margin-top: 2px; }
    .mover-news a { color: var(--blue-link); text-decoration: underline; text-decoration-color: rgba(101,141,198,0.3); }
    .mover-news a:hover { text-decoration-color: var(--blue-link); }

    /* ── NEWS ── */
    .news-item { padding: 7px 0; border-bottom: 1px solid var(--border2); }
    .news-item:last-child { border-bottom: none; }
    .news-meta { font-size: 0.7em; color: var(--text-dim); margin-bottom: 2px; }
    .news-item a { color: var(--blue-link); text-decoration: underline; text-decoration-color: rgba(101,141,198,0.3); font-size: 0.84em; line-height: 1.45; }
    .news-item a:hover { text-decoration-color: var(--blue-link); opacity: 0.9; }
    .tag {
      display: inline-block; padding: 1px 7px; border-radius: 4px;
      font-size: 0.68em; font-weight: 600; margin-left: 6px; vertical-align: middle;
      border: 1px solid transparent;
    }
    .tag-tw { background: rgba(86,211,100,0.12);  color: var(--green);  border-color: rgba(86,211,100,0.25); }
    .tag-us { background: rgba(210,168,255,0.12); color: var(--purple); border-color: rgba(210,168,255,0.25); }

    /* ── INDUSTRY ── */
    .industry-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
    .industry-name { font-weight: 700; font-size: 0.88em; color: var(--text-sub); margin-bottom: 5px; }

    /* ── HOT STOCKS / RADAR ── */
    .hot-stock { padding: 9px 0; border-bottom: 1px solid var(--border2); }
    .hot-stock:last-child { border-bottom: none; }
    .hot-company { font-weight: 700; font-size: 0.88em; color: var(--amber); }
    .hot-reason  { color: var(--text-sub); font-size: 0.82em; margin: 3px 0 5px; }
    .hot-news a  { color: var(--blue-link); font-size: 0.82em; text-decoration: underline; text-decoration-color: rgba(101,141,198,0.3); }
    .hot-news a:hover { text-decoration-color: var(--blue-link); }
    .hot-news-row { display: flex; align-items: baseline; gap: 5px; margin-top: 2px; }
    .hot-news-arrow { color: var(--text-dim); font-size: 0.75em; flex-shrink: 0; }

    .radar-item { padding: 8px 0; border-bottom: 1px solid var(--border2); }
    .radar-item:last-child { border-bottom: none; }
    .radar-company { font-weight: 700; font-size: 0.88em; color: var(--blue); }
    .radar-reason { color: var(--text-sub); font-size: 0.82em; margin: 3px 0 2px; }
    .radar-basis  { font-size: 0.75em; color: var(--text-dim); }

    /* ── CALENDAR ── */
    .cal-item {
      display: flex; align-items: center; gap: 8px;
      padding: 5px 0; border-bottom: 1px solid var(--border2); font-size: 0.82em;
    }
    .cal-item:last-child { border-bottom: none; }
    .cal-date { color: var(--text-dim); min-width: 78px; font-size: 0.88em; flex-shrink: 0; }
    .cal-name { color: var(--text); flex: 1; }
    .cal-badge {
      font-size: 0.7em; font-weight: 700; padding: 1px 6px;
      border-radius: 3px; white-space: nowrap; flex-shrink: 0;
    }
    .cal-high   { background: rgba(255,123,114,0.15); color: var(--red); }
    .cal-medium { background: rgba(227,179,65,0.15);  color: var(--amber); }
    .cal-timing { font-size: 0.75em; color: var(--text-dim); flex-shrink: 0; }

    /* ── FOOTER ── */
    .footer {
      text-align: center; color: var(--text-dim);
      font-size: 0.7em; margin-top: 18px; padding-bottom: 10px;
    }
  </style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div class="header-top">
    <div class="header-brand">
      <h1>金融早報</h1>
      <div class="meta">{{ date }} &nbsp;·&nbsp; 台股開盤前速覽</div>
    </div>
    <div class="header-badge">Daily Brief</div>
  </div>
  {% set q = processed.get('daily_quote', {}) %}
  {% if q and q.en %}
  <div class="quote-block">
    <div class="quote-en">"{{ q.en }}"</div>
    <div class="quote-zh">{{ q.zh }}</div>
    <div class="quote-source">— {{ q.source }}</div>
  </div>
  {% endif %}
</div>

<!-- 今日市場解析 -->
{% set narrative = processed.get('market_narrative', {}) %}
{% if narrative %}
<div class="card" style="border-left: 3px solid var(--amber);">
  <div class="section-title amber">今日市場解析</div>
  {% if narrative is mapping %}
    {% if narrative.summary %}
    <div class="narrative-summary">{{ narrative.summary }}</div>
    {% endif %}
    {% if narrative.sections %}
    <div style="margin-bottom: 4px;">
      {% for section in narrative.sections %}
      <div class="narrative-row">
        <span class="narrative-label">{{ section.label }}</span>
        <span class="narrative-body">{{ section.text }}</span>
      </div>
      {% endfor %}
    </div>
    {% endif %}
  {% else %}
    <p class="narrative-body" style="white-space:pre-line;">{{ narrative }}</p>
  {% endif %}
  {% if processed.highlights %}
  <div class="inner-divider"></div>
  <div class="inner-header">重點速覽</div>
  {% for item in processed.highlights %}
  <div class="highlight">{{ item }}</div>
  {% endfor %}
  {% endif %}
</div>
{% endif %}

<!-- 市場速覽 -->
<div class="card">
  <div class="section-title">市場速覽</div>
  <div class="market-grid">
    {% for group_name, group_symbols in market_groups.items() %}
    <div>
      <div class="market-group-title">{{ group_name }}</div>
      <table>
        <tr><th>指標</th><th>數值</th><th>漲跌</th></tr>
        {% for name in group_symbols %}
        {% set data = market_data.get(name, {}) %}
        <tr>
          <td>{{ name }}</td>
          <td style="color:var(--text); font-variant-numeric: tabular-nums;">
            {% if data.price != 'N/A' %}{{ data.price }}{% else %}<span class="na">—</span>{% endif %}
          </td>
          <td>
            {% if data.price != 'N/A' %}
              <span class="{{ 'up' if data.change_pct >= 0 else 'dn' }}">
                {% if data.change_pct >= 0 %}+{% endif %}{{ data.change_pct }}%
              </span>
            {% else %}<span class="na">—</span>{% endif %}
          </td>
        </tr>
        {% endfor %}
      </table>
    </div>
    {% endfor %}
  </div>

  {% if tw_movers.gainers or tw_movers.losers or us_movers.gainers or us_movers.losers %}
  <div class="inner-divider"></div>
  <div class="inner-header">昨日強弱勢</div>
  <div class="movers-3col">

    <!-- 台股漲幅 -->
    <div>
      <div class="movers-col-title" style="color:var(--green)">🇹🇼 台股 ▲</div>
      {% for m in tw_movers.gainers %}
      {% set mn = tw_movers_news | selectattr("code", "equalto", m.code) | first | default(None) %}
      <div class="mover-item">
        <div class="mover-row">
          <span class="mover-name">{{ m.name }}</span>
          <span class="mover-cn">{{ m.code }}</span>
          <span class="mover-pct up">+{{ m.change_pct }}%</span>
        </div>
        {% if mn and mn.related_news %}
        <div class="mover-news">↳ <a href="{{ mn.related_news.link }}" target="_blank">{{ mn.related_news.title[:30] }}…</a></div>
        {% endif %}
      </div>
      {% endfor %}
    </div>

    <!-- 台股跌幅 -->
    <div>
      <div class="movers-col-title" style="color:var(--red)">🇹🇼 台股 ▼</div>
      {% for m in tw_movers.losers %}
      {% set mn = tw_movers_news | selectattr("code", "equalto", m.code) | first | default(None) %}
      <div class="mover-item">
        <div class="mover-row">
          <span class="mover-name">{{ m.name }}</span>
          <span class="mover-cn">{{ m.code }}</span>
          <span class="mover-pct dn">{{ m.change_pct }}%</span>
        </div>
        {% if mn and mn.related_news %}
        <div class="mover-news">↳ <a href="{{ mn.related_news.link }}" target="_blank">{{ mn.related_news.title[:30] }}…</a></div>
        {% endif %}
      </div>
      {% endfor %}
    </div>

    <!-- 美股 -->
    <div>
      <div class="movers-col-title" style="color:var(--purple)">🇺🇸 美股</div>
      {% if us_movers.gainers %}
      <div class="movers-sub up">▲ 漲幅</div>
      {% for m in us_movers.gainers %}
      {% set mn = us_movers_news | selectattr("code", "equalto", m.code) | first | default(None) %}
      {% set cn = ticker_cn.get(m.code, '') %}
      <div class="mover-item">
        <div class="mover-row">
          <span class="mover-name">{{ m.code }}</span>
          {% if cn %}<span class="mover-cn">{{ cn }}</span>{% endif %}
          <span class="mover-pct up">+{{ m.change_pct }}%</span>
        </div>
        {% if mn and mn.related_news %}
        <div class="mover-news">↳ <a href="{{ mn.related_news.link }}" target="_blank">{{ mn.related_news.title[:30] }}…</a></div>
        {% endif %}
      </div>
      {% endfor %}
      {% endif %}
      {% if us_movers.losers %}
      <div class="movers-sub dn" style="margin-top:8px;">▼ 跌幅</div>
      {% for m in us_movers.losers %}
      {% set mn = us_movers_news | selectattr("code", "equalto", m.code) | first | default(None) %}
      {% set cn = ticker_cn.get(m.code, '') %}
      <div class="mover-item">
        <div class="mover-row">
          <span class="mover-name">{{ m.code }}</span>
          {% if cn %}<span class="mover-cn">{{ cn }}</span>{% endif %}
          <span class="mover-pct dn">{{ m.change_pct }}%</span>
        </div>
        {% if mn and mn.related_news %}
        <div class="mover-news">↳ <a href="{{ mn.related_news.link }}" target="_blank">{{ mn.related_news.title[:30] }}…</a></div>
        {% endif %}
      </div>
      {% endfor %}
      {% endif %}
    </div>

  </div>
  {% endif %}
</div>

<!-- 台股新聞 -->
{% set active_industries = processed.industry.items() | selectattr('1') | list %}
{% if processed.tw_market or active_industries %}
<div class="card">
  <div class="section-title green">台股新聞</div>
  {% if processed.tw_market %}
  <div class="inner-header">精選新聞</div>
  {% for item in processed.tw_market %}
  <div class="news-item">
    {% if item.source or item.time %}
    <div class="news-meta">[{{ item.source }}{% if item.time %} · {{ item.time }}{% endif %}]</div>
    {% endif %}
    <a href="{{ item.link }}" target="_blank">{{ item.title }}</a>
    <span class="tag tag-tw">{{ item.tag }}</span>
  </div>
  {% endfor %}
  {% endif %}
  {% if active_industries %}
  {% if processed.tw_market %}<div class="inner-divider"></div>{% endif %}
  <div class="inner-header">各產業動態</div>
  <div class="industry-grid">
    {% for industry, items in active_industries %}
    <div>
      <div class="industry-name">{{ industry }}</div>
      {% for item in items %}
      <div class="news-item">
        {% if item.source or item.time %}
        <div class="news-meta">[{{ item.source }}{% if item.time %} · {{ item.time }}{% endif %}]</div>
        {% endif %}
        <a href="{{ item.link }}" target="_blank">{{ item.title }}</a>
      </div>
      {% endfor %}
    </div>
    {% endfor %}
  </div>
  {% endif %}
</div>
{% endif %}

<!-- 美股 & 總經 -->
{% if processed.us_macro %}
<div class="card">
  <div class="section-title purple">美股 &amp; 總經</div>
  {% for item in processed.us_macro %}
  <div class="news-item">
    {% if item.source or item.time %}
    <div class="news-meta">[{{ item.source }}{% if item.time %} · {{ item.time }}{% endif %}]</div>
    {% endif %}
    <a href="{{ item.link }}" target="_blank">{{ item.title }}</a>
    <span class="tag tag-us">{{ item.tag }}</span>
  </div>
  {% endfor %}
</div>
{% endif %}

<!-- 個股焦點 -->
{% if processed.hot_stocks or processed.market_radar %}
<div class="card">
  <div class="section-title amber">個股焦點</div>
  {% if processed.hot_stocks %}
  <div class="inner-header">熱門話題股</div>
  {% for stock in processed.hot_stocks %}
  <div class="hot-stock">
    <div class="hot-company">{{ stock.company }}</div>
    <div class="hot-reason">{{ stock.reason }}</div>
    {% if stock.related_news %}
    <div class="hot-news">
      {% for news in stock.related_news %}
      <div class="hot-news-row">
        <span class="hot-news-arrow">↳</span>
        <a href="{{ news.link }}" target="_blank">{{ news.title }}</a>
      </div>
      {% endfor %}
    </div>
    {% endif %}
  </div>
  {% endfor %}
  {% endif %}
  {% if processed.market_radar %}
  {% if processed.hot_stocks %}<div class="inner-divider"></div>{% endif %}
  <div class="inner-header">潛力關注股</div>
  {% for item in processed.market_radar %}
  <div class="radar-item">
    <div class="radar-company">{{ item.company }}</div>
    <div class="radar-reason">{{ item.reason }}</div>
    <div class="radar-basis">
      依據：{% if item.basis_link %}<a href="{{ item.basis_link }}" target="_blank" style="color:var(--blue-link);text-decoration:none;">{{ item.basis }}</a>{% else %}{{ item.basis }}{% endif %}
    </div>
  </div>
  {% endfor %}
  {% endif %}
</div>
{% endif %}

<!-- 本週關注 -->
{% if weekly_calendar.economic_events or weekly_calendar.earnings %}
<div class="card">
  <div class="section-title">本週關注</div>
  {% if weekly_calendar.economic_events %}
  <div class="inner-header">重要總經數據</div>
  {% for event in weekly_calendar.economic_events %}
  <div class="cal-item">
    <span class="cal-date">{{ event.date }}</span>
    <span class="cal-name">{{ event.name }}</span>
    <span class="cal-badge {{ 'cal-high' if event.impact == 'high' else 'cal-medium' }}">{{ event.impact }}</span>
  </div>
  {% endfor %}
  {% endif %}
  {% if weekly_calendar.earnings %}
  {% if weekly_calendar.economic_events %}<div class="inner-divider"></div>{% endif %}
  <div class="inner-header">美股財報</div>
  {% for e in weekly_calendar.earnings %}
  <div class="cal-item">
    <span class="cal-date">{{ e.date }}</span>
    <span class="cal-name">{{ e.symbol }}{% if e.cn_name %} · {{ e.cn_name }}{% endif %}</span>
    {% if e.timing %}<span class="cal-timing">{{ e.timing }}</span>{% endif %}
  </div>
  {% endfor %}
  {% endif %}
</div>
{% endif %}

<div class="footer">由 Claude Haiku 自動生成 &nbsp;·&nbsp; TWSE + yfinance + RSS + Finnhub &nbsp;·&nbsp; {{ date }}</div>
</body>
</html>"""


def build_report(market_data: dict, processed: dict,
                 tw_movers: dict, us_movers: dict,
                 weekly_calendar: dict | None = None,
                 date_str: str | None = None) -> str:
    if date_str is None:
        date_str = datetime.now().strftime("%Y年%m月%d日")
    if weekly_calendar is None:
        weekly_calendar = {"economic_events": [], "earnings": []}

    tw_movers_news = processed.get("tw_movers_news", [])
    us_movers_news = processed.get("us_movers_news", [])

    template = Template(HTML_TEMPLATE)
    return template.render(
        date=date_str,
        market_data=market_data,
        market_groups=MARKET_INDICES,
        processed=processed,
        tw_movers=tw_movers,
        us_movers=us_movers,
        tw_movers_news=tw_movers_news,
        us_movers_news=us_movers_news,
        ticker_cn=US_TICKER_CN_NAMES,
        weekly_calendar=weekly_calendar,
    )
