# Hai hướng kể chuyện bằng ảnh thật + không gian 3D

Đây là manifest gốc của TYRANNO và công cụ chuẩn bị hai demo, không phải bản sao video hay bộ nhận diện của kênh tham chiếu. Hai demo đang chờ người dùng nhận xét. Phân tích nguồn nằm ở `docs/video-references/2026-11-12-two-directions/REFERENCE_AUDIT.md`.

- `long.json`: mở bằng một email chào hàng, lật từ “viết nhanh” sang “ai kiểm tra và chịu trách nhiệm”; hình sáng/kem/coral, nhịp trực tiếp.
- `hidden.json`: mở bằng mâu thuẫn tên nghề/từng nhiệm vụ, đi qua một khung quan sát rồi trở về thử nghiệm nhỏ; navy/ivory/teal, nhịp trầm hơn.

Cả hai tuân theo thứ tự **hook → miễn trừ ngắn → nội dung → CTA** theo yêu cầu của người dùng. Không suy rộng rằng mọi video tham chiếu đều có disclaimer đầu. Giọng Nhật Phong, Eleven v3, vi, speed 1.0 giữ nguyên lựa chọn đã chốt; lời mới có exact character alignment riêng. Không dùng tốc độ take cũ, không cắt câu cuối để vừa một mốc thời lượng.

## Chạy lại demo

Từ thư mục dự án:

```powershell
python workflows/reference-video/directions.py all --direction long
python workflows/reference-video/directions.py all --direction hidden
```

Các bước `plan`, `voice`, `prepare`, `mix` có thể chạy riêng. `voice` dùng cache và đối chiếu request hash; file intent ngăn tự gọi trùng khi provider chưa được hòa giải. `prepare` đòi khớp toàn bộ từ với script, tìm từng phrase theo thứ tự, kiểm tra cut tăng dần, kiểm hash ảnh nguồn, tạo captions tối đa 44 ký tự. `mix` giữ giọng nguyên tốc độ, duck nhạc theo giọng, dùng Foley đúng hành động.

Ảnh gốc giữ nguyên trong `batch/assets`. Public JPEG texture được `exif_transpose`, thumbnail giữ tỉ lệ trong khung 2048×1280 và lưu quality 94 để giảm RAM giải mã. `render-assets.json` ghi hash/kích thước cả nguồn và bản render. Có thể chạy riêng `python workflows/reference-video/directions.py render-assets --direction both` để tạo lại texture cho batch đã chuẩn bị, không gọi giọng/mix hay thay timing. Khi thiếu RAM, render tuần tự với concurrency 1 và bundle lại sau khi thay texture; không dùng chung thư mục bundle tạm đang bị lệnh render khác dọn.

Đầu ra mặc định là `videos/2026-11-12-hai-huong/{long,hidden}/`, public assets ở `cinematic/public/directions/{long,hidden}/`. `props.json` chứa `{data: timeline}` cho CLI Remotion. Renderer và đăng ký composition do source `cinematic/src/directions/` và `Root.tsx` quản lý. Bundle/still/render chạy tuần tự để tránh khóa cache Rspack.

## Render và đóng gói an toàn

Sau khi đã chuẩn bị voice/data/mix/texture, dùng một lệnh từ thư mục dự án:

```powershell
python workflows/reference-video/render_directions.py --batch videos/2026-11-12-hai-huong
```

Lệnh này bundle entry riêng `cinematic/src/directions-entry.tsx` vào `<batch>/render-bundle` bằng flag **`--out-dir=` rõ ràng**, stage duy nhất ảnh JPEG/data/mix thuộc `directions/` vào `<batch>/render-public`, rồi render **tuần tự** ở concurrency 1, H264, CRF 19. Dùng Node + local CLI, `shell=False` và các argument tách riêng. Bundle/public bền vững tồn tại sau mỗi job; không tham chiếu bundle tạm do job khác tự dọn.

Mỗi MP4 được kiểm bằng `direction_qa.py` trước khi chuyển sang bản kế tiếp. Sau cả hai, `directions_review.py` tạo trang so sánh, credits và source snapshot có entry, renderer, profiles, scripts và hashes. Mỗi lần chạy có thư mục `render-attempts/<UTC-id>/` riêng chứa command/log/source snapshot; lỗi không ghi đè log cũ. Không chạy orchestrator khi còn lệnh bundle/render thủ công khác hoạt động. Lock của orchestrator ngăn các lần chạy của chính nó dùng chung Rspack cache.

Nếu đã có `final.mp4`, mặc định sẽ dừng. Để giữ video đã có và chỉ QA lại / render phần còn thiếu:

```powershell
python workflows/reference-video/render_directions.py --batch videos/2026-11-12-hai-huong --skip-existing
```

Chỉ khi cần xuất thay mới, dùng `--overwrite`; final cũ được giữ trong thư mục attempt sau khi render mới thành công. `--direction long` hoặc `--direction hidden` xử lý một bản; đóng gói trang hai hướng chỉ chạy với `--direction both` (mặc định). `--dry-run` kiểm input/hash và in các argv dự kiến, không gọi bundle/render/QA hoặc sửa file. Chạy với batch chủ đề mới bằng `--batch` mới. Nếu public texture đã bị topic khác thay, chạy lại action `render-assets` cho đúng batch trước.

## Chủ đề mới

Sao chép một manifest vào thư mục batch mới rồi viết lại toàn bộ lời và shotlist. Dùng `--batch` mới, `--profile` mới và `--direction` tương ứng:

```powershell
python workflows/reference-video/directions.py all --direction long --profile videos/new-topic/content.json --batch videos/new-topic
```

`sourceBatch` chỉ tới kho ảnh đã có manifest. Mỗi shot ghi `phrase`, `layout`, danh sách ID ảnh và chữ ngắn cần nhấn. Phrase phải tồn tại trong exact take theo cùng thứ tự. Chủ đề khác cần nguồn ảnh khác đúng câu nói; không chỉ đổi tên đề tài trên bộ ảnh công sở này. Catalog bổ sung `EXTRA_IMAGES` giữ URL trang nguồn, CDN, tác giả và giấy phép. Các ảnh minh họa không phải bằng chứng những người trong ảnh dùng AI, bị sa thải hay quảng cáo cho TYRANNO.

Hai gallery 3D ngắn cho thấy quan hệ giữa chính các ảnh thật; chúng không thay toàn bộ lời kể bằng chip, cổng, đồng hồ hoặc khối trang trí. Không mặc định micro/waveform. Phần QA phải xem MP4, crop, chuyển động, chữ và lời xuyên suốt; preflight/decoding không xác nhận chất lượng thẩm mỹ hay sự chấp nhận của người dùng.
