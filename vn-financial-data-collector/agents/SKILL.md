# VN Financial Data Collector

Thu thập số liệu tài chính doanh nghiệp niêm yết Việt Nam — **đặc thù cần cross-check nhiều nguồn vì mỗi nguồn có độ trễ/sai số khác nhau**.

## Workflow 4 bước

### Bước 1: Xác định năm phân tích (RẤT QUAN TRỌNG)
**Luôn kiểm tra ngày hiện tại** trước khi thu thập. Quy tắc "5 năm gần nhất":
- Nếu tháng hiện tại **≥ 4** (sau Q1): kỳ năm gần nhất = **N-1 đã có BCTC kiểm toán** (công bố ~tháng 3-4). Ví dụ tháng 6/2026 → kỳ 5 năm = **2021-2025**.
- Nếu tháng hiện tại **< 4**: kỳ gần nhất = N-2 (BCTC N-1 chưa ra). Ví dụ tháng 2/2026 → kỳ 5 năm = **2020-2024**.

### Bước 2: Fetch data từ vnstock API (NGUỒN #1 — BẮT BUỘC)
**Luôn dùng vnstock API trước**, KHÔNG web scraping. Tham khảo `references/vnstock_api.md` cho code đầy đủ. Tóm tắt:
```python
from vnstock.api.financial import Finance
from vnstock.api.company import Company
from vnstock.api.quote import Quote

f = Finance(symbol='HPG', source='VCI')
# BCTC đầy đủ 2018Q1-2026Q1:
income = f.income_statement()      # Doanh thu, LNST, EPS...
balance = f.balance_sheet()        # VCSH, Tổng TS, Nợ...
cashflow = f.cash_flow()           # CFO, CapEx...
ratios = f.ratio()                  # PE/PB/ROE/EV-EBITDA tính sẵn!

c = Company(symbol='HPG', source='VCI')
overview = c.overview()             # market_cap, issue_share, target_price
events = c.events()                 # công bố thông tin, cổ tức
