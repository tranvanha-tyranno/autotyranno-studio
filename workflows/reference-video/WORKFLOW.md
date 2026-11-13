> **Sửa hướng Trung Quốc sau phản hồi lặp kiểu (13/11/2026):** r02 bị người dùng từ chối vì lặp vài mẫu hình. Đọc [CHINA_VARIETY.md](CHINA_VARIETY.md) cho r03 Remotion `cinematic/src/china-v2/`, giữ nguyên take/mix, thiết kế hành động riêng cho từng cảnh và kiểm năm thời điểm của mọi cảnh bằng `china_variety_qa.py`. Số cảnh và tên mechanic không chứng minh đa dạng; phải mở bản dựng thật. Chưa có chấp thuận r03.

> **Nhánh kinh tế Trung Quốc theo yêu cầu riêng (13/11/2026):** xem [CHINA_ECONOMY.md](CHINA_ECONOMY.md) cho pipeline khoảng mười phút bằng bản đồ/biểu đồ/mô phỏng nguyên bản, take Nhật Phong, nguồn số liệu và benchmark thời gian/chi phí. Dùng `china.py` / `china_audio.py` / `china_render.py` / `cinematic/src/china/`, không thêm nhận diện kênh. Đây là nhánh theo đề tài, không thay mặc định ảnh/gallery của video đời sống. Bản mới vẫn chờ phản hồi.

> **Luồng ảnh/gallery đời sống (13/11/2026):** đọc REFERENCE_LEARNING.md, PRODUCTION.md và LEARNING_LOOP.md. Dùng production.py cho kịch bản nguyên bản, toàn bộ mệnh đề lời–hình, nguồn/ảnh đã mở/hash, take Nhật Phong mới, tài sản riêng batch, hàng đợi tuần tự và lưu bài học có bằng chứng. Giữ giao diện ảnh/gallery3D được khôi phục; hình phải đúng nghĩa và vai trò, không trở lại bảng/email/dashboard dày chữ. REAL_IMAGE_DIRECTION.md vẫn hướng dẫn chọn tư liệu. Các renderer cũ phía dưới giữ để tái tạo lịch sử; không tự ghi đè chỉ đạo mới.

# Cập nhật ưu tiên — Lăng Kính / Tyranno

Người dùng đã xác nhận hướng footage thật bắt đầu đúng nhưng yêu cầu nhiều style trong một video; không giữ micro/waveform chạy suốt. `lang-kinh.profile.json` lưu nhận diện và sound presets; `editorial.py` dựng 7 kiểu bố cục dùng footage chuyển động. Cùng màu và giọng dẫn, đổi cách trình bày theo luận điểm. `documentary.py` giữ để tái tạo bản cũ; không mặc định dùng layout mic/wave nữa.

## Luồng âm thanh mới

- `audio_stages.py plan --batch ...` ghi giới hạn số lượt mới; cache theo payload/model/voice, không theo filename đơn thuần.
- `audio_stages.py samples --batch ...` tạo sample ngắn Thùy Tiên và Adam; giữ nguyên take và thông số.
- `audio_stages.py voice --batch ...` dùng lựa chọn voice trong manifest; API with-timestamps trả character alignment của đúng take.
- `audio_stages.py sounds --batch ...` chỉ tạo các effect manifest yêu cầu, tái dùng cache; không gọi lại vì đổi hình.
- `editorial.py render --batch ...` tạo căn giọng, subtitle, 11 đoạn hình, bus SFX, nhạc và mix. `editorial.py qa --batch ...` đo frame, duration, audio LUFS/true peak, xuất sheet 1fps.

Credentials đọc ELEVENLABS_API_KEY hoặc Windows DPAPI .secrets/elevenlabs.dpapi.xml; key không được đặt vào manifest/prompt/profile. `eleven_audio.py` lưu intent trước POST, chặn lặp khi chưa rõ kết quả; đổi script/model cần revision mới. Không retry provider lỗi vô hạn.

## Phối cảnh và âm thanh

Mỗi cảnh khai báo style và nguồn chính/phụ; cache shot gồm hash source bytes, config, overlay và renderer. Inset/split/filmstrip vẫn phải có chuyển động, không dùng collage ảnh tĩnh để thay footage. PNG typography cần loop/framerate riêng khi fade alpha; kiểm tra output thật vì ảnh một frame có thể bị giữ ở alpha=0. Subtitle và chữ nhấn có vùng riêng, không chồng nhau. Tính linh hoạt không có nghĩa mỗi giây đổi màu/đổi giọng.

SFX đặt theo sự kiện, dùng thấp hơn lời: mở đầu nhẹ, chuyển bố cục, nhấn đối lập, giấy/bàn phím và ambience liên quan; không thêm tiếng báo động hoặc tiếng nổ vô cớ. Nhạc dùng sidechain duck khi có giọng. Giữ bus hiệu ứng riêng và cue sheet. Đo loudness cuối, không đồng nhất decode pass với duyệt âm/hình.

# Video bình luận theo 17 mẫu YouTube

Trước khi sản xuất, đọc `docs/video-references/2026-11-11/RELEARN_AUDIT.md`, xem media mẫu của profile đã chọn và xem lỗi của hai bản đầu. Thư viện có `index.html`, `catalog-complete.json`, 17 thư mục ID; mỗi thư mục có reference-av.mp4 và evidence.json. Tải lại nếu thiếu bằng `python workflows/reference-video/complete_reference_downloads.py` (giữ các bản đã có).

Nhánh podcast: footage chuyển động làm nền, voice-over nam bình luận, khung 16:9, grade nhẹ để vẫn thấy nội dung, mic và waveform từ audio thật, caption nhỏ căn word timestamps. Nhánh bản tin/bình luận có bố cục khác. Không coi màu tối và icon micro là đủ nếu cảnh nền vẫn chỉ là hình vẽ.

Mỗi batch mới dùng thư mục riêng dưới videos/. batch.json ghi script, thời lượng, danh sách MP4, in/out, mục đích cảnh và nguồn kiểm chứng. asset-sources.json lưu trang item, link tải và giấy phép. Không gọi tư liệu stock quốc tế là cảnh quay Việt Nam. Không lấy footage/nhạc/lời của các kênh mẫu để tạo final mới.

Chốt giọng trước timeline. documentary.py tạo/giữ narration-original.mp3, word-boundaries.json, narration.wav và aligned-words.json. Nếu tốc độ để khớp 49 giây nằm ngoài 0,8–1,22, phải sửa script. Nửa giây cuối dành nhịp nghỉ; không cắt câu cuối. Caption khôi phục dấu câu từ script chỉ sau khi token khớp và không để một từ cuối thành thẻ riêng.

Chạy từ thư mục dự án:

    python workflows/reference-video/documentary.py voice --batch videos/<batch>
    python workflows/reference-video/documentary.py render --batch videos/<batch>
    python workflows/reference-video/documentary.py qa --batch videos/<batch>

Voice hiện dùng Microsoft Edge online TTS NamMinh; không mô tả là OpenAI hay Adam. Đọc voice-info.json để biết nhà cung cấp và tempo. Mỗi lần sửa script dùng batch/revision mới; không dùng lại timestamp cũ. Nếu thay asset hoặc grade, tạo lại shot đó trước render (shots/*.mp4 đang là cache theo batch).

QA kỹ thuật: giải mã, 1.500 frame ở 30fps, 50 giây, không cắt last_word, đủ audio. QA hình: xem full-duration-review.jpg 1fps và khung lớn đầu/giữa/cuối; đánh giá cảnh có chuyển động, đúng ý, độ sáng và chữ. ASR local là phép đối chiếu lời cuối, có lỗi từ/tên/số; không phải chứng nhận phát âm chính xác. Giữ trạng thái user_acceptance pending đến khi người dùng duyệt. Hai renderer cũ render_one_minute.py và render_reference_style.py là prototype bị từ chối, không dùng lại cho profile này.

## Vòng đánh giá có bản xuất riêng

`review_rounds.py run --round N` tạo batch mới từ vòng trước, giữ giọng/SFX gốc bằng asset immutable, chỉ encode lại shot có source/config/overlay khác. `review-focus.jpg` là khung lớn quanh thay đổi; `review-all.jpg` lấy 1fps cả 50 giây. Chỉ sau khi xem mới chạy `review_rounds.py review --round N --note ...` để lưu điều quan sát và quyết định giữ. Script mang manifest của series đánh giá hiện tại; khi dùng cho nội dung khác phải thay source và edit plan, không gán giả quan sát cũ.

Bài học thực tế: ví dụ xưởng may phải có cảnh may/vải; phòng thí nghiệm không thay cho mọi ngành. Nhãn xuất/nhập cần cảnh thương mại và nói rõ minh họa. Cắt hình theo câu từ exact voice alignment, không chia đều số giây. Giữ khoảng nguồn khác nhau khi dùng lại cùng clip. Panel chỉ che phần cần thiết; đo chiều rộng caption trong safe area. Grade mặc định không được làm mất màu vật thật; per-source override có ưu tiên rõ ràng. Không chấm điểm thẩm mỹ từ histogram.

**Lỗi frame phát hiện ở vòng 8:** picture.mp4 có 1500 frame nhưng final có 1498 frame dù container vẫn 50s. Sau khi đổi một đoạn split thành full-screen, metadata màu giữa các shot không thống nhất có thể làm pipeline filter/subtitle khởi tạo lại và rơi frame biên. Renderer nay chuẩn hóa SAR và BT.709 TV-range cho mọi shot trước concat; bản sửa vòng 8 đã decode đủ 1500 frame. Giữ output rejected-1498-frames.mp4 và frame-failure.json trong batch để đối chiếu, không coi duration container là đủ QA.


## Ưu tiên mới nhất: Motion graphics mạnh, 3D và chữ động — 11/11/2026

Người dùng đã từ chối chất lượng animation, style và âm thanh của chuỗi mười bản editorial. Các vòng đó kiểm chứng được kỹ thuật nhưng không được người dùng duyệt thẩm mỹ. Sau câu hỏi chọn hướng, người dùng chọn chính xác **“Motion graphics mạnh, 3D và chữ động”**. Áp dụng `cinematic.profile.json` và `cinematic/` cho bản làm lại; tên thư mục “cinematic-reset” là tên batch cũ, không có nghĩa làm phim tài liệu footage làm nền chủ đạo.

Pipeline hiện tại tạo số extrude có bevel, container có chiều sâu thật, địa cầu texture với các cung luồng hàng minh họa, chữ theo spring/frame, đoạn may thực tế và token giá trị. Cung và lượng token chỉ minh họa, không thể hiện dữ liệu định lượng. Không gọi hình học 3D là footage quay thật. Nhạc `motion-score.mp3` được tạo bằng Eleven Music, không tái dùng nền sine ở bản cũ; giọng Nhật Phong Eleven v3 giữ take/receipt/alignment. Một cue máy may liên quan đến hình; khoảng hạ nhạc theo câu “Nhưng khoan”. Không chèn tiếng whoosh ngẫu nhiên mỗi lần cắt.

Chạy ở root dự án:

    python workflows/reference-video/prepare_motion.py --batch videos/<batch>
    python workflows/reference-video/motion_audio.py --batch videos/<batch>

`prepare_motion.py` là adapter cho script thương mại hiện tại: tên phrase cut và hai clip may phải được thay trong source/manifest khi đổi chủ đề, không coi đây là bộ hiểu kịch bản tổng quát. `--skip-media` chỉ cập nhật timing/caption khi giữ take và footage. Không sửa take sau khi đóng timeline mà vẫn dùng timing cũ. Caption không nối câu “Nhưng khoan” vào câu trước chỉ vì nó ngắn. Cue chữ lớn cũng bám thời điểm từ tương ứng.

Chạy ở `workflows/reference-video/cinematic/`:

    npx tsc --noEmit
    npx remotion studio --no-open --port=3191
    npx remotion render src/index.ts Motion3D <absolute-output.mp4> --gl=angle --concurrency=2 --crf=18

Dùng đường dẫn output tuyệt đối. Preview dùng `--scale=0.5` (960×540 chính xác); `0.6666667` làm kích thước 720.000036 và renderer từ chối. Node/Remotion đã pin cùng 4.0.542; chạy npx trong đúng thư mục có package.json, tránh tải nhầm gói `tsc` từ root.

Lỗi thực tế: TextureLoader + setState rồi continueRender ngay có thể capture địa cầu trắng trước khi texture commit. Dùng Fiber useLoader/Suspense để canvas chờ texture trước lần draw. Kiểm tra cả globe ở frame đầu tiên xuất hiện và các frame sau; vẫn phải xem output cuối, không chỉ Studio. QA kỹ thuật/ASR không đồng nghĩa đã nghe thủ công chất giọng hoặc âm nhạc. Trạng thái user_acceptance giữ pending cho đến khi người dùng đánh giá.

Bản kiểm tra cuối dùng motion_qa.py --file <MP4> --out <QA-folder>: giải mã toàn bộ frame và xuất full-duration.jpg, keyframes.jpg, motion-strips.jpg. Các chỉ số delta chỉ xác nhận thay đổi pixel, không chấm điểm chất lượng. Bản final dùng nền kem ở đoạn dòng giá trị để tạo tương phản với globe tối và may màu ấm. Nhìn lại frame sau thay đổi và không dùng sheet preview cũ để ký duyệt final.


## Chốt mẫu đã duyệt — 11/11/2026

Người dùng đã phản hồi “rất ok” cho final của batch cinematic-reset và yêu cầu lưu toàn bộ giọng/sound/style. Các ghi chú pending trước đó là lịch sử trước phản hồi này. Từ nay đọc **APPROVED_BASELINE.md** và **cinematic.profile.json** làm mặc định cho nhánh explainer này. Profile chứa exact voice ID/settings, đường dẫn stem nhạc/hiệu ứng/mix, asset hashes và source snapshot. Giữ bản duyệt nguyên vẹn; chủ đề mới tạo batch mới, căn take mới và thay cảnh/Foley theo nội dung. Chờ người dùng yêu cầu video sau.


## Mở rộng video 5 phút theo yêu cầu tiếp theo

Xem LONGFORM.md và longform.py. Composition WorkAI5min dùng public/longform/ và các module src/longform/, giữ nguyên media và profile đã duyệt của Motion3D 50s. Một take narration mới + exact alignment; kế hoạch nhạc phát triển dài, kiểm tra đủ 300s trước mix. QA phải truyền timeline để đo đủ 9000 frame. Không giữ expectedFrames=1500 cho mọi thời lượng.


## Ưu tiên cao nhất — ảnh internet minh họa sát lời, 12/11/2026

Người dùng đánh giá bản 5 phút quá nhiều 3D và ít ảnh ngoài; đã cấp phép tìm/lấy ảnh internet và yêu cầu thay toàn bộ hướng làm. Đọc REAL_IMAGE_DIRECTION.md và cinematic.profile.json bản cập nhật. Từ nay hình/footage thực có nguồn là chính; 3D chỉ hỗ trợ giải thích. Bộ video này dùng visual_story.py / WorkAIVisual5min. Giữ giọng/âm thanh đã duyệt; không tạo take mới cho một lần sửa hình. Bản gốc và các mẫu cũ được giữ nguyên để đối chiếu, không còn là mặc định hình ảnh.
