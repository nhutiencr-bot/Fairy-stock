import pandas as pd
from vnstock import financial_ratio, stock_historical_data
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator

def get_stock_insights(ticker):
    # Đảm bảo mã viết hoa (vd: vnm -> VNM)
    ticker = ticker.upper().strip()
    
    try:
        # ---------------------------------------------------------
        # 1. KÉO DỮ LIỆU TÀI CHÍNH 5 NĂM (Từ vnstock)
        # ---------------------------------------------------------
        df_finance = financial_ratio(symbol=ticker, report_range='yearly', is_all=False)
        
        # Lấy 5 năm gần nhất. Cấu trúc của vnstock trả về cột 'year', 'eps', 'roe', v.v.
        df_5_years = df_finance.head(5)[['year', 'eps', 'roe', 'priceToEarning', 'priceToBook']]
        
        # ---------------------------------------------------------
        # 2. KÉO DỮ LIỆU GIÁ LỊCH SỬ & PHÂN TÍCH KỸ THUẬT
        # ---------------------------------------------------------
        # Lấy dữ liệu giá trong 1 năm gần nhất để tính toán các đường MA, RSI
        df_history = stock_historical_data(symbol=ticker, 
                                           start_date='2025-07-17', # Chỉnh lùi lại 1 năm so với hiện tại
                                           end_date='2026-07-17', 
                                           resolution='1D', type='stock')
        
        # Tính đường trung bình động (MA20)
        sma_20 = SMAIndicator(close=df_history['close'], window=20)
        df_history['MA20'] = sma_20.sma_indicator()
        
        # Tính chỉ số sức mạnh tương đối (RSI 14 ngày)
        rsi_14 = RSIIndicator(close=df_history['close'], window=14)
        df_history['RSI'] = rsi_14.rsi()
        
        # Lấy thông số của ngày giao dịch gần nhất
        latest_data = df_history.iloc[-1]
        
        # ---------------------------------------------------------
        # 3. ĐÓNG GÓI DỮ LIỆU ĐỂ TRẢ VỀ GIAO DIỆN
        # ---------------------------------------------------------
        return {
            "status": "success",
            "ticker": ticker,
            "financials_5y": df_5_years.to_dict(orient='records'),
            "technical": {
                "current_price": latest_data['close'],
                "ma20": round(latest_data['MA20'], 2),
                "rsi_14": round(latest_data['RSI'], 2),
                "verdict": "Mua" if latest_data['RSI'] < 30 else ("Bán" if latest_data['RSI'] > 70 else "Nắm giữ")
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Không thể lấy dữ liệu cho mã {ticker}. Lỗi chi tiết: {str(e)}"
        }

# Chạy thử code
# print(get_stock_insights("FPT"))
