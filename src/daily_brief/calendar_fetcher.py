import os
from datetime import datetime, timedelta

import requests

from config import EARNINGS_WATCHLIST, US_TICKER_CN_NAMES

IMPORTANT_EVENTS = [
    "CPI", "PCE", "NFP", "Non-Farm", "GDP", "PMI", "FOMC",
    "Fed", "Interest Rate", "Unemployment", "Retail Sales",
    "PPI", "ISM", "Consumer Confidence", "Housing Starts",
]

EVENT_CN = {
    "Non-Farm":          "非農就業",
    "NFP":               "非農就業",
    "CPI":               "消費者物價指數 CPI",
    "PCE":               "個人消費支出 PCE",
    "PPI":               "生產者物價指數 PPI",
    "FOMC":              "Fed 利率決議",
    "Interest Rate":     "Fed 利率決議",
    "GDP":               "GDP 季增率",
    "ISM Manufacturing": "ISM 製造業 PMI",
    "ISM Services":      "ISM 服務業 PMI",
    "ISM":               "ISM PMI",
    "PMI":               "採購經理人指數 PMI",
    "Unemployment":      "失業率",
    "Retail Sales":      "零售銷售",
    "Consumer Confidence": "消費者信心指數",
    "Housing Starts":    "新屋開工",
    "Fed":               "Fed 官員談話",
}


def _translate_event(name: str) -> str:
    for keyword, cn in EVENT_CN.items():
        if keyword.lower() in name.lower():
            return cn
    return name


def fetch_economic_calendar() -> list[dict]:
    api_key = os.environ.get("FINNHUB_API_KEY", "")
    if not api_key:
        return []
    today = datetime.now()
    end = today + timedelta(days=7)
    try:
        resp = requests.get(
            "https://finnhub.io/api/v1/calendar/economic",
            params={
                "from": today.strftime("%Y-%m-%d"),
                "to": end.strftime("%Y-%m-%d"),
                "token": api_key,
            },
            timeout=10,
        )
        resp.raise_for_status()
        events = []
        for e in resp.json().get("economicCalendar", []):
            name = e.get("event", "")
            impact = e.get("impact", "")
            if (
                any(kw.lower() in name.lower() for kw in IMPORTANT_EVENTS)
                and impact in ("high", "medium")
            ):
                date_raw = e.get("time", "")
                events.append({
                    "date": date_raw[:10],
                    "name": _translate_event(name),
                    "name_en": name,
                    "country": e.get("country", ""),
                    "impact": impact,
                })
        events.sort(key=lambda x: x["date"])
        return events[:8]
    except Exception as ex:
        print(f"[Calendar] Economic fetch error: {ex}")
        return []


def fetch_earnings_calendar() -> list[dict]:
    api_key = os.environ.get("FINNHUB_API_KEY", "")
    if not api_key:
        return []
    today = datetime.now()
    end = today + timedelta(days=7)
    try:
        resp = requests.get(
            "https://finnhub.io/api/v1/calendar/earnings",
            params={
                "from": today.strftime("%Y-%m-%d"),
                "to": end.strftime("%Y-%m-%d"),
                "token": api_key,
            },
            timeout=10,
        )
        resp.raise_for_status()
        watchlist = set(EARNINGS_WATCHLIST)
        earnings = []
        for item in resp.json().get("earningsCalendar", []):
            symbol = item.get("symbol", "")
            if symbol in watchlist:
                hour = item.get("hour", "")
                timing = "盤前" if hour == "bmo" else "盤後" if hour == "amc" else ""
                earnings.append({
                    "date": item.get("date", ""),
                    "symbol": symbol,
                    "cn_name": US_TICKER_CN_NAMES.get(symbol, ""),
                    "timing": timing,
                })
        earnings.sort(key=lambda x: x["date"])
        return earnings
    except Exception as ex:
        print(f"[Calendar] Earnings fetch error: {ex}")
        return []


def fetch_weekly_calendar() -> dict:
    economic = fetch_economic_calendar()
    earnings = fetch_earnings_calendar()
    print(f"[Calendar] 總經事件 {len(economic)} 筆，財報 {len(earnings)} 筆")
    return {"economic_events": economic, "earnings": earnings}
