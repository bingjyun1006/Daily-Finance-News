import time
from datetime import datetime, timezone

import feedparser
import urllib3
import requests
import yfinance as yf

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from config import MARKET_INDICES, RSS_SOURCES, TW_MOVERS_TOP_N, US_MOVERS_TICKERS, US_MOVERS_TOP_N


def _parse_published_time(entry) -> str:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        local_offset = datetime.now().astimezone().utcoffset()
        dt_local = dt + local_offset
        return dt_local.strftime("%H:%M")
    return ""


def fetch_rss_feeds(max_items_per_source: int = 10) -> list[dict]:
    all_articles = []
    for source in RSS_SOURCES:
        try:
            feed = feedparser.parse(source["url"])
            for entry in feed.entries[:max_items_per_source]:
                title = entry.get("title", "").strip()
                link = entry.get("link", "")
                if not title or not link:
                    continue
                all_articles.append({
                    "source": source["name"],
                    "category": source["category"],
                    "title": title,
                    "link": link,
                    "summary": entry.get("summary", "")[:200],
                    "time": _parse_published_time(entry),
                })
        except Exception as e:
            print(f"[WARN] RSS fetch failed for {source['name']}: {e}")
    return all_articles


def fetch_market_data() -> dict:
    """Fetch indices and macro indicators (no individual stocks)."""
    all_symbols = {}
    for group_symbols in MARKET_INDICES.values():
        all_symbols.update(group_symbols)

    market_data = {}
    for name, symbol in all_symbols.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")
            if len(hist) == 0:
                raise ValueError("empty history")
            latest = hist.iloc[-1]
            prev = hist.iloc[-2] if len(hist) >= 2 else hist.iloc[-1]
            price = round(float(latest["Close"]), 2)
            change = round(float(latest["Close"] - prev["Close"]), 2)
            change_pct = round(float(change / prev["Close"] * 100), 2) if prev["Close"] != 0 else 0
            market_data[name] = {
                "symbol": symbol,
                "price": price,
                "change": change,
                "change_pct": change_pct,
            }
        except Exception as e:
            print(f"[WARN] Market data failed for {name} ({symbol}): {e}")
            market_data[name] = {"symbol": symbol, "price": "N/A", "change": 0, "change_pct": 0}
    return market_data


def fetch_tw_movers(top_n: int = TW_MOVERS_TOP_N) -> dict:
    """Fetch Taiwan stock top gainers/losers from TWSE Open API."""
    url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
    try:
        resp = requests.get(url, timeout=15, headers={"Accept": "application/json"}, verify=False)
        resp.raise_for_status()
        data = resp.json()

        stocks = []
        for item in data:
            try:
                code = item.get("Code", "")
                # Keep only 4-char all-numeric codes (regular stocks + ETFs, exclude warrants)
                if not (len(code) == 4 and code.isdigit()):
                    continue
                close_str = item.get("ClosingPrice", "").replace(",", "")
                change_str = item.get("Change", "").replace(",", "").replace("+", "")
                trade_val_str = item.get("TradeValue", "0").replace(",", "")
                close = float(close_str) if close_str not in ("--", "", "除權息") else None
                change = float(change_str) if change_str not in ("--", "", "X", "") else None
                trade_value = int(trade_val_str) if trade_val_str.isdigit() else 0
                if close is None or change is None or close == 0:
                    continue
                prev = close - change
                change_pct = round(change / prev * 100, 2) if prev != 0 else 0
                stocks.append({
                    "name": item.get("Name", code),
                    "code": code,
                    "price": close,
                    "change": change,
                    "change_pct": change_pct,
                    "trade_value": trade_value,
                })
            except (ValueError, ZeroDivisionError):
                continue

        # Filter to top 300 by daily trading value (proxy for market cap) to exclude micro-caps
        stocks = sorted(stocks, key=lambda x: x["trade_value"], reverse=True)[:300]
        gainers = sorted(stocks, key=lambda x: x["change_pct"], reverse=True)[:top_n]
        losers = sorted(stocks, key=lambda x: x["change_pct"])[:top_n]
        return {"gainers": gainers, "losers": losers}
    except Exception as e:
        print(f"[WARN] TWSE movers fetch failed: {e}")
        return {"gainers": [], "losers": []}


def fetch_us_movers(top_n: int = US_MOVERS_TOP_N) -> dict:
    """Fetch US stock top gainers/losers from the tracked ticker list."""
    try:
        tickers = list(dict.fromkeys(US_MOVERS_TICKERS))  # deduplicate
        hist = yf.download(tickers, period="2d", progress=False, auto_adjust=True)

        if hist.empty:
            raise ValueError("empty data")

        close = hist["Close"]
        if len(close) < 2:
            raise ValueError("insufficient history")

        prev_close = close.iloc[-2]
        last_close = close.iloc[-1]
        pct_change = ((last_close - prev_close) / prev_close * 100).dropna()

        results = []
        for ticker, pct in pct_change.items():
            price = round(float(last_close[ticker]), 2)
            chg = round(float(last_close[ticker] - prev_close[ticker]), 2)
            results.append({
                "name": ticker,
                "code": ticker,
                "price": price,
                "change": round(chg, 2),
                "change_pct": round(float(pct), 2),
            })

        gainers = sorted(results, key=lambda x: x["change_pct"], reverse=True)[:top_n]
        losers = sorted(results, key=lambda x: x["change_pct"])[:top_n]
        return {"gainers": gainers, "losers": losers}
    except Exception as e:
        print(f"[WARN] US movers fetch failed: {e}")
        return {"gainers": [], "losers": []}
