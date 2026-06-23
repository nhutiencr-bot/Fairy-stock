# name: vn-fundamental-analysis
**description:** Phân tích cơ bản doanh nghiệp niêm yết VN từ dữ liệu BCTC 5 năm — tính ROE/ROA/ROS/CAGR, DuPont decomposition (3 thành phần), phân tích xu hướng và chất lượng lợi nhuận. Use when đã thu thập data qua skill `vn-financial-data-collector` và cần phân tích sức khỏe tài chính, hiệu quả kinh doanh.

## VN Fundamental Analysis
Phân tích cơ bản từ BCTC 5 năm — tập trung vào chất lượng lợi nhuận (không chỉ con số).

### Điều kiện tiên quyết
Cần JSON data từ skill `vn-financial-data-collector` với schema chuẩn chứa các thông tin: `data_years`, `shares_outstanding_b`, `income_statement`, `balance_sheet`, `cash_flow`.

---

## Workflow 3 bước

### Bước 1: Tính 5 chỉ số chính (cho mỗi năm)
| Chỉ số | Công thức | Đơn vị | Benchmark tốt (VN) |
|---|---|---|---|
| **EPS** | LNST[tỷ] / số CP[tỷ] | đồng/cp | Tăng dần |
| **BVPS** | VCSH[tỷ] / số CP[tỷ] | đồng/cp | Tăng dần |
| **ROE** | LNST / VCSH × 100% | % | > 15% tốt, > 20% xuất sắc |
| **ROA** | LNST / Tổng TS × 100% | % | > 8% tốt |
| **ROS** | LNST / Doanh thu × 100% | % | Tùy ngành |

⚠️ **Kiểm tra đơn vị:** tỷ / tỷ = đơn vị cơ bản, KHÔNG nhân thêm ×1000. BVPS hợp lý cho CP VN: 5,000-50,000 đồng. Nếu BVPS > 1,000,000 đ → sai đơn vị.

### Bước 2: DuPont Decomposition (Chất lượng ROE)
Tách ROE thành 3 phần để hiểu nguồn gốc thay vì chỉ nhìn con số cuối:
`ROE = Biên LN (ROS) × Vòng quay TS (ATO) × Đòn bẩy (FLM)`

**Diễn giải nhanh:**
- Biên LN giảm nhưng ROE ổn → Công ty hy sinh biên để tăng quy mô (mở rộng).
- ROE tăng chỉ nhờ đòn bẩy → Cảnh báo chất lượng kém, rủi ro cao.
- Biên LN giảm mạnh → Chu kỳ ngành đi xuống hoặc mất lợi thế cạnh tranh.
- 3 thành phần ổn định, biên LN là driver chính → ROE chất lượng cao.

### Bước 3: Phân tích xu hướng & CAGR
`CAGR = (Giá trị cuối / Giá trị đầu)^(1/số năm) - 1`

⚠️ **Bẫy CAGR với cổ phiếu chu kỳ:** Năm đáy chu kỳ làm CAGR âm hoặc phình to. 
- *Quy tắc:* Với cổ phiếu chu kỳ (thép, dầu khí, BĐS), tính CAGR từ đỉnh đến đỉnh hoặc từ đáy đến đáy.
- Với cổ phiếu tăng trưởng (công nghệ, bán lẻ), tính CAGR từ đầu đến cuối là hợp lý.
- Luôn show cả 2: CAGR full 5 năm + CAGR giai đoạn phục hồi.

---

## Output (Đầu ra JSON)
Trả về JSON + diễn giải text theo Schema chuẩn (bao gồm: `ratios_by_year`, `dupont_202X`, `cagr`, `quality_verdict`).

## Phân công cho skill tiếp theo
- Định giá (giá hợp lý từ ratios): dùng skill `vn-valuation-engine`
- Dashboard HTML: dùng skill `vn-research-dashboard`
