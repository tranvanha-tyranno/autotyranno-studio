# Trang xem bản dựng riêng

`production_review.py` tạo `index.html`, `review.json` và `review-checks.json` ở gốc một pilot/batch. Nó chỉ đọc artifact đang có; không gọi giọng, dựng lại, chạy queue, thay giao diện trong video hoặc tự ghi người dùng đã duyệt.

```powershell
python workflows/reference-video/production_review.py --root videos/2026-11-13-di-sieu-thi --batch r04 --manifest production-v4.json
```

`--batch` và `--manifest` tương đối với `--root`. Trang dùng đúng revision được chọn; không lấy MP4 revision cũ thay cho file chưa sẵn. `--direction long` là mặc định; có thể chọn `hidden` cho pipeline khác.

Nếu cần trang xem trước khi render xong, thêm `--allow-pending`. Phần MP4, QA và frame chưa có sẽ được ghi chờ; các mốc chỉ lấy từ `data.json` theo exact take đã lưu, không ước lượng từ số từ. Sau khi QA hoàn tất, chạy lại không có cờ này.

Trang bao gồm:

- MP4 và poster của revision, thời lượng/frame theo timeline, trạng thái chờ phản hồi người dùng.
- Toàn bộ lời dẫn, góc khai thác, nhu cầu người xem được suy luận, lời hứa của hook và điều chốt lại.
- Mỗi shot: mệnh đề nguyên vẹn, mốc vào/ra theo frame, kiểu bố cục, vai trò hình, điều cần thấy, phạm vi hỗ trợ và giới hạn.
- Frame QA giữa shot khi đã có, liên kết file gốc và các contact sheet toàn thời lượng; ảnh chọn mẫu không được gọi là đã xem liên tục.
- Nguồn ảnh/clip, giấy phép, creator, hash, crop chuẩn hóa và focus; nguồn nghiên cứu nội dung tách khỏi tư liệu minh họa.
- Biên nhận QA, giọng/nhạc/mix, guidance đã pin và tệp review/learning đang giữ cùng pilot.

Builder kiểm các shot liên tiếp, số frame giải mã khớp timeline, hash MP4 khớp QA và hash nguồn/crop khớp biên nhận. Nó không xác thực ý nghĩa của hình chỉ từ nhãn, không chấm thẩm mỹ hoặc xác nhận đã nghe tiếng. Nội dung nguồn được đưa vào DOM bằng `textContent`; dữ liệu JSON nhúng escape dấu `<` để không thực thi HTML trong lời/script.

Có thể mở HTML trực tiếp. Để phát và tua MP4 qua HTTP Range, dùng máy chủ loopback đã có:

```powershell
python workflows/reference-video/serve_reference_study.py --root videos/2026-11-13-di-sieu-thi --port 8881
```

Máy chủ chỉ phục vụ artifact cục bộ tại `127.0.0.1`; đây không phải bước xuất bản.

`videos/production-queue.json` hiện chỉ chứa pilot đã được yêu cầu, không có bước `voice` hay job chủ đề mới. Tệp queue là cấu hình; việc tồn tại của nó không có nghĩa queue đã chạy. Trạng thái hoàn tất chỉ do runner ghi sau khi thực sự thực hiện hoặc kiểm lại các bước.
