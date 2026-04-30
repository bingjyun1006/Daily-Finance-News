import json
import os

import anthropic

from config import INDUSTRY_KEYWORDS

SYSTEM_PROMPT = """你是一位資深金融分析師，專注台灣與美國資本市場。你的讀者是 AI 顧問，每天需要快速掌握市場動態。

任務：根據提供的市場數據、強弱勢個股與新聞列表，產出結構化日報摘要。

過濾原則：
- 保留：有具體數字、政策訊號、產業動態、重要事件、外資法人動作的新聞
- 剔除：廣告稿、情緒化標題、無數據支撐的預測文章

必須以合法 JSON 格式回應（不要加 markdown code block），結構如下：
{
  "daily_quote": {"en": "英文激勵名言原文", "zh": "中文翻譯", "source": "來源（人名或書名）"},

  "highlights": ["今日最重要的市場訊號，一句話描述，共3-5條"],
  "market_narrative": {
    "summary": "今日市場最核心主題（一句話，25字以內）",
    "sections": [
      {"label": "台股", "text": "台股今日主要動態或驅動力（一句話）"},
      {"label": "美股", "text": "美股今日重要動態（一句話）"},
      {"label": "總經", "text": "重要總經訊號或政策變化（一句話）"},
      {"label": "今日關注", "text": "最值得追蹤的 1-2 個議題、產業或個股及原因（一句話）"}
    ]
  },
  "tw_market": [{"title": "標題", "link": "連結", "tag": "分類", "source": "來源", "time": "HH:MM"}],
  "us_macro": [{"title": "標題", "link": "連結", "tag": "分類", "source": "來源", "time": "HH:MM"}],
  "hot_stocks": [
    {
      "company": "公司名稱（含股票代號）",
      "reason": "一句話說明今日為何被討論",
      "related_news": [{"title": "新聞標題", "link": "連結"}]
    }
  ],
  "industry": {
    "半導體製造": [{"title": "標題", "link": "連結", "source": "來源", "time": "HH:MM"}],
    "IC設計": [],
    "封測封裝": [],
    "PCB/基板": [],
    "記憶體": [],
    "被動元件": [],
    "面板": [],
    "AI伺服器/ODM": [],
    "電源/散熱": [],
    "重電/電力": [],
    "網通": [],
    "生技醫療": [],
    "金融/壽險": [],
    "航運": [],
    "外資動態": []
  },
  "us_industry": {
    "半導體(美)": [{"title": "標題", "link": "連結", "source": "來源", "time": "HH:MM"}],
    "半導體設備(美)": [],
    "記憶體(美)": [],
    "科技巨頭": [],
    "軟體/AI(美)": [],
    "金融(美)": [],
    "生技(美)": []
  },
  "tw_movers_news": [
    {"code": "股票代號", "name": "公司名稱", "related_news": {"title": "同日相關新聞標題（若有）", "link": "連結"}}
  ],
  "us_movers_news": [
    {"code": "TICKER", "name": "公司名稱", "related_news": {"title": "同日相關新聞標題（若有）", "link": "連結"}}
  ],
  "market_radar": [
    {
      "company": "公司名稱",
      "reason": "一句話說明為何值得關注",
      "basis": "出現在哪則新聞或數據中（簡短描述）",
      "basis_link": "若依據來自特定新聞文章則填入連結，否則填 null"
    }
  ]
}

規則：
- daily_quote：根據今日星期幾輪替來源；週一=投資人（Buffett/Munger/Dalio/Lynch）；週二=科技創業家（Jobs/Bezos/Musk/Gates）；週三=哲學歷史（Seneca/Churchill/孔子/Marcus Aurelius）；週四=商業管理（Drucker/Grove/Welch）；週五=行為心理（Kahneman/Taleb/Thaler）；避免廣泛流傳的老梗名言；英文原文 + 中文翻譯
- highlights：3-5 條，每條一句話
- tw_market：限 5 則；判斷標準：新聞主詞必須是台股整體市場、加權指數、央行、外資整體買賣超或台幣匯率；**絕對不放個股或特定產業新聞**；寧缺毋濫
- us_macro：限 5 則；涵蓋 Fed 決議、Powell 發言、利率、油價、美元指數、CPI、非農、S&P 500/NASDAQ 整體走勢等宏觀訊號；不放個股或產業新聞
- industry：台灣上市／上櫃公司為主；每產業最多 4 則；**同一篇新聞的 link 只能出現在一個台股產業欄**；無相關新聞給空陣列 []
- us_industry：美國及國際公司（NVDA/AMD/ASML/Samsung/Micron 等）依產業歸類；每產業最多 3 則；**同一篇新聞的 link 只能出現在一個美股產業欄**；無相關新聞給空陣列 []
- hot_stocks：台美公司皆可，今日有具體新聞被討論的公司，3-8 家
- tw_movers_news / us_movers_news：為每支強弱勢個股配對同日相關新聞；若無相關新聞，related_news 給 null
- market_radar：從新聞中發現值得特別關注的公司或訊號（包含尚未在 hot_stocks 的），5-10 則；依據若來自新聞文章則附 basis_link；無訊號則給 []
- market_narrative：summary 一句話總結今日最核心市場主題；sections 固定四個 label（台股、美股、總經、今日關注），每個 text 一句話精要描述，label 不可更改
- 所有 time 欄位若原始資料為空字串，JSON 中也保持空字串"""


def process_with_claude(market_data: dict, articles: list[dict],
                         tw_movers: dict, us_movers: dict) -> dict:
    from datetime import datetime as _dt
    _now = _dt.now()
    _weekday_zh = {"Monday": "週一", "Tuesday": "週二", "Wednesday": "週三",
                   "Thursday": "週四", "Friday": "週五",
                   "Saturday": "週六", "Sunday": "週日"}.get(_now.strftime("%A"), "週一")
    date_prefix = f"今日日期：{_now.strftime('%Y-%m-%d')}（{_weekday_zh}）\n\n"

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Market indices/macro
    market_lines = ["【市場概覽數據】"]
    for name, data in market_data.items():
        if data["price"] != "N/A":
            sign = "+" if data["change_pct"] >= 0 else ""
            market_lines.append(f"• {name}: {data['price']} ({sign}{data['change_pct']}%)")
        else:
            market_lines.append(f"• {name}: 數據暫無")

    # Taiwan movers
    movers_lines = ["\n【昨日台股強弱勢（供配對相關新聞用）】"]
    for m in tw_movers.get("gainers", []):
        movers_lines.append(f"漲 {m['name']}({m['code']}) {m['change_pct']:+.2f}%")
    for m in tw_movers.get("losers", []):
        movers_lines.append(f"跌 {m['name']}({m['code']}) {m['change_pct']:+.2f}%")

    # US movers
    movers_lines.append("\n【昨日美股強弱勢（供配對相關新聞用）】")
    for m in us_movers.get("gainers", []):
        movers_lines.append(f"漲 {m['name']} {m['change_pct']:+.2f}%")
    for m in us_movers.get("losers", []):
        movers_lines.append(f"跌 {m['name']} {m['change_pct']:+.2f}%")

    # News
    articles_lines = ["\n【新聞列表（來源 / 時間 / 標題 / 連結）】"]
    for i, article in enumerate(articles, 1):
        time_str = f" · {article['time']}" if article.get("time") else ""
        articles_lines.append(f"{i}. [{article['source']}{time_str}] {article['title']}")
        articles_lines.append(f"   連結：{article['link']}")

    user_content = (
        date_prefix
        + "\n".join(market_lines)
        + "\n".join(movers_lines)
        + "\n".join(articles_lines)
        + "\n\n請根據以上資料產出日報摘要 JSON。"
    )

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=8096,
        system=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": user_content}],
    )

    cache_read = getattr(response.usage, "cache_read_input_tokens", 0)
    cache_write = getattr(response.usage, "cache_creation_input_tokens", 0)
    print(f"[Claude] input={response.usage.input_tokens} cache_read={cache_read} cache_write={cache_write} output={response.usage.output_tokens}")

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    try:
        result = json.loads(raw)
        _normalize_movers_news(result, "tw_movers_news")
        _normalize_movers_news(result, "us_movers_news")
        _deduplicate_result(result)
        return result
    except json.JSONDecodeError:
        print("[WARN] Claude returned invalid JSON, using fallback structure")
        return _fallback_structure(articles)


def _deduplicate_result(result: dict) -> dict:
    tw_seen: set[str] = set()
    us_seen: set[str] = set()

    def _clean(items: list, seen: set, link_key: str = "link") -> list:
        out = []
        for item in (items or []):
            link = item.get(link_key)
            if not link or link not in seen:
                if link:
                    seen.add(link)
                out.append(item)
        return out

    # Taiwan side: tw_market → tw industry (shared seen set)
    result["tw_market"] = _clean(result.get("tw_market", []), tw_seen)
    for key in result.get("industry", {}):
        result["industry"][key] = _clean(result["industry"][key], tw_seen)

    # US side: us_macro → us industry (independent seen set)
    result["us_macro"] = _clean(result.get("us_macro", []), us_seen)
    for key in result.get("us_industry", {}):
        result["us_industry"][key] = _clean(result["us_industry"][key], us_seen)

    # hot_stocks: dedup only within itself, allow overlap with industry sections
    hs_seen: set[str] = set()
    for stock in result.get("hot_stocks", []):
        rn = stock.get("related_news") or []
        if isinstance(rn, list):
            stock["related_news"] = _clean(rn, hs_seen)
        elif isinstance(rn, dict):
            link = rn.get("link")
            if link and link in hs_seen:
                stock["related_news"] = None
            elif link:
                hs_seen.add(link)

    result["market_radar"] = _clean(
        result.get("market_radar", []), tw_seen | us_seen, link_key="basis_link"
    )

    return result


def _normalize_movers_news(result: dict, key: str) -> None:
    """Ensure related_news is always a dict or None (Claude sometimes returns a list)."""
    for item in result.get(key, []):
        rn = item.get("related_news")
        if isinstance(rn, list):
            item["related_news"] = rn[0] if rn else None


def _fallback_structure(articles: list[dict]) -> dict:
    tw = [{"title": a["title"], "link": a["link"], "tag": a["category"],
           "source": a["source"], "time": a.get("time", "")}
          for a in articles if a["category"] == "台股"][:5]
    us = [{"title": a["title"], "link": a["link"], "tag": a["category"],
           "source": a["source"], "time": a.get("time", "")}
          for a in articles if a["category"] in ("美股", "總經", "國際")][:5]
    empty_industry = {k: [] for k in INDUSTRY_KEYWORDS}
    return {
        "daily_quote": {"en": "Keep going.", "zh": "繼續前行。", "source": "—"},
        "highlights": ["AI 處理異常，以下為原始新聞清單，請自行篩選"],
        "market_narrative": {"summary": "", "sections": []},
        "tw_market": tw,
        "us_macro": us,
        "hot_stocks": [],
        "industry": empty_industry,
        "us_industry": {k: [] for k in ["半導體(美)", "半導體設備(美)", "記憶體(美)", "科技巨頭", "軟體/AI(美)", "金融(美)", "生技(美)"]},
        "tw_movers_news": [],
        "us_movers_news": [],
        "market_radar": [],
    }
