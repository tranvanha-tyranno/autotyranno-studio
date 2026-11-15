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

## Ảnh Việt Nam, miễn trừ rõ và hoạt ảnh 3D

Các nâng cấp này bật bằng manifest mới, không đổi mặc định hay ghi đè batch trước:

```json
{
  "visualPolicy": {
    "preferredCountry": "VN",
    "requireLocationEvidence": true,
    "explicitDisclaimer": true
  }
}
```

Ảnh/clip được xác định tại Việt Nam thêm `location` bên cạnh `source`: `{"countryCode":"VN","place":"Hà Nội","sourceURL":"https://trang-nguon-co-thong-tin-dia-diem","evidence":"Mô tả nguồn nêu cụ thể địa điểm tại Hà Nội."}`. Khi bật `requireLocationEvidence`, mọi tài sản khai báo nước ưu tiên phải có địa điểm, URL HTTPS và chứng cứ địa điểm. Đây là kiểm hồ sơ; người kiểm vẫn phải đối chiếu trang nguồn với file. Không suy quốc gia từ khuôn mặt, tên tác giả hoặc cảm giác ảnh. Tài sản không rõ địa điểm, ảnh nước khác hoặc sơ đồ tự tạo vẫn dùng được khi đúng câu thoại; không tự gán `VN` cho chúng.

`explicitDisclaimer` yêu cầu mỗi shot trong phần `disclaimer` có `eyebrow` đúng `MIỄN TRỪ TRÁCH NHIỆM` và `body` ngắn, tối đa 45 từ/280 ký tự. Người viết phải chọn nội dung phù hợp phạm vi bài. Nhãn hiển thị này không đổi narration, timing hay take đã chốt.

Cảnh cơ chế có thể dùng `layout: "object3d"` và `motion: {"kind":"basket","revealFrames":[0,32,64]}`. `kind` nhận `basket`, `price`, `journey`; `price` thêm `stage: "unit"` hoặc `"total"`. Chỉ layout này nhận `motion`. `revealFrames` tùy chọn gồm 1–3 frame cục bộ nguyên không âm, tăng nghiêm ngặt; compiler từ chối cue nằm ngoài khoảng lời chính xác. Các cue thiếu do renderer đặt theo thời lượng. Cảnh `price` hiện dùng ví dụ giả định cố định 1 hộp 30 nghìn, 2 hộp 50 nghìn, 25 nghìn/hộp và chi thêm 20 nghìn, có nhãn minh họa; schema không nhận giá bán tùy ý. `images` và kiểm nguồn/khớp lời vẫn bắt buộc cho ngữ cảnh ảnh, kể cả khi cơ chế dùng hình học Three.js thật.

`preflight.visualCoverage` ghi các quốc gia có chứng cứ trong từng shot, thời gian có tài sản nước ưu tiên và thời gian `gallery3d`/`object3d`. Chỉ slot ảnh được renderer dùng mới được tính; cảnh `price` thuần hình học không tăng tỷ lệ ảnh Việt Nam từ tài sản đính kèm. Thời gian dùng các khoảng shot không chồng nhau; shot có ảnh nhiều nước được ghi nhận từng nước. Đây là sự hiện diện theo catalog, không phải tỷ lệ diện tích ảnh, thời gian reveal từng ảnh, thời gian phủ toàn màn hình, xác minh địa lý độc lập hay phê duyệt thẩm mỹ. `image-sources.json` giữ nguyên hồ sơ `location`. Bộ sửa từng đoạn cũng so sánh `motion`, nên không thể đổi hoạt ảnh của shot ngoài danh sách sửa.

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

Gallery và panel ảnh `object3d` dùng poster tĩnh, nên clip trong các layout này bắt buộc có `posterFile` và `posterSHA256`; poster được thu nhỏ và kiểm hash riêng. Thời lượng poster không bị giới hạn theo số frame của clip nguồn. Ảnh di chuyển hoặc poster không được gọi thành footage động. Phần `disclaimer` luôn dùng layout riêng; không nhận `object3d` có motion bị bỏ qua.

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

## Sửa một số cảnh sau khi đã xem bản xuất

`production_repair.py` dành cho một **revision mới**, sau khi quan sát thật chỉ ra cảnh nào cần sửa. Nó không tự đoán lỗi và không đổi file/bundle/final của revision trước. Ví dụ hai cảnh `c12` và `a1`:

```powershell
python -X utf8 workflows/reference-video/production_repair.py --previous videos/previous-topic/long --manifest videos/next-topic/production.json --batch videos/next-topic --changed-shot c12 --changed-shot a1 --memory-profile bounded
```

Đầu vào trước cần `final.mp4`, data, script, bản giọng gốc/receipt/alignment, exact mix, nguồn/derivative receipts và `qa/report.json` có hash final hiện tại cùng frame count đúng. Manifest mới phải dùng nguồn riêng có hash và ghi chú đã xem. Công cụ sao chép nguyên take/mix sang revision mới rồi dùng `production.prepare`, không gọi provider tạo giọng hoặc mixer.

Chỉ được sửa cách lên hình của những shot đã chọn. Tổng frame/FPS, phase, mốc đầu/cuối, lời của mọi shot, toàn caption, title, script và bytes audio phải giữ nguyên. Các shot không chọn phải có cùng appearance; URL asset khác batch được so bằng hash derivative, credit, focus, fit và các trường hiển thị. Nếu một tài sản dùng chung đổi `fit` hoặc crop ở nhiều nơi, phải tách asset ID cho đúng placement hoặc chọn đủ mọi shot bị ảnh hưởng. `fit: contain|cover` là tùy chọn asset truyền sang renderer.

Khoảng vá bắt đầu tại `shot.start`, kết thúc tại `min(shot.end + 7, totalFrames)` độc quyền. Bảy frame đuôi giữ đúng cảnh cũ nằm dưới fade-in của cảnh tiếp theo. Cảnh cuối chỉ tới frame cuối; nhiều khoảng trùng/chạm nhau được gộp. Remotion nhận frame tuyệt đối `start–endInclusive` để animation vẫn dùng đúng mốc timeline. Patch tắt audio; ghép final dùng nguyên file exact mix một lần từ đầu.

Bundle/patch/log/snapshot nằm trong `repair-attempts/` mới. FFmpeg lấy các đoạn trước/sau từ MP4 trước, xen patch mới, chuẩn hóa 30 fps / SAR 1 / BT709 / YUV420p rồi encode video một lần. Do bản cũ đã nén H264, pixel ngoài vùng vá **không được khẳng định byte-identical** sau encode lại. Không dùng stream-copy/concat file mù; kiểm full decoded frames và QA toàn video mới. Thẩm mỹ và việc đã nghe vẫn pending cho đến khi thật sự kiểm.

`--dry-run` chỉ đọc/so sánh revision mới **đã chuẩn bị sẵn**, không tự copy/prepare/bundle. Bỏ cờ mới thực hiện sửa. Nếu audio, timing, caption hoặc cảnh không chọn đổi, công cụ dừng và yêu cầu một đợt dựng đầy đủ thay vì ghép sai timeline.

Nếu một attempt bị lỗi giữa chừng, thêm `--resume-from-attempt <batch>/repair-attempts/<id>` vào đúng lệnh cũ, giữ nguyên manifest, danh sách shot và render options. Có thể thêm `--dry-run` để kiểm chỉ đọc trước. Resume dùng nguyên bundle/source snapshot đã giữ; không prepare, bundle hay thay mã đang chạy từ source mới. Nó đối chiếu hash snapshot, manifest/data/props/receipt và cả tài sản staged/bundled, đồng thời giải mã lại từng patch hoàn tất và kiểm frame/FPS/SHA trước khi dùng lại. Thay đổi một input bị đóng băng sẽ dừng, không âm thầm render tiếp với hai phiên bản khác nhau. Không yêu cầu tài liệu/mã working hiện tại giống snapshot cũ.

Mỗi patch mới được lưu receipt ngay sau khi giải mã đạt. Patch chưa hoàn tất được **đổi tên giữ nguyên bytes** thành `patch-xx.failed-<id>.mp4`, rồi chỉ khoảng thiếu mới được render lại; patch đạt không xuất lại. Attempt trước resume, controller mới và log mỗi lần thử được giữ riêng. Không xóa file lỗi hoặc ghi đè final đã có. Sau các patch còn lại vẫn ghép và QA toàn video; resume không phải duyệt thẩm mỹ.

Attempt cũ chưa có `resume-integrity.json`/hash patch được tiếp nhận một lần sau khi đối chiếu `sourcesContent` trong source map với source snapshot, tài sản bundle với receipt, log hoàn tất và frame giải mã thực. Lần đầu này ghim SHA của bytes hiện tại; không chứng minh được lịch sử bytes trước khi ghim. Các lần resume sau bắt buộc khớp checkpoint SHA. Giới hạn này được ghi trong `resumeSessions`; không gọi việc tiếp nhận attempt cũ là xác minh hash lịch sử. Nếu final đã được cài nhưng bước QA sau đó lỗi, chạy QA riêng cho final hiện có; không dùng resume để ghi đè nó.

Kiểm riêng cơ chế sửa:

```powershell
python -X utf8 -m pytest workflows/reference-video/test_production_repair.py -q
```

Các test gồm ranh giới frame/đuôi chuyển cảnh, cảnh cuối, nhiều khoảng gộp, hash asset giữa namespace khác, audio/caption/timing bất biến và phép ghép FFmpeg nhỏ có frame count/pixel/audio thật. Chúng không xác nhận một sửa đổi hình ảnh cụ thể đã đẹp.

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
