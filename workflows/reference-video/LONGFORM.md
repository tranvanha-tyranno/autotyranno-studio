> **Ưu tiên mới nhất 12/11/2026:** dùng REAL_IMAGE_DIRECTION.md cho hình ảnh. Người dùng đã yêu cầu ảnh/footage internet minh họa sát câu nói, giảm vai trò 3D. Nội dung bên dưới giữ để tái tạo mẫu cũ và tái dùng giọng/âm thanh.

# Video dài theo mẫu 3D đã duyệt

Áp dụng cho yêu cầu 5 phút ngày 11/11/2026: `videos/2026-11-11-ai-va-cong-viec-5phut/`. Giữ `APPROVED_BASELINE.md` và `cinematic.profile.json` làm chuẩn giọng/âm thanh/thiết kế. Người dùng đã yêu cầu video tiếp theo, nên điều kiện chờ yêu cầu mới trong mẫu cũ đã được đáp ứng.

`content.json` chứa từng chương, lời kể, loại vật thể, theme và phrase cho chữ nhấn. `longform.py plan` lưu chính xác payload trước gọi nhà cung cấp: một take Nhật Phong/v3, hai instrumental 120s và ba Foley. Credential chỉ đọc tại thời điểm gọi từ vault. Sau thành công vẫn giữ payload trong generation-plan.json, tránh mất prompt gốc khi intent được dọn. Receipt và hash kiểm tra từng asset, cache không phát sinh lại hóa đơn khi chỉ sửa hình.

    python workflows/reference-video/longform.py plan --batch videos/<batch>
    python workflows/reference-video/longform.py voice --batch videos/<batch>
    python workflows/reference-video/longform.py music --batch videos/<batch>
    python workflows/reference-video/longform.py effects --batch videos/<batch>
    python workflows/reference-video/longform.py prepare --batch videos/<batch>
    python workflows/reference-video/longform.py mix --batch videos/<batch>

Adapter mix hiện dành riêng cấu trúc 300s: 40s theme đã duyệt + hai đoạn mới 120s + 30s theme kết, với ba crossfade 3,333333s. Đổi thời lượng cần đổi kế hoạch nhạc, không lặp hoặc kéo dài lời máy móc. Cue Foley được khai báo theo chapter và đổi khi thay chủ đề; không tái dùng tiếng máy may từ video kinh tế cho video AI. Caption/chapter/beat đều dùng exact-take alignment; không dùng timestamp của clip chuẩn 50s.

## Lỗi đã phát hiện và sửa

Ghép intro và outro từ hai nhánh `asplit` chung một đầu vào trong graph acrossfade dài đã tạo WAV chỉ 30s dù câu lệnh đặt -t 300. Đầu vào outro độc lập + trim/reset PTS riêng tạo đủ 300s. `mix` nay đo duration trước khi ghép voice và dừng nếu thiếu; không để amix giọng dài che giấu việc thiếu nhạc. Kiểm tra thêm RMS từng phút của stem nhạc. Giữ nhật ký debug trong batch.

## Dựng

Composition `WorkAI5min` trong `cinematic/` có 18 module cảnh riêng ở `src/longform/scenes/`, tái dùng renderer vật thể và layout để sửa thống nhất. Native geometry gồm chip, nhiệm vụ, giấy, bốn người, cổng duyệt, đồng hồ, hai cột dự báo 170/92, mạng ngữ cảnh và bậc kỹ năng. Bậc/mạng/khối là minh họa; chỉ cột dữ liệu dùng tỷ lệ dự báo có nguồn. Các wrapper từng cảnh là điểm mở rộng cho bố cục riêng. Bốn đoạn footage công việc quốc tế ngắn được phối với 3D, không kéo footage tĩnh hết cảnh.

    npx tsc --noEmit
    npx remotion render src/index.ts WorkAI5min <absolute-final.mp4> --gl=angle --concurrency=4 --crf=18

Lệnh chạy trong cinematic/. Không ghi đè Motion3D hoặc public/data.json/mix.wav của bản 50s. Bản mới dùng public/longform/. Giữ source-snapshot trong batch trước khi sửa cho nội dung khác. Cấu trúc Root thêm composition mới, còn bản MP4/preset/source snapshot đã duyệt trước đó được giữ nguyên.

## QA

    python workflows/reference-video/motion_qa.py --file <final.mp4> --out <qa-folder> --timeline <timeline.json>

`--timeline` mở rộng QA theo số frame thật (9000 ở 5 phút), xuất sheet toàn thời lượng từng trang 50 frame lấy 1fps, keyframe theo beat và chuỗi frame ngắn từng chương. Không dùng kiểm tra 1500 frame của clip 50s cho bản dài. Các mẫu per-second lưu thumbnail để hạn chế RAM; keyframe riêng vẫn giữ kích thước đủ xem. Đối chiếu ASR của mix để phát hiện thiếu lời nhưng không gọi đó là nghe thủ công. Đo lại loudness trên chính MP4, không chỉ WAV. User acceptance giữ pending cho video mới đến khi có phản hồi.
