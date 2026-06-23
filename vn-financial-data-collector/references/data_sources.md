# Nguồn dữ liệu tài chính VN — URL & Cách truy cập

Tài liệu này cung cấp URL pattern và mẹo trích xuất từ các nguồn dữ liệu tài chính dự phòng (Web Scraping) khi `vnstock` API bị thiếu hụt dữ liệu.

## Mục lục
1. [Vietstock](#1-vietstock)
2. [CafeF](#2-cafef)
3. [cophieu68](#3-cophieu68)
4. [Trang QHCD doanh nghiệp](#4-trang-qhcd-doanh-nghiệp)
5. [VSDC](#5-vsdc)
6. [Nguồn quốc tế phụ trợ](#6-nguồn-quốc-tế-phụ-trợ)

---

## 1. Vietstock
**Dùng cho:** Giá realtime, EPS/BVPS/P/E/P/B cập nhật, số CP lưu hành, lịch sử giá.

| Dữ liệu | URL pattern |
|---|---|
| **Trang tổng quan** | `finance.vietstock.vn/[MÃ]-ten-cong-ty.htm` |
| **Tài chính (KQKD/CDKT)** | `finance.vietstock.vn/[MÃ]/tai-chinh.htm` |
| **Tài liệu BCTC (PDF)** | `finance.vietstock.vn/[MÃ]/tai-tai-lieu.htm` |
| **Lịch sử giá** | `finance.vietstock.vn/[MÃ]/lich-su-gia.htm` |

**💡 Tips:**
- Trang tổng quan hiển thị ngày cập nhật ở góc trên — kiểm tra độ mới.
- Ô "BVPS", "EPS", "P/E", "P/B" thường hiển thị sẵn ở trang tổng quan — dùng để cross-check với số tự tính.
- Lịch sử giá theo ngày — dùng để trích xuất giá đóng cửa cuối năm.

---

## 2. CafeF
**Dùng cho:** Chuỗi BCTC theo năm (KQKD/CDKT/LCTT), tin tức kết quả kinh doanh.

| Dữ liệu | URL pattern |
|---|---|
| **Trang cổ phiếu** | `cafef.vn/du-lieu/hose/[mã]-ten-cong-ty.chn` |
| **BCTC theo năm** | `cafef.vn/du-lieu/bao-cao-tai-chinh/[mã].chn` |
| **Lịch sử giá** | `cafef.vn/du-lieu/hose/[mã].chn` *(tab Lịch sử)* |

**💡 Tips:**
- Trang cổ phiếu hiển thị số CP lưu hành hiện tại ở sidebar — dùng để verify nhanh.
- Tin tức kết quả kinh doanh công bố ~cuối tháng 1 năm sau → search `"[tên DN] kết quả kinh doanh năm [N]"` với filter Google `search_recency_filter=oneMonth`.

---

## 3. cophieu68
**Dùng cho:** Lịch sử chia tách cổ phiếu, sự kiện cổ đông.

| Dữ liệu | URL pattern |
|---|---|
| **Sự kiện (chia tách, cổ tức)** | `cophieu68.vn/quote/event.php?id=[mã]` |
| **Tóm tắt tài chính** | `cophieu68.vn/quote/summary.php?id=[mã]` |
| **BCTC chi tiết** | `cophieu68.vn/quote/financial.php?id=[mã]` |

**💡 Tips:**
- Trang `event.php` liệt kê lịch sử phát hành CP trả cổ tức + chia tách — nguồn **TỐT NHẤT** để dò `shares_outstanding_b` qua các năm.
- Mỗi dòng sự kiện có *"Cổ phiếu sau phát hành: X,XXX,XXX,XXX"* — hãy đọc số này để xây chuỗi số lượng cổ phiếu chính xác.

---

## 4. Trang QHCD doanh nghiệp
**Dùng cho:** BCTC kiểm toán chính thức (PDF), Báo cáo thường niên (BCTN). Cú pháp tìm kiếm (Google Dork): `site:[domain-dn] báo cáo tài chính` → vào trang `/quan-he-co-dong
