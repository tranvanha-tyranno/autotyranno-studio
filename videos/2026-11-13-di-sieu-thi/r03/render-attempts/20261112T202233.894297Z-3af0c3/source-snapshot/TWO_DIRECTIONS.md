# Hai hướng explainer — 12/11/2026

> **CHỈ THỊ MỚI NHẤT — 13/11/2026:** người dùng đã gửi bốn video Lóng và yêu cầu tải, học từng đoạn, lưu cách viết/góc khai thác/người xem hướng tới. Đọc REFERENCE_LEARNING.md và hồ sơ docs/video-references/2026-11-13-user-samples/. Phạm vi hiện tại là nghiên cứu; chưa bắt đầu video hoặc đổi giao diện mới. Giữ phần ảnh + gallery3D cũ mà người dùng muốn quay lại; ảnh chưa khớp lời vẫn là lỗi cần sửa. Không dùng SEMANTIC_REBUILD.md để ép video sang bảng biểu/email/dashboard dày chữ.

Người dùng yêu cầu phát triển song song hướng tham chiếu Lóng và The Hidden Self, bổ sung nhiều ảnh internet và giao diện 3D. Đây là bước phát triển tiếp của REAL_IMAGE_DIRECTION.md: ảnh thật vẫn kể chuyện, 3D dùng để tổ chức/so sánh hình và giải thích mối quan hệ. Giữ giọng Nhật Phong và hướng phối âm đã chốt. Product review và mica không đổi theo tài liệu này.

## Tham chiếu thực tế

Đọc `docs/video-references/2026-11-12-two-directions/REFERENCE_AUDIT.md`. Lóng đã được xác định là `@longngghienn`; không suy đoán từ tên hiển thị. Audit dùng media tải thật, frame mở/thân/kết và transcript theo thời gian. Không coi đọc transcript là đã nghe hoặc xem liên tục.

Các mẫu Lóng có hook trước rồi lưu ý nguồn/góc nhìn, sau đó nội dung và CTA. Các mẫu The Hidden Self được kiểm tra có cold-open, bumper và phân tích; không mặc định tất cả đều có disclaimer. **Cấu trúc hook → miễn trừ trách nhiệm → nội dung → CTA cho cả hai là yêu cầu của người dùng**, không phải khẳng định mọi video của hai kênh đều như nhau.

## Hướng 1: trực diện, giàu ví dụ

Mở bằng tình huống cụ thể và mâu thuẫn dễ hiểu; trả lời từng bước, có ví dụ trực quan và phản biện. Nhịp dựng dứt khoát, ảnh chi tiết xen ảnh bối cảnh, nền cream/ink với điểm nhấn coral. 3D dùng bảng ảnh có chiều sâu để đặt bản nháp, bước kiểm tra và quyết định cạnh nhau. Dựng theo logic đã quan sát ở Lóng, dùng kịch bản và nhận diện riêng.

## Hướng 2: phân tích, chiêm nghiệm

Mở bằng một nghịch lý liên quan người xem, rồi giải thích cơ chế bằng ẩn dụ ngắn, ví dụ và giới hạn. Hình giữ lâu hơn khi cần người xem suy nghĩ; palette navy/ivory/teal, chuyển cảnh mềm. 3D dùng không gian ảnh để làm rõ chuỗi thao tác và vai trò con người. Giữ mạch phân tích tham chiếu The Hidden Self, xây nhận diện riêng bằng ảnh và chiều sâu thay vì micro/waveform cố định.

## Bốn phần bắt buộc

1. Hook: tình huống/nghịch lý có giá trị thật, hứa rõ câu hỏi sẽ trả lời. Không giật gân bằng số liệu hoặc kết luận không có nguồn.
2. Miễn trừ trách nhiệm: một câu đúng phạm vi chủ đề sau hook; đọc cùng lời dẫn, hình gọn và đọc được. Nội dung giải thích không trở thành tư vấn cá nhân hoặc dự báo chắc chắn chỉ nhờ thêm câu này. Không dùng lời miễn trừ để bù cho thông tin sai.
3. Nội dung: mỗi luận điểm có câu hỏi hình ảnh riêng; chọn ảnh phù hợp hành động được nhắc. Cut theo exact take narration, không dùng một bộ máy tính/đô thị cho mọi ý. Nguồn ảnh stock là minh họa, tách khỏi nguồn chứng minh luận điểm.
4. CTA: chốt lại điều người xem vừa học, mời làm một việc cụ thể và đặt câu hỏi bình luận liên quan; lời đăng ký kênh ngắn. Giữ nguyên câu cuối và khoảng đệm sau lời.

## Mã tái dùng và kiểm tra

- `directions.py`: nội dung theo shot/phrase, tạo exact take bằng preset đã duyệt, timing và phối âm trong batch riêng. Nguồn ảnh có URL/license/hash; call trả phí có cache/receipt.
- `direction-profiles/`: hai cấu hình có thể dùng lại; việc tạo profile không huấn luyện trọng số mô hình.
- `cinematic/src/directions/`: `DirectionFilm` render dữ liệu, gồm ảnh lớn, diptych, evidence, không gian ảnh 3D bằng Three.js, disclaimer và kết.
- `direction_qa.py`: kiểm tra thứ tự bốn phần, độ phủ timeline, số frame thực giải mã, ảnh theo shot và loudness trên MP4. Tạo sheet toàn thời lượng và chuỗi frame 3D để kiểm tra bằng mắt. Không tự chứng nhận thẩm mỹ.
- Batch so sánh: `videos/2026-11-12-hai-huong/`, hai bản mẫu hoàn chỉnh ngắn trên chủ đề AI/công việc. Đây là mẫu mới chờ phản hồi, không thay hay gắn nhãn duyệt cho các bản trước.

Không chạy nhiều lệnh bundle/still/render chia sẻ Rspack persistent cache cùng lúc. Kiểm tra ảnh/crop của từng bản xuất mới, lưu lỗi và sửa có bằng chứng. Giữ caption ngắn trong safe area; nguồn/nhãn không đè lên phụ đề. Ảnh chuyển động pan/zoom và plane 3D vẫn là ảnh tĩnh, không gọi thành footage của nhân vật.

### Font tiếng Việt phải kiểm tra glyph thật

Bản Hidden xuất đầu dùng Georgia đã bị tách dấu và giãn sai bên trong “nguồn”, “tiếp” dù đo chiều rộng chữ vẫn vừa khung. Mở frame 1080p mới phát hiện được; contact sheet nhỏ không đủ để bỏ qua dấu hiệu này. Georgia trên máy thiếu cmap cho nhiều ký tự tiếng Việt dựng sẵn (`ề`, `ồ`, `ệ`, `ụ`, `ế`, `ộ`, `ự`).

Headline Hidden dùng **Times New Roman** sau khi kiểm tra cmap của `C:/Windows/Fonts/times.ttf` chứa mọi codepoint của toàn bộ headline trong batch; renderer chuẩn hóa headline về NFC. Giữ bản lỗi và QA cũ, xem lại frame chữ khó ở kích thước thật rồi mới xuất lại toàn bộ. Với máy hoặc font mới, phải kiểm tra cmap đầy đủ và ảnh render thực tế; đo width hay có một vài dấu đọc được không chứng minh font hỗ trợ tiếng Việt. Không chỉ thêm tên font vào fallback rồi mặc định glyph đúng.

### Bộ nhớ và bundle ổn định

Lần xuất đầu chạy 4 tab render trên máy Windows đang ít RAM trống đã làm Chrome báo thiếu bộ nhớ/dung lượng tạm. Một job thứ hai đọc bundle tạm của job đầu cũng mất asset khi job đầu dừng và dọn bundle. Giữ cả hai log lỗi; không gọi đó là MP4 đã xuất.

Ảnh nguồn giữ nguyên trong batch/assets; `directions.py render-assets` tạo bản public JPEG vừa kích thước cần dựng, có `render-assets.json` ghi hash và kích thước trước/sau. Dùng `cinematic/src/directions-entry.tsx` để chỉ bundle renderer mới, public directory riêng chỉ chứa tài sản hai hướng. Bundle vào thư mục bền vững thuộc batch rồi render tuần tự ở concurrency 1 khi máy ít RAM. Không chia sẻ thư mục bundle tạm có vòng đời thuộc job khác.
