# Bản chuẩn bị theo video mẫu — chưa sinh video

Hai bản 20 giây, mỗi bản 17 giây nhân vật nam trưởng thành hư cấu nói trực tiếp (Adam / eleven_v3) và 3 giây cận sản phẩm. Không chèn chữ. Mạch: hook → chi tiết cận → lợi ích → ô báo pin → CTA. Các hành động tay khác nhau, chỉ một cảnh miết vỏ. Cảnh nói ở 1×; cận sản phẩm 1,5×. Tất cả chỉ là manifest/prompt, chưa có hình hoặc video mới.

API Muse local chưa nhận audio điều khiển khẩu hình. Sau khi có nguồn được QA và TTS, talking_review.py chuẩn bị hình/tiếng ở thời gian cuối để đưa qua engine lip-sync thực. Render chặn nếu chưa có synced.mp4 và review khớp hash. Số call lip-sync/giá chưa xác định.
