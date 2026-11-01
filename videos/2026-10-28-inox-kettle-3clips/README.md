# 3 clip batch — Ấm inox cao cấp 1,8 lít

Ba video dọc 9:16, mỗi video 6 giây, ghép thoại Adam `eleven_v3` tiếng Việt. Ảnh đầu vào được dùng trực tiếp nên không phát sinh lượt tạo opening image.

- `01-01-factory-forward/final.mp4`: xưởng sản xuất, chuyển động camera tiến.
- `02-02-mall-sidewalk/final.mp4`: trung tâm thương mại, chuyển động camera dịch ngang.
- `03-03-appliance-shelf/final.mp4`: cửa hàng gia dụng, hạ nhẹ rồi dịch ngang.

Muse2API đã thử 1 job cho clip đầu nhưng provider trả lỗi 502/text-only, không có media. Theo workflow, không gửi lại job. Ba MP4 hoàn tất dùng FFmpeg zoompan/pan từ ảnh gốc chính xác và audio Adam; vì vậy không mô phỏng chuyển động vật lý của tay hoặc hộp mica. Xem `verification.json` và `contact-sheet.jpg` trong từng thư mục.
