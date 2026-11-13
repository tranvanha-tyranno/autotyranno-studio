# Cải tiến sau mỗi batch video

`learning.py` lưu phản hồi, thay đổi và kết quả kiểm tra thành lịch sử cục bộ. Quy trình giúp lần sau dùng lại điều đã kiểm chứng, không phải huấn luyện trọng số mô hình, tự đổi giao diện/giọng, tự xuất bản hay tạo lịch chạy nền.

Giữ giao diện ảnh/gallery 3D cũ và giọng Nhật Phong đã chốt. Những điều rút từ bốn mẫu Lóng nằm trong `REFERENCE_LEARNING.md` và `reference-learning.profile.json`; các quan sát tham chiếu chưa tự trở thành bài học đã kiểm chứng trên một bản dựng mới.

## Vòng cải tiến

1. Xuất một revision mới vào batch riêng; giữ bản cũ, script, take, asset, nguồn và hash.
2. Chạy kiểm kỹ thuật và ghi bằng `record-check`. Ví dụ: giải mã, số frame, thời lượng, độ phủ lời và âm lượng. Kết quả kỹ thuật không phải đánh giá đẹp/xấu, khớp nghĩa hoặc giọng đã nghe.
3. Kiểm bản dựng thực tế. Với từng vấn đề, ghi đúng mệnh đề, mốc thời gian, frame đã nhìn, asset/crop liên quan, quan sát và hành động sửa. `record-feedback` lưu `pending`, `revision_needed`, `rejected` hoặc `accepted` cùng phương pháp kiểm tra.
4. Đề xuất một quy tắc có thể dùng lại từ phản hồi đã có: `propose-lesson`. Ví dụ: không dùng cảnh phố rộng cho câu nói về lối hẹp cản phương tiện. Một quy tắc đề xuất chưa được xuất sang guidance áp dụng.
5. Thực hiện sửa vào revision có tên mới, lưu artifact và hash: `apply-lesson`. Đây là xác nhận đã có thay đổi cụ thể, không phải ghi một kế hoạch rồi coi như đã sửa.
6. Kiểm revision đã sửa bằng một phản hồi mới, sau sự kiện áp dụng. Chỉ `accepted` đúng phạm vi và phương pháp mới được dùng cho `verify-lesson`. Một lượt decode, feedback cũ, revision khác hoặc kiểm một khía cạnh khác đều không đủ.
7. `export-guidance` chỉ xuất bài học đã verified, chưa retired và bằng chứng còn khớp hash. Runner có thể lưu bản guidance cùng hash trong batch tiếp theo. Nó vẫn phải kiểm ảnh của chủ đề mới, không tự đánh dấu mọi video sau đó là đạt.

Ba trạng thái **đề xuất → đã áp dụng → đã kiểm chứng** là trạng thái quy tắc. Phản hồi `accepted` của agent là nhận xét biên tập có phạm vi, không phải người dùng đã duyệt cả video. Trạng thái duyệt của người dùng chỉ có khi lưu đúng câu người dùng nói, file phản hồi gốc và hash của bản render được nói đến. Không tự viết lời khen rồi ghi người dùng đã nói.

## Lệnh

Từ thư mục dự án, chọn một ledger dùng chung cho chuỗi explainer. Không cần chạy scheduler hoặc gọi API:

```powershell
python workflows/reference-video/learning.py --store workflows/reference-video/learning-data record-feedback --input videos/BATCH/review/feedback.json --request-key BATCH-r01-c03-visual-review
python workflows/reference-video/learning.py --store workflows/reference-video/learning-data record-check --input videos/BATCH/review/decode-check.json --request-key BATCH-r01-decode
python workflows/reference-video/learning.py --store workflows/reference-video/learning-data propose-lesson --input videos/BATCH/review/lesson.json --request-key BATCH-lesson-01
python workflows/reference-video/learning.py --store workflows/reference-video/learning-data apply-lesson --input videos/BATCH/review/application.json --request-key BATCH-r02-apply-lesson-01
python workflows/reference-video/learning.py --store workflows/reference-video/learning-data verify-lesson --input videos/BATCH/review/verification.json --request-key BATCH-r02-verify-lesson-01
python workflows/reference-video/learning.py --store workflows/reference-video/learning-data export-guidance --output workflows/reference-video/learning-data/guidance.json
python workflows/reference-video/learning.py --store workflows/reference-video/learning-data report --output workflows/reference-video/learning-data/report.json
python workflows/reference-video/learning.py --store workflows/reference-video/learning-data audit --output workflows/reference-video/learning-data/audit.json
```

Mỗi lệnh ghi trả về ID sự kiện. Dùng các ID đó trong bước kế tiếp. `--request-key` cố định cho một thao tác: gọi lại cùng nội dung sẽ trả lại sự kiện cũ; dùng cùng key với nội dung khác sẽ bị chặn. Với một lần sửa/review mới phải dùng key mới. Không dùng `--request-key` chứa token hay thông tin đăng nhập.

`--workspace` mặc định là gốc repository; có thể chỉ định một thư mục khác cho chạy thử độc lập. Store và mọi evidence phải nằm trong workspace đó. Trong JSON, dùng đường dẫn **tương đối từ workspace**, không dùng đường dẫn tương đối từ file JSON, URL hay `../`.

Tệp JSON mẫu ở `learning-templates/` chỉ là khuôn để điền; placeholder và SHA rỗng chưa phải bằng chứng hợp lệ. Không ghi credential vào template, report, nội dung phản hồi hoặc source receipt.

## Feedback gắn với lời và hình

```json
{
  "batch": "videos/BATCH",
  "revision": "r01",
  "dimension": "visual_relevance",
  "decision": "revision_needed",
  "reviewer": {"kind": "agent", "name": "Người kiểm hình"},
  "target": {
    "clause_id": "c03",
    "narration": "Cánh cửa hẹp khiến xe không đi qua.",
    "start": 12.4,
    "end": 16.8
  },
  "method": "rendered_frame_comparison",
  "observation": "Crop hiện tại cho thấy phố rộng; chưa thấy cửa hẹp hoặc vật cản đang được nhắc.",
  "action": "Chọn tư liệu đúng lối hẹp và giữ cửa cùng phương tiện trong crop mới.",
  "evidence": [
    {"role": "render", "path": "videos/BATCH/r01/final.mp4", "sha256": "SHA256_THỰC"},
    {"role": "frame", "path": "videos/BATCH/r01/qa/frame-012.4.png", "sha256": "SHA256_THỰC"},
    {"role": "asset", "path": "videos/BATCH/assets/source.jpg", "sha256": "SHA256_THỰC"}
  ]
}
```

`dimension`: `visual_relevance`, `script`, `voice`, `sound`, `overall`, `workflow`. `decision`: `pending`, `revision_needed`, `rejected`, `accepted`. Mỗi feedback là một vấn đề/đối tượng rõ ràng; dùng `clause_id` riêng nếu một đoạn có nhiều vấn đề độc lập.

`method` phản ánh việc thật đã làm: `rendered_frame_comparison`, `continuous_av_review`, `audio_listening`, `script_review`, `human_feedback`, `metadata_only`. Metadata chỉ hỗ trợ trạng thái pending; không dùng nó để đánh giá biên tập. Đánh giá giọng/âm thanh cần file audio và nghe thực tế; agent đánh giá `overall` cần đã xem/nghe toàn bản. Xem contact sheet không được ghi thành `continuous_av_review`.

Feedback hình khác pending cần cả render, frame và asset đã kiểm. Feedback script cần bản script. Phản hồi tổng thể cần hash render thật. Cho đánh giá cả bản, dùng `clause_id` như `__whole_video__` và một đoạn script nhận diện rõ phạm vi; thời gian phủ khoảng được đánh giá. Không dùng một lời duyệt cũ cho revision mới.

Để sửa nhận xét cùng batch/revision/dimension/clause, thêm `supersedes` trỏ tới **sự kiện mới nhất** của đúng đối tượng đó. Lịch sử cũ được giữ. Nếu nhận xét nguồn hoặc nhận xét xác minh một quy tắc bị supersede, quy tắc đó sẽ tạm không còn trong guidance hiệu lực, dù sự kiện verified lịch sử vẫn tồn tại. Có thể `retire-lesson` cùng lý do để chấm dứt một quy tắc đã lỗi thời; muốn đổi quy tắc thì đề xuất một bản mới có nguồn.

## Phản hồi của người dùng

Chỉ dùng `reviewer.kind = human_user` cho câu trực tiếp từ người dùng. Đặt `method = human_feedback`, thêm `quote` nguyên văn và evidence `role = feedback` trỏ tới file UTF-8 có đúng câu đó. File feedback cùng render cũng phải có SHA256 thực. Công cụ kiểm được sự hiện diện của câu trong file và tính toàn vẹn file; nó không xác thực danh tính tác giả của một file mà người ghi tự tạo. Người vận hành phải giữ nguồn phản hồi thật.

Guidance lưu `verification_from_user_feedback` riêng cho từng quy tắc. `user_acceptance_by_batch` chỉ gắn `user_approved = true` khi feedback **overall** mới nhất của batch/revision là người dùng chấp nhận và bằng chứng còn nguyên. Agent accepted, technical passed, hoặc người dùng chỉ duyệt một frame không tự nâng thành duyệt cả batch.

## Giao tiếp với runner sản xuất

Export có schema `reference-video-guidance/1`, gồm:

- `ledger_head_sha256`, `source_ledger`: nguồn lịch sử có thể đối chiếu.
- `lessons`: chỉ quy tắc verified còn hiệu lực, có rule/action/rationale, phạm vi, nguồn feedback, application/verification ID, người/phương pháp kiểm và evidence.
- `excluded_lessons`: quy tắc chưa verified, đã retired, feedback bị thay hoặc bằng chứng đã đổi.
- `user_acceptance_by_batch`: phản hồi tổng thể của người dùng, tách khỏi lesson và technical check.

`production.py --guidance ...` có thể snapshot export này và hash của nó. Guidance là **hướng dẫn biên tập**, không chứa lệnh đổi preset giọng/giao diện hoặc tự gọi API. `lessons: []` là kết quả đúng khi chưa có cải tiến mới được xác minh; không điền bài học giả để làm báo cáo trông đầy đủ.

## Tính toàn vẹn và khôi phục

Sự kiện trong `events/` có số thứ tự, ID từ nội dung, hash sự kiện trước và SHA256 riêng. Lệnh ghi dùng khóa độc quyền, ghi/fsync file staging rồi publish bằng hard link để không ghi đè sự kiện đã có. File staging bị gián đoạn không được xem là sự kiện. Không xóa hay sửa `events/*.json` bằng tay; tạo sự kiện mới để sửa ý nghĩa.

Nếu `.write.lock` còn sau khi tiến trình dừng bất thường, kiểm PID/tiến trình và các tệp đã ghi trước khi xử lý khóa; công cụ không tự phá khóa của tác vụ khác. Sao lưu ledger và pin `ledger_head_sha256` vào mỗi batch. Có thể dùng `audit --expected-head SHA256` để so với một receipt đã pin. Hash chain phát hiện nội dung hoặc thứ tự thay đổi; khi không có head đã pin, nó không tự biết một đuôi lịch sử hợp lệ đã bị ai đó xóa bên ngoài công cụ.

Bằng chứng phải là artifact/snapshot giữ nguyên của revision. Không dùng file mã đang tiếp tục sửa làm evidence duy nhất; giữ snapshot mã cùng batch để lần kiểm sau hash vẫn khớp. Nếu file bị đổi/mất, audit báo lỗi và quy tắc liên quan không được xuất như hướng dẫn đã verified. Điều đó không xóa sự kiện cũ và không khẳng định chất lượng đã xấu đi — chỉ cho biết bằng chứng đã không còn nguyên vẹn.

Kiểm tra offline:

```powershell
python -m pytest workflows/reference-video/test_learning.py -q
```

Các test kiểm việc không thăng hạng từ decode/pending, thứ tự áp dụng–kiểm lại, đúng revision/phạm vi, phản hồi supersede, quote gốc, hash/path, idempotency, lịch sử bất biến, lock và head đã pin. Chúng không thay lượt QA thẩm mỹ hoặc nghe giọng của video.
