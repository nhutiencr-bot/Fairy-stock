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
