# Video bài giảng chuyển động

## Bài học từ mẫu người dùng — 01/11/2026

Người dùng yêu cầu nâng cấp video SQL đã dựng để giống phong cách video
`FDown.vn_Tai_video_Facebook_720p (HD)_57ac.mp4`.
Mẫu được kiểm tra trực tiếp: 720 × 900, 30 fps, khoảng 7 phút 04 giây.
Đã lấy 24 ảnh toàn video, 6 khung kích thước gốc và 12 khung cách nhau
2 giây trong đoạn 66–88 giây để xem cách bổ sung nội dung theo bước.

Các đặc điểm cần dùng lại cho video giáo dục cùng phong cách:

1. Khung dọc 4:5, nền giấy trắng; chữ serif xanh đậm, code monospace.
2. Bố cục ổn định: nhận diện bài ở trên trái, checklist giấy vàng trên phải,
   tiêu đề, bảng/đồ họa trung tâm, kết luận được đánh dấu và lời dẫn dưới cùng.
3. Bảng dữ liệu có đường kẻ mảnh, tên bảng trên nhãn màu, cột rõ ràng.
   Phân vai nguồn/kết quả bằng xanh dương/xanh lá.
4. Chuyển động phục vụ giải thích: hiện thêm hàng hoặc ý, tô màu hàng đang
   nói, vẽ mũi tên kết nối, di chuyển hàng sang vị trí mới. Không thêm quay
   camera hoặc phóng to liên tục nếu chúng không giúp hiểu bài.
5. Lời dẫn dưới cùng nằm trên dải giấy có băng dính minh họa. Chia câu thành
   cụm đủ nghĩa, tránh để lại một hay hai từ cuối thành một thẻ riêng.
6. Dùng cùng dữ liệu xuyên suốt. Kiểm tra kết quả truy vấn trước khi dựng.
7. Tạo minh họa riêng và nhận diện bài riêng; không sao chép logo hoặc
   nhân vật của đơn vị làm video mẫu.

## Triển khai

- `paper_classroom.json`: cấu hình phong cách, màu, typography và quy tắc.
- `sql_paper.py`: dựng bài SQL 8 cảnh ở 1080 × 1350, 30 fps.
- `align_narration.py`: lấy timestamp giọng đọc bằng Whisper base cục bộ,
  khớp lại với đúng lời dẫn đã duyệt; nội suy từ không khớp.
- `sql_priority.py`: giữ lại bản ngang cũ và dữ liệu bài học.

```powershell
python workflows/motion-slides/align_narration.py `
  --source videos/2026-11-01-sql-motion-slides `
  --output videos/2026-11-01-sql-motion-slides-v2/alignment

python workflows/motion-slides/sql_paper.py `
  --source videos/2026-11-01-sql-motion-slides `
  --output videos/2026-11-01-sql-motion-slides-v2 --previews

python workflows/motion-slides/sql_paper.py `
  --source videos/2026-11-01-sql-motion-slides `
  --output videos/2026-11-01-sql-motion-slides-v2
```

Dùng thư mục mới cho mỗi bản nâng cấp. `--force` chủ động dựng lại video
từng cảnh; mặc định giữ các cảnh đã có. Audio được dùng lại từ bản đầu.
Không gọi lại TTS hoặc Muse chỉ vì thay đổi bố cục.

## Kiểm tra trước khi giao

- Xem storyboard và các khung trích từ MP4 cuối.
- Kiểm tra vị trí chữ, dấu tiếng Việt, cột, đường nối và subtitle.
- So sánh khung trước/trong/sau thao tác lọc, sắp xếp, chuyển trang.
- Giải mã toàn bộ MP4, kiểm tra kích thước/thời lượng/audio.
- Lưu script, profile, lời dẫn, timestamp, subtitle SRT và báo cáo QA.

Đây là cải tiến mã dựng và lưu quy tắc phong cách theo mẫu. Không có
fine-tuning hay cập nhật trọng số mô hình. Tỷ lệ từ khớp trong bước căn
timestamp không phải điểm đánh giá độ chính xác subtitle; vẫn phải kiểm
tra các cụm quan trọng và thừa nhận mốc nội suy khi mô tả phương pháp.
