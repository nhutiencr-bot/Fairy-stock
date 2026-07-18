"""
Cô Tiên Stock — FastAPI Backend
Deploy: Railway.app (free tier) hoặc Render.com
Chạy local: uvicorn main:app --reload
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio, time
from functools import lru_cache

app = FastAPI(title="Cô Tiên Stock API", version="1.0.0")

# CORS — cho phép Vercel frontend gọi vào
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: thay bằng domain Vercel của bạn
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ===================== CACHE đơn giản =====================
_cache: dict = {}
CACHE_TTL = 3600  # 1 giờ

def cache_get(key: str):
    if key in _cache:
        data, ts = _cache[key]
        if time.time() - ts < CACHE_TTL:
            return data
        del _cache[key]
    return None

def cache_set(key: str, data):
    _cache[key] = (data, time.time())

# ===================== ENDPOINT: Danh sách mã =====================
@app.get("/api/tickers")
def get_tickers():
    """Trả về danh sách tất cả mã trên HOSE/HNX/UPCOM"""
    cached = cache_get("tickers")
    if cached:
        return cached

    try:
        from vnstock.api.company import Company
        # vnstock 4.x — lấy danh sách mã từ sàn
        # Cách 1: dùng listing
        try:
            from vnstock import Vnstock
            stock = Vnstock()
            df = stock.stock(symbol='VN30', source='VCI').listing.all_symbols()
            tickers = df[['ticker','organ_name','exchange']].rename(columns={
                'ticker':'t','organ_name':'n','exchange':'e'
            }).to_dict('records')
        except Exception:
            # Fallback: hardcode top mã
            tickers = _top_tickers()

        result = {"tickers": tickers, "total": len(tickers)}
        cache_set("tickers", result)
        return result
    except Exception as e:
        return {"tickers": _top_tickers(), "total": 26, "warning": str(e)}

# ===================== ENDPOINT: Phân tích mã =====================
@app.get("/api/stock/{ticker}")
def get_stock(ticker: str, source: str = "VCI"):
    """
    Fetch toàn bộ dữ liệu cho 1 mã: BCTC 5 năm, định giá, tin tức
    GET /api/stock/HPG
    """
    ticker = ticker.upper().strip()
    cache_key = f"stock:{ticker}"
    cached = cache_get(cache_key)
    if cached:
        return {**cached, "cached": True}

    try:
        from vnstock.api.financial import Finance
        from vnstock.api.company import Company
        from vnstock.api.quote import Quote
    except ImportError as e:
        raise HTTPException(503, f"vnstock chưa được cài: {e}. Chạy: pip install vnstock")

    try:
        f = Finance(symbol=ticker, source=source)
        c = Company(symbol=ticker, source=source)
        q = Quote(symbol=ticker, source=source)

        # BCTC
        income = f.income_statement()
        balance = f.balance_sheet()
        cashflow = f.cash_flow()
        overview = c.overview()

        # Xác định năm gần nhất (quy tắc tháng >= 4)
        import datetime
        now = datetime.datetime.now()
        latest_year = now.year - 1 if now.month >= 4 else now.year - 2
        years = list(range(latest_year - 4, latest_year + 1))

        # Parse income statement — hỗ trợ cả Community và Sponsor format
        data_years, revenue, lnst, eps_arr = [], [], [], []

        if 'report_period' in income.columns:
            # Sponsor format — cột tiếng Anh HOA
            annual = income[income['report_period'] == 'year'].copy()
            annual['year'] = annual['ticker'].apply(lambda x: int(str(x)[-4:]) if str(x)[-4:].isdigit() else 0)
            # Thực ra report_period = 'year', lấy cột year từ tên khác
            # Tùy version — adapt nếu cần
            for yr in years:
                row = annual[annual['year'] == yr]
                if not row.empty:
                    data_years.append(yr)
                    revenue.append(float(row['Net sales'].iloc[0]) / 1e9)
                    lnst.append(float(row.get('Attributable to parent company', row.get('Net profit',0)).iloc[0]) / 1e9)
                    eps_arr.append(float(row.get('EPS basic (VND)', 0).iloc[0]))
        else:
            # Community format — rows = metrics, cols = periods
            def get_row(df, keywords):
                for kw in keywords:
                    mask = df['item_en'].str.contains(kw, case=False, na=False) if 'item_en' in df.columns else \
                           df['item'].str.contains(kw, case=False, na=False)
                    rows = df[mask]
                    if not rows.empty:
                        return rows.iloc[0]
                return None

            rev_row = get_row(income, ['Net revenue','Net sales','Revenue'])
            lnst_row = get_row(income, ['parent company','Attributable','Net profit after'])
            eps_row = get_row(income, ['EPS basic','Basic EPS'])

            year_cols = [c for c in income.columns if str(c).endswith('-12-31') or (len(str(c))==4 and str(c).isdigit())]
            for yr in years:
                col = next((c for c in year_cols if str(yr) in str(c)), None)
                if col and rev_row is not None:
                    data_years.append(yr)
                    revenue.append(float(rev_row.get(col, 0) or 0) / 1e9)
                    lnst.append(float((lnst_row.get(col, 0) or 0) if lnst_row is not None else 0) / 1e9)
                    eps_arr.append(float((eps_row.get(col, 0) or 0) if eps_row is not None else 0))

        # Balance sheet — VCSH
        vcsh_arr = []
        if 'Owner' in ' '.join(balance.columns):
            # Sponsor
            annual_b = balance[balance.get('report_period','') == 'year'] if 'report_period' in balance.columns else balance
            for yr in data_years:
                row = annual_b[annual_b.get('year', pd.Series()) == yr]
                vcsh_arr.append(float(row["Owner's Equity"].iloc[0]) / 1e9 if not row.empty else 0)
        else:
            eq_row = _get_balance_row(balance, ["Owner's equity","Total equity","Equity"])
            year_cols_b = [c for c in balance.columns if str(c).endswith('-12-31') or (len(str(c))==4 and str(c).isdigit())]
            for yr in data_years:
                col = next((c for c in year_cols_b if str(yr) in str(c)), None)
                vcsh_arr.append(float((eq_row.get(col, 0) or 0) if eq_row is not None and col else 0) / 1e9)

        # BVPS tự tính
        issue_share = float(overview.get('issue_share', overview.get('shares_outstanding', 1)) or 1)
        bvps_arr = [round(v * 1e9 / (issue_share * 1e6)) if issue_share else 0 for v in vcsh_arr]

        # ROE, ROS, ROA
        ta_arr = []  # total assets
        roe_arr = [round(lnst[i]/vcsh_arr[i]*100, 1) if vcsh_arr[i] else 0 for i in range(len(data_years))]
        ros_arr = [round(lnst[i]/revenue[i]*100, 1) if revenue[i] else 0 for i in range(len(data_years))]

        # Market data
        price_current = float(q.history(period='1D')['close'].iloc[-1]) * 1000 if not q.history(period='1D').empty else 0

        # EPS, PE, PB
        eps_ttm = eps_arr[-1] if eps_arr else 0
        bvps = bvps_arr[-1] if bvps_arr else 0
        pe = round(price_current / eps_ttm, 2) if eps_ttm else None
        pb = round(price_current / bvps, 2) if bvps else None

        # Graham
        graham = round((22.5 * eps_ttm * bvps) ** 0.5) if eps_ttm > 0 and bvps > 0 else None
        mos = round((graham - price_current) / graham * 100, 1) if graham else None

        result = {
            "ticker": ticker,
            "name": overview.get('organ_name', overview.get('company_name', ticker)),
            "exchange": overview.get('exchange', ''),
            "sector": overview.get('industry_name', overview.get('sector', '')),
            "price_current": price_current,
            "market_cap": float(overview.get('market_cap', 0)),
            "shares_outstanding": issue_share,
            "data_years": data_years,
            "revenue": [round(v, 1) for v in revenue],
            "lnst": [round(v, 1) for v in lnst],
            "eps": [round(v) for v in eps_arr],
            "bvps": bvps_arr,
            "vcsh": [round(v, 1) for v in vcsh_arr],
            "roe": roe_arr,
            "ros": ros_arr,
            "pe_current": pe,
            "pb_current": pb,
            "graham_value": graham,
            "margin_of_safety_pct": mos,
            "sources": ["vnstock API (VCI)"],
            "cached": False
        }

        cache_set(cache_key, result)
        return result

    except Exception as e:
        import traceback
        raise HTTPException(500, detail={"error": str(e), "trace": traceback.format_exc()[-500:]})

# ===================== ENDPOINT: Tin tức =====================
@app.get("/api/news/{ticker}")
def get_news(ticker: str, days: int = 30):
    """Lấy tin tức 30 ngày gần nhất cho mã"""
    ticker = ticker.upper()
    cache_key = f"news:{ticker}:{days}"
    cached = cache_get(cache_key)
    if cached:
        return cached
    try:
        from vnstock.api.company import Company
        c = Company(symbol=ticker, source='VCI')
        events = c.events()
        # Filter theo ngày
        import datetime
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
        news_list = []
        for _, row in events.iterrows():
            try:
                dt = row.get('event_date', row.get('date', ''))
                news_list.append({
                    "date": str(dt)[:10],
                    "title": row.get('event_title', row.get('title', '')),
                    "source": row.get('source', 'HOSE/HNX'),
                    "type": row.get('event_type', 'Thông báo')
                })
            except Exception:
                continue
        result = {"ticker": ticker, "news": news_list[:30], "total": len(news_list)}
        cache_set(cache_key, result)
        return result
    except Exception as e:
        return {"ticker": ticker, "news": [], "error": str(e)}

# ===================== ENDPOINT: Health check =====================
@app.get("/")
def health():
    try:
        import vnstock
        ver = getattr(vnstock, '__version__', 'unknown')
    except ImportError:
        ver = "NOT INSTALLED"
    return {"status": "ok", "vnstock": ver, "endpoints": ["/api/tickers", "/api/stock/{ticker}", "/api/news/{ticker}"]}

# ===================== HELPERS =====================
def _get_balance_row(df, keywords):
    for kw in keywords:
        for col in ['item_en', 'item']:
            if col in df.columns:
                mask = df[col].str.contains(kw, case=False, na=False)
                if mask.any():
                    return df[mask].iloc[0]
    return None

def _top_tickers():
    return [
        {"t":"HPG","n":"Tập Đoàn Hòa Phát","e":"HOSE"},
        {"t":"VCB","n":"Ngân hàng Vietcombank","e":"HOSE"},
        {"t":"FPT","n":"Tập Đoàn FPT","e":"HOSE"},
        {"t":"VNM","n":"Vinamilk","e":"HOSE"},
        {"t":"MWG","n":"Thế Giới Di Động","e":"HOSE"},
        {"t":"TCB","n":"Techcombank","e":"HOSE"},
        {"t":"VIC","n":"Tập Đoàn Vingroup","e":"HOSE"},
        {"t":"VHM","n":"Vinhomes","e":"HOSE"},
        {"t":"BID","n":"BIDV","e":"HOSE"},
        {"t":"VPB","n":"VPBank","e":"HOSE"},
        {"t":"ACB","n":"ACB","e":"HOSE"},
        {"t":"MSN","n":"Masan Group","e":"HOSE"},
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
