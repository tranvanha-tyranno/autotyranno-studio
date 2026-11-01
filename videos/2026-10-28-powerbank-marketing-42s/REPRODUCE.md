# Tiếp tục batch

Từ thư mục gốc repo:

```powershell
python workflows/product-video/run.py cache --batch videos/2026-10-28-powerbank-marketing-42s
python workflows/product-video/run.py plan --batch videos/2026-10-28-powerbank-marketing-42s
python workflows/product-video/run.py status --batch videos/2026-10-28-powerbank-marketing-42s
python workflows/product-video/run.py render --batch videos/2026-10-28-powerbank-marketing-42s
```

Các bước images/voices/videos cũng tiếp tục theo file/task đã có; thêm --scene 1 đến 6 để chọn riêng. `scene-05-r02` là bản sửa đã chọn; `scene-05` giữ lần bị loại. Không ghi đè hoặc xóa task cũ để ép sinh lại. Đổi revision và ghi lý do QA khi cần lần thử mới. Không chạy lại script prepare trên batch hiện có.

Mỗi cảnh giữ ảnh gốc tải về, prompt, QA hash, video nguồn và thoại riêng. Upload tự chuyển sang PNG thật trong bộ nhớ. Chữ trên video do runner ghép bằng Pillow/FFmpeg. TTS và Muse dùng cache có hash, không lưu credential vào batch.
