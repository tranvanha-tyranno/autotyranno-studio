# Học mẫu người dùng gửi — 13/11/2026

## Cập nhật ưu tiên nội dung — 14/11/2026

Người dùng tiếp tục bác chất lượng lời: luông tuồng, thiếu phân đoạn và trọng tâm.
Đọc `CONTENT_FIRST.md` cùng `docs/video-references/2026-11-14-content-study/README.md`
trước khi viết bài mới. Đợt học này đọc lại caption theo chương, phân biệt câu hỏi,
luận điểm, ví dụ, cơ chế, chốt ý, cầu nối và payoff; nghiên cứu cả điểm yếu của mẫu.
Chương phải có chức năng lập luận, không chỉ một tiêu đề. `editorial_gate.py` và
chốt trong `eleven_audio.generate` kiểm map/review khớp lời trước timed TTS mới.
Exact take/cached audio cũ vẫn dùng cho sửa hình; không tạo video mới từ yêu cầu học.

Đọc trước khi viết/dựng video explainer tiếp theo:

1. `docs/video-references/2026-11-13-user-samples/README.md` — mục lục, phạm vi kiểm tra và vị trí bốn bản tải.
2. `docs/video-references/2026-11-13-user-samples/PLAYBOOK.md` — góc kể, người xem suy luận, cách viết và quy tắc chọn hình.
3. `analysis.md`, `analysis.json`, `script-pattern.md` hoặc `scriptpattern.md` trong mỗi thư mục ID — phân tích toàn timeline, không chỉ opening.
4. Bản MP4 và các trang hình ngay tại mốc liên quan — kiểm lại quan sát trước khi áp dụng chi tiết.

## Ràng buộc hiện tại

- Người dùng đã gửi bốn mẫu và yêu cầu tải/học/lưu. Sau đó ngày 13/11/2026, người dùng yêu cầu nâng cấp quy trình, cải tiến sau mỗi batch để sản xuất nhiều video và chọn để agent tự chọn chủ đề đời sống cho bản thử. Dùng PRODUCTION.md và LEARNING_LOOP.md cho bước sản xuất hiện tại; bản dựng mới vẫn chờ phản hồi, không tự coi là đã được duyệt.
- Giữ giao diện ảnh/gallery 3D cũ ở `cinematic/src/directions/` và `videos/2026-11-12-hai-huong/`. Giữ giọng Nhật Phong và hướng âm thanh đã duyệt. Không dùng bản email/table/dashboard bị bác làm mặc định.
- Cả bốn mẫu mới đều thuộc Lóng; không ghi các kết luận này thành quan sát về The Hidden Self.
- Phân biệt mẫu thực tế với yêu cầu người dùng: bốn phần hook → miễn trừ ngắn → nội dung → CTA vẫn là yêu cầu cho bản gốc tương lai, nhưng không phải cả bốn mẫu đều có disclaimer đầu.
- Không dùng ảnh/clip/câu văn/mascot/nhạc của nguồn làm tài sản xuất bản chỉ vì đã tải để nghiên cứu. Viết mới và có hồ sơ nguồn tài sản riêng.

## Cách áp dụng bài học

Chọn **trục câu hỏi và nhân quả**, sau đó viết lời. Với từng mệnh đề, ghi vai trò hình: tư liệu, bối cảnh, giải thích cơ chế hoặc ẩn dụ. Kiểm actual subject/action/object/state và điều tài sản có thể chứng minh. Không kéo stock đẹp nhưng chung chung qua nhiều lời khác nhau; cũng không dựng một màn hình ứng dụng hoặc bảng chữ cho mọi câu trừu tượng.

Hình sự kiện cần đúng sự kiện. Sơ đồ cần đúng quan hệ. Con số cần đúng giá trị, đơn vị, năm và phạm vi; chữ rút gọn không được đổi nghĩa lời. Đổi bố cục vì đổi chức năng của ý; giữ hình đủ lâu nếu cần đọc. Tạo callback có thông tin mới và trả đúng lời hứa của hook trước CTA.

Đây là hướng biên tập được ghi lại từ nghiên cứu, chưa phải xác nhận mọi hình trong demo cũ đã khớp lời hoặc mọi lựa chọn mới sẽ được người dùng duyệt.

## Mã tái sử dụng cho nghiên cứu

```powershell
python workflows/reference-video/reference_study.py --root docs/video-references/2026-11-13-user-samples --phase captions
python workflows/reference-video/reference_study.py --root docs/video-references/2026-11-13-user-samples --phase media
python workflows/reference-video/reference_study.py --root docs/video-references/2026-11-13-user-samples --phase study
python workflows/reference-video/build_study_library.py --root docs/video-references/2026-11-13-user-samples
python workflows/reference-video/audit_reference_study.py --root docs/video-references/2026-11-13-user-samples
python workflows/reference-video/serve_reference_study.py --root docs/video-references/2026-11-13-user-samples --port 8880
```

`reference_study.py` lấy caption gốc, tải AVC 360p + AAC thành MP4 có tiếng, kiểm giải mã toàn A/V, ghi nguồn/hash, tạo các block60 s liên tiếp và ảnh chọn mẫu theo nhịp 5s cộng ứng viên thay đổi lớn từ luồng 2 fps. Không ghi signed media URLs hay credential vào báo cáo. Khi dùng batch mới, cần metadata đúng nguồn trong từng thư mục ID và truyền `--ids` rõ ràng; không tự dùng lại danh sách mặc định cho nguồn khác.

`build_study_library.py` dựng trang đọc tài liệu và phát bản tải theo mốc, chỉ tham chiếu media đang có. Nó không sản xuất video hay sửa giao diện sản phẩm.

`audit_reference_study.py` kiểm bốn báo cáo/mẫu viết, số block, đầu/cuối và tính liên tiếp, các tệp hình, hash MP4/caption so với biên nhận. `serve_reference_study.py` phục vụ riêng thư mục nghiên cứu tại loopback, có HTTP Range để tua MP4; không dùng máy chủ này để xuất bản tài sản nguồn.

Ảnh chọn mẫu giúp phân tích phủ toàn timeline nhưng không chứng minh đã nghe âm thanh/xem liên tục, không thấy chắc mọi cut ngắn và không xác lập hiệu quả retention. Chỉ ghi phần đã kiểm tra thật; phần chưa nghe/đọc/kiểm nguồn phải giữ nhãn chưa xác nhận.
