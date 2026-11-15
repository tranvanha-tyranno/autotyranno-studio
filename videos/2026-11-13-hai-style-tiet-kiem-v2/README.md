# Thử lại sau góp ý slide và nhân vật

Người dùng chê video tối giản r02 giống slide và tạo hình nhân vật r03 chưa ưa mắt; sau đó chọn **“Comic biểu cảm mạnh, hơi hài hước”**. Phản hồi gốc có hash và được lưu vào learning-data tại evt29/30. Chọn hướng comic không phải duyệt các tạo hình mới.

Lần này xuất **hai trích đoạn17,83giây**, cùng đúng hai cảnh daily+dinner của take Nhật Phong cũ, từ frame890 đến1424. Không tạo lại voice, nhạc, ảnh hoặc video bằng API. Đây là bản thử hướng sửa trước khi dựng lại cả phim/bộ30.

- `r02/flow/final.mp4`: hành động liên tục của dải30ngày, hóa đơn60k, bộ cộng tiền, bữa ăn200k và phần tăng lương2triệu. Nhãn/số theo cue của take.
- `r02/comic/final.mp4`: hai nhân vật comic mới; tiến lại gần, cùng giữ hóa đơn bằng vị trí lòng bàn tay thực trong rig, đổi biểu cảm khi thấy tổng chi.
- `r02/comic/character-sheet.png`: hai nhân vật với ba trạng thái đối thoại.
- `index.html`: xem song song; chỉ bật tiếng một bản.

`r01` giữ preflight chưa đạt: bộ đếm tiền chậm hơn câu nói, nhãn ví bị crop, hóa đơn tổng mờ đè máy tính và phép cộng comic chưa ghi200k trên cùng hóa đơn. `preflight-review.json` ghi bằng chứng và thay đổi. R02 là bản sửa, không tự gắn user-approved.

Mã dùng lại: `workflows/reference-video/cinematic/src/finance-flow/`, `finance-cast-v2/`, `finance-comic/`, entry `finance-reset-entry.tsx`, runner `finance_style_reset.py`. Source được snapshot trước bundle; source/props/audio đổi thì phải dùng revision mới. Giữ nguyên thư viện30 cũ để đối chiếu, chưa nhân rộng tạo hình mới trước khi nhận xét thẩm mỹ.

QA giải mã toàn535frame cho mỗi đoạn, cùng PCM audio,30fps1920×1080, chọn năm frame trong mỗi cảnh và xem các preflight thật. Số frame và ảnh chọn mẫu không xác lập đã xem/nghe liên tục hoặc đẹp hơn với người dùng. Nhân vật có hoạt họa miệng theo khoảng có lời, không xác nhận lip-sync âm vị.
