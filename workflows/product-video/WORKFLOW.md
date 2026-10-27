# Quy trình tạo video sản phẩm của Tyranno

**Chọn đúng chế độ:** với yêu cầu hộp mica xách tay và bộ prompt 11–20, dùng [mica/WORKFLOW.md](mica/WORKFLOW.md), [bộ prompt nâng cấp](mica/optimized-prompts.md) và [bộ gốc](mica/original-prompts.txt). Đó là chế độ N × 3 ảnh riêng, clip POV 6 giây có hành động từ đầu, mặt hộp luôn hướng camera. Không áp vòng cung rộng/20 giây của chế độ review dưới đây. Tăng tốc 1,5× không tự tạo cảm giác sinh động nếu cảnh gốc gần tĩnh.

Đã chốt ngày 27/10/2026. Lần sau chỉ cần đưa ảnh và yêu cầu tạo video; mặc định tạo **2 clip**, mỗi clip **20 giây**, **9:16, 720 × 1280**, **30 fps**, **hình nhanh 1,5×**. Người dùng thấy bản tốc độ gốc còn chậm: dùng 3 cảnh mới × 10 giây, tăng tốc phần hình 1,5× thành 20 giây. Muốn nhiều hơn thì nói số lượng. Không tự đăng lên TikTok.

- Hình: Muse qua Muse2API local `http://127.0.0.1:18610`. Nếu chưa chạy, dùng `experiments/start-muse2api.ps1`.
- Thoại: ElevenLabs `eleven_v3`, Adam (`pNInz6obpgDQGcFmaJgB`), tiếng Việt. Giữ audio tags trong đầu vào V3. Phong cách gần gũi, nhịp nhanh, hook 3 giây, twist và CTA tự nhiên như người dùng đã chọn. Không thêm claim thiếu căn cứ từ ảnh hoặc thông tin được cung cấp.
- Đổi hook giữa các biến thể: nỗi đau → gây tranh luận nhẹ → tò mò/bất ngờ → lật ngược suy nghĩ → hài hước. Dùng tự nhiên “ê ê ê”, “các dợ”, “mấy ní”, “dữ thần vậy”, nhấn HOA vừa phải và CTA giỏ hàng khi phù hợp. Đọc kịch bản người dùng mới nhất nếu họ đã chốt lời; không tự sửa sang quảng cáo MC.
- Hai biến thể dùng bối cảnh và người mẫu AI trưởng thành khác nhau. Người mẫu không dựa trên một người thật cụ thể; cử chỉ nhỏ tự nhiên, không che sản phẩm. Thoại là voice-over, không yêu cầu khớp môi. Nếu không cần người hoặc phải giữ background ảnh gốc, ưu tiên yêu cầu mới.
- Nếu yêu cầu “chỉ tay, không lộ mặt”, đặt `presentation_mode: "hands_only"` cho từng clip. `presenter` chỉ mô tả bàn tay/cổ tay/ống tay áo người lớn. Ảnh và video tuyệt đối không có đầu, mặt, thân hoặc phản chiếu mặt; kiểm tra cả ảnh mở đầu và các khung cuối. Bàn tay đưa lòng bàn tay hoặc chỉ cạnh bảng điều khiển, không che sản phẩm. Không dùng prompt người mẫu nửa người cho chế độ này.
- Khóa nhận diện sản phẩm: đúng hình dáng, màu, vật liệu, logo, nút, số liệu; không tự thêm chức năng hoặc đánh giá trải nghiệm thật. Bỏ vỏ hộp chỉ khi bố cục review cần thấy sản phẩm rõ và mô tả đủ chính xác.
- Chuyển động: vòng cung rõ, mượt khoảng 25–45° mỗi cảnh nguồn 10 giây, phát hình nhanh 1,5× để có nhịp sinh động. Ba cảnh đổi hướng/cao độ, cắt khoảng 6–7 giây/lần. Camera luôn bám tâm sản phẩm, giữ trọn đáy, nắp và tay cầm trong khung; góc vừa đủ và quay rộng tốt hơn xoay quá xa làm cắt mất hàng. Người mẫu đứng yên ở nền, không chuyển focus sang mặt. Không xoay trọn mặt sau từ một ảnh. Các mặt không có ảnh tham chiếu là AI suy diễn.
- **Không kéo chậm 10 giây thành 20 giây, không lặp lại cảnh.** Manifest mặc định `visual_speed: 1.5`, `scene_count: 3`. Thoại xử lý tốc độ độc lập, không tự tăng giọng 1,5× theo hình. Batch cũ vẫn hỗ trợ hai cảnh 10 giây ở 1× khi không có trường mới. Nếu tổng nguồn ngắn hơn mục tiêu, tạo thêm cảnh mới theo phạm vi được yêu cầu; không giấu thời lượng thiếu bằng vòng lặp.
- Xuất 30 fps, không nội suy quang học nặng theo mặc định. Chỉ điều chỉnh tốc độ thoại nhẹ nếu cần để giữ đủ lời. Không cắt câu cho vừa video.
- Tiết kiệm chi phí: chạy `plan` trước khi gọi provider. TTS và media Muse được cache theo hash của model, voice, prompt và nội dung ảnh; cùng input sẽ copy local, không gọi lại. Cache không chứa key. Nếu cần bắt buộc tạo biến thể mới, đổi prompt/bối cảnh hoặc tắt cache trong manifest (`cache: {"muse": false, "tts": false}`).
- Phân công xử lý: LLM chỉ nên viết/chỉnh kịch bản, tạo hook/CTA và chuyển mô tả sản phẩm thành prompt khi người dùng chưa cung cấp. Code xử lý hash/cache, crop ảnh, kiểm tra schema, đếm cost, polling task, ghép/cắt/tăng tốc video, âm thanh, QA và xuất file. Không gọi LLM cho việc encode, đo thời lượng, resize, kiểm tra duplicate hay kiểm tra file.
- Kiểm tra ảnh mở đầu trước khi sinh video; kiểm tra contact sheet sau mỗi cảnh và file cuối. Ghi lại thiếu sót hoặc sửa biến thể lỗi; không tuyên bố giữ đúng tuyệt đối hay tránh vi phạm chỉ vì thay người/background.

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
