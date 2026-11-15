# Kể chuyện kinh tế, ưu tiên nội dung — 14/11/2026

> **Đã bị yêu cầu làm lại toàn bộ, 15/11/2026:** phản hồi mới bác lời rời rạc,
> nhịp chậm, nhân vật hoạt hình, hình như slide, voice ngang, subtitle thấp/nhỏ,
> thiếu footage thật và đoạn miễn trừ đầu dài. Không dùng r06 làm baseline được
> duyệt. Nhánh mới là `BREAD_DOCUMENTARY.md`, `bread_documentary.py` và
> `videos/2026-11-14-banh-mi-documentary/`. Người dùng chọn một giọng Việt khác
> sau khi ElevenLabs hết quota; batch mới dùng Nam Minh toàn bộ, các batch cũ
> và hai take Nhật Phong mới được giữ. Các trạng thái pending trước đây trong
> tài liệu này là lịch sử, không phủ nhận yêu cầu làm lại hiện tại.

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

## Phản hồi mới: r03 bị bác vì vẫn là slide — 14/11/2026

Người dùng xem bản r03 và phản hồi: **“sao chứ làm như cái slide vậy nhỉ nhân vật thì chueyern độngt í đi nghĩ sao để nó đứng im 1 chô như thế vậy”**. Trạng thái r03 chuyển thành `rejected_visual_slide_static_cast`; các kiểm frame, ASR, số liệu và thời lượng trước đó không thay đổi trạng thái này. Giữ nguyên MP4, audio, ảnh, receipt và báo cáo r03 để đối chiếu.

Lỗi nằm ở hướng dựng: `QuietActor` dùng `frame=0`, `pose=idle`, `speaking=false` cho toàn beat, còn nội dung chỉ thay headline/ảnh/graphic. Góc xoay nhẹ không đủ tạo hành động. Bản sửa phải cho nhân vật và vật thể thực hiện hành động có quan hệ với mệnh đề đang đọc: cầm và đặt ổ bánh, kéo/tách hóa đơn, đổ bột, đưa vật vào lò, xếp lại giỏ, cân/so sánh tiền, hoặc chuyển trạng thái sơ đồ khi phép tính diễn ra. Mỗi cảnh cần có mở đầu → thao tác → trạng thái mới; một ảnh đứng yên với zoom, yaw, bob, blink hoặc đổi chữ không được tính là chuyển động đạt yêu cầu.

Đây là thay đổi riêng mới nhất cho bản thử kinh tế và **ghi đè chỉ dẫn “đứng yên, chỉ xoay nhẹ” ở phần đầu tài liệu**. Giữ Be Vietnam Pro, ảnh thật, exact Nhật Phong và mix hiện có; không tạo lại voice/music/image provider. Sửa trong `cinematic/src/economy-story/` và runner dùng chung, tạo proof đầy đủ đầu–giữa–cuối có hành động nhìn thấy được, mở proof để đối chiếu, rồi mới cân nhắc render dài. Bản proof mới vẫn `pending` cho đến khi người dùng xem.


## r06 — sửa chuyển động theo phản hồi người dùng

Revision
06 đã thay QuietActor frame0/idle bằng hành động có ngữ nghĩa trong cinematic/src/economy-story/: ổ bánh/biên lai/tiền đi vào vùng tay, pose chuyển idle → receive/give/point/count, cảm xúc và hướng nhìn đổi, còn thanh chi phí/giá/giỏ hàng được lắp theo từng giai đoạn. Các proof hoàn chỉnh được lưu tại ideos/2026-11-14-o-banh-mi-va-lam-phat/r06/proof/; 01-copy, 15-copy, 56-copy đã được mở theo chuỗi frame. Chân nhân vật vẫn neo và miệng đóng; đây không phải lip-sync.

Bản dài
06/final.mp4 giữ nguyên lời/nhạc/mix và không gọi provider mới. QA đủ 18.671 frame, nhưng duyệt thẩm mỹ của người dùng vẫn pending.
03/final.mp4 và bằng chứng bị bác vẫn giữ nguyên để đối chiếu. Khi proof r06 được người dùng chấp nhận, có thể dùng renderer này làm baseline hành động cho đề tài mới; không tự gán chấp thuận cho batch khác.
