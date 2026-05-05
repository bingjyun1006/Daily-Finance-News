RSS_SOURCES = [
    # 台股（確定可用）
    {"name": "鉅亨網",        "url": "https://news.cnyes.com/rss/id/headline",                         "category": "台股"},
    {"name": "經濟日報",      "url": "https://money.udn.com/rssfeed/news/1001/5591",                   "category": "台股"},
    {"name": "工商時報",      "url": "https://www.ctee.com.tw/feed",                                   "category": "台股"},
    {"name": "MOPS",          "url": "https://mops.twse.com.tw/mops/web/rss",                         "category": "台股"},
    {"name": "中央社財經",    "url": "https://www.cna.com.tw/cna/rss/cat/biz.xml",                    "category": "台股"},
    {"name": "科技新報",      "url": "https://technews.tw/feed/",                                     "category": "台股"},
    {"name": "自由財經",      "url": "https://news.ltn.com.tw/rss/business.xml",                    "category": "台股"},
    {"name": "股感",          "url": "https://www.stockfeel.com.tw/feed/",                            "category": "台股"},
    # 台股（測試中，RSS 已失效）
    {"name": "MoneyDJ",       "url": "https://www.moneydj.com/rss/rss.aspx?a=news",                  "category": "台股"},
    {"name": "今周刊",        "url": "https://www.businesstoday.com.tw/rss/rss.aspx",                 "category": "台股"},
    {"name": "財訊快報",      "url": "https://www.wealth.com.tw/rss.aspx",                            "category": "台股"},
    {"name": "天下雜誌",      "url": "https://www.cw.com.tw/rss",                                     "category": "台股"},
    {"name": "商業周刊",      "url": "https://www.businessweekly.com.tw/rss",                         "category": "台股"},
    # 美股
    {"name": "CNBC",          "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html",         "category": "美股"},
    {"name": "Reuters",       "url": "https://feeds.reuters.com/reuters/businessNews",                "category": "美股"},
    {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/rss/topstories",                      "category": "美股"},
    {"name": "MarketWatch",   "url": "https://feeds.marketwatch.com/marketwatch/topstories/",         "category": "美股"},
    {"name": "Benzinga",      "url": "https://www.benzinga.com/feed",                                 "category": "美股"},
    {"name": "Bloomberg",     "url": "https://feeds.bloomberg.com/markets/news.rss",                  "category": "美股"},
    {"name": "WSJ",           "url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",                "category": "美股"},
    # 總經（測試中）
    {"name": "Investing.com", "url": "https://tw.investing.com/rss/news.rss",                        "category": "總經"},
    {"name": "Fed官方",       "url": "https://www.federalreserve.gov/feeds/press_all.xml",            "category": "總經"},
    {"name": "US Treasury",   "url": "https://home.treasury.gov/news/press-releases-rss",            "category": "總經"},
    {"name": "Motley Fool",   "url": "https://www.fool.com/feeds/index.aspx",                        "category": "美股"},
    # 國際
    {"name": "BBC Business",      "url": "https://feeds.bbci.co.uk/news/business/rss.xml",            "category": "國際"},
    {"name": "Guardian Business", "url": "https://www.theguardian.com/uk/business/rss",               "category": "國際"},
    {"name": "DW Business",       "url": "https://rss.dw.com/rdf/rss-en-bus",                        "category": "國際"},
    {"name": "FT",                "url": "https://www.ft.com/markets?format=rss",                    "category": "國際"},
    # 科技 & AI
    {"name": "TechCrunch",         "url": "https://techcrunch.com/feed/",                             "category": "科技"},
    {"name": "The Verge",          "url": "https://www.theverge.com/rss/index.xml",                   "category": "科技"},
    {"name": "VentureBeat",        "url": "https://venturebeat.com/feed/",                            "category": "科技"},
    {"name": "Ars Technica",       "url": "https://feeds.arstechnica.com/arstechnica/index/",         "category": "科技"},
    {"name": "Wired",              "url": "https://www.wired.com/feed/rss",                           "category": "科技"},
    {"name": "Bloomberg Tech",     "url": "https://feeds.bloomberg.com/technology/news.rss",          "category": "科技"},
    {"name": "iThome",             "url": "https://www.ithome.com.tw/rss",                            "category": "科技"},
    {"name": "TechOrange",         "url": "https://buzzorange.com/techorange/feed/",                  "category": "科技"},
    {"name": "數位時代",           "url": "https://www.bnext.com.tw/rss",                             "category": "科技"},
]

# 市場概覽：大盤指數 + 總經指標（無個股）
MARKET_INDICES = {
    "大盤": {
        "台灣加權":    "^TWII",
        "元大台灣50":  "0050.TW",
        "S&P 500":     "^GSPC",
        "NASDAQ":      "^IXIC",
        "道瓊":        "^DJI",
        "費半(SOX)":   "^SOX",
        "恒生":        "^HSI",
        "日經225":     "^N225",
    },
    "總經": {
        "10Y美債":    "^TNX",
        "美元指數":   "DX-Y.NYB",
        "台幣匯率":   "TWD=X",
        "VIX":        "^VIX",
        "黃金":       "GC=F",
        "原油":       "CL=F",
    },
}

# 台股強弱勢：使用 TWSE Open API，此處存放顯示用設定
TW_MOVERS_TOP_N = 10

# 美股強弱勢：S&P 500 代表性成分股（涵蓋各產業）
US_MOVERS_TICKERS = [
    # 科技/半導體
    "AAPL", "MSFT", "NVDA", "AMD", "INTC", "QCOM", "AVGO", "TXN", "MU",
    "AMAT", "LRCX", "KLAC", "MRVL", "ASML", "NXPI", "ON", "SWKS",
    # 網路/AI/軟體
    "GOOGL", "META", "AMZN", "NFLX", "ORCL", "CRM", "NOW", "ADBE",
    "INTU", "PLTR", "SNOW", "DDOG", "ZS", "CRWD", "NET",
    # 電動車/硬體
    "TSLA", "AAPL", "DELL", "HPQ", "STX", "WDC",
    # 金融
    "JPM", "BAC", "GS", "MS", "WFC", "C", "V", "MA", "AXP", "BLK",
    # 醫療/生技
    "JNJ", "ABBV", "PFE", "MRK", "UNH", "AMGN", "GILD", "LLY", "BMY",
    # 消費
    "WMT", "COST", "HD", "LOW", "NKE", "MCD", "SBUX", "KO", "PEP", "AMZN",
    # 能源
    "XOM", "CVX", "COP", "SLB", "OXY",
    # 工業/航太
    "CAT", "DE", "BA", "RTX", "LMT", "GE", "HON", "UPS", "FDX",
    # 電信/媒體
    "T", "VZ", "DIS", "CMCSA",
    # ETF（用於市場情緒參考）
    "SPY", "QQQ", "SOXX",
]
US_MOVERS_TOP_N = 5

# 財報追蹤清單：具市場影響力的美股（財報日期每週自動拉取）
EARNINGS_WATCHLIST = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "META", "AMZN", "TSLA", "AMD",
    "INTC", "AVGO", "JPM", "BAC", "GS", "V", "MA", "NFLX", "ORCL",
    "CRM", "ASML", "TSM", "UNH", "XOM", "CVX", "LMT", "QCOM",
]

# 美股代號對應中文名
US_TICKER_CN_NAMES = {
    "AAPL": "蘋果", "MSFT": "微軟", "NVDA": "輝達", "AMD": "超微",
    "INTC": "英特爾", "QCOM": "高通", "AVGO": "博通", "TXN": "德州儀器",
    "MU": "美光", "AMAT": "應材", "LRCX": "科林研發", "KLAC": "科磊",
    "MRVL": "邁威爾", "ASML": "艾斯摩爾", "NXPI": "恩智浦",
    "ON": "安森美", "SWKS": "思佳訊",
    "GOOGL": "谷歌", "GOOG": "谷歌", "META": "Meta臉書", "AMZN": "亞馬遜",
    "NFLX": "奈飛", "ORCL": "甲骨文", "CRM": "Salesforce", "NOW": "ServiceNow",
    "ADBE": "奧多比", "INTU": "直覺軟體", "PLTR": "帕蘭泰爾",
    "SNOW": "Snowflake", "DDOG": "Datadog", "ZS": "Zscaler",
    "CRWD": "CrowdStrike", "NET": "Cloudflare",
    "TSLA": "特斯拉", "RIVN": "Rivian",
    "DELL": "戴爾", "HPQ": "惠普", "STX": "希捷", "WDC": "威騰",
    "JPM": "摩根大通", "BAC": "美國銀行", "GS": "高盛",
    "MS": "摩根士丹利", "WFC": "富國銀行", "C": "花旗",
    "V": "Visa", "MA": "萬事達", "AXP": "美國運通", "BLK": "貝萊德",
    "JNJ": "嬌生", "ABBV": "艾伯維", "PFE": "輝瑞", "MRK": "默克",
    "UNH": "聯合健康", "LLY": "禮來", "AMGN": "安進",
    "GILD": "吉利德", "BMY": "百時美施貴寶",
    "WMT": "沃爾瑪", "COST": "好市多", "HD": "家得寶",
    "NKE": "耐吉", "MCD": "麥當勞", "SBUX": "星巴克",
    "KO": "可口可樂", "PEP": "百事可樂",
    "XOM": "埃克森美孚", "CVX": "雪佛龍", "COP": "康菲石油",
    "SLB": "斯倫貝謝", "OXY": "西方石油",
    "CAT": "卡特彼勒", "DE": "迪爾", "BA": "波音",
    "RTX": "雷神", "LMT": "洛馬", "GE": "奇異",
    "HON": "漢威聯合", "UPS": "UPS", "FDX": "FedEx",
    "T": "AT&T", "VZ": "威訊", "DIS": "迪士尼", "CMCSA": "康卡斯特",
    "SPY": "S&P500 ETF", "QQQ": "那指ETF", "SOXX": "費半ETF",
}

# 靜態網站設定
SITE_HASH = "f3k9m2qx"
SITE_BASE_URL = "https://bingjyun1006.github.io/Daily-Finance-News"

# 產業動態關鍵字（空產業當天不顯示）
INDUSTRY_KEYWORDS = {
    "半導體製造": [
        "台積電", "TSMC", "聯電", "世界先進", "晶圓代工", "先進製程", "N2", "N3", "EUV",
        "foundry", "wafer", "2nm", "3nm", "CoWoS", "SoIC",
    ],
    "IC設計": [
        "聯發科", "瑞昱", "聯詠", "智原", "M31", "Qualcomm", "Intel", "fabless",
        "IC設計", "SoC", "CPU", "GPU", "NPU", "晶片設計",
    ],
    "封測封裝": [
        "日月光", "矽品", "京元電", "ASE", "封測", "封裝", "先進封裝",
        "Chiplet", "2.5D", "3D IC", "HBM封裝",
    ],
    "PCB/基板": [
        "PCB", "印刷電路板", "欣興", "台光電", "景碩", "電路板", "基板", "ABF基板",
        "載板", "substrate",
    ],
    "記憶體": [
        "DRAM", "HBM", "HBM3", "HBM4", "美光", "Micron", "SK海力士", "Hynix",
        "三星記憶體", "南亞科", "華邦電", "記憶體", "memory", "NAND",
    ],
    "被動元件": [
        "國巨", "華新科", "MLCC", "電容", "電阻", "電感", "被動元件", "Yageo", "Walsin",
    ],
    "面板": [
        "友達", "群創", "OLED", "LCD", "面板", "AUO", "Innolux", "MicroLED",
        "顯示器", "display",
    ],
    "AI伺服器/ODM": [
        "AI伺服器", "廣達", "鴻海", "緯創", "緯穎", "英業達", "仁寶",
        "GB200", "GB300", "液冷", "散熱", "ODM", "CSP", "data center",
        "資料中心", "超微", "hyperscaler",
    ],
    "電源/散熱": [
        "台達電", "健策", "奇鋐", "散熱", "電源供應器", "PSU", "冷卻", "液冷模組",
        "thermal", "Delta Electronics",
    ],
    "重電/電力": [
        "台電", "世紀鋼", "中興電", "變壓器", "離岸風電", "風電", "電網",
        "再生能源", "儲能", "電力", "輸配電",
    ],
    "網通": [
        "中磊", "智邦", "合勤", "Wi-Fi 7", "Wi-Fi7", "網路設備", "交換器",
        "路由器", "Ethernet", "800G", "400G", "網通",
    ],
    "生技醫療": [
        "生技", "醫療器材", "FDA", "新藥", "臨床", "IND", "NDA", "藥證",
        "biotech", "pharma", "医療", "疫苗",
    ],
    "金融/壽險": [
        "國泰金", "富邦金", "中信金", "升息", "降息", "Fed利率", "金融股",
        "壽險", "銀行", "利差", "信貸", "金融市場",
    ],
    "航運": [
        "長榮", "陽明", "萬海", "貨櫃", "運費", "運價", "SCFI", "BDI",
        "Evergreen", "航運", "shipping", "關稅衝擊",
    ],
    "Big Tech(美)": [
        "Apple", "蘋果", "Microsoft", "微軟", "Google", "Alphabet", "Meta",
        "Amazon", "AWS", "Azure", "GCP", "OpenAI", "Anthropic",
    ],
    "半導體設備": [
        "ASML", "Applied Materials", "Lam Research", "KLA", "東京威力",
        "半導體設備", "EUV機台", "蝕刻", "沉積", "CVD", "PVD",
    ],
    "外資動態": [
        "摩根士丹利", "美銀", "美林", "高盛", "摩根大通", "瑞銀", "花旗",
        "匯豐", "野村", "外資調升", "外資調降", "外資買超", "外資賣超",
        "目標價", "上調評等", "下調評等",
        "Morgan Stanley", "Goldman Sachs", "BofA", "JPMorgan", "UBS",
        "Citi", "HSBC", "Nomura",
    ],
}
