# 7 Bẫy dữ liệu đặc thù thị trường chứng khoán VN

Mỗi bẫy có: dấu hiệu nhận biết → cách phát hiện → cách sửa. Lấy ví dụ thực từ case HPG (2026) và BSR (2026).

## Thứ tự ưu tiên (theo mức độ nghiêm trọng)

| Mức | Bẫy | Tác động |
|:---:|:---|:---|
| 🔴 **CRITICAL** | **5B. Split-adjustment consistency** | PE/PB sai hoàn toàn, kết luận định giá sai |
| 🟠 **CAO** | **1. Số CP lưu hành thay đổi** | EPS/BVPS sai |
| 🟠 **CAO** | **3. LNST vs LN trước thuế** | LNST sai, ROE sai |
| 🟡 **TRUNG BÌNH** | **2. Đơn vị tính** | BVPS phình 1000x |
| 🟡 **TRUNG BÌNH** | **4. Data cũ** | Phân tích sai kỳ |
| 🟡 **TRUNG BÌNH** | **5. Split-adjusted price** | So sánh giá sai |
| 🟢 **THẤP** | **6. Vốn hóa sai format** | Hiển thị sai |

---

## ⭐ Audit procedure ĐẦU TIÊN (Chạy trước khi tính multiples)

**Bước 0: Detect split + verify số CP trước khi tính EPS/PE/PB**

```python
from vnstock.api.company import Company
from vnstock.api.financial import Finance

# 1. Check events cho split/dividend-stock
events = Company(symbol=TICKER, source='VCI').events()
splits = [e for e in events.to_dict('records')
          if any(k in str(e.get('event_title_vi','')).lower()
                 for k in ['chia cổ phiếu','phát hành cổ phiếu','tăng vốn'])]
print(f"Splits found: {len(splits)}")

# 2. Check capital history
cap = Company(symbol=TICKER, source='KBS').capital_history()
print(f"Charter capital changes: {len(cap)}")

# 3. Back-calc CP từng năm: CP = LNST/EPS
inc = Finance(symbol=TICKER, source='VCI').income_statement(period='year')
for y in ['2021','2022','2023','2024','2025']:
    lnst = inc[inc['item']=='Lợi nhuận của Cổ đông của Công ty mẹ'][y].values[0] / 1e9  # tỷ
    eps = inc[inc['item']=='Lãi cơ bản trên cổ phiếu (VND)'][y].values[0]
    cp = lnst*1e9 / eps / 1e9  # tỷ CP
    print(f"  {y}: LNST={lnst:,.0f} tỷ, EPS={eps:,.0f} đ → CP back-calc = {cp:.3f} tỷ")

# 4. Nếu CP 2025 / CP 2024 > 1.2 → split đã xảy ra → áp dụng Bẫy 5B
🔴 Bẫy 5B: Split-adjustment consistency — RỦI RO NGHIÊM TRỌNG
Dấu hiệu: PE/PB history có values "đẹp bất thường" (VD: PE 1-2x cho năm lợi nhuận cao) → mismatch chuẩn giữa giá (split-adjusted) và EPS/BVPS (BCTC gốc).

Ví dụ BSR (sai nghiêm trọng): BSR chia tách 15/10/2025 — 31.5% cổ phiếu thưởng + 30% cổ tức cổ phiếu = 1.615x dilution (3.10 tỷ → 5.007 tỷ CP). vnstock Quote.history() trả giá SPLIT-ADJUSTED (toàn bộ lịch sử scale về base 5.007 tỷ CP), nhưng BCTC gốc dùng base 3.10 tỷ CP cho 2021-2024.

Lỗi cụ thể đã mắc:

EPS 2021 từ BCTC = 2,166 đ (base 3.10 tỷ)

Year-end price 2021 từ vnstock = 13,210 đ (split-adjusted, base 5.007 tỷ)

PE tính sai = 13,210 / 2,166 = 6.10x (mix 2 chuẩn)

PE đúng = 13,210 / (2,166/1.615) = 13,210 / 1,341 = 9.85x
Cách sửa (procedure chuẩn):
# 1. Detect split từ events
events = Company(symbol='BSR', source='VCI').events()
splits = [e for e in events.to_dict('records')
          if 'chia cổ phiếu' in str(e.get('event_title_vi','')).lower()
          or 'phát hành' in str(e.get('event_title_vi','')).lower()]

# Sum dilution ratio: VD 31.5% + 30% = 0.615 → multiplier 1.615
SPLIT_MULT = 1.0
for s in splits:
    ratio = float(s.get('exercise_ratio', 0) or 0)
    if ratio > 0:
        SPLIT_MULT *= (1 + ratio)

# 2. Adjust EPS/BVPS cho các năm TRƯỚC split date về base post-split
for year < split_year:
    eps_adjusted[year] = eps_original[year] / SPLIT_MULT
    bvps_adjusted[year] = bvps_original[year] / SPLIT_MULT
    shares_adjusted[year] = shares_original[year] * SPLIT_MULT
# Year của split và sau: giữ nguyên

# 3. PE/PB = price_adjusted / eps_adjusted (cùng base)
Quy tắc vàng: Nếu công ty có split/dividend-stock trong kỳ phân tích → LUÔN adjust EPS/BVPS/shares về CÙNG base với giá (thường là post-split) trước khi tính PE/PB/MC cross-year.

🟢 Bẫy 6: Vốn hóa sai do số CP cũ hoặc sai format
Dấu hiệu: Vốn hóa hiển thị sai format (VD: "₫136.5B tỷ" — vừa trùng lặp đơn vị B+tỷ, vừa sai số) hoặc sai giá trị tuyệt đối > 20% so với nguồn chính thức.

Cách phát hiện: So sánh vốn hóa hiển thị với market_cap field từ vnstock:
from vnstock.api.company import Company
info = Company(symbol='HPG', source='VCI').overview()
# info['market_cap'] = 1.99e14 = 199,254,000,000,000 đ = 199,254 tỷ
🟠 Bẫy 1: Số CP lưu hành thay đổi qua các năm
Dấu hiệu: EPS/BVPS giảm liên tục dù LNST/VCSH tăng — vì mẫu số (số CP) tăng. HOẶC EPS tự tính ≠ EPS từ BCTC công bố.

Cách phát hiện (3 method):

Back-calc verification: Tính CP = LNST(đồng) / EPS(đ/cp) từng năm. Nếu khác capital_history() > 5% → có vấn đề.

Cross-check EPS: Tính EPS = LNST / CP với CP giả định, so sánh với EPS trong income_statement.

capital_history() audit: Fetch Company(symbol, source='KBS').capital_history() xem vốn điều lệ từng mốc.

🟡 Bẫy 2: Đơn vị tính sai (BVPS phình 1000 lần)
Dấu hiệu: BVPS = hàng triệu đồng (thay vì hàng nghìn) — vô lý so với giá CP (~20,000-30,000 đ).

Công thức đúng: VCSH[tỷ đồng] / số CP[tỷ cp] = đồng/cp (tỷ/tỷ = 1, không cần ×1000).

🟠 Bẫy 3: LNST vs LN trước thuế vs LNST thuộc CĐ mẹ
Dấu hiệu: Cùng 1 năm, các nguồn cho 2 số "lợi nhuận" khác nhau (chênh ~30-70%).

Cách sửa: Dùng Lợi nhuận của Cổ đông của Công ty mẹ (dòng cuối cùng của BCTC, dùng cho EPS). Verify với BCTC kiểm toán PDF từ trang QHCD.

🟡 Bẫy 4: Data cũ trong search results
Dấu hiệu: Search "HPG BCTC 2025" trả về kết quả BCTN 2024 ở vị trí đầu.

Cách sửa: Ép WebSearch với search_recency_filter=oneMonth hoặc fetch trực tiếp trang QHCD DN.

🟡 Bẫy 5: Split-adjusted price khi so sánh nhiều năm
Dấu hiệu: Giá CP năm 2021 và 2025 trông giảm mạnh, nhưng có thể do chia tách chứ không phải giảm giá thật.

Khi nào cần adjust: So sánh giá tuyệt đối qua các năm (line chart giá 5 năm), tỷ suất sinh lời.

Khi nào KHÔNG cần adjust: ROE/ROS/ROA (không phụ thuộc số CP), CAGR LNST/doanh thu.
