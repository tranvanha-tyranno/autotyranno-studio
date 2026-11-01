# Quy trình tạo video sản phẩm của Tyranno

## Ưu tiên mới — 29/10/2026: nhân vật nói khớp miệng theo mẫu Viesnap

Người dùng đưa `viesnap.vn_tiktok_7693215191420456212.mp4` và nhấn mạnh: **phần lớn video phải là nhân vật có khẩu hình hợp lời thoại**. Yêu cầu này ưu tiên hơn mặc định cũ “miệng khép, voice-over”, cảnh cận không thấy mặt và tăng hình 1,5× tách khỏi giọng. Chế độ hands-only/mica được yêu cầu riêng vẫn dùng workflow riêng.

Tham chiếu đã lưu tại `videos/2026-10-29-reference-viesnap/`: bản gốc, ảnh sản phẩm, contact sheet và `inspection/` có 85 mẫu hình cách nhau 0,25s, file audio và hash nguồn. Hình có 634 frame/30fps ≈21,133s; duration container khoảng 21,15s. Khoảng 0–1,5s mở đoạn tình huống; 1,5–7,75s có hành động hài bất ngờ; từ khoảng 7,75s chuyển sang nam nhân vật cầm sản phẩm, nét mặt/miệng và tay tạo nhịp trên khung khá ổn định. Đây là quan sát hình; chưa có transcript hoặc điểm đo lip-sync khách quan. Ghi nhận yêu cầu khớp miệng từ người dùng, không suy ra đã kiểm định lip-sync chỉ nhờ contact sheet.

Học **cú bất ngờ → giới thiệu có lợi ích → chứng minh chi tiết → CTA**, không bê nguyên đoạn phá tường không liên quan, nhân dạng người thật, chữ chèn, viền đen hoặc fade tối. Đưa sản phẩm và hook cụ thể vào 0–3s thay vì dành gần 8s cho tiểu phẩm. Năng lượng đến từ biểu cảm, nhấn giọng và cử chỉ có mục đích; camera vẫn ổn định. Chỉ một cảnh miết vỏ, các cảnh khác thực hiện hành động phục vụ câu đang nói. Không bịa giá/dung lượng/công suất để giật gân.

`prepare_reference_review.py` chuẩn bị hai bản 20s, 5 cảnh có thời lượng 3/3/5/4/5s: 17s `speech_mode: "lip_sync"` với gương mặt/miệng rõ, 3s `voiceover` cận chi tiết. Dùng hai nam nhân vật trưởng thành hư cấu phù hợp giọng Adam; đây là lựa chọn template, không phải yêu cầu mọi sản phẩm đều dùng nam. Mỗi bản vẫn tạo canonical portrait và duyệt trước ảnh cảnh. Khóa sản phẩm ở tư thế gốc, tay đỡ đứng yên; cảnh có mặt cần QA lại vì medium shot từng làm biến dạng sản phẩm. Các prompt mới là **chưa kiểm nghiệm bằng generation**, không gán “đã sửa ổn định” cho lời prompt.

Luồng audio-first:

1. Chốt từng câu thoại → tạo Adam / eleven_v3 → nghe đúng take và căn thời gian, bỏ khoảng lặng theo phép đo nếu cần.
2. Tạo và QA ảnh/nguồn video. `speech_mode: "lip_sync"` bắt buộc `face_visible: true`; không dùng “no speaking”, “lips closed”, crop mất mặt hoặc che miệng.
3. Chạy `python workflows/product-video/talking_review.py --batch <batch>` (có `--clip`, `--scene`). Đây chỉ là xử lý local, không gọi engine hay provider. Nó chốt crop/trim/tốc độ hình, bù sáng và tempo/khoảng lặng giọng **trước** đồng bộ, lưu `scene-XX/speech/video.mp4`, `voice.wav`, `input.json` với hash đầy đủ. Đổi lời/take/timing/nguồn thì dùng revision mới.
4. Đưa đúng `speech/video.mp4` + `speech/voice.wav` qua engine nhận audio điều khiển khẩu hình thực; lưu `speech/synced.mp4`. Chuẩn hóa kết quả 30fps và đủ frame trước khi QA. **API Muse local hiện chỉ nhận prompt/ảnh, không có audio input, và engine lip-sync chưa được kết nối.** Việc prompt “talking” hoặc mux giọng vào hình không giải quyết bước này. Plan ghi chi phí/lần gọi lip-sync chưa xác định, không tính lẫn vào Muse/TTS.
5. Xem/nghe toàn cảnh và so miệng ở đầu/giữa/cuối, chỗ bật môi b/p/m, khoảng dừng và cuối câu; kiểm tra cả mặt, sản phẩm, tay và sáng sau xử lý. Không ghi accepted dựa trên ảnh tĩnh hoặc hash. Lưu `speech/sync-review.json` có `result: "accepted"`, `engine`, `notes`, `mouth_audio_reviewed: true`, `product_face_hands_reviewed: true`, `reviewed_interval_seconds: [0, <seconds>]` cùng `audio_sha256`, `video_sha256`, `synced_sha256`. Đây là QA do agent thực hiện khi thực sự có công cụ xem/nghe; không tự tạo review hợp lệ chỉ để vượt chặn.
6. `run.py render` chỉ nhận cảnh nói có kết quả và review khớp đúng input. Sau đồng bộ giữ tốc độ hình/tiếng 1×, không cắt lại khoảng lặng. Cảnh B-roll vẫn có thể 1,5× độc lập. Kiểm tra final có tiếng và hình trước khi giao.

`reference_style: "viesnap-talking-review-v1"` bật chỉ dẫn kể chuyện trong payload ảnh/video và yêu cầu ít nhất 60% thời lượng có khẩu hình, cảnh hook nói ≤3s, beat/hành động rõ và marketing hook/CTA thật sự nằm trong thoại. Metadata chỉ kiểm tra cấu trúc, không chấm hay bảo đảm độ hấp dẫn/độ khớp. Test dùng hình màu/tiếng sine để kiểm tra timeline, hash và chặn sai trạng thái; **không** phải bằng chứng model tạo khẩu hình tốt. Lưu profile/workflow là học quy trình có thể dùng lại, không phải fine-tune trọng số model.

```powershell
python workflows/product-video/inspect_reference.py --video 'C:\path\reference.mp4' --output videos/new-reference-inspection
python workflows/product-video/prepare_reference_review.py --image 'C:\path\powerbank.png' --output videos/new-talking-review-drafts
# init chỉ chuẩn bị local. Đọc cost-plan và trạng thái engine trước provider stages.
python workflows/product-video/run.py cache --batch videos/new-talking-review-drafts/variant-01
python workflows/product-video/run.py plan --batch videos/new-talking-review-drafts/variant-01
```

Các mặc định dưới đây giữ cho batch cũ và cảnh B-roll; không ghi đè ưu tiên nhân vật nói ở trên.

**Chọn đúng chế độ:** với yêu cầu hộp mica xách tay và bộ prompt 11–20, dùng [mica/WORKFLOW.md](mica/WORKFLOW.md), [bộ prompt nâng cấp](mica/optimized-prompts.md) và [bộ gốc](mica/original-prompts.txt). Đó là chế độ N × 3 ảnh riêng, clip POV 6 giây có hành động từ đầu, mặt hộp luôn hướng camera. Không áp vòng cung rộng/20 giây của chế độ review dưới đây. Tăng tốc 1,5× không tự tạo cảm giác sinh động nếu cảnh gốc gần tĩnh.

Đã chốt ngày 27/10/2026. Lần sau chỉ cần đưa ảnh và yêu cầu tạo video; mặc định tạo **2 clip**, mỗi clip **20 giây**, **9:16, 720 × 1280**, **30 fps**, **hình nhanh 1,5×**. Người dùng thấy bản tốc độ gốc còn chậm: dùng 3 cảnh mới × 10 giây, tăng tốc phần hình 1,5× thành 20 giây. Muốn nhiều hơn thì nói số lượng. Không tự đăng lên TikTok.

- Hình: Muse qua Muse2API local `http://127.0.0.1:18610`. Nếu chưa chạy, dùng `experiments/start-muse2api.ps1`.
- Thoại: ElevenLabs `eleven_v3`, Adam (`pNInz6obpgDQGcFmaJgB`), tiếng Việt. Giữ audio tags trong đầu vào V3. Phong cách gần gũi, nhịp nhanh, hook 3 giây, twist và CTA tự nhiên như người dùng đã chọn. Không thêm claim thiếu căn cứ từ ảnh hoặc thông tin được cung cấp.
- Đổi hook giữa các biến thể: nỗi đau → gây tranh luận nhẹ → tò mò/bất ngờ → lật ngược suy nghĩ → hài hước. Dùng tự nhiên “ê ê ê”, “các dợ”, “mấy ní”, “dữ thần vậy”, nhấn HOA vừa phải và CTA giỏ hàng khi phù hợp. Đọc kịch bản người dùng mới nhất nếu họ đã chốt lời; không tự sửa sang quảng cáo MC.
- Hai biến thể dùng bối cảnh và người mẫu AI trưởng thành khác nhau. Người mẫu không dựa trên một người thật cụ thể; cử chỉ nhỏ tự nhiên, không che sản phẩm. Thoại là voice-over, không yêu cầu khớp môi. Nếu không cần người hoặc phải giữ background ảnh gốc, ưu tiên yêu cầu mới.
- Nếu yêu cầu “chỉ tay, không lộ mặt”, đặt `presentation_mode: "hands_only"` cho từng clip. `presenter` chỉ mô tả bàn tay/cổ tay/ống tay áo người lớn. Ảnh và video tuyệt đối không có đầu, mặt, thân hoặc phản chiếu mặt; kiểm tra cả ảnh mở đầu và các khung cuối. Bàn tay đưa lòng bàn tay hoặc chỉ cạnh bảng điều khiển, không che sản phẩm. Không dùng prompt người mẫu nửa người cho chế độ này.
- Khóa nhận diện sản phẩm: đúng hình dáng, màu, vật liệu, logo, nút, số liệu; không tự thêm chức năng hoặc đánh giá trải nghiệm thật. Bỏ vỏ hộp chỉ khi bố cục review cần thấy sản phẩm rõ và mô tả đủ chính xác.
- Chuyển động: hành động tay rõ từ đầu, có nhịp dừng ngắn tự nhiên rồi xoay sản phẩm nhẹ 5–10° và dùng tay còn lại chạm/miết vỏ. Mặt chính vẫn hướng camera, không xoay trọn mặt sau từ một ảnh. Camera đứng hoặc dịch rất nhỏ, không chạy vòng cung lớn mặc định. Tăng tốc hình khoảng 1,4–1,5× khi phù hợp; không tăng tốc thay cho hành động. Giữ toàn bộ sản phẩm và quai trong khung.
- **Không kéo chậm 10 giây thành 20 giây, không lặp lại cảnh.** Manifest mặc định `visual_speed: 1.5`, `scene_count: 3`. Thoại xử lý tốc độ độc lập, không tự tăng giọng 1,5× theo hình. Batch cũ vẫn hỗ trợ hai cảnh 10 giây ở 1× khi không có trường mới. Nếu tổng nguồn ngắn hơn mục tiêu, tạo thêm cảnh mới theo phạm vi được yêu cầu; không giấu thời lượng thiếu bằng vòng lặp.
- Xuất 30 fps, không nội suy quang học nặng theo mặc định. Chỉ điều chỉnh tốc độ thoại nhẹ nếu cần để giữ đủ lời. Không cắt câu cho vừa video.
- Tiết kiệm chi phí: chạy `plan` trước khi gọi provider. TTS và media Muse được cache theo hash của model, voice, prompt và nội dung ảnh; cùng input sẽ copy local, không gọi lại. Cache không chứa key. Nếu cần bắt buộc tạo biến thể mới, đổi prompt/bối cảnh hoặc tắt cache trong manifest (`cache: {"muse": false, "tts": false}`).
- Phân công xử lý: LLM chỉ nên viết/chỉnh kịch bản, tạo hook/CTA và chuyển mô tả sản phẩm thành prompt khi người dùng chưa cung cấp. Code xử lý hash/cache, crop ảnh, kiểm tra schema, đếm cost, polling task, ghép/cắt/tăng tốc video, âm thanh, QA và xuất file. Không gọi LLM cho việc encode, đo thời lượng, resize, kiểm tra duplicate hay kiểm tra file.
- Kiểm tra ảnh mở đầu trước khi sinh video; kiểm tra contact sheet sau mỗi cảnh và file cuối. Ghi lại thiếu sót hoặc sửa biến thể lỗi; không tuyên bố giữ đúng tuyệt đối hay tránh vi phạm chỉ vì thay người/background.

## Bài học đã đưa vào code — 28/10/2026

**Yêu cầu marketing luôn áp dụng:** đưa thông tin bất ngờ/giá trị cụ thể hoặc cú lật nhận diện ngay 0–3 giây. Người dùng đã chê “Pin đỏ đúng lúc cần?” là yếu; chỉ có câu hỏi nỗi đau và chữ “hook” trong manifest không chứng minh hook tốt. Ví dụ ấm inox “mấy chục cành…” là cách dẫn bằng giá trị, chỉ được dùng nếu giá bán áp dụng đã kiểm chứng. Tiếp theo phát triển lợi ích, chi tiết có nguồn, rồi CTA chốt đơn bằng lời. Không mở đầu dài hoặc bịa trải nghiệm, khan hiếm, giá/giảm giá. `marketing.hook` phải mở đầu lời cảnh một; `marketing.cta` phải kết thúc lời cuối. QA vẫn phải nghe/đánh giá sức hút thực tế, không chỉ dựa validation.

**KHÔNG CHÈN CHỮ:** mặc định `text_overlays: false`. Không subtitle, hook/spec/CTA card, watermark hoặc chữ nền do AI tự vẽ. Giữ chữ/số vốn có trên sản phẩm như trong ảnh gốc. Trường `on_screen` chỉ còn dùng nếu một yêu cầu sau explicitly bật lại chữ; schema có sẵn không phải phép thêm chữ.

**Chuẩn nhân vật trước cảnh:** khai báo `character.prompt`, chạy `characters`, xem `character/portrait.png` và lưu `portrait-review.json` với hash trước khi chạy `images`. Ảnh chân dung nhân vật trưởng thành hư cấu phải tách khỏi sản phẩm, thấy rõ mặt, tóc và trang phục trong ánh sáng đều. Mọi ảnh cảnh dùng sản phẩm + chân dung chuẩn; mọi video dùng ảnh mở đầu + sản phẩm + chân dung chuẩn. Không lấy ảnh cảnh đầu làm chuẩn mặt một cách mặc định khi người dùng đã yêu cầu chuẩn riêng.

**Ánh sáng và nhịp hành động:** khóa exposure/white balance, dùng nguồn sáng tán đều cố định, tránh đổi góc camera khiến nền/cửa sổ làm hình tối dần. Mỗi cảnh có mốc: đưa sản phẩm từ đầu → dừng khoảng 0,3–0,7s → xoay nhẹ 5–10° → tay kia chạm/miết mặt vỏ không che màn hình → trở về tư thế. Không cấm chạm hoặc cấm mọi xoay trong prompt rồi hy vọng model làm đúng yêu cầu mới. Không dùng loop/freeze-frame để tạo nhịp dừng.

Với cảnh cận cầm ngang, “xoay nhẹ” vẫn có thể bị model hiểu thành dựng đứng/lật sản phẩm. Cần khóa vị trí tương đối cụ thể (ô đen dưới-phải, quai trên-phải như ảnh mở đầu), cạnh nào gần camera, tay đỡ/cổ tay không đổi grip; chỉ cho nghiêng theo chiều sâu 3–5° khi cần. Nếu ô đen biến xám, quai nhân đôi hoặc xoay lật thì QA loại nguồn đó, đơn giản hóa riêng cảnh, giữ lần thử và task ID. Không ghi “accepted” chỉ vì có chạm vỏ.

`quality.lock_exposure` thêm yêu cầu ánh sáng vào prompt; `quality.exposure_lock` đo độ sáng ROI so với ảnh mở đầu và tạo hiệu chỉnh luma nội suy có giới hạn, lưu `exposure-plan.json`. Có thể bị ảnh hưởng bởi đổi bố cục, không coi thống kê trung bình là phép đo riêng da/sản phẩm. Xem khung đầu/giữa/cuối và so lại vùng sản phẩm, tránh tăng sáng quá mức. `quality.require_video_review` bắt buộc kết quả QA motion khớp SHA-256 trước render.

Hiệu chỉnh mặc định chỉ bù sáng (`allow_dimming: false`); không tự hạ sáng cảnh vốn sáng chỉ để ép mean ROI trùng ảnh mở đầu. Bố cục sáng hơn không phải lỗi cần làm tối đi. Chỉ bật bù hai chiều cho một yêu cầu grading cụ thể và có QA.

Video review dài hơn 30 giây hoặc cần đổi cảnh nên dùng schema `clips[].scenes` trong `run.py` và module `storyboard.py`. Mỗi cảnh có `seconds`, `dialogue`, `opening_prompt`, `video_prompt`, tùy chọn `visual_speed` và `source_start`. Tổng `seconds` phải bằng `duration_seconds`; phần nguồn dùng cho mỗi cảnh không vượt 10 giây. `clip.dialogue` phải đúng phép nối các thoại cảnh bằng hai newline. Runner cũ vẫn chạy manifest không có `scenes`.

- Tạo ảnh mở đầu riêng cho từng cảnh với cùng chân dung chuẩn đã duyệt. Khi ảnh gốc là collage nhiều màu, chọn một crop sản phẩm làm tham chiếu chính, giữ toàn bộ ảnh gốc trong `input/`.
- Với sản phẩm có khe, nhãn, màn hình hoặc cổng nhỏ, giới hạn xoay khoảng 5–10° đủ thấy hành động nhưng giữ mặt chính và thiết kế. Không mặc định xoay 25–45°: video mũ đã chứng minh góc xoay lớn làm AI thay đổi khe/vân. Tay kia phải chạm thực sự khi kịch bản demo yêu cầu.
- Video dùng hai tham chiếu theo thứ tự: ảnh mở đầu rồi ảnh sản phẩm gốc/crop. Không suy diễn mặt sau hoặc thêm cổng/cáp/tính năng. Upload được chuẩn hóa thành PNG thật trong bộ nhớ, tránh WebP mang đuôi `.png`; giữ file tải về nguyên trạng.
- Nếu ảnh cận không có mặt, AI có thể mở rộng khung và tự tạo nhân vật khác. Cảnh đó có thể thêm `presenter_reference` (đường dẫn ảnh nhân vật trong batch) làm tham chiếu thứ ba, yêu cầu giữ tóc/trang phục gốc và khóa camera vào sản phẩm. `revision: 2` dùng thư mục `scene-XX-r02`, giữ nguyên lần đầu và task ID; chỉ gọi lại cảnh đã bị QA loại, không tự lặp retry.
- Trường `extra` giải quyết yêu cầu xóa chữ mặc định của Muse: chỉ loại overlay/watermark thêm vào, giữ nhãn gốc và chi tiết màn hình. Không hứa chữ nhỏ đúng tuyệt đối.
- Sau khi xem ảnh, lưu `scene-XX/opening-review.json` chứa `result: "accepted"`, `sha256` ảnh hiện tại và `notes`. Runner chặn tạo video nếu thiếu hoặc hash thay đổi. Đây là bước QA do agent thực hiện, không phải yêu cầu người dùng xác nhận.
- TTS từng cảnh được cache và căn riêng vào timeline, giữ âm thanh độc lập tốc độ hình. Không dùng mốc tách giọng hard-code từ batch trước. Nếu đoạn quá dài trên 1,25× thì sửa riêng lời cảnh đó hoặc phân bổ lại thời lượng; không cắt mất lời.
- Nếu giọng có khoảng lặng dài đã đo, `audio_segments` giữ các vùng có lời cùng biên an toàn để bỏ riêng khoảng lặng và phần dư cuối; luôn giữ file giọng gốc và ghi mốc silence/QA. Không mang mốc này sang batch hoặc bản TTS khác; template tái dùng không chứa mốc cắt đo từ một take cụ thể.
- `cache`, `plan`, `images`, `voices`, `videos`, `render`, `status` và `--scene` dùng cho cả storyboard. Plan đếm toàn bộ ảnh/giọng/video theo cảnh, nhận biết task đã gửi; không POST lại tự động khi task lỗi hoặc kết quả chưa rõ.
- Kiểm tra thông số sản phẩm trên internet khi người dùng yêu cầu. Lưu nguồn, mức chắc chắn và claim được dùng vào batch. Ảnh giống mẫu không đủ xác nhận dung lượng/công suất của chiếc đang bán. Nếu nguồn mâu thuẫn, viết rõ “theo nhà cung cấp/tùy phiên bản”, bỏ claim không xác minh, tiếp tục kịch bản hữu ích với thiết kế thấy được.
- Render kiểm tra toàn bộ giải mã, âm lượng, đoạn đen/đứng hình, xuất contact sheet bao trùm toàn thời lượng và ảnh cuối. Dùng `scale` + `pad` thay vì crop tự động mất mép; vẫn phải xem QA vì AI có thể tự đẩy sản phẩm ra khung.

Ví dụ tạo một video 40 giây: 6 cảnh × 6,6667 giây từ 6 nguồn 10 giây ở 1,5×. Thư mục mỗi cảnh giữ ảnh, prompt, thoại, task ID, nguồn video và nhận xét QA. Mọi lần sửa có nguyên nhân và phạm vi cụ thể; không lặp sinh vô hạn.

## Thư mục và cách chạy

`run.py` nhận manifest, không hard-code sản phẩm. Mỗi batch:

```
videos/<batch-name>/
  batch.json
  input/                         ảnh gốc và crop nếu có
  clip-01-.../
    dialogue.txt
    opening-prompt.txt
    opening.png
    scene-01-prompt.txt
    scene-01.mp4
    scene-02-prompt.txt
    scene-02.mp4
    scene-03-prompt.txt
    scene-03.mp4
    voice.mp3
    final.mp4
    contact-sheet.jpg
    verification.json
  clip-02-.../
    ...
```

Agent đọc ảnh mới, viết manifest dựa trên thông tin sản phẩm, hai kịch bản khác nhau và hai người mẫu/bối cảnh. Không tái dùng các claim Coco Bear cho sản phẩm khác. Tham khảo `example-cocobear.json` cho cấu trúc có người mẫu; `example-cocobear-hands-fast.json` cho bản chỉ tay nhịp nhanh. `init` chụp bản sao ảnh và config vào batch mới; không ghi đè batch có sẵn. Tạo batch khác cho một lần thử mới; các bước sau có thể resume trong đúng batch.

```powershell
python workflows/product-video/run.py init --config workflows/product-video/example-cocobear.json --image 'C:\path\product.png' --output videos/my-product-batch
python workflows/product-video/run.py cache --batch videos/my-product-batch # index old local artifacts; no provider call
python workflows/product-video/run.py plan --batch videos/my-product-batch
python workflows/product-video/run.py characters --batch videos/my-product-batch # nếu có character
# Xem chân dung chuẩn và lưu portrait-review.json trước images.
python workflows/product-video/run.py voices --batch videos/my-product-batch
python workflows/product-video/run.py images --batch videos/my-product-batch
# Xem ảnh mở đầu trước bước videos.
python workflows/product-video/run.py videos --batch videos/my-product-batch
# Xem contact sheet cảnh gốc trước bước render.
python workflows/product-video/run.py render --batch videos/my-product-batch
python workflows/product-video/run.py status --batch videos/my-product-batch
```

Thêm `--clip 1` hoặc `--clip 2` để xử lý riêng; `--scene 1`, `2`, `3` cho từng cảnh. Các yêu cầu Muse được gửi tuần tự vì cấu hình hiện có một worker; có thể chạy TTS độc lập với hình. Script lưu task ID trước polling và resume đúng task, không POST lặp. Nếu task thất bại thì dừng, kiểm tra nguyên nhân và quyết định sửa; không tự gọi lặp vô hạn.

`plan` ghi `cost-plan.json`. Con số là số lần gọi provider dự kiến theo file hiện tại; giá tiền thật phụ thuộc tài khoản/model/provider nên không hard-code trong runner. Nếu mọi đầu vào đã có trong cache, plan sẽ báo 0 call và chỉ còn bước xử lý local.

API ElevenLabs đọc từ biến `ELEVENLABS_API_KEY`, nếu không có thì đọc khóa đã mã hóa bằng Windows DPAPI trong `.secrets/elevenlabs.dpapi.xml` ở project này. Chỉ tài khoản Windows hiện tại giải mã được. Không đưa khóa vào manifest, skill, prompt hoặc log. Muse dùng key `.env` cục bộ đã có. Khóa bị thu hồi hoặc thiếu quota cần thông báo đúng lỗi, không thay dịch vụ âm thầm.

Khi hoàn thành, trả cả hai video inline và đường dẫn batch, nêu rõ số kịch bản, bối cảnh, thời lượng và các hạn chế có ảnh hưởng. Thông báo trong chat này khi xong; không gửi sang ứng dụng khác hoặc tạo automation nếu người dùng chỉ muốn báo khi tác vụ hiện tại hoàn tất.

**28/10/2026 — sửa xung đột prompt xóa chữ của Muse:** chỉ thêm lời giữ nhãn bằng tiếng Anh vào `extra` vẫn có thể khiến provider dừng để hỏi, vì lớp dịch vụ tự chèn câu tiếng Trung “xóa mọi chữ”. `PRODUCT_LOCK` nay ghi rõ bằng tiếng Trung rằng quy tắc cuối ghi đè câu template đó: chỉ xóa overlay, giữ nguyên số/nhãn gốc trên sản phẩm và trực tiếp tạo ảnh. Giữ task đã lỗi, chuyển revision riêng cho cảnh đó; dùng cache cho giọng cùng nội dung, không gọi lại toàn batch.

**28/10/2026 — pose ảnh mở đầu:** mô tả “mặt trước hướng camera” vẫn có thể sinh cảnh dựng đứng và kéo dài thân ở ảnh medium/CTA. Khóa tư thế ngay trong prompt ảnh của TẤT CẢ cảnh: thân thấp, nằm trên lòng bàn tay theo góc chéo gốc, ô đen dưới-phải, quai trên-phải, giữ tỷ lệ thân bo ngắn. Không chỉ khóa trong video hoặc cảnh cận. `prepare_powerbank_variants.py` chuẩn bị hai bản 20s với hai chân dung riêng; không tự gọi provider. QA loại ảnh sai dáng trước khi tốn lượt video.

**28/10/2026 — kiểm tra chuyển động bản mới:** prompt tiếng Anh dài có timeline vẫn sinh dựng đứng/xoay nhiều lần và ô đen hóa xám dù có chạm thật. Không duyệt nguồn chỉ vì có chạm. `prepare_powerbank_variants.locked_video_prompt()` dùng brief ngắn tiếng Trung khóa đúng ảnh mở đầu, cùng tay đỡ/grip, chỉ nghiêng theo chiều sâu 3°, một lượt miết vỏ. Nếu nguồn hỏng, giữ task/source/review, tăng revision riêng video và tái dùng ảnh đã duyệt + TTS cache. Không lặp retry nếu biến thể rút gọn vẫn hỏng nghiêm trọng.

**28/10/2026 — kết quả xác minh tiếp theo (ưu tiên hơn giả thuyết trước):** brief tiếng Trung rút gọn vẫn dựng đứng sản phẩm trong cảnh medium; không coi là cách sửa đã thành công. Dừng lặp kiểu pose đó, dùng cảnh cận thật sự (crop ảnh cảnh đã có product + canonical reference) và brief CRADLED HORIZONTALLY từng thành công; `prepare_powerbank_closeups.py` lưu crop/provenance và tái dùng hai nguồn đã duyệt với cùng sản phẩm, không gán nhầm là sinh mới. Chỉ mở rộng provider sau khi xem cảnh cận thử.

**24 fps QA:** Muse trả nguồn 10s/24fps, frame cuối ở 9,9583s; seek cứng 9,96s trả rỗng. `quality.exposure_plan` nay lấy mẫu cuối trong 100ms trước kết thúc (9,9s), có regression test full ten-second 24fps. Không bỏ QA sáng chỉ vì lệch seek.

**28/10/2026 — kết quả cuối batch hai bản 20s:** bố cục cận từ ảnh cảnh đã tạo bằng product + canonical portrait, kết hợp brief CRADLED HORIZONTALLY, đã giữ tư thế chéo/ô đen và có miết vỏ ở 4 nguồn mới được duyệt. Hai nguồn cận cũ được xem lại và tái dùng có provenance; tổng 6 nguồn khác nhau trong hai final, không lặp/kéo chậm. Không khẳng định đổi ngôn ngữ prompt là nguyên nhân sửa được; thay đổi có hiệu quả là bố cục cận + tay đỡ đứng yên + brief từng được QA. `prepare_powerbank_variants.py` nay mặc định prompt cận và free-hand-first, `prepare_powerbank_closeups.py` giữ crop/provenance cho batch hiện có. Final phải xem sau bù sáng: ROI cuối/ảnh mở đầu ở bản 2 sau xử lý khoảng 0,98–1,02, nhưng vẫn đánh giá da/sản phẩm trực tiếp vì AI có nới khung. Chữ số nhỏ thay đổi, đôi lúc ngón tay gần viền ô đen và miệng cử động; công bố giới hạn, không quảng cáo giữ tuyệt đối.

**28/10/2026 — phản hồi tăng thuyết phục:** bản 20s chỉ nói ngoại hình/chạm vỏ chưa đủ lý do mua sạc. Khi được yêu cầu làm dài, dùng mạch 6 cảnh/40s: hook giá trị cụ thể → tình huống cần nguồn pin → thiết kế → kiểm tra mức pin → chọn đúng phiên bản/điện thoại → CTA. Thêm cảnh điện thoại/đồ mang đi nhưng không bịa dây, cổng hoặc animation đang sạc từ một ảnh. `prepare_powerbank_sales.py` chuẩn bị hai script/canonical identity riêng, tái dùng 3 nguồn được duyệt và tạo 3 nguồn ngữ cảnh mới mỗi bản. Hạn chế một cảnh chỉ để gỡ băn khoăn phiên bản; đừng biến toàn quảng cáo thành lời cảnh báo. Listing khớp ngoại hình vẫn không phải thông số exact unit.

**Bù sáng và ô đen:** `quality.exposure_filters` hỗ trợ `preserve_blacks`: mask theo luma nguồn giữ nguyên vùng tối dưới shadow floor, chuyển mềm sang vùng bù sáng, giữ chroma gốc. Không dùng cộng sáng toàn ảnh để làm xám ô đen. Test ảnh nửa đen/nửa xám xác nhận nâng vùng sáng mà không nâng vùng đen; vẫn xem da/vỏ/ô đen ở final thực tế.

**Ổn định bằng biên tập có kiểm tra:** nếu chỉ đuôi nguồn bị mất số/ô đen đổi, có thể dùng riêng khoảng tốt đã xem, tăng tốc 1,3–1,5× đủ thời lượng, không lặp/kéo chậm. Lưu `video-review.json.reviewed_interval_seconds`; `storyboard.render` chặn nếu khoảng lấy vượt phần được duyệt, có regression test. Không coi trim là sửa phần hỏng, luôn giữ nguồn đầy đủ và nêu đoạn bị bỏ. `audio_timing.py` đo khoảng lặng của đúng take, chỉ bỏ phần giữa của pause >0,36s với guard 0,12s hai đầu; giữ file giọng gốc/hash và không tái dùng mốc cho take khác. `review_final.py` tạo so ảnh mở đầu/nguồn cuối/phần đầu–giữa–cuối final của từng cảnh; chỉ tạo sheet/metrics, không auto-approve chất lượng hình.

**29/10/2026 — QA bàn tay phải phóng lớn:** sheet 20 ô thu nhỏ có thể che lỗi bàn tay thứ ba ở giữa cảnh. Với cảnh có tay nghỉ trên bàn, khóa rõ chỉ đúng HAI tay: tay đỡ giữ grip; tay đang trên bàn di chuyển liên tục lên vỏ, chỗ trên bàn phải trống, rồi chính tay đó trở lại. Một cảnh đã được duyệt tạm phải đổi sang rejected nếu audit phóng lớn phát hiện lỗi; giữ bản render cũ dưới tên draft, không giao. `review_final.py` nay xuất thêm `source-detail-review.jpg` ở 25/50/75% của phần nguồn được dùng, bên cạnh sheet toàn thời lượng. Không khẳng định prompt “two hands” tự bảo đảm anatomy, vẫn xem nguồn thật.

**24fps → 30fps đủ hình/tiếng:** `fps=30` mặc định làm mất một frame cuối mỗi scene 10s/24fps sau 1,5×; sáu scene chỉ còn 1194 frame dù audio báo 40s. `fps=30:eof_action=pass` giữ endpoint của nguồn (không thêm loop/pad) cho đủ 1200 frame/40s. Render đếm video_frame_count sau giải mã và chặn nếu lệch timeline; regression test 240 frame nguồn → 200 frame ở 1,5×. Không dùng duration container có audio để kết luận hình đủ thời lượng.
