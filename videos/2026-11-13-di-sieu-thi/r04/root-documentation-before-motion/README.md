# Video thử và quy trình đã nâng cấp

Mở [trang xem video, lời–hình và hồ sơ](index.html). Bản hiện tại là [r04/long/final.mp4](r04/long/final.mp4): 3 phút 25 giây, 1920×1080, 30 fps, 6.150 frame giải mã đầy đủ. [production-v4.json](production-v4.json) giữ toàn bộ brief, 24 mệnh đề/cảnh, nguồn, quan sát ảnh, giới hạn và take thật. [PRODUCTION_NOTES.md](PRODUCTION_NOTES.md) giải thích nội dung, các lần sửa và giới hạn kiểm tra.

Giữ giọng Nhật Phong và giao diện ảnh/gallery3D cũ. Nội dung, ảnh và ví dụ là của chủ đề mới; các tài sản của kênh tham chiếu không được đưa vào bản xuất này. Phần nghiên cứu có nguồn riêng, ảnh/clip stock có giấy phép và vai trò minh họa; không khẳng định người trong ảnh mua thừa hoặc đây là siêu thị Việt Nam.

## Những phần đã kiểm chứng

- Take mới khớp toàn lời, giữ tốc độ 1.0 và câu cuối; caption/timing/mix giữ nguyên giữa r03 và r04.
- R03 được kiểm toàn bộ 24 keyframe, bảy trang ảnh mỗi giây phủ thời lượng và một số frame native. Phát hiện crop c12 và tiêu đề che danh sách a1.
- R04 render lại 600 frame quanh đúng hai cảnh, gồm đuôi chuyển cảnh, sau đó ghép/encode và kiểm toàn 6.150 frame. Hai lỗi được mở lại từ MP4 mới và kiểm độc lập. Video ngoài vùng sửa được encode lại, không cam kết pixel giống byte.
- Âm lượng toàn r04 khoảng -16 LUFS. Đây là phép đo; chưa nghe liên tục để phê duyệt chất giọng/nhạc/SFX trong phiên này.
- Bộ regression engine, học và sửa riêng cảnh: **65 test đạt**. [Biên nhận sửa](r04/long/repair-receipt.json), [QA](r04/long/qa/report.json), [kiểm hình độc lập](r04/long/qa/INDEPENDENT_REPAIR_VERIFICATION.md).
- Vòng học thực tế có hai bài học được xác minh với bằng chứng và hash: gọi đúng tổng chi/chênh lệch và giữ trọn chữ/số khi chia panel. [Lịch sử](learning-report.json), [guidance](learning-guidance.json), [audit](learning-audit.json). Kiểm kỹ thuật được lưu riêng; chưa có feedback duyệt toàn video của người dùng.

## Dùng lại quy trình

Đọc `workflows/reference-video/PRODUCTION.md` và `LEARNING_LOOP.md` từ gốc dự án. Các công cụ mới:

- `production.py`: manifest nguyên bản, đủ mệnh đề, tài sản đã xem/nguồn/hash, take mới, public riêng batch, mix và queue tuần tự có resume.
- `production_repair.py`: sửa riêng các cảnh đã xác định trong revision mới; giữ đúng giọng/timing/caption, kiểm cả vùng nối và toàn final.
- `learning.py`: lịch sử nối tiếp, kiểm hash, phản hồi riêng với kỹ thuật, bài học đề xuất → áp dụng → kiểm lại; chỉ xuất lesson đã verified.
- `production_review.py`: tạo trang đối chiếu từng mệnh đề với đúng frame, crop, tài sản và nguồn của bản xuất.

`videos/production-queue.json` chỉ chứa job kiểm lại pilot r04, không gọi giọng mới. Queue đã được chuẩn bị, chưa giả lập trạng thái chạy xong; khi chạy sẽ tự kiểm output/hash. Với tập tiếp theo, tạo manifest/topic/assets và batch mới, pin guidance đã kiểm ngay từ đầu; không đổi chủ đề trên bộ ảnh hiện tại.

Đây là cải tiến quy trình dùng lại theo từng batch. Không phải huấn luyện trọng số, lịch chạy nền, đăng tự động, hoặc năng suất hàng loạt đã được đo. Bản thử vẫn chờ phản hồi thực tế của người dùng.
