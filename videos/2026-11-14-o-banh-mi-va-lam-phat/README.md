# Một ổ bánh mì kể chuyện lạm phát

Bản thử r03: **10 phút 22,37 giây**, Full HD 1920×1080, 30fps.

Video: `r03/final.mp4`. Font Be Vietnam Pro local; nhân vật giữ pose, chỉ xoay nhẹ theo cue lời. Giọng Nhật Phong / eleven_v3, tốc độ tự nhiên 1.0. Không có thương hiệu kênh. Nhân vật và giá/chi phí là giả định; ảnh thật chỉ minh họa bối cảnh.

- 00:00 — Tờ bảng giá buổi sáng
- 00:58 — Giá cao và giá tăng nhanh
- 02:11 — Sau quầy bánh có gì?
- 03:36 — Khi người mua đông hơn
- 04:51 — Vì sao bảng giá chưa hạ?
- 06:04 — Giỏ hàng của ai?
- 07:38 — Làm sao để bớt nóng?
- 08:55 — Trở lại bữa sáng

Kiểm kỹ thuật: đủ 18.671 frame; giải mã tiếng 622,379 giây, giữ câu kết. ASR base cục bộ nhận dạng đủ tám chương, không có cờ chẩn đoán nghi bỏ đoạn. Đã mở 150 khung chọn mẫu của MP4 cuối cùng và chuỗi proof đầu/giữa/cuối; các việc này không phải nghe/xem liên tục hoặc người dùng đã duyệt thẩm mỹ.

Nguồn và phạm vi: `research/sources.json`, `research/photo-sources.json`, `research/clause-photo-selection.json`. Ảnh thật hiện diện khoảng 65,61% thời lượng kể cả disclaimer, 18 nguồn ảnh thực sự được renderer chọn. Không gán người hoặc cửa hàng trong ảnh cho Hạnh hư cấu.

Lịch sử sửa: giữ r01 có lỗi ảnh dọc và r02 đã sửa; r03 xử lý sẵn nền ảnh để giảm chi phí render. Toàn bộ src đã được rà: 145 mã/văn bản đọc đủ, 2 JSON parse dữ liệu, 3 font kiểm CMAP/hash. Các nhánh cũ và phản hồi bị bác vẫn được giữ.

Hồ sơ QA ở `r03/qa-report.json`, kiểm lời `audio/asr-base-review.json`, kiểm hình ở `review/`. Trạng thái: **chờ phản hồi người dùng**.
