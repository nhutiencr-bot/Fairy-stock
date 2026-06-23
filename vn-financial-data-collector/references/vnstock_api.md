
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
Source	Tên	Hỗ trợ	Ưu tiên
VCI	Vietcombank Securities	Quote, Finance, Company (news/events/overview), Listing	#1 — Đầy đủ nhất
KBS	KBS Securities (TCBS mới)	Company (capital_history, shareholders)	#2 — Bổ sung VCI
DNSE	DNSE	Quote	#3 — Backup
<img width="647" height="266" alt="image" src="https://github.com/user-attachments/assets/11f2a8e9-888b-416a-8ce6-99976df3c105" />
Quy hoạch nguồn: vnstock vs web
Ưu tiên #1: vnstock API (Luôn thử trước)
Loại data	Method vnstock	Thay thế web nào
Giá lịch sử	Quote.history()	Investing.com, Yahoo
BCTC (KQKD/CDKT)	Finance...	Vietstock, CafeF
Ratios	Finance.ratio()	Vietstock
Vốn hóa, số CP	Company.overview()	CafeF sidebar
Tin tức / Sự kiện	Company.news() / events()	CafeF / HOSE / VSD
<img width="443" height="157" alt="image" src="https://github.com/user-attachments/assets/6494549c-8941-4a58-a38c-9e6633d28119" />
Ưu tiên #2: Web scraping (Chỉ khi vnstock thiếu)

BCTC kiểm toán PDF chính thức → Trang QHCD DN

Lịch sử chia tách chi tiết → cophieu68 (/quote/event.php)
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

print(f"=== {ticker} DATA SUMMARY ===")
print(f"Giá hiện tại: {int(overview['current_price'].iloc[0]):,} đ")
print(f"Vốn hóa: {overview['market_cap'].iloc[0]/1e9:,.0f} tỷ VNĐ")
print(f"Số CP: {overview['issue_share'].iloc[0]/1e9:.2f} tỷ")
