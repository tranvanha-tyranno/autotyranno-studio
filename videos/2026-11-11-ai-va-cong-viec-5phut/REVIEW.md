# Kiểm tra video AI và công việc — bản 5 phút

Yêu cầu: giữ mẫu 3D/chữ động, giọng Nhật Phong và hướng phối âm đã được duyệt; người dùng cho tự chọn chủ đề. Batch mới độc lập, không thay MP4 đã duyệt.

## Nội dung và lời kể

18 chương, 1.067 đơn vị cách nhau bằng khoảng trắng, một take Eleven v3 tiếng Việt. Take tự nhiên 295,81s; tempo 0,992651, vừa 298s lời và 2s kết. Các chapter và 54 beat chữ lớn dùng exact character alignment. ASR độc lập nhận được câu hỏi cuối đến 298,28s; các mốc ILO một phần tư và dự báo WEF 170/92 được nhận đúng ý. Có lỗi ASR một số từ Việt, lưu nguyên kết quả thay vì sửa thành script để giả xác minh phát âm.

## Hình

Giữ palette tối/emerald/coral và nền kem của mẫu được duyệt. Chín họ vật thể native 3D, chữ kinetic thay theo câu, bốn đoạn footage công việc có giấy phép. Cột 170/92 biểu diễn tỷ lệ dự báo; các bậc, khối nhiệm vụ và mạng là minh họa. Cảnh đầu và cột dự báo đã được kiểm tra ở frame lớn trước render. Preview 540p toàn thời lượng được dừng tại khoảng frame 2778 để chuyển sang render chính; không coi preview đó là bản đã kiểm tra đủ 300s. Kiểm tra toàn bộ thực hiện trên final sau xuất.

## Âm thanh

Nhạc theme đã duyệt + hai phần instrumental 120s mới, nối bằng crossfade; sáu cue Foley nhỏ theo ngữ cảnh. Phát hiện graph dùng asplit chung đầu vào intro/outro chỉ ra 30s: đã sửa thành đầu vào độc lập, đo stem đủ 300s, kiểm tra từng phút đều có tín hiệu. Mix hiện đo -16,09 LUFS và -4,29 dBTP trước AAC. Không dùng tiếng máy may của video trước.

Công cụ phiên này kiểm tra bằng độ dài, waveform/loudness và ASR, không cung cấp nghe trực tiếp. Không ghi nhận đã nghe thủ công hoặc bảo đảm giọng/nhạc hay bằng chỉ số. Bản MP4 cuối cần đo lại sau encode.

## Nguồn

RESEARCH.md và sources.json phân biệt nghiên cứu tiềm năng, dự báo, ví dụ giả định và gợi ý biên tập. ILO/WEF năm 2025 được ghi đúng năm, không gọi là số liệu thực tế mới năm 2026. Các nguồn stock không được gọi là bằng chứng người trong hình đang dùng AI.

Trạng thái duyệt thẩm mỹ của video mới: pending. Chỉ bản 50s trước được người dùng duyệt rõ ràng.


## Kết quả trên MP4 giao cuối

Giải mã đủ **9.000 frame / 30fps / 300,00s / 1920×1080**. File 66.629.580 byte. Đã xem sáu trang full-duration lấy mẫu 1fps toàn 300s, bốn trang gồm 36 keyframe và ba trang gồm 108 frame theo chuỗi ngắn cho các chương. Tất cả là frame từ final.mp4. Các chữ lớn nằm vùng trái, có xuống dòng tự nhiên; không phát hiện tràn khung trong mẫu. Native 3D hiện phía phải; cảnh bốn người giữ một người emerald; hai cột dự báo có nhãn và đúng tỷ lệ. Footage công việc chuyển sang vật thể thay vì lặp hết chương. Chữ câu kết hiện đủ trước fade; ASR nhận câu hỏi cuối. Chuỗi frame cho thấy spring/rotation của chữ, kim đồng hồ và di chuyển qua cổng; một số vật thể giữ trạng thái ổn định giữa các beat, không diễn giải delta pixel thành điểm thẩm mỹ.

Âm thanh trên MP4: **-16,10 LUFS / -4,35 dBTP**, không clipping. Đây là đo kỹ thuật; không tuyên bố đã nghe trực tiếp. Chưa có phản hồi duyệt thẩm mỹ cho bản mới.
