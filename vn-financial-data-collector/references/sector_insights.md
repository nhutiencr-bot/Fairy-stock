# Đặc thù định giá theo ngành — Thị trường VN

Mỗi ngành có đặc thù riêng ảnh hưởng đến: (1) chỉ số ưu tiên, (2) hệ số tham chiếu, (3) cách giải thích BCTC. 
Tài liệu này cung cấp Insight cốt lõi để Agent lựa chọn phương pháp định giá phù hợp.

## Mục lục
1. [Ngân hàng](#ngân-hàng)
2. [Thép / Công nghiệp nặng (Chu kỳ)](#thép--công-nghiệp-nặng-chu-kỳ)
3. [Bất động sản](#bất-động-sản)
4. [Bán lẻ / Tiêu dùng](#bán-lẻ--tiêu-dùng)
5. [Công nghệ / Viễn thông](#công-nghệ--viễn-thông)
6. [Dầu khí / Hóa chất](#dầu-khí--hóa-chất)
7. [Bảng tóm tắt hệ số tham chiếu](#bảng-tóm-tắt-hệ-số-tham-chiếu-theo-ngành)

---

## Ngân hàng
* **Cổ phiếu tiêu biểu:** VCB, BID, CTG, TCB, MBB, VPB, ACB, STB, HDB
* **Đặc thù định giá:**
  * KHÔNG dùng PE/ROA truyền thống — ngân hàng có đòn bẩy tài chính cực cao (tài sản = nợ huy động).
  * **Định giá chuẩn = P/B + ROE.**
  * ROE target: 15-20% (cao hơn ngành khác vì đòn bẩy).
  * P/B hợp lý: 1.5 - 3.0x (tùy chất lượng); < 1.0x = báo động (vấn đề tài sản).

* **Chỉ số đặc thù bắt buộc:**

| Chỉ số | Ý nghĩa | Benchmark tốt |
|---|---|---|
| **NPL** (Non-performing loan) | Tỷ lệ nợ xấu | < 3% (VN avg ~2-3%) |
| **NPL coverage** (LLR/NPL) | Dự phòng che chắn nợ xấu | > 100% |
| **CAS / CASA** | Tỷ lệ tiền gửi không kỳ hạn (vốn rẻ) | > 20% |
| **NIM** | Biên lãi thuần | 3.5 - 4.5% |
| **CIR** (Cost-to-Income) | Tỷ lệ Chi phí / Thu nhập | < 35% |
| **CAR** (Capital Adequacy) | Hệ số an toàn vốn | > 8% (Basel II) |

⚠️ **Lưu ý BCTC:** Ngân hàng có Bảng CĐKT khác biệt (không "hàng tồn kho", thay bằng "cho vay khách hàng" + "dự phòng rủi ro"). KQKD có "lãi thuần từ HĐĐT" thay vì "doanh thu thuần".

---

## Thép / Công nghiệp nặng (Chu kỳ)
* **Cổ phiếu tiêu biểu:** HPG, HSG, NKG, TVA, PAC
* **Đặc thù định giá:**
  * Cổ phiếu chu kỳ (Cyclical) — LNST biến động mạnh theo giá hàng hóa thế giới.
  * **PE trung bình 5 năm bị SAI:** Đáy chu kỳ PE phình to (do LNST thấp), đỉnh chu kỳ PE lại co lại.
  * **Định giá đúng = P/B + ROE + EV/EBITDA** (Loại trừ khấu hao vì ngành tư bản lớn).
  * P/B hợp lý: < 1.3x = Vùng mua, > 2.0x = Vùng bán.

* **Chỉ số đặc thù:**

| Chỉ số | Ý nghĩa |
|---|---|
| **Giá HRC** (Hot Rolled Coil) | Giá thép cán nóng thế giới — driver chính lợi nhuận. |
| **Spread** (HRC - Quặng/Than) | Biên chế biến, ~$200-400/tấn. |
| **Sản lượng thép** | Tấn/năm — driver tăng trưởng. |
| **EV/EBITDA** | 4-8x hợp lý (Loại trừ phần khấu hao tài sản khổng lồ). |

* **Catalyst VN đặc thù (Ví dụ HPG):** Thuế chống bán phá giá (AD) HRC Trung Quốc, Dự án lò cao mới (Dung Quất 2).
* **Cách định giá:** Tính EPS bình thường hóa (bỏ năm đáy chu kỳ) → dùng median PE 5N hoặc PB median. Chạy DCF với FCFF (CFO - CapEx).

---

## Bất động sản
* **Cổ phiếu tiêu biểu:** VHM, VIC, VRE, KDH, NLG, DXG, PDR, DIG
* **Đặc thù định giá:**
  * **Định giá = NAV (Net Asset Value) + P/B** (Giá trị tài sản đất đai dự án).
  * Doanh thu ghi nhận theo tiến độ bàn giao (Trễ 1-2 năm so với ký HĐMB).
  * **PE SAI hoàn toàn** vì doanh thu không đều và lạm phát tài sản.

* **Chỉ số đặc thù:**

| Chỉ số | Ý nghĩa |
|---|---|
| **NAV/share** | Giá trị tài sản ròng = (TS thị trường - Nợ) / Số CP |
| **Landbank** (ha) | Quỹ đất tương lai, số năm phát triển |
| **Unrecognized revenue** | Doanh thu chưa ghi nhận (Người mua trả tiền trước) |
| **Gross margin** | 30-50% (Thường rất cao vì vốn đất rẻ) |
| **Net debt / Equity** | Đòn bẩy rủi ro, < 1.0x là an toàn |

---

## Bán lẻ / Tiêu dùng
* **Cổ phiếu tiêu biểu:** VNM, MWG, PNJ, MSN, FRT, DGW
* **Đặc thù định giá:**
  * **Định giá = PE + PEG + SSSG**
  * Biên LN thấp (5-15%) nhưng vòng quay tài sản rất cao.
  * PE 5 năm hợp lý: 15-25x (Cao hơn ngành chu kỳ vì tính ổn định).

* **Chỉ số đặc thù:**

| Chỉ số | Ý nghĩa | Benchmark |
|---|---|---|
| **SSSG** | Tăng trưởng doanh thu cùng cửa hàng | > 5% tốt |
| **Inventory days** | Số ngày tồn kho | 30 - 90 ngày |
| **PEG** (PE/Growth) | Định giá so với tốc độ tăng trưởng | < 1.0 = Rẻ |

---

## Công nghệ / Viễn thông
* **Cổ phiếu tiêu biểu:** FPT, VGI, CMG
* **Đặc thù định giá:**
  * **Định giá = PE + PEG** (Tăng trưởng là driver chính).
  * PE cao (20-40x) hợp lý nếu tốc độ tăng trưởng cao tương xứng.
  * Tiền mặt chiếm tỷ trọng lớn. R&D và nhân sự là tài sản cốt lõi.

* **Chỉ số đặc thù:** Doanh thu tăng trưởng (> 15%/năm), Biên gộp (Dịch vụ 30-50%, Phần mềm 60-80%), Backlog (Hợp đồng đã ký).

---

## Dầu khí / Hóa chất & Đặc thù Lọc hóa dầu (Refining)
* **Cổ phiếu tiêu biểu:** GAS, PLX, BSR, DPM, DGC
* **Đặc thù định giá chung:** Cổ phiếu chu kỳ. PE sai, dùng **EV/EBITDA + P/CF** (Do CapEx và khấu hao cực lớn).

### 🛢️ Đặc thù REFINING (Case Study: BSR 2026)
Phân tích BSR (Lọc hóa dầu Bình Sơn) phải đặc biệt chú ý sự sai lệch so với cổ phiếu khai thác dầu (E&P):
1. **Lợi nhuận phụ thuộc Crack Spread, KHÔNG PHẢI Giá dầu thô:**
   * `LNST = (Giá sản phẩm − Giá dầu thô) × Sản lượng = Crack Spread`.
   * Paradox (Nghịch lý): Quý 1/2026 LNST đạt kỷ lục 8,265 tỷ dù dầu Brent đi ngang (65-70$), lý do là Crack Spread châu Á tăng vọt từ $7 lên $43/bbl do nguồn cung thắt chặt.
   * *Hành động cho Agent:* Tính tương quan (Correlation) giá dầu vs cả LNST VÀ giá cổ phiếu.
2. **CapEx khổng lồ ảnh hưởng LNST ngắn hạn:**
   * Dự án Dung Quất 2 (1.5 tỷ USD) khởi công 2026. Trích lập khấu hao/CapEx lớn sẽ dìm KH LNST 2026 giảm 59%. Catalyst thực sự nằm ở giai đoạn hoàn thành (2029-2030).
3. **Free float thấp (Rủi ro niêm yết):**
   * PVN nắm 92.13% BSR, free float < 8% (Dưới ngưỡng 10% của HOSE).
   * Rủi ro thanh khoản quỹ ngoại, đối diện nguy cơ bị ép chuyển sàn UpCom.

**👉 Yêu cầu cho Dashboard Agent (Ngành Dầu khí/BSR):**
- **Mở khóa Section 9.5 (Tương quan giá dầu):** Chart BSR vs Brent, Phân tích Crack Spread.
- **Section 8 (Bear Case):** Cảnh báo KH LNST giảm, rủi ro Free Float, delay tiến độ DQ2.

---

## Bảng tóm tắt hệ số tham chiếu theo ngành

| Ngành | Định giá chính | Định giá phụ | Hệ số "Mua" | Hệ số "Bán" |
|---|---|---|---|---|
| **Ngân hàng** | P/B + ROE | — | P/B < 1.5x | P/B > 3.0x |
| **Thép / Chu kỳ** | P/B + EV/EBITDA | ROE | P/B < 1.3x | P/B > 2.0x |
| **Bất động sản** | NAV + P/B | Discount NAV | P/B < 1.0x | P/B > 1.5x |
| **Bán lẻ / Tiêu dùng** | PE + PEG | Gross margin | PEG < 1.0 | PEG > 2.0 |
| **Công nghệ** | PE + PEG | Rev Growth | PEG < 1.0 | PE > 50x |
| **Dầu khí / Hóa chất**| EV/EBITDA + P/CF | — | EV/EBITDA < 5x | EV/EBITDA > 8x |
