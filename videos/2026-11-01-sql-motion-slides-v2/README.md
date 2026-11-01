# SQL — bản nâng cấp theo mẫu bài giảng trên giấy

Ngày 01/11/2026. Giữ nội dung bài học 8 cảnh / 180 giây và giọng Adam tiếng
Việt từ bản đầu, dựng lại hình ảnh theo video tham khảo người dùng cung cấp.

## Nội dung nâng cấp

- Khung dọc 4:5, 1080 × 1350, 30 fps.
- Nền trắng, chữ serif xanh đậm; bảng có đường kẻ và nhãn màu.
- Checklist giấy vàng, mũi tên cong nối dữ liệu và đánh dấu ý chính.
- Xuất hiện nội dung theo bước; chuyển vị trí dòng khi ORDER BY; minh họa
  các dòng bị bỏ qua trong OFFSET.
- Dải lời dẫn kiểu giấy dán ở dưới. Text dùng nguyên văn lời dẫn gốc,
  timestamp hỗ trợ bởi nhận dạng cục bộ và nội suy những từ không khớp.
- Không gọi lại TTS/Muse. Bản đầu giữ nguyên.

## Tệp để xem

- `SQL-paper-classroom-v2.mp4`: video cuối.
- `storyboard-v2.jpg`: xem nhanh bố cục 8 cảnh.
- `subtitles-vi.srt`: lời dẫn và timestamp, có thể chỉnh sửa.
- `style-profile.json`: cấu hình phong cách tái sử dụng.
- `reference/`: các khung lấy từ video mẫu và thông tin kiểm tra.
- `alignment/`: kết quả nhận dạng và các cụm lời dẫn đã căn.
- `scene-*/`: âm thanh dùng lại và video từng cảnh.
- `qa.json`, `layout-check.json`: kiểm tra video và giới hạn chữ.

Nguồn dựng được lưu ở `workflows/motion-slides/sql_paper.py`, cấu hình
`paper_classroom.json`, và quy trình `WORKFLOW.md`. “Học theo mẫu” ở bản này
là cập nhật renderer và quy tắc thiết kế; không huấn luyện trọng số AI.
