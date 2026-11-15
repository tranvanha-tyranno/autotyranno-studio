# Rà soát và lọc nguồn video — 14/11/2026

Yêu cầu mới nhất ưu tiên **nội dung kể chuyện kinh tế**, chỉnh lại phông chữ; nhân vật đứng tại chỗ, chỉ xoay nhẹ theo mệnh đề đang đọc. Đây là chỉ dẫn cho lần làm hiện tại, không phải người dùng đã duyệt tạo hình comic cũ. Vì vậy không ép nhân vật thực hiện hành động hoặc cắt cảnh dồn dập chỉ để tuân theo những thử nghiệm trước.

Đã kiểm kê **150 tệp / 1,498,018 byte** trong toàn bộ `cinematic/src/`, lưu SHA-256 từng tệp tại `src-review-2026-11-14.json`. Sau vòng đọc mở rộng: **145 tệp mã/văn bản được đọc trực tiếp toàn bộ**, **2 JSON dữ liệu hình học/font được parse và duyệt cấu trúc đầy đủ**, **3 font nhị phân kiểm CMAP/hash/nguồn**. **Không còn tệp chỉ kiểm kê.** Hai payload số/glyph được ghi đúng là parse dữ liệu, không giả là đọc từng tọa độ như văn xuôi. Đây là rà soát nguồn, không phải xem/nghe liên tục mọi phim lịch sử hay duyệt thẩm mỹ.

Ba hồ sơ chi tiết được đối chiếu lại hash khi hợp nhất: [tài chính](src-review-finance-2026-11-14.json) — 52 tệp; [kinh tế/3D](src-review-economics-2026-11-14.json) — 67 tệp; [ảnh/giao diện/root](src-review-photos-2026-11-14.json) — 27 tệp. Nguồn EconomyStory, CSS/entry và hồ sơ font được đọc/kiểm riêng ở lượt tạo và hợp nhất. Các nhóm có phần trùng, nên không cộng số báo cáo để tự suy số tệp duy nhất.

## Lọc theo mục đích sử dụng

| Nhóm nguồn | Tệp | Đọc mã/văn bản | Parse dữ liệu | Font nhị phân | Cách dùng hiện tại |
| --- | ---: | ---: | ---: | ---: | --- |
| `(root)` | 17 | 16 | 1 | 0 | Multiple historical entrypoints are retained. New story uses its isolated entry. |
| `business` | 11 | 11 | 0 | 0 | Topic-specific cafe/business renderer; selected components inspected, retained as optional reference. |
| `china` | 12 | 11 | 1 | 0 | China r02 criticized for repetitive visual styles; retain sources and exports. |
| `china-v2` | 9 | 9 | 0 | 0 | Revision offers variety but not established as user-approved. |
| `directions` | 5 | 5 | 0 | 0 | Photo/gallery interface explicitly restored; actual past image selection still not approved. |
| `economy-story` | 7 | 4 | 0 | 3 | Current request: content first, local Vietnamese fonts, mostly photos, static actor with cue yaw only. |
| `finance-cast` | 7 | 7 | 0 | 0 | Thirty original SVG designs retained; earlier appearance criticized. |
| `finance-cast-v2` | 4 | 4 | 0 | 0 | Comic direction was chosen; new actual artwork has no user aesthetic approval. |
| `finance-comic` | 1 | 1 | 0 | 0 | Short original comic proof, not a full-production baseline. |
| `finance-demo` | 6 | 6 | 0 | 0 | Earlier demo implementation, retain for reference; no reset to this default. |
| `finance-flow` | 5 | 5 | 0 | 0 | Local continuous object simulation; not substitute for real source photos. |
| `finance-long-comic` | 3 | 3 | 0 | 0 | Long r03 finance film rejected as slides. |
| `finance-long-flow` | 2 | 2 | 0 | 0 | Long r03 finance film rejected as slides. |
| `finance-pace-comic` | 9 | 9 | 0 | 0 | Faster SVG shots failed latest real-photo priority; helper reuse only. |
| `finance-pace-flow` | 5 | 5 | 0 | 0 | Faster SVG shots failed latest real-photo priority; helper reuse only. |
| `finance-photo` | 4 | 4 | 0 | 0 | Best existing photo/crop primitives; old Python runner references absent finance_photo_plan.py and pins old audio. |
| `finance-simple` | 1 | 1 | 0 | 0 | Minimalist film criticized as a slide presentation. |
| `longform` | 23 | 23 | 0 | 0 | Five-minute AI film rejected for too little internet imagery and too much 3D. |
| `scenes` | 6 | 6 | 0 | 0 | 50-second cinematic reset accepted historically; later photo priority overrides dominant-3D default. |
| `semantic` | 10 | 10 | 0 | 0 | Semantic email/table/dashboard rebuild rejected; no default reuse. |
| `visualstory` | 3 | 3 | 0 | 0 | Earlier photo-led AI branch, acceptance not inferred from render. |

Không xóa hoặc ghi đè batch/source cũ. “Lọc” ở đây là chọn rõ entry, tách nguồn đang dùng khỏi các hướng đã bị bác và lưu phạm vi kiểm; không giả sử đổi tên file hoặc tăng số shot chứng minh chất lượng.

## Bốn sửa đổi cụ thể

1. **Phông chữ:** mã cũ pha Arial, Bahnschrift và Times New Roman, nhiều trọng số phụ thuộc hệ điều hành. Cả Arial/Bahnschrift trên máy có các dấu tiếng Việt đã thử; không có bằng chứng để gán lỗi thiếu glyph. Bản mới dùng một họ **Be Vietnam Pro** 400/600/700 local, có OFL, URL nguồn và hash; renderer đợi font thật tải xong trước khi lấy frame. Tiêu đề bớt chữ, line-height 1,27 và phụ đề 1,5 để giữ dấu tiếng Việt.
2. **Nhân vật:** `CharacterV2` có bob/chớp mắt ngay cả khi `idle`. `QuietActor` mới cố định `frame=0`, `speaking=false`, `pose=idle`, biểu cảm trung tính; chân giữ nguyên, chỉ lớp ngoài xoay ngang khoảng −6° đến +7° trong 18 frame sau cue lời. Không gọi đó là lip-sync, diễn xuất hay tạo hình được duyệt.
3. **Ảnh và đồ họa:** giữ khả năng hiển thị ảnh full/split có chiều sâu vừa phải, không dùng lại cảnh 3D/chip/slide làm hình chính. Nhánh ảnh portrait/đồ vật dùng `fit:contain` nhằm giữ trọn nội dung trên nền mờ tối; phải kiểm trên frame thực tế, vì r01 đã phát hiện lỗi lớp ảnh bên dưới; ghi rõ ảnh minh họa và không nhận người trong ảnh là nhân vật Hạnh. Đồ họa chỉ giải thích giá, chi phí, rổ hàng, thu nhập thực hoặc quan hệ nhân quả.
4. **Entry và quy trình:** `economy-story-entry.tsx` cùng `economy-story/` là nhánh cô lập có thể tái sử dụng. `finance_photo_render.py` cũ đang tham chiếu **tệp `finance_photo_plan.py` không tồn tại** và khóa audio của bài cũ; không gọi nó cho bài mới. Root cũ tiếp tục giữ các composition lịch sử.

## Schema và kiểm kỹ thuật

`EconomyStory` nhận `plan` với `segments`, `captions` và `assets` theo tag; `offset` là frame toàn cục để kiểm/render một đoạn. `cueFrame` và `turnCues` là frame **cục bộ bên trong segment**. Nếu renderer dùng `--frames=...` trên toàn phim thì để `offset=0`; nếu render proof từ frame 0 cho một khoảng, truyền `offset` là điểm đầu khoảng. Không cộng hai lần.

Các graphic hiện hỗ trợ `price_path`, `cost_stack`, `cost_compare`, `basket`, `real_wage`, `unit_price`, `flow`, `takeaway` và một số alias. Phần trăm thu nhập/giá/sức mua tính từ dữ liệu, tránh cố định kết quả trong renderer. Bài dùng ví dụ giả định phải giữ nhãn minh họa.

Đã qua TypeScript scoped của entry mới và kiểm CMAP các font mới. Việc này chưa chứng minh crop đẹp, khớp toàn bộ lời hoặc người dùng duyệt. Bản dài phải có preflight frame, proof các phần đầu/giữa/cuối và full decode/âm thanh/timing riêng; ghi đúng phạm vi quan sát khi bàn giao.

## Phát hiện thực tế ở preflight r01 và sửa lớp ảnh

Parent đã kiểm frame preflight của `videos/2026-11-14-o-banh-mi-va-lam-phat/r01/` và phát hiện ảnh `fit:contain` chỉ còn nền mờ, không thấy lớp ảnh nét dự kiến. Hai `CanvasImage` đang ở normal document flow: ảnh nền chiếm chiều cao trước, làm ảnh nét thứ hai bị đẩy xuống dưới vùng stage. Vì vậy việc khai báo `objectFit:contain` và kiểm font/TypeScript trước đó **không xác minh được** hình cuối.

Parent đã sửa cả lớp nền lẫn lớp ảnh nét thành `position:absolute; inset:0` trong `Photograph`, để hai ảnh chồng tại cùng vùng. Nguồn audit đã đọc phần sửa, cập nhật hash và chạy lại TypeScript scoped: đạt. Các frame r01 lỗi được giữ lại; r01 không dùng như preflight đạt. Tại lần cập nhật audit này, r02 đang dựng preflight, **chưa ghi nhận xác minh hình r02**. Quan sát lỗi r01 do parent báo lại; agent lập audit không nhận là đã tự mở các frame đó. Việc kiểm actual r02 thuộc hồ sơ QA tiếp theo, tách khỏi kiểm mã và phông chữ này.

## Xác minh mẫu r03 và nền mờ xử lý trước

Sau hồ sơ lỗi r01, kiểm r02 đã ghi nhận sửa lớp ảnh trong các mẫu liên quan tại [r02-preflight-editorial.json](../../videos/2026-11-14-o-banh-mi-va-lam-phat/review/r02-preflight-editorial.json) và giữ cặp trước/sau kèm hash ở [r02-repair-evidence.json](../../videos/2026-11-14-o-banh-mi-va-lam-phat/review/r02-repair-evidence.json). Hồ sơ bác r01 tiếp tục nằm ở [preflight-editorial.json](../../videos/2026-11-14-o-banh-mi-va-lam-phat/review/preflight-editorial.json).

Parent đã mở **cả bốn contact sheet r03**, bao phủ **50 frame giữa cảnh**, và báo: ảnh nét nằm đúng trong vùng contain, không thấy lỗi cắt chữ rõ rệt trong các mẫu, e40 không hiện sớm kết quả sức mua. Audit ghi nhận đúng nguồn quan sát của parent; agent lập audit không nhận là tự mở các sheet. SHA-256 bốn sheet thực tế được lưu trong JSON audit. Đây là xác minh frame chọn mẫu, **không phải kiểm chuyển động liên tục, nghe toàn bài hay người dùng duyệt**.

r03 thêm `Asset.backgroundFile` để dùng nền mờ đã xử lý một lần bằng Pillow thay vì CSS blur trên từng frame. Nếu thiếu backgroundFile, nền tối thay thế; ảnh nét vẫn có `position:absolute; inset:0` và `fit:contain`. Các hash nguồn trong audit đã được cập nhật sau sửa này. Tốc độ r03 còn chờ đo; không tự gán phần trăm tăng tốc từ thay đổi mã.

## Chọn nguồn cho lần sản xuất tiếp theo

- **Chạy hiện tại:** entry `cinematic/src/economy-story-entry.tsx` → `economy-story/`, dữ liệu/ảnh/audio cô lập theo batch. Giữ Be Vietnam Pro local và nhân vật đứng yên chỉ xoay tại cue lời. Đây là nhánh chờ phản hồi, chưa được người dùng duyệt.
- **Tái dùng có điều kiện:** hợp đồng timing/asset, crop contain, kiểm nguồn, primitive ngắn cần cho phép tính; đối chiếu lại nội dung và đúng take. `CharacterV2` chỉ dùng ở trạng thái đông cứng như bản hiện tại khi không cần diễn.
- **Giữ làm lịch sử:** các renderer finance-long/simple đã bị bác, hướng semantic nhiều bảng/email, nhánh 3D cũ và entry Root tổng hợp. Không đưa trở lại mặc định chỉ vì mã compile được hoặc có nhiều tên scene; không xóa vì các primitive còn được module khác nhập.

Các lỗi/giới hạn nguồn cụ thể mới được ghi trong báo cáo chi tiết: CastSheet ghi 8 tư thế nhưng union có 7; ID nhân vật sai âm thầm về Minh; `person()` chặn scale ở 1,6 dù callsite yêu cầu lớn hơn; `Person` khai báo prop phone nhưng chỉ vẽ cash/receipt; nhiều nhánh numeric pace giữ cố định 120.000/tháng hoặc 1.200.000/năm dù có kiểm trường data. Nhiều cue và scene gắn `bXX`, part modulo hoặc fallback; helper chữ ước lượng bằng số ký tự không thay được đo glyph/crop. Những điểm này hướng dẫn lọc/tái dùng cho lần sau, **không sửa nguồn r03 đang render**.
