# Kể chuyện kinh tế, ưu tiên nội dung — 14/11/2026

Yêu cầu mới: “học lại toàn bộ src lọc lại điều chỉnh phông chữ”, nhân vật “không cần chuyển động”, chỉ xoay qua lại theo lời thoại, tập trung nội dung và làm thử một bài kinh tế khoảng 10 phút. Đây là thay đổi được người dùng cho phép đối với bản thử này. Không tiếp tục ép nhân vật diễn, nhún, nháy hay cắt nhanh để đáp ứng quy tắc cũ.

Nhánh sản xuất mới dùng `economy_story.py`, `economy_story_content.py`, `economy_story_assets.py`, `cinematic/src/economy-story/` và `economy-story-entry.tsx`. Các nhánh cũ được giữ nguyên làm lịch sử; không đổi nhãn rejected/pending thành approved. Xem bản kiểm kê SRC_REVIEW_2026-11-14.md để phân biệt mã đã đọc và tệp mới chỉ được kiểm kê/hash.

Nội dung gốc “Một ổ bánh mì kể chuyện lạm phát” theo một tiệm hư cấu, phân biệt giá một mặt hàng với rổ CPI, tốc độ tăng giá với mức giá, chi phí với lợi nhuận, thu nhập danh nghĩa với sức mua. Không dùng thống kê thị trường hiện tại hoặc ảnh stock để chứng minh các con số giả định. Hồ sơ nguồn kiến thức nằm trong batch/research/sources.json; giá/chi phí nhân vật là ví dụ tự viết.

Be Vietnam Pro 400/600/700 được đóng gói cùng giấy phép OFL và hồ sơ nguồn. Renderer chờ font thật tải xong trước khi lưu hình. Chữ lớn vừa đủ, nhãn ngắn, phụ đề theo exact alignment. Không thay font toàn bộ các renderer cũ vì việc đó làm mất khả năng tái tạo những bản đã lưu.

Nhân vật giữ nguyên tọa độ và pose, frame=0, speaking=false: không chuyển động miệng, blink, body bob hoặc cử chỉ tự động. Wrapper chỉ xoay góc nhỏ theo đầu câu thực tế trong exact take. Không gọi đó là lip-sync hoặc chuyển động 3D nhân vật thực. Ảnh đời sống là phần minh họa chính, sơ đồ dùng cho tính toán hoặc quan hệ nhân quả. Mọi hình là bối cảnh trừ khi có chứng cứ riêng; ảnh không mô tả người chủ tiệm hư cấu.

Giọng giữ Nhật Phong / eleven_v3 / vi, speed1.0. Mỗi chương tạo một lần có cache, receipt và unresolved-intent guard; khóa lời trước khi gọi. Tái sử dụng nhạc có receipt, mix lời nổi và duck nhạc. Không tạo thêm ảnh AI, footage AI hoặc nhạc mới. Nhánh âm thanh exact-take dùng lại các helper trong finance_long.py; điều này không tái sử dụng renderer hình cũ bị bác.

Từ gốc dự án, chạy với Python đã cài đủ dependencies:

```powershell
python workflows/reference-video/economy_story.py prepare
python workflows/reference-video/economy_story.py voice
python workflows/reference-video/economy_story.py mix
python workflows/reference-video/economy_story.py preflight --revision r01
python workflows/reference-video/economy_story.py proof --revision r01
python workflows/reference-video/economy_story.py render --revision r01
python workflows/reference-video/economy_story.py qa --revision r01
```

`economy_story_assets.py` lưu ảnh và metadata vào batch; phải mở ảnh thật và ghi inspection trước bundle. Kiểm khung render đại diện tất cả beat, xem chuỗi frame trong các proof đầu/giữa/cuối, rồi xuất đầy đủ. Lưu source snapshot, hash, render timing và full decoded-frame/audio QA. Kiểm kỹ thuật, quan sát hình chọn mẫu, nghe/xem liên tục và duyệt của người dùng là các việc riêng. Không dùng decode, số shot hoặc đổi font để tự xác nhận thẩm mỹ.

Đã đo lại cùng đoạn e56 410 frame: r02 mất 107,682 giây; r03 dùng nền xử lý sẵn mất 37,357 giây. Đây là benchmark đoạn này trên máy hiện tại, không phải bảo đảm tốc độ toàn phim. Hai đoạn proof e01 và e30 của r02/r03 giữ nguyên byte MP4; e56 đã được mở chuỗi khung chọn mẫu sau sửa để kiểm ảnh nét và đoạn cuối.

Kiểm lời bằng nhận dạng cục bộ có thể chạy sau render để tránh tranh RAM: `python workflows/reference-video/economy_story_asr.py --batch videos/2026-11-14-o-banh-mi-va-lam-phat`. Verifier dùng base/int8 CPU hai luồng, beam1, tách exact mix theo tám chương và lưu cache/hash từng chương. Lượt small/beam3/word-timestamps toàn mix từng lỗi cấp phát RAM ở 134,28 giây khi chạy song song renderer; giữ lại dữ liệu dở dang và hồ sơ lỗi. Lượt base theo chương đã chạy đủ tám chương trong 157,697 giây, nhận được câu kết. Nhận dạng có thể sai từ/tên/số; đây là bằng chứng chẩn đoán, không phải nghe thủ công hoặc duyệt giọng.

## Tối ưu nền ảnh dựa trên phép đo thực tế

Proof r02 đo `e56` dùng ảnh dọc/contain và nền CSS blur: **107,682 giây cho 410 frame**, khoảng **3,81 frame/giây**. Hai proof cover `e01` và `e30` lần lượt là 30,124 giây/332 frame và 30,653 giây/358 frame. Đây là phép đo các cảnh khác nhau, không phải thí nghiệm chỉ thay blur để quy toàn bộ chênh lệch cho một yếu tố. Receipt gốc được giữ tại [r02/proof/proof-receipts.json](../../videos/2026-11-14-o-banh-mi-va-lam-phat/r02/proof/proof-receipts.json).

r03 xử lý nền một lần: Pillow center-cover **1280×720**, GaussianBlur **23,333 px**, brightness **0,5**, JPEG quality90. Tệp gốc giữ nguyên; `research/derived-backgrounds.json` lưu phương pháp, source hash và derivative hash. `Asset.backgroundFile` trỏ đến bản nền local, renderer không áp filter runtime; ảnh nét foreground tiếp tục dùng contain và absolute inset0. Thiếu nền thì hiển thị nền tối. Bố cục và nội dung không đổi theo mục đích tối ưu này. **Tốc độ r03 đang chờ đo**, không ghi sẵn mức cải thiện.

Parent đã mở bốn sheet preflight r03 với 50 frame giữa cảnh: ảnh nét contain hiện đúng; không thấy cắt chữ rõ rệt trong các mẫu; e40 giữ kết quả sức mua cho cảnh tính tiếp theo. Đây là quan sát frame chọn mẫu, không phải kiểm chuyển động, nghe toàn bộ video hoặc người dùng duyệt. Bằng chứng lỗi r01 và sửa r02 tiếp tục được giữ tại [preflight-editorial.json](../../videos/2026-11-14-o-banh-mi-va-lam-phat/review/preflight-editorial.json), [r02-preflight-editorial.json](../../videos/2026-11-14-o-banh-mi-va-lam-phat/review/r02-preflight-editorial.json) và [r02-repair-evidence.json](../../videos/2026-11-14-o-banh-mi-va-lam-phat/review/r02-repair-evidence.json).
