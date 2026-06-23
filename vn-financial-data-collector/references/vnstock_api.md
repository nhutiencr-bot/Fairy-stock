vnstock API Reference — Nguồn data #1 cho mọi skill

`vnstock` là thư viện Python lấy data trực tiếp từ VCI/TCBS/KBS — đáng tin hơn web scraping vì:
- Data chính thức từ nguồn HOSE (qua VCI broker).
- Không bị block/bot detection như CafeF/Vietstock web.
- Có sẵn BCTC, ratios, news, events — không cần parse HTML.
- Đơn vị nhất quán (nghìn đồng cho giá).

## Mục lục
1. [Cài đặt](#cài-đặt)
2. [Quote — Giá & lịch sử](#quote--giá--lịch-sử)
3. [Finance — BCTC & ratios](#finance--bctc--ratios)
4. [Company — News, Events, Cổ đông](#company--news-events-cổ-đông)
5. [Listing — Danh mục CP](#listing--danh-mục-cp)
6. [Sources](#sources)
7. [Quy hoạch nguồn: vnstock vs web](#quy-hoạch-nguồn-vnstock-vs-web)
8. [Code template: fetch toàn bộ data cho 1 CP](#code-template-fetch-toàn-bộ-data-cho-1-cp)
9. [Đặc thù schema theo ngành](#đặc-thù-schema-theo-ngành)
10. [Troubleshooting](#troubleshooting)

---

## Cài đặt
```bash
pip install vnstock --upgrade
⚠️ API breaking change (31/08/2025): Module vnstock cũ deprecated. Bắt buộc dùng vnstock.api submodule:
from vnstock.api.quote import Quote
from vnstock.api.financial import Finance
from vnstock.api.company import Company
from vnstock.api.listing import Listing
Quote — Giá & lịch sử
Dùng cho skills: vn-technical-analysis (giá 52 tuần, indicators, Beta/Correlation)
from vnstock.api.quote import Quote
q = Quote(symbol='HPG', source='VCI')
df = q.history(start='2025-06-22', end='2026-06-21', interval='1W')
# Columns: time, open, high, low, close, volume
# ⚠️ Giá tính bằng NGHÌN đồng (19.38 = 19,380 đ)
# interval: '1D' daily, '1W' weekly
df = df.dropna(subset=['close'])  # bỏ tuần chưa hoàn thành

# Index (VNINDEX, VN30):
q_vni = Quote(symbol='VNINDEX', source='VCI')
df_vni = q_vni.history(...)
Finance — BCTC & ratios
Dùng cho skills: vn-financial-data-collector, vn-fundamental-analysis, vn-valuation-engine.
from vnstock.api.financial import Finance
f = Finance(symbol='HPG', source='VCI')

# Balance sheet (CDKT) — 122 items, 2018Q1-2026Q1
bs = f.balance_sheet()

# Income statement (KQKD) — 25 items
inc = f.income_statement()
# Chú ý dòng: 'Lợi nhuận của Cổ đông của Công ty mẹ' và 'Lãi cơ bản trên cổ phiếu (VND)' (EPS)

# Cash flow (LCTT) — 41 items
cf = f.cash_flow()

# Ratios — 54 items (TÍNH SẴN!)
ratios = f.ratio() 
🚨 CẢNH BÁO QUAN TRỌNG (Case BSR 2026): API f.ratio() có thể trả về data stale (cũ). Ví dụ chỉ trả 2018-2019 cho BSR dù request 2021-2025.

Cách test: Nếu rt.shape là (54, 7) thay vì (54, 30+) → stale.

Xử lý: Nếu stale, KHÔNG dùng ratio(). Tự tính ROE/ROA/PE/PB từ income_statement + balance_sheet + giá.

🚨 CẢNH BÁO EPS: EPS vnstock có thể sai hoặc dùng weighted-average. Luôn cross-check EPS bằng: LNST(đồng) / số CP năm đó.

Hàm trích xuất dữ liệu BCTC chuẩn:
def get_yearly(df, item_name, years=['2021-Q4','2022-Q4','2023-Q4','2024-Q4','2025-Q4']):
    row = df[df['item'] == item_name]
    return [row[y].values[0] if not row.empty else None for y in years]

lnst = get_yearly(f.income_statement(), 'Lợi nhuận của Cổ đông của Công ty mẹ')
revenue = get_yearly(f.income_statement(), 'Doanh thu thuần')
equity = get_yearly(f.balance_sheet(), 'VỐN CHỦ SỞ HỮU')
Company — News, Events, Cổ đông
Dùng cho skills: vn-news-digest, vn-financial-data-collector (events chia tách), vn-valuation-engine
from vnstock.api.company import Company
c = Company(symbol='HPG', source='VCI')

info = c.overview()     # Vốn hóa, số lượng CP, target_price
news = c.news()         # 50 tin gần nhất
events = c.events()     # 50 sự kiện (cổ tức, chia tách)

# Đổi source KBS để lấy cổ đông & vốn điều lệ
c_kbs = Company(symbol='HPG', source='KBS')
shareholders = c_kbs.shareholders()
cap = c_kbs.capital_history()
Listing — Danh mục CP
from vnstock.api.listing import Listing
lst = Listing(source='VCI')
all_symbols = lst.all_symbols() 
by_industry = lst.symbols_by_industries()

 # Sources (Nguồn cấp dữ liệu API)

| Source | Tên | Hỗ trợ | Ưu tiên |
| :--- | :--- | :--- | :--- |
| **VCI** | Vietcombank Securities | Quote, Finance, Company (news/events/overview), Listing | #1 — đầy đủ nhất |
| **KBS** | KBS Securities (TCBS mới) | Company (capital_history, shareholders) | #2 — bổ sung VCI |
| **DNSE** | DNSE | Quote | #3 — backup |
## 7. Quy hoạch nguồn: vnstock vs web

### Ưu tiên #1: vnstock API (luôn thử trước)

| Loại data | Method vnstock | Thay thế cho web nào |
| :--- | :--- | :--- |
| Giá lịch sử | `Quote.history()` | Investing.com, Yahoo Finance |
| BCTC (KQKD/CDKT/LCTT) | `Finance.balance_sheet / income_statement / cash_flow` | Vietstock, CafeF BCTC page |
| Ratios (PE/PB/ROE/EV-EBITDA) | `Finance.ratio()` | Vietstock ratios page |
| Vốn hóa, số CP | `Company.overview()` | Vietstock, CafeF sidebar |
| Tin tức | `Company.news()` (50 tin) | CafeF, VnExpress search |
| Công bố thông tin | `Company.events()` (50 sự kiện) | HOSE disclosure, VSD |
| Cổ đông lớn | `Company.shareholders()` (KBS) | BCTN, trang QHCD |
| Target price analyst | `Company.overview()['target_price']` | Báo cáo CTCK |
| Index (VNINDEX/VN30) | `Quote(symbol='VNINDEX')` | CafeF, VNDirect |

### Ưu tiên #2: Web scraping (chỉ khi vnstock thiếu)

| Loại data | Web nguồn | Lý do vnstock thiếu |
| :--- | :--- | :--- |
| BCTC kiểm toán PDF chính thức | Trang QHCD DN | vnstock chỉ có data, không có PDF |
| Báo cáo thường niên | Trang QHCD DN | Không có trong API |
| Tin tức > 50 bài gần nhất | CafeF, VnExpress | API chỉ trả 50 bài |
| Lịch sử chia tách chi tiết | cophieu68 /quote/event.php | vnstock events có nhưng hạn chế |
| Tin vĩ mô ngành | VietnamBiz, VSA | Không có trong API |
Ưu tiên #3: WebSearch (chỉ cho verify/bổ sung)
Dùng WebSearch tool để:

Verify số liệu quan trọng (LNST, VCSH) sau khi fetch vnstock

Tìm data mới nhất chưa có trong API (BCTC năm vừa công bố)

Bổ sung góc nhìn định tính (sentiment, news analysis)
Code template: fetch toàn bộ data cho 1 CP
from vnstock.api.quote import Quote
from vnstock.api.financial import Finance
from vnstock.api.company import Company

ticker = 'HPG'
source = 'VCI'

# 1. Giá 52 tuần
q = Quote(symbol=ticker, source=source)
prices = q.history(start='2025-06-22', end='2026-06-21', interval='1W').dropna(subset=['close'])

# 2. BCTC + Ratios
f = Finance(symbol=ticker, source=source)
income = f.income_statement()
balance = f.balance_sheet()
cashflow = f.cash_flow()
ratios = f.ratio()

# 3. Info + News + Events
c = Company(symbol=ticker, source=source)
overview = c.overview()
news = c.news()
events = c.events()

# 4. Index cho Beta
vni = Quote(symbol='VNINDEX', source=source).history(
    start='2025-06-22', end='2026-06-21', interval='1W'
).dropna(subset=['close'])

print(f"=== {ticker} DATA SUMMARY ===")
print(f"Giá hiện tại: {int(overview['current_price'].iloc[0]):,} đ")
print(f"Vốn hóa: {overview['market_cap'].iloc[0]/1e9:,.0f} tỷ VNĐ")
print(f"Số CP: {overview['issue_share'].iloc[0]/1e9:.2f} tỷ")
print(f"BCTC: income {income.shape}, balance {balance.shape}, cashflow {cashflow.shape}")
print(f"Tin tức: {len(news)} bài, Sự kiện: {len(events)}")
## 9. Đặc thù schema theo ngành

⚠️ Ngân hàng (VCB, BID, CTG, TCB...) dùng schema KQKD **KHÁC** công ty thường:

| Công ty thường | Ngân hàng |
| :--- | :--- |
| Doanh thu thuần | Thu nhập lãi thuần + Tổng thu nhập hoạt động |
| Lợi nhuận của Cổ đông của Công ty mẹ | Lợi nhuận sau thuế (hoặc "Cổ đông của Công ty mẹ") |
| Giá vốn hàng bán | Chi phí lãi + Trích lập dự phòng |
| — | Trích lập dự phòng tổn thất tín dụng (đặc thù NH) |
Code fetch LNST ngân hàng:
# Thay vì 'Lợi nhuận của Cổ đông của Công ty mẹ'
lnst = get_yearly(inc, 'Lợi nhuận sau thuế') # cho NH
# HOẶC
lnst = get_yearly(inc, 'Cổ đông của Công ty mẹ')
Code fetch "doanh thu" ngân hàng:
# Không có 'Doanh thu thuần' — dùng:
net_interest_income = get_yearly(inc, 'Thu nhập lãi thuần') # NIM driver
total_income = get_yearly(inc, 'Tổng thu nhập hoạt động') # tổng QT
## 10. Troubleshooting & Cập nhật

| Lỗi | Sửa |
| :--- | :--- |
| `KeyError: 'data'` ở Company | `pip install vnstock --upgrade` |
| `cannot convert float NaN to integer` | Dùng `.dropna(subset=['close'])` trước |
| `Vnstock class deprecated` | Dùng `vnstock.api.*` thay vì `vnstock.Vnstock` |
| `Source VCI does not support X` | Đổi `source='KBS'` hoặc `'DNSE'` |
| `RetryError NotImplementedError` | Method chưa hỗ trợ source đó — đổi source |
| `Auth failed` | `pip install vnstock --upgrade` (tự re-auth) |
Cập nhật vnstock
Kiểm tra version định kỳ:

pip show vnstock | grep Version
pip install vnstock --upgrade
vnstock update thường xuyên — API có thể thay đổi. Luôn check changelog tại https://vnstocks.com/docs/tai-lieu/lich-su-phien-ban
