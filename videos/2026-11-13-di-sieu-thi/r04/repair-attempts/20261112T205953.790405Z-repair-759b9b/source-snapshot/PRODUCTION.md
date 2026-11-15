# Sản xuất explainer bằng nguồn riêng và vòng kiểm tra có thể dùng lại

`production.py` là lớp chuẩn bị nội dung và điều phối mới. Nó dùng giao diện ảnh/gallery 3D hiện có trong `cinematic/src/directions/`, giữ giọng Nhật Phong đã chốt, chuẩn bị tài sản trong từng batch riêng và gọi renderer tuần tự. Đây không phải công cụ tự chứng nhận ảnh khớp lời hoặc tự huấn luyện mô hình.

Đọc `REFERENCE_LEARNING.md` và `docs/video-references/2026-11-13-user-samples/PLAYBOOK.md` trước khi viết. Hai hướng Lóng/The Hidden Self vẫn có cấu hình giao diện riêng; nghiên cứu bốn mẫu ngày 13/11 chỉ bổ sung hướng Lóng.

## Đầu vào và thư mục

Mỗi đề tài có một manifest mới và thư mục riêng, ví dụ:

```text
videos/new-original-topic/
  production.json
  research/
  long/
    assets/                         nguồn đã tải, giữ nguyên
    audio/narration-original.mp3    take mới và alignment/receipt
    production-manifest.json        snapshot nội dung
    data.json, props.json            timeline cho renderer cũ
    image-sources.json               nguồn, hash, quan sát thực tế
    render-assets.json               bản dùng render và hash
    preflight.json                   kiểm máy; người dùng vẫn chưa duyệt
    final.mp4, qa/
  production-public/directions/long/ tài sản render riêng batch
  render-attempts/                   log và snapshot từng lần xuất
```

`--batch` là thư mục gốc của đề tài, không phải thư mục `long/`. Tài sản `assets[].file` tương đối với vị trí manifest; ví dụ `long/assets/basket.jpg`. Nếu tài sản đã ở đúng thư mục đích thì không sao chép đè lên chính nó. Không thay file của batch cũ.

## Manifest

```json
{
  "schema": "reference-video-production/1",
  "id": "new-original-topic",
  "direction": "long",
  "title": "Một câu hỏi đời sống cụ thể",
  "editorialAngle": "Trục nhân quả duy nhất của bài",
  "audience": "Nhu cầu người xem được suy luận, không giả làm analytics",
  "hookPromise": "Câu hỏi hook hứa trả lời",
  "payoff": "Câu trả lời và điều kiện sẽ rút ra cuối bài",
  "researchSources": [
    {"id": "source-one", "url": "https://example.org/original-source", "scope": "Phạm vi nguồn hỗ trợ"}
  ],
  "claims": [
    {"id": "claim-one", "text": "Mệnh đề cần kiểm chứng", "sourceIds": ["source-one"], "scope": "Đúng nhóm/ngày/đơn vị", "limitations": "Điều chưa suy ra được"}
  ],
  "assets": [
    {
      "id": "basket",
      "file": "long/assets/basket.jpg",
      "sha256": "HASH_CUA_FILE_THAT",
      "source": {
        "kind": "stock",
        "url": "https://example.org/photo-page",
        "creator": "Tác giả",
        "license": "Giấy phép thực tế",
        "licenseURL": "https://example.org/license"
      },
      "observed": {
        "subject": "Chủ thể đã thấy trong file",
        "action": "Hành động hoặc trạng thái thực sự thấy",
        "objects": "Các vật liên quan",
        "limits": "Điều hình này không chứng minh"
      },
      "inspection": {
        "status": "inspected",
        "reviewer": "Người hoặc agent đã mở file",
        "sha256": "HASH_CUA_FILE_THAT",
        "observations": "Quan sát thật sau khi mở ảnh/clip"
      },
      "crop": [0, 0, 1, 1],
      "focus": [50, 50]
    }
  ],
  "sections": [
    {
      "phase": "hook",
      "text": "Một câu mở đầu cụ thể.",
      "shots": [
        {
          "id": "hook-one",
          "phrase": "Một câu",
          "narrationClause": "Một câu mở đầu cụ thể.",
          "needToSee": "Điều khán giả cần nhìn để hiểu thêm",
          "mediaRole": "context",
          "supports": "Quan hệ nào được hình hỗ trợ",
          "limits": "Không gán hành vi hoặc số liệu ngoài hình",
          "layout": "full",
          "images": ["basket"],
          "headline": "Chữ ngắn nếu cần",
          "review": {
            "status": "inspected",
            "reviewer": "Người hoặc agent đã đối chiếu câu với tài sản",
            "observations": "Quan sát về sự khớp và giới hạn",
            "assetHashes": {"basket": "HASH_CUA_FILE_THAT"}
          }
        }
      ]
    }
  ]
}
```

Ví dụ trên chỉ minh họa schema, chưa đủ bốn phần để chạy. `sections` bắt buộc theo đúng thứ tự `hook`, `disclaimer`, `content`, `cta`. Ghép `narrationClause` của các shot phải bằng toàn bộ `section.text`, đủ từ một lần và đúng thứ tự. `phrase` phải là những từ đầu của chính clause đó; công cụ không tìm một cụm giống nhau ở đoạn xa hơn rồi âm thầm dịch cut.

`mediaRole` là `evidence`, `context`, `mechanism` hoặc `metaphor`. Nếu là `evidence`, ít nhất một tài sản phải có `source.kind: evidence`, có `sourceIds` trỏ tới `researchSources`. Stock có thể tạo bối cảnh; nó không thể chứng minh một vụ việc hay số liệu cụ thể. Mọi claim khai báo phải có nguồn, phạm vi và giới hạn.

`layout` chọn giao diện đã giữ: `full`, `diptych`, `gallery3d`, `evidence`, `closing`; thêm `graphic` cho ví dụ/sơ đồ gốc cần xem trọn ảnh, có nhãn minh họa rõ. Graphic là cảnh giải thích ngắn trong tổng thể ảnh thật, không dùng để quay lại bảng/email/dashboard dày chữ. Diptych/gallery cần tối thiểu hai ảnh khác nhau. Dữ liệu quan sát và nhận xét không xuất hiện thành chữ trong video; chỉ `headline`, `eyebrow`, `body`, `sourceNote` là thông tin hiển thị nếu khai báo. Chúng phải ngắn, đúng nghĩa lời và được kiểm sau render.

`source.kind: original` dùng cho tài sản tự tạo, có thể dùng URI ghi nhận nội bộ thay cho URL web. Vẫn phải ghi tác giả, quyền sử dụng, quan sát và hash. Không ghi “đã kiểm” chỉ vì tên file hoặc prompt trùng chủ đề.

## Ảnh và clip thật

Ảnh được giữ nguyên; compiler tạo JPEG riêng, EXIF transpose, crop theo `[left, top, right, bottom]` chuẩn hóa 0–1 và thu trong khung 2048×1280. `focus` là điểm trọng tâm sau crop, tính theo phần trăm. Source inspection chưa thay việc kiểm crop trong MP4 đã render.

Clip MP4 thêm:

```json
{
  "mediaType": "video",
  "trimBeforeFrames": 0,
  "availableFrames": 360,
  "posterFile": "long/assets/clip-poster.jpg",
  "posterSHA256": "HASH_POSTER"
}
```

Tất cả số frame trên là đơn vị của composition 30 fps. Compiler đếm frame giải mã thực, lấy FPS nguồn để tính thời lượng tương đương, từ chối khai báo dài hơn nguồn hoặc shot không đủ thời gian. Renderer cũ chồng bảy frame chuyển cảnh nên clip trước cảnh cuối phải đủ cả phần chồng. Clip không được loop/freeze để lấp lời. Nên chuẩn hóa riêng bản clip 720p/30 fps trước khi catalog; compiler chỉ chấp nhận MP4 tối đa 2048×1280. Âm thanh native của stock được tắt trong renderer để không đè lời.

Gallery dùng poster tĩnh, nên clip trong `gallery3d` bắt buộc có `posterFile` và `posterSHA256`; poster được thu nhỏ và kiểm hash riêng. Ảnh di chuyển hoặc poster không được gọi thành footage động.

## Các lệnh

Từ thư mục dự án, thay đường dẫn bằng batch thật:

```powershell
python workflows/reference-video/production.py plan --manifest videos/new-original-topic/production.json --batch videos/new-original-topic
python workflows/reference-video/production.py check --manifest videos/new-original-topic/production.json --batch videos/new-original-topic
python workflows/reference-video/production.py voice --manifest videos/new-original-topic/production.json --batch videos/new-original-topic
python workflows/reference-video/production.py prepare --manifest videos/new-original-topic/production.json --batch videos/new-original-topic
python workflows/reference-video/production.py mix --manifest videos/new-original-topic/production.json --batch videos/new-original-topic
python workflows/reference-video/production.py render --manifest videos/new-original-topic/production.json --batch videos/new-original-topic
```

- `plan`: kiểm khung viết và coverage của clause, lưu snapshot/script/preset. Manifest khác snapshot đã có phải sang revision/batch mới; không tự ghi đè nội dung cũ.
- `check`: kiểm file, hash, nguồn, quyền, bản ghi mở file thật, notes đối chiếu từng câu và asset hash. Trạng thái pending sẽ dừng. Đây chỉ xác nhận hồ sơ đầy đủ và nhất quán, không chứng minh nhận xét của người kiểm đúng.
- `voice`: gọi helper ElevenLabs hiện có, giọng Nhật Phong / `eleven_v3` / `vi`, speed 1.0, stability 0.5, similarity 0.8. Cache/receipt tránh gọi lại cùng request; intent chưa hòa giải ngăn gọi trùng sau lỗi mạng.
- `prepare`: chỉ dùng take/receipt đúng script và preset, kiểm toàn bộ từ, lấy cut từ điểm đầu từng clause, giữ câu cuối và ít nhất một giây đệm. Ghi timeline/nguồn/bản render riêng cho batch. Không thay tốc độ giọng.
- `mix`: chỉ dùng nhạc và cue được chỉ rõ, có hash; ưu tiên lời, duck nhạc. Không tự dùng tiếng máy may, bàn phím hoặc âm thanh đề tài khác. Không loop nhạc thiếu.
- `render`: gọi orchestrator cũ với `--public-source <batch>/production-public --skip-existing`; bundle/render/QA tuần tự, giữ attempt cũ. Final đã có chỉ QA lại, không tự xuất thay.

Nhạc/cue khai báo trong `audio`:

```json
{
  "audio": {
    "music": [{"file": "videos/approved-batch/audio/selected-score.mp3", "sha256": "HASH"}],
    "cues": [{"file": "videos/new-original-topic/long/audio/basket.mp3", "sha256": "HASH", "phrase": "Cụm mở một shot", "offsetSeconds": 0.2, "role": "Tiếng đặt giỏ đúng hành động"}]
  }
}
```

Đường audio có thể tương đối với manifest hoặc với gốc repository, nhưng phải nằm trong repository. Ghép nhiều stem trọn một lần bằng crossfade ba giây; sau crossfade phải đủ chiều dài video. Lựa chọn nhạc/âm lượng vẫn cần nghe thực tế; script mix không ghi nhận “đã nghe”. Có thể dùng mixer riêng nếu giữ `long/audio/final-mix.wav` và `long/audio-sources.json` đúng chuẩn hash của renderer.

## Tùy chọn cache có giới hạn cho batch tương lai

Manifest mới có thể chọn `"renderOptions": {"memoryProfile": "bounded"}`. Wrapper truyền `--memory-profile bounded` tới `render_directions.py`; tùy chọn này luôn dùng một trang render và `--media-cache-size-in-bytes=268435456` (256 MiB). Mặc định vẫn giữ cách chạy trước đó, không thêm flag cache. Không sửa manifest đã ghim hoặc thay tùy chọn của job đang chạy; áp dụng cho batch/revision mới.

Giới hạn này chỉ là ngân sách cache decoded media của `<Video>`/`<Audio>` từ `@remotion/media`, không phải trần RAM tổng thể. Mã cục bộ phiên bản 4.0.542 yêu cầu ít nhất 240 MiB khi đặt flag; mặc định khi RAM thấp có thể vẫn chọn tối thiểu 500 MiB. `attempt.json` ghi các tùy chọn đã phân giải và RAM vật lý khả dụng tại lúc bắt đầu, để so sánh các lần sau. Ghi nhận này không chứng minh preset sẽ nhanh hơn hoặc giảm tổng RAM tới một con số chắc chắn.

Trước khi đổi mặc định, cần benchmark các đoạn đại diện ảnh, clip và gallery 3D; so thời gian, peak RAM, frame thực giải mã và hình đầu ra. Chưa đổi decoder Offthread, encoder phần cứng, Chrome/GL hoặc tách bước JPEG/encode vì các tùy chọn đó có tác động khác và chưa được kiểm trên batch này. Job hiện tại tiếp tục dùng argv và bundle cũ.

Nguồn kiểm tra cục bộ: `cinematic/node_modules/@remotion/renderer/dist/options/video-cache-size.js`, `@remotion/media/dist/esm/index.mjs` phần `getUncachedMaxCacheSize`, cùng các option trong bản package đã khóa. Các file dependency này được đọc để hiểu đúng phiên bản đang chạy, không sửa package.

## Hàng đợi sản xuất nhiều video

```json
{
  "schema": "reference-video-queue/1",
  "jobs": [
    {"id": "topic-one-v1", "manifest": "topic-one/production.json", "batch": "topic-one", "steps": ["plan", "check", "voice", "prepare", "mix", "render"]},
    {"id": "topic-two-v1", "manifest": "topic-two/production.json", "batch": "topic-two", "steps": ["plan", "check", "prepare"]}
  ]
}
```

Đường dẫn job tương đối với file queue và phải nằm trong thư mục chứa queue. Các bước phải đúng thứ tự, không lặp. Mặc định job chỉ `plan/check/prepare`; muốn gọi giọng mới phải ghi `voice` rõ trong job.

```powershell
python workflows/reference-video/production.py queue --queue videos/production-queue.json
```

Hàng đợi chạy từng video/bước, lưu `.state.json` và giữ lock độc quyền. Bước hoàn tất được bỏ qua nếu output còn đúng hash. Nếu nội dung/batch/bước/guidance thay đổi, phải dùng job id mới. File output bị thay sẽ dừng thay vì tự gọi lại giọng. Bước lỗi hoặc bị ngắt dừng hàng đợi; chỉ sau kiểm tra nguyên nhân mới chạy `--retry-failed`. Cờ đó không xóa unresolved provider intent và không bỏ qua guard chống trùng phí của helper. Không có vòng retry vô hạn.

## Vòng học sau mỗi video

Agent phụ trách viết/dựng ghi vấn đề cụ thể, ví dụ câu nào sai hình, crop che vật thể, nguồn nào không hỗ trợ số. `learning.py` lưu feedback, áp dụng và bằng chứng kiểm lại thành các sự kiện riêng. Chỉ lesson đã được xác minh mới được xuất sang guidance; phản hồi phê duyệt của người dùng vẫn là một nguồn riêng.

Thêm `--guidance <export.json>` khi chạy production để lưu nguyên file và hash vào batch. Nó là tài liệu biên tập, không tự đổi style/voice, không làm các bước kiểm pending thành accepted và không chạy mã từ lesson. Queue gắn hash guidance với job để bản xuất có thể tra chính xác nó đã tham khảo phiên bản nào.

## Kiểm tra bắt buộc và giới hạn

Sau MP4, mở ảnh/crop/chữ/chuyển động, đối chiếu từng clause theo take thật và nghe tiếng nếu công cụ cho phép. QA tự động chỉ kiểm độ phủ, giải mã, loudness và dữ liệu; nó luôn để trạng thái thẩm mỹ/user acceptance pending. Lưu lỗi và bản sửa, không gọi decode pass là đẹp hoặc “người dùng đã duyệt”. Muốn học hiệu ứng/âm thanh cụ thể từ mẫu, kiểm trực tiếp đoạn media tương ứng; nghiên cứu contact sheet không đủ để xác nhận đã nghe.

Kiểm regression từ thư mục `workflows/reference-video`:

```powershell
python -X utf8 -m unittest test_production -v
```

Các test xác nhận file/caption bị đổi không được dùng lại với ghi chú cũ, stock không giả làm evidence, toàn lời được phủ đúng thứ tự, asset namespace tách batch, receipt giọng đúng preset, queue không lặp speech khi resume và không tự retry lỗi. Chúng không giả vờ kiểm thẩm mỹ.
