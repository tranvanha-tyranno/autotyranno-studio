# AutoTyranno Studio local

Web hiện có backend thật, tách khỏi dashboard mock tại `/mock`. Chạy tại `http://127.0.0.1:3000`; API ở `127.0.0.1:8000`; Muse2API ở `127.0.0.1:18610`.

## Dashboard 2.0

- **Tổng quan:** số dự án hoạt động, sản phẩm, video, job đang chạy/chờ và ảnh chưa duyệt. Biểu đồ 7 ngày tính từ ngày file video được lưu và ngày tạo tác vụ theo giờ Việt Nam; không phải số liệu lượt xem TikTok.
- **Dự án:** tìm tên, lọc mica/review, sắp xếp, kiểu lưới/danh sách, ghim, đổi tên, lưu trữ và khôi phục. Không có thao tác xóa vĩnh viễn. Dự án đang chạy phải đợi job hoàn tất trước khi sửa metadata.
- **Xuất ZIP:** ảnh gốc, prompt, lời thoại, media và báo cáo của dự án. Không xuất thư mục key hoặc file ẩn. Tác vụ đang chạy thì chờ để tránh xuất dữ liệu dở. File ZIP tạm được xóa sau khi tải, bản gốc vẫn giữ nguyên.
- **Thư viện:** ảnh poster FFmpeg được cache local, xem video trong hộp thoại, tải file, tìm kiếm/lọc, đánh dấu yêu thích lưu trên server. Giữ được các video batch cũ.
- **Kho prompt:** đủ mẫu mica 11–20, lọc một/hai tay, xem toàn bộ và sao chép. Xem prompt không gọi provider.
- **Không gian clip:** tách Xem trước, Prompt & thoại và Trợ lý AI; chọn từng ảnh/cảnh/thoại để sửa. Theo dõi đủ bốn bước tạo ảnh, thoại, video, ghép/QA. Khi nhân bản clip có bản nháp chưa lưu, nội dung bản nháp được lưu vào bản sao, không mất ý tưởng đang chỉnh.
- **Hàng đợi:** lọc trạng thái, tìm log, mở dự án liên quan và hủy job vẫn còn `queued`. Không ngắt job provider đã bắt đầu; worker kiểm tra trạng thái hủy trước khi chạy.
- **Tài khoản Muse:** đọc danh sách pool qua API local và chỉ trả trường cho phép. Không hiện cookie, raw note hoặc API key. Hiển thị lượt sử dụng/trạng thái phiên/thời gian hết hạn; không đánh đồng số lượt dùng với quota còn lại. Đây là màn hình xem, chưa có tự đăng nhập/OTP hoặc thay đổi account pool.
- **Kết nối:** cấu hình key mã hóa và bật service Muse hiện có.
- **Điều hướng:** `Ctrl+K`, tìm trang hoặc tên dự án, `Esc` đóng hộp thoại. Link `?project=<id>` mở lại dự án sau refresh. Hộp thoại giữ focus bàn phím, hỗ trợ màn hình nhỏ và reduced motion.

Endpoint mới: `GET /studio/overview`, `/studio/media`, `/studio/templates`, `/studio/accounts`; `PATCH /studio/projects/{id}/metadata`; `GET /studio/projects/{id}/export`; `POST /studio/jobs/{id}/cancel`; `POST /studio/media/{id}/favorite`; `GET /studio/media/{id}/poster`. Các endpoint quản lý không sinh media trả phí.

## Chạy

```powershell
pip install -r backend/requirements.txt
cd frontend
npm install
npm run build
cd ..
.\start-studio.ps1 -Open
```

Script dùng Python/Node đã cài, chạy server nền với cửa sổ ẩn và log ở `data/studio-logs`. Nếu đã có service nghe cổng 3000/8000, script giữ service đó; kiểm tra đúng ứng dụng nếu mở nhầm. Khởi động lại web sau khi build bản mới. Tắt máy thì tác vụ dừng; đây chưa phải dịch vụ cloud chạy khi máy tắt.

## Luồng

1. Tạo dự án, chọn **Mica POV 6 giây** hoặc **Review 20 giây**.
2. Tải một hoặc nhiều ảnh theo thứ tự. Nhập và lưu tên, mô tả nhận diện, các tính năng có thật. Lập kế hoạch bằng code, chưa cần gọi LLM.
3. Review tạo 1–3 biến thể mỗi sản phẩm, mỗi clip có 3 cảnh, hình nhanh 1,5× và thoại mẫu Adam. Mica tạo 3 bối cảnh theo thứ tự mall/điện máy/xưởng, clip 6 giây, chọn prompt 11–20; mặc định không thoại. Bạn có thể điền thoại ngắn sau.
4. Sửa prompt/thoại trực tiếp. Nếu muốn ý kiến, chọn **Muse Chat** hoặc **Gemini**, model và trường cần sửa. AI chỉ trả đề xuất; bấm đưa vào bản nháp rồi lưu để áp dụng. Cache đề xuất dựa trên đầu vào đầy đủ.
5. Xem số lượt gọi. Chọn tạo từng bước, một clip, hoặc toàn dự án. Nút chạy provider thể hiện rõ có thể tiêu tốn quota; bước tính toán không dùng LLM.
6. Tạo ảnh rồi duyệt ảnh opening trước video. Toàn quy trình sẽ dừng với trạng thái `needs_review` khi ảnh chưa duyệt; bấm tiếp tục sau khi duyệt. Đây là kiểm tra bố cục để tránh tốn lượt tạo cảnh lỗi.
7. Xem preview, audio, contact sheet, video cuối và tải file. Việc decode thành công chỉ là QA kỹ thuật, không xác nhận chữ/chi tiết sản phẩm chính xác hay tuân thủ nền tảng.

Khi clip đã có media/task, sửa trên **bản nhân bản**. Không ghi đè kết quả cũ và không áp prompt mới lên job cũ. Hàng đợi dùng một worker để không tranh Muse. Job `interrupted` sau restart không tự chạy lại; người dùng chọn tiếp tục, runner dùng task ID đã lưu. Request đã gửi nhưng chưa xác định ID dừng để đối chiếu, không tự POST lặp.

## Dịch vụ AI

- Muse Chat: `/v1/chat/completions`, model mặc định `muse-spark`, key từ `.env` Muse đã cấu hình. Không dùng Chat khi có tác vụ Studio đang chiếm worker.
- Gemini: `generateContent`, API key qua header `x-goog-api-key`, model nhập được; mặc định `gemini-2.5-flash`. API chính thức: https://ai.google.dev/api/generate-content . Không chắc model/khả năng key tồn tại thì lỗi được hiển thị, không fallback âm thầm.
- Sửa prompt bằng Gemini Flash dùng `thinkingBudget: 0` để tránh tiêu nhiều token suy luận cho việc viết lại ngắn. Phản hồi bị cắt (`MAX_TOKENS`/`length`) bị từ chối và không cache; không hiển thị như bản sửa hoàn chỉnh. Đã thử thật Gemini và nhận bản sửa đầy đủ, rồi thử lại trên web để xác nhận cache.
- ElevenLabs: Adam `pNInz6obpgDQGcFmaJgB` / `eleven_v3`. Cùng thoại/settings/model dùng cache.
- “Kết nối AI” lưu key Gemini/ElevenLabs bằng Windows DPAPI trong `.secrets/`, không trả key qua API hoặc đưa vào frontend. Trạng thái “đã cấu hình” không đồng nghĩa key hợp lệ/còn quota. Nút bật Muse dùng script local sẵn có.

LLM chỉ nhận văn bản gồm tên, mô tả, claim và đoạn cần sửa; phiên bản này **chưa gửi ảnh/video cho vision model để phân tích tự động**, chưa có chat đa lượt hoặc chỉnh sửa pixel bằng Gemini. Mọi thay đổi ảnh/video được làm bằng prompt rồi sinh một phiên bản mới; ghép/cắt/đổi tốc độ/QA do code xử lý.

## Lưu trữ và phạm vi

- Dự án, ảnh upload, prompt, media, job, suggestion cache: `data/studio/<project-id>/`.
- Media sinh dùng hash cache của runner tại `.cache/product-video/`.
- Thư viện đọc thêm các `videos/*/clip-*/final.mp4` và hai video Adam cũ để xem lại công việc trước.
- Gemini/Muse không tự sinh video khi chỉ hỏi góp ý. Không có auto-publish TikTok/OAuth trong Studio; các API publish cũ của MVP vẫn là mô phỏng.
- Server chỉ bind loopback và chặn origin lạ với thao tác Studio. Chưa có tài khoản người dùng, phân quyền hoặc TLS. Muốn mở Internet/multi-user phải bổ sung auth, kiểm soát quota, persistent worker và lưu trữ phù hợp trước.

## Kiểm thử

`PYTHONPATH=backend python -m pytest backend/tests -q` kiểm tra upload/validation, thứ tự clip, hai pipeline bằng nguồn màu và âm cục bộ, pause/approval, clone, file playback/range, AI cache và không lộ key. Provider được mock trong test để không tính phí. `npm run build` kiểm tra Next/TypeScript. Giao diện được xem trực tiếp bằng trình duyệt local.
