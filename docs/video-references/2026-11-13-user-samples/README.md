# Bốn video mẫu người dùng gửi — 13/11/2026

Mở **[trang tra cứu có video và mốc thời gian](index.html)**. Chọn video, đọc phân tích hoặc bấm một đoạn timeline để nhảy tới bản tải. **[PLAYBOOK.md](PLAYBOOK.md)** tổng hợp cách viết kịch bản, góc khai thác, đối tượng suy luận và bài học chọn hình dùng lại.

## Bản tải và hồ sơ từng video

| Video gốc — đều thuộc Lóng | Thời lượng | Bản tải riêng | Báo cáo theo đoạn | Cách viết rút ra |
|---|---:|---|---|---|
| [Châu Âu đang rơi vào khủng hoảng toàn diện như thế nào?](https://www.youtube.com/watch?v=w3z43Hlzq3c) | 20:51 | [MP4 có tiếng](w3z43Hlzq3c/reference.mp4) | [21 đoạn](w3z43Hlzq3c/analysis.md) | [Mẫu tư duy](w3z43Hlzq3c/script-pattern.md) |
| [Tại sao dự án tái thiết đô thị Vĩnh Hưng lại cần thiết?](https://www.youtube.com/watch?v=1OGwWLvasIk) | 25:24 | [MP4 có tiếng](1OGwWLvasIk/reference.mp4) | [26 đoạn](1OGwWLvasIk/analysis.md) | [Mẫu tư duy](1OGwWLvasIk/script-pattern.md) |
| [Vì sao 1 thẻ bài TCG lại đắt giá đến thế?](https://www.youtube.com/watch?v=gNznfzAUiLw) | 17:32 | [MP4 có tiếng](gNznfzAUiLw/reference.mp4) | [18 đoạn](gNznfzAUiLw/analysis.md) | [Mẫu tư duy](gNznfzAUiLw/script-pattern.md) |
| [Chúng ta học được gì từ sự nổi tiếng của Huấn Hoa Hồng?](https://www.youtube.com/watch?v=3JUxxp2sIDM) | 13:23 | [MP4 có tiếng](3JUxxp2sIDM/reference.mp4) | [14 đoạn](3JUxxp2sIDM/analysis.md) | [Mẫu tư duy](3JUxxp2sIDM/scriptpattern.md) |

Tổng thời lượng metadata: **77 phút 10 giây**. Bản tải là AVC 360p + AAC để học tham chiếu, không phải master xuất bản. Cả bốn đã kiểm giải mã toàn luồng video và audio, có biên nhận SHA256 riêng. Việc tải để học không xác lập quyền tái sử dụng hình/nhạc/nhận diện của kênh trong video mới.

## “Từng đoạn” đã được ghi như thế nào?

- **79 khoảng thời gian liên tiếp** từ đầu tới cuối bốn video, mỗi khoảng tối đa 60 giây; bên trong chia tiếp thành **273 mạch ý có ý nghĩa** với mốc xấp xỉ theo caption.
- **2.587 dòng caption** được đọc toàn tuyến. Bản JSON3 gốc được giữ; thời gian/wordoffset là dữ liệu YouTube cung cấp, không phải forced alignment đo độc lập.
- **174 trang hình / 1.656 khung hình chọn mẫu**, chọn theo nhịp 5 giây cộng ứng viên thay đổi lớn trên luồng 2 fps; mọi trang đã có lượt kiểm tra. Một số chi tiết được mở thêm ở kích thước gốc.
- Mỗi đoạn ghi vai trò trong kịch bản, nội dung, hình thực sự thấy, mức hỗ trợ của hình cho lời, chuyển ý, cơ chế giữ chú ý suy luận và bài học áp dụng.

Đây là phân tích phủ toàn timeline bằng transcript và khung hình chọn mẫu. **Chưa phải lượt phát/nghe liên tục toàn bộ 77:10**, không đủ để kết luận mọi cut rất ngắn, chất lượng giọng/nhạc/SFX hoặc hiệu quả retention thực tế. Không dùng kiểm giải mã thay cho đánh giá thẩm mỹ. Khi cần tái tạo nhịp chuyển động/âm thanh cụ thể, phải kiểm lại đoạn MP4 liên quan.

## Tệp giữ để dùng lại

Trong mỗi thư mục ID:

- `metadata.json`: tiêu đề, kênh, thời lượng, mô tả và chapter nếu nguồn cung cấp.
- `reference.mp4`, `media-receipt.json`: bản có hình/tiếng, nguồn, dung lượng, hash và kết quả decode.
- `captions.json3`, `caption-receipt.json`, `transcript.json`, `transcript.txt`, `caption-word-offsets.json`: lời gốc, mốc thời gian và giới hạn nhận dạng.
- `study-blocks.json`, `sampling-receipt.json`, `sheets/`: chỉ mục mọi khoảng và bằng chứng hình có thời gian.
- `analysis.json`, `analysis.md`, tệp scriptpattern: quan sát, diễn giải và mẫu tư duy.

`catalog.json`, `library-checks.json` và `REVIEW_COVERAGE.json` ở gốc cung cấp mục lục và đối chiếu độ phủ. Tài liệu tái dùng ở `workflows/reference-video/REFERENCE_LEARNING.md`; mã tạo bộ nghiên cứu là `reference_study.py`, mã tạo trang đọc là `build_study_library.py` trong cùng workflow.

## Bài học chính để không lặp lỗi cũ

Học **trục kể chuyện và quan hệ lời–hình**, không chỉ đếm nhiều ảnh hay bắt chước hiệu ứng. Sự kiện cụ thể cần tư liệu đúng chủ thể; cơ chế trừu tượng có thể dùng một sơ đồ ngắn. Chuyển bố cục khi nhiệm vụ giải thích đổi, giữ đủ lâu khi cần đọc. Một stock đẹp không tự chứng minh câu nói. Kiểm cả chữ, số, đơn vị và năm vì nguồn/caption cũng có chỗ không khớp.

Giao diện ảnh/gallery 3D cũ, giọng Nhật Phong và hướng âm thanh đã duyệt vẫn được giữ theo yêu cầu. Đợt này lưu kiến thức và bằng chứng; không tự sản xuất video mới, không gắn nhãn người dùng đã phê duyệt một bản dựng mới, không huấn luyện trọng số mô hình.
