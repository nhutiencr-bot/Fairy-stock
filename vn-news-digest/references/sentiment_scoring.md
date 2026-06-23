# Sentiment Scoring — Hệ thống tính điểm

Tin tức tài chính VN cần phân tích định tính vì sentiment thường mơ hồ. Bảng dưới giúp chuẩn hóa.

## Bước 1: Gán sentiment cho từng tin

| Sentiment | Ký hiệu | Tiêu chí |
| :--- | :--- | :--- |
| **bullish** | ▲ | Tin tăng lợi nhuận / tăng sản lượng / dự án tốt / giá ngành tăng / khối ngoại mua / CTCK khuyến nghị MUA |
| **bearish** | ▼ | Tin giảm lợi nhuận / giá ngành giảm / khối ngoại bán / đối thủ cạnh tranh mạnh / CTCK hạ khuyến nghị |
| **neutral** | ◆ | Cổ tức (trung tính), thay đổi nhân sự (chưa rõ), công bố thông tin quy trình |

⚠️ **Quan trọng:** Dùng đồng nhất giá trị `bullish` / `bearish` / `neutral` (tiếng Anh lowercase) cho cả `sentiment` field và `sentiment_breakdown`. Không dùng positive/negative để tránh bug khi render.

**Mẹo phân biệt:**
- "LNST tăng X%" → `bullish` (dù X nhỏ, vẫn tăng)
- "LNST giảm Y%" → `bearish`
- "Cổ tức tỷ lệ Z%" → `neutral` (cổ tức luôn được công bố)
- "Tăng trưởng thấp hơn cùng kỳ" → `bearish` (âm arguably, nhưng dù dương mà thấp hơn kỳ vọng → nhẹ bearish)

---

## Bước 2: Gán impact weight

| Impact | Weight | Tiêu chí |
| :--- | :--- | :--- |
| **Rất cao** | 2.0 | Sự kiện 1 lần lớn: dự án lò cao mới, M&A, thay đổi CEO, KQ quý vượt/kém kỳ vọng > 50% |
| **Cao** | 1.5 | Tin ảnh hưởng định giá dài hạn: sản lượng +20%+ YoY, biên LN ±3 điểm %, giá ngành ±10% |
| **Trung bình** | 1.0 | Tin giao dịch (khối ngoại mua/bán), cổ tức, tin kinh doanh thông thường |
| **Thấp** | 0.5 | Tin quy trình: thông báo cuộc họp, sửa điều lệ, thay đổi đại diện |

**Quy tắc heuristic:**
- Nếu tin xuất hiện trên 3+ nguồn → bump impact lên 1 cấp (tín hiệu thị trường quan tâm).
- Nếu tin về catalyst dài hạn (Dung Quất 2, HRC new line) → impact Rất cao/Cao.
- Nếu tin về ngành/vĩ mô → impact Cao (ảnh hưởng tất cả công ty ngành).

---

## Bước 3: Tính sentiment score

```javascript
const news = [...];  // mảng tin đã gán sentiment + impact
const sentimentValue = { bullish: 1, neutral: 0, bearish: -1 };
const impactWeight = { 'Rất cao': 2.0, 'Cao': 1.5, 'Trung bình': 1.0, 'Thấp': 0.5 };

let rawSum = 0, maxPossible = 0;

news.forEach(n => {
  const w = impactWeight[n.impact];
  rawSum += sentimentValue[n.sentiment] * w;
  maxPossible += w;
});

const score = Math.round((rawSum / maxPossible) * 100);  // -100 → +100
