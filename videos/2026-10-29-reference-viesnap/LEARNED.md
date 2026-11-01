# Bài học từ video mẫu — 29/10/2026

Ưu tiên người dùng bổ sung: **phần lớn video là nhân vật nói, miệng hợp đúng lời thoại**. Đây là yêu cầu cốt lõi, cùng nhịp mở đầu bất ngờ, biểu cảm và động tác có ý nghĩa. Bản cũ dùng voice-over và prompt miệng khép không đạt phong cách này.

## Bằng chứng đã giữ

- `input/reference.mp4`: bản sao nguyên video người dùng cung cấp, SHA-256 `2965598e7057aab487ddf4c953777b2f5112780ebb1381a94f22f03b275a255b`.
- `input/product-original.png`: ảnh gốc bốn màu sạc dự phòng; template chọn riêng chiếc tím.
- `reference-contact-sheet.jpg`: tổng quan.
- `inspection/quarter-second-sheet.jpg`: 85 mẫu hình, cách 0,25 giây, bao phủ toàn video.
- `inspection/mouth-motion-detail.jpg`: phóng to mặt/miệng ở các thời điểm 8–9,25s và 12–13,25s.
- `inspection/reference-audio.wav`, `inspection/audio-levels.txt`, `inspection/inspection.json`: audio tách local, thông tin giải mã và đo thay đổi hình.

Video có 634 frame ở 30fps (21,133 giây hình), container khoảng 21,15 giây. Đầu video có fade tối; khoảng 1,5s đổi sang đoạn hành động bất ngờ; khoảng 7,75s đổi sang nhân vật cầm sản phẩm giới thiệu. Phần sau giữ bố cục tương đối ổn định, miệng, mắt, đầu và tay cùng tạo nhịp. Học cơ chế diễn và kể chuyện, giữ sản phẩm liên quan ngay đầu; không sao chép fade, viền đen, phụ đề, danh tính người thật hoặc tiểu phẩm không liên quan.

Đây là phân tích hình và yêu cầu người dùng về khẩu hình. Chưa có transcript, chưa nghe/chấm khách quan độ lệch môi–tiếng của mẫu; không ghi nhận đã đo lip-sync chính xác từ contact sheet.

## Đã chuyển thành code dùng lại

- `workflows/product-video/inspect_reference.py`: kiểm tra và tách tư liệu local cho các video mẫu sau.
- `workflows/product-video/talking_review.py`: kiểm tra cảnh nói, chuẩn bị hình/tiếng ở thời gian cuối, ràng buộc input và review theo hash.
- `workflows/product-video/storyboard.py`: áp hướng dẫn reference vào payload, chặn render cảnh nói thiếu kết quả lip-sync thật; giữ hình/tiếng 1× sau đồng bộ.
- `workflows/product-video/prepare_reference_review.py`: tạo hai manifest 20 giây, mỗi bản 17 giây nói trực tiếp và 3 giây cận sản phẩm, có các hành động khác nhau.
- `AGENTS.md`, `workflows/product-video/WORKFLOW.md`: lưu ưu tiên mới cho các lần sau.

`talking-review-drafts/` chứa hai batch đã init local và cost-plan, không có ảnh/video mới hoặc khẩu hình mới. Chưa gọi Muse/ElevenLabs, không có phí generation từ công việc này. Mỗi bản dự kiến 16 submission Muse/TTS nếu thực hiện đầy đủ; phần lip-sync là chi phí/lần gọi chưa xác định.

## Trạng thái thực tế

Đã chạy 24 test thành công, gồm kiểm tra FFmpeg không tăng tốc lại sau đồng bộ, đủ frame, vô hiệu hóa kết quả khi đổi audio/timing, từ chối prompt cấm nói và từ chối render thiếu kết quả.

Test dùng hình màu và tiếng sine, chỉ chứng minh hợp đồng dữ liệu và timeline. Chưa chứng minh chất lượng khẩu hình hoặc độ ổn định sản phẩm của các prompt mới.

API Muse local hiện không có audio input trong `VideoRequest`; chưa kết nối engine lip-sync nhận audio thật. Lưu profile và code là cải thiện workflow có thể dùng lại, không phải huấn luyện lại trọng số model. Không giao một video ghép giọng đơn thuần dưới tên “đã khớp miệng”.
