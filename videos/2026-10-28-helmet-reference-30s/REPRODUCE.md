# Chạy lại hoặc tiếp tục batch

Từ thư mục gốc repo, dùng `python videos/helmet_reference_stages.py plan` để kiểm tra phần còn thiếu. Các lệnh `images`, `videos`, `voices`, `align-voice`, `render` tiếp tục theo task ID và file đã có; `--scene 1` đến `--scene 5` chọn riêng một cảnh. Không chạy lại `prepare_helmet_reference.py` trên batch hiện có.

Các cảnh dùng ảnh mở đầu riêng. File gốc video người dùng nằm trong `input/reference-style.mp4`, chỉ để tham khảo nhịp dựng; không ghép hình ảnh người mẫu hoặc mũ hồng từ video mẫu vào sản phẩm cuối.

`voice.mp3` là bản Adam gốc; `voice-aligned.wav` là lời đọc đã khớp năm đoạn sáu giây. `voice-timing.json` lưu các mốc tách trong khoảng lặng. `scene-XX.mp4` giữ nguyên clip AI tải về. `final.mp4` lấy chín giây từ bốn nguồn ở 1,5×, cảnh đội thử lấy tám giây ở 1,33×; âm thanh được xử lý riêng.

Không đặt khóa truy cập vào batch. Runner dùng cơ chế credential cục bộ sẵn có.
