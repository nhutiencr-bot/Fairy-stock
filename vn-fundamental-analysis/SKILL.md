# name: vn-fundamental-analysis
**description:** Chuyên trách tính toán, phân tích và bóc tách các chỉ số tài chính cơ bản của doanh nghiệp niêm yết Việt Nam. Kích hoạt khi nhận được dữ liệu JSON thô từ `vn-financial-data-collector` để thực hiện phân tích chất lượng lợi nhuận, tăng trưởng và mô hình DuPont 3 bước.

## VN Fundamental Analysis Engine
Phân tích sức khỏe nội tại và hiệu quả hoạt động của doanh nghiệp dựa trên số liệu lịch sử 5 năm đã được xác minh.

---

## Luồng xử lý tính toán

### 1. Tính toán hiệu suất tài chính thô
Nạp số liệu từ chuỗi JSON đầu vào để bóc tách xu hướng 5 năm:
- **Biên lợi nhuận gộp (Gross Margin):** Lợi nhuận gộp / Doanh thu thuần.
- **Biên lợi nhuận thuần (Net Margin):** Lợi nhuận sau thuế của công ty mẹ / Doanh thu thuần.
- **Tốc độ tăng trưởng kép hàng năm (CAGR):** Tính CAGR 3 năm và 5 năm của Doanh thu và LNST công ty mẹ để xác định doanh nghiệp đang trong chu kỳ tăng trưởng, bão hòa hay phục hồi.

### 2. Mô hình phân rã DuPont 3 bước (Core Logic)
Tuyệt đối không chỉ nhìn ROE độc lập. Bắt buộc phải mổ xẻ cấu trúc ROE (Lợi nhuận trên vốn chủ sở hữu) từng năm qua 3 biến số cấu thành để tìm ra động lực thực sự:
$$\text{ROE} = \text{Biên lợi nhuận thuần (ROS)} \times \text{Vòng quay tổng tài sản (ATO)} \times \text{Đòn bẩy tài chính (FLM)}$$

**Tiêu chuẩn chấm điểm chất lượng ROE:**
- **ROE tăng do ROS (Tốt nhất):** Doanh nghiệp tối ưu hóa được chi phí, tăng biên lãi hoặc có lợi thế độc quyền nâng giá bán.
- **ROE tăng do ATO (Tốt):** Doanh nghiệp cải tiến được công suất, bán hàng nhanh hơn, giải phóng hàng tồn kho tốt.
- **ROE tăng do FLM (Rủi ro cao):** Doanh nghiệp không tăng được hiệu quả kinh doanh mà chỉ đang "gồng" nợ vay nợ để kích ROE ảo. Phải phát tín hiệu cảnh báo nếu FLM tăng liên tục qua các năm.

---

## Định dạng đầu ra (Output structured)
Đóng gói các chỉ số đã tính toán thành cấu trúc mảng JSON đồng bộ để chuyển tiếp sang tầng định giá.
