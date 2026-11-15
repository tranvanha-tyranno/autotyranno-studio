# Quan sát hình ảnh — hướng Hidden / TYRANNO

Ngày kiểm tra: 12/11/2026. Trạng thái: lỗi font bản đầu đã được sửa và xác minh lại trên frame trích từ MP4 cuối. Chưa có xác nhận thẩm mỹ của người dùng.

## Kiểm tra lại MP4 cuối sau sửa font

Đã mở lại **`qa/frame-01311.jpg`**, **`qa/frame-02253.jpg`**, **`qa/keyframes-02.jpg`**, **`qa/keyframes-03.jpg`**, **`qa/last-frame.jpg`** được tạo mới từ MP4 cuối có SHA-256 **`213f57342363e61eb081b45284d230cf4f4ed7f08466edf915a5d39fe7a10e5b`**.

“Quay về nguồn” tại 43,70s và “Nhiệm vụ nào tiếp theo?” tại 75,10s đã hiển thị liền chữ, dấu đúng vị trí; không còn lỗi khoảng trống trong từ đã thấy ở bản đầu. Các headline gallery, split và CTA trong hai sheet mới nằm trong khung, không thấy glyph tách hoặc tràn chữ. Frame cuối vẫn có câu chốt và phụ đề “đang thay đổi.”, không bị che bởi fade cuối. Không thấy thay đổi vị trí ảnh/timing ngoài thay font trong các mốc đối chiếu.

Báo cáo QA mới xác nhận 2490/2490 frame, 83s, 1920×1080/30fps. Nhận xét trên là quan sát frame trích từ bản cuối đã sửa, tách riêng với hai still chứng minh font trước đó; không khẳng định đã nghe liên tục hoặc được người dùng duyệt.

## Phạm vi đã mở

Đã mở `qa/keyframes-01.jpg`, `keyframes-02.jpg`, `keyframes-03.jpg`, `spatial-motion.jpg`, `last-frame.jpg`; sau đó mở riêng ảnh 1080p `frame-00480.jpg`, `frame-01311.jpg`, `frame-02253.jpg`, `frame-01644.jpg`. Các file này tại thời điểm kiểm tra thuộc bản xuất đầu có SHA-256 `3c0afd10e27694dd0f0eeca2b76b5013908fa1396f0d2fc52b976f011f00b3e1`.

Bản đầu đã được giữ riêng thành `review-before-vietnamese-font-fix.mp4`; bộ QA tương ứng được chuyển vào `qa-before-vietnamese-font-fix/`. `qa/` hiện chứa bộ trích mới của bản cuối được kiểm tra lại ở mục trên.

Đây là quan sát mẫu hình từ MP4, không phải tuyên bố đã phát liên tục hoặc nghe toàn bộ video. Không suy diễn chất lượng giọng/nhạc từ ảnh hoặc số loudness.

## Lỗi thực tế đã phát hiện và cách sửa

- Ảnh 1080p tại **43,70s** cho thấy dấu trong “Quay về nguồn” bị tách và tạo khoảng trống bên trong từ.
- Ảnh 1080p tại **75,10s** cho thấy “tiếp” trong “Nhiệm vụ nào tiếp theo?” cũng bị tách dấu. Đây là lỗi thật ở frame xuất, không phải chỉ do thu nhỏ contact sheet.
- Kiểm tra cmap Georgia trên máy xác nhận thiếu 21 codepoint đang dùng trong các headline. Cmap `C:/Windows/Fonts/times.ttf` chứa đầy đủ 63 codepoint riêng của toàn bộ 11 headline; các dấu tiếng Việt khó có glyph dựng sẵn. Bằng chứng tên glyph, ký tự thiếu và hash font nằm trong `font-validation.json`.
- Đã sửa renderer tái dùng sang **Times New Roman**, chuẩn hóa headline NFC và ghi nhận font trong profile. Không đổi dữ liệu câu chữ, timing hoặc audio. ESLint file renderer và TypeScript đã qua.
- Đã mở **`font-proof-source.png`** và **`font-proof-cta.png`** ở 1920×1080 sau sửa: “Quay về nguồn” và “Nhiệm vụ nào tiếp theo?” đã liền chữ, dấu đặt đúng vị trí, không còn khoảng trống lạ trong từ; cả hai vẫn nằm trong vùng chữ. Hash và quan sát của hai still được thêm vào `font-validation.json`. Đây là bằng chứng sửa glyph trong still, chưa đồng nghĩa MP4 xuất lại đã được kiểm tra.

## Quan sát bố cục và hình minh họa ở bản đầu

- **1,47–10,70s:** hướng navy/ivory, serif và điểm nhấn teal phân biệt rõ với bản Lóng cream/coral. Phỏng vấn, làm việc tại nhà và bảng nhiệm vụ phù hợp câu hỏi tên nghề so với việc thật. Ảnh dọc giữ người/tay/laptop bằng contain; đổi lại vùng mờ hai bên khá rộng.
- **16,00s / lưu ý:** tiêu đề và câu miễn trừ trên cột navy riêng bên trái, ảnh cuộc trao đổi bên phải. Dòng giải thích, nguồn và phụ đề có khoảng riêng; không thấy bị cắt khung.
- **19,67–28,27s:** ảnh hỗ trợ đồng nghiệp, file hồ sơ, gõ máy, đối chiếu giấy và họp nhóm minh họa các nhiệm vụ. Ảnh file hồ sơ chỉ cho bối cảnh tổ chức thông tin, chưa biểu diễn trực tiếp một thao tác tìm kiếm; ảnh màn hình gõ máy là stock, không phải chụp giao diện AI đang chạy đúng tình huống.
- **34,83–38,90s / gallery thứ nhất:** ảnh viết, đối chiếu giấy và nhóm quyết định giữ đúng chuỗi tạo nháp/đối chiếu/chịu trách nhiệm. Cả ba texture hiển thị, mặt phẳng có chiều sâu và không tràn khung; nguồn/phụ đề tách khỏi ảnh. Những mẫu liên tiếp cho thấy dịch chuyển nhẹ, không xác nhận độ mượt phát liên tục.
- **43,70s / evidence:** tay chỉ giấy và calculator thể hiện việc quay về nguồn. Cột chữ không chồng lên ảnh; lỗi ở đây thuộc glyph chữ như ghi ở trên. Tài liệu stock có chữ nước ngoài và không được trình bày như bằng chứng một bảng số thực tế của câu chuyện.
- **46,57–49,23s:** người đeo headset và nhóm hỗ trợ đúng vai trò chăm sóc khách hàng. Người trong ảnh được minh họa trung tính, không được gán là khách hoặc nhân viên có sự cố AI thật.
- **54,80s / split:** headline dài vẫn nằm trong khung; đủ mặt/tay/giấy của hai người kiểm tra. Bố cục giữ tỷ lệ ảnh nên có vùng đệm trên ảnh phải. Phụ đề ở hàng riêng, không che mặt người.
- **57,57–61,70s / gallery thứ hai:** giấy/công cụ, cuộc trò chuyện và nhóm quyết định làm rõ kiểm tra/bối cảnh/quyết định. Photo planes và đường nối nằm gọn, không thấy vùng mất texture hay khối hình rỗng.
- **63,37–72,40s:** laptop/giấy, bảng nhiệm vụ, trao đổi và người ghi chú phù hợp thử một nhiệm vụ, tự so kết quả, đo thời gian sửa. Ảnh đào tạo kết phần nội dung giữ đủ người trong cảnh; không phải bằng chứng kết quả thử nghiệm.
- **75,10–82,97s / CTA:** câu hỏi, mời bình luận và lời đăng ký xuất hiện lần lượt. Tiêu đề ở ảnh cuối rõ trên nền tối; phụ đề cuối “đang thay đổi.” vẫn hiện ở frame cuối, không có fade sớm tại mẫu đã mở. Câu hỏi CTA trước đó có lỗi dấu và cần bản sửa.

Không thấy chữ tràn khung, lỗi mất texture hay vùng đen bất thường trong các mẫu đã mở. Nhận xét này không xóa lỗi dấu đã tìm thấy và không thay thế phản hồi thẩm mỹ của người dùng.

Theo báo cáo bản đầu: 2490/2490 frame, 83s, 1920×1080, 30fps; 26 shot, 24 ảnh riêng, 33 lượt đặt ảnh, 10,27s gallery không gian. Đó là kiểm tra kỹ thuật tách khỏi đánh giá hình và tiếng.
