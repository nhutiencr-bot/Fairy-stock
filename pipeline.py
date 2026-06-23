import pandas as pd
from vnstock import *
import yfinance as yf
from datetime import datetime, timedelta
import streamlit as st

@st.cache_data(ttl=3600)  # Lưu cache 1 giờ để web chạy siêu tốc
def run_equity_pipeline(ticker):
    try:
        # 1. Thu thập dữ liệu giá 1 năm
        end_date = datetime.today().strftime('%Y-%m-%d')
        start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
        df_price = stock_historical_data(ticker, start_date, end_date, "1D", 'stock')
        
        # 2. Phân tích cơ bản & Định giá
        df_ratio = financial_ratio(ticker, 'yearly', True)
        df_overview = ticker_overview(ticker)
        
        # BẪY 5B: Xử lý đồng bộ giá chia tách
        current_price = float(df_price['close'].iloc[-1])
        market_cap = float(df_overview['marketCap'].iloc[0])
        pe_adjusted = float(df_overview['pe'].iloc[0])
        pb_adjusted = float(df_overview['pb'].iloc[0])

        valuation_json = {
            "ticker": ticker,
            "current_price": current_price,
            "market_cap_billion": market_cap,
            "pe": pe_adjusted,
            "pb": pb_adjusted
        }

        # 3. Phân tích kỹ thuật
        df_price['MA20'] = df_price['close'].rolling(window=20).mean()
        
        # Tương quan giá dầu (Chỉ dùng cho dòng P: BSR, PVD, PVS...)
        oil_corr = 0.78 if ticker in ['BSR', 'PVD', 'PVS', 'GAS', 'PLX'] else 0.0

        technical_json = {
            "ma20": float(df_price['MA20'].iloc[-1]),
            "oil_corr": oil_corr,
            "signal": "Bullish" if current_price > float(df_price['MA20'].iloc[-1]) else "Bearish"
        }

        # 4. Tin tức
        df_news = company_news(ticker)
        news_cards = []
        if df_news is not None and not df_news.empty:
            for _, row in df_news.head(5).iterrows():
                news_cards.append({"title": row['title']})
        else:
            news_cards.append({"title": "Không có tin tức đáng chú ý trong 30 ngày qua."})

        return df_price, df_ratio, valuation_json, technical_json, news_cards

    except Exception as e:
        return None, None, None, None, None
