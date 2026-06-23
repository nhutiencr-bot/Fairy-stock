# vnstock API Reference — Nguồn data #1 cho mọi skill

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
