# SQL — video slide thuyết trình chuyển động

Kịch bản gốc do người dùng cung cấp, ngày 01/11/2026. Bản dựng ngang
1920 × 1080, 24 fps, 8 cảnh theo các mốc 0 / 15 / 35 / 55 / 88 / 113 / 140 /
165 / 180 giây. Giọng đọc tiếng Việt: Adam, ElevenLabs `eleven_v3`.

## Tệp chính

- `SQL-motion-slides.mp4`: video H.264, âm thanh AAC.
- `storyboard.jpg`: bảng xem trước 8 cảnh.
- `source-script.txt`: nguyên văn kịch bản nhận được.
- `manifest.json`: lời dẫn, dữ liệu, SQL và cấu hình.
- `audio-timing.json`: thời lượng giọng gốc và hệ số căn nhịp mỗi cảnh.
- `data-check.json`: kết quả chạy truy vấn với dữ liệu minh họa.
- `qa.json`: kết quả giải mã toàn bộ video.
- `media-info.txt`: thông tin luồng media đọc từ video cuối.
- `clip-*/`: giọng gốc, giọng đã căn nhịp và video từng cảnh.

## Cách dựng

Đồ họa được vẽ và hoạt họa bằng mã nguồn để giữ chính xác chữ tiếng Việt,
code SQL và các dòng dữ liệu. Các thao tác trực quan gồm đưa phiếu vào màn
hình, loại phiếu không hợp lệ, di chuyển phiếu về đúng thứ tự, đổi trang,
tô sáng code và từng trạm xử lý logic.

Giữ nguyên các đoạn lời dẫn trong kịch bản. Các câu chữ trên slide được
rút gọn để dễ đọc. Giọng được căn nhịp độc lập, giảm tốc tối đa 15% cho
những đoạn đọc nhanh; thời lượng các cảnh giữ nguyên như kịch bản.

Bảng minh họa có 10 phiếu, 7 phiếu thỏa điều kiện. Thứ tự sau sắp xếp:
104, 109, 102, 105, 108, 110, 101. Trang 1: 104, 109, 102.
Trang 2: 105, 108, 110. Giả định `id` là duy nhất, các cột được dùng không
có giá trị NULL, dữ liệu không thay đổi trong lúc phân trang.

Kiểm tra dữ liệu dùng SQLite với phần cú pháp SELECT chung trong ví dụ;
đây không phải một lượt chạy kiểm thử PostgreSQL. Sơ đồ xử lý là mô hình
logic cho truy vấn minh họa, không mô tả kế hoạch thực thi vật lý.

## Dựng lại

Từ thư mục gốc dự án:

```powershell
python workflows/motion-slides/sql_priority.py `
  --source videos/2026-11-01-sql-motion-slides/source-script.txt `
  --output videos/2026-11-01-sql-motion-slides `
  --stage all
```

Nguồn dùng lại ở `workflows/motion-slides/sql_priority.py`. Giọng đã tạo
được lưu và tái sử dụng; thông tin xác thực tiếp tục nằm trong cơ chế
DPAPI cục bộ của dự án, không ghi trong bản dựng.
