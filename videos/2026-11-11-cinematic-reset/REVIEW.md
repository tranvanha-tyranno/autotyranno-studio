# Bản làm lại theo lựa chọn Motion graphics mạnh, 3D và chữ động

Bản trước bị người dùng từ chối: chuyển động, thiết kế, giọng và hiệu ứng chưa tốt. Không coi mười lượt QA trước là mười lượt được chấp nhận.

## Thay đổi thực tế

- Số 1.000 là mesh extrude có bevel; container và token là geometry Three.js thực, camera có phối cảnh. Địa cầu có texture và cung hàng chạy; cung/đếm token chỉ minh họa, không phải tỷ trọng hay bản đồ số liệu được đo.
- Chữ xoay vào theo mặt phẳng, translate/spring bám các mốc lời kể. Sáu cảnh riêng, chuyển slide/wipe/fade, nền tối sang may màu ấm rồi dòng giá trị nền kem.
- Hai footage may có nguồn Mixkit được giữ lại vì đúng ví dụ. Không lấy hình/nhạc/giọng từ 17 kênh tham khảo để xuất final.
- Đổi take sang giọng nam Việt Nhật Phong / Eleven v3; lời dài 47,07s được giảm tempo nhẹ xuống 49s, chừa đuôi nghỉ 1s. Giữ exact-take character alignment.
- Thay nhạc sine cũ bằng instrumental Eleven Music. Hạ nhạc ở câu “Nhưng khoan”, duck nhạc theo lời; chỉ có một Foley máy may đúng ngữ cảnh.

## Quan sát bản preview thực tế

Đã giải mã 1.500 frame của preview 960×540. Đã xem sheet toàn 50s, 9 keyframe và 24 frame theo chuỗi ngắn để thấy số đi vào, container ghép tầng, chữ XUẤT/NHẬP và câu kết xoay vào. Đây là kiểm tra chuỗi hình theo thời gian, không phải tuyên bố đã nghe và xem liên tục playback.

Phát hiện/sửa: globe bị chụp trước texture commit thành khối trắng; thay TextureLoader callback bằng useLoader/Suspense, kiểm tra lại thấy đầy đủ bề mặt đất. Chỉnh góc để châu Á hiện mặt trước. Không nối “Nhưng khoan” vào caption câu trước. Canh chữ VẢI/MÁY MÓC/THIẾT KẾ theo các từ thật. Preview đầu có các token tròn nhỏ như chấm trang trí; sửa bản final thành vật thể lớn hơn có độ dày/góc xoay, chuyển sang nền kem, kiểm tra lại frame 1230. Slide/wipe và bản nền kem phải được kiểm tra lại trên final.

## Phạm vi kiểm tra âm thanh

Mix WAV đo -16,19 LUFS, true peak -4,88 dBTP, không clipping. ASR local đối chiếu được nội dung và câu cuối đến 48,96s; có lỗi nhận dạng một số từ Việt, lưu nguyên bản kết quả thay vì sửa thành kịch bản để giả QA. Đo LUFS và ASR không thay việc nghe đánh giá thẩm mỹ. Công cụ của phiên này không cung cấp nghe âm thanh trực tiếp; không ghi nhận đã nghe thủ công. Có các stem gốc để người dùng đánh giá và thay độc lập khi cần.

## Giới hạn

Một tác vụ Muse cảng đã thất bại vì session HTTP 401; không dùng và không mô tả nó là footage sinh thành công. Bản giao dùng 3D native và hai clip may. Lưu style profile/source code không phải huấn luyện trọng số model. Mức “wow” chờ đánh giá người dùng; userAcceptance=pending.


## Kiểm tra đúng MP4 final

Final đã giải mã đủ **1.500 frame, 30fps, 1920×1080, 50,00s**. Đã xem lại `qa-final/full-duration.jpg`, `motion-strips.jpg` và frame 1185 lớn: globe giữ texture, cung chuyển vị trí, chữ lần lượt vào; đoạn token nền kem có độ dày/góc xoay, nằm bên phải và không che tiêu đề bên trái; caption có dải tương phản phía dưới. Hai cue chữ còn lại xuất hiện lần lượt đến 41s. Câu hỏi cuối hiện đầy đủ trước fade-out; không tràn khung trong các frame đã kiểm tra. Slide mở và wipe vào nền kem đã có trong final. Đây là nhận xét từ các frame thật của final, không dùng sheet preview cũ.

Âm thanh trong chính MP4 final đo **-16,20 LUFS / -4,83 dBTP**; không clipping. Không tự gán nhãn âm thanh hay / thẩm mỹ đạt chuẩn từ các số đo đó. Giữ trạng thái chờ người dùng duyệt.


## Người dùng đã duyệt — 11/11/2026

Người dùng xác nhận “rất ok” và yêu cầu giữ giọng đọc, sound và toàn bộ cách làm cho video sau. Trạng thái đã chuyển từ pending sang approved trên batch, QA report và profile. approved-assets.json lưu hash của final và các stem chuẩn; approved-style-profile.json giữ bản preset tại thời điểm duyệt. Những ghi chú pending phía trên là lịch sử trước khi nhận phản hồi này. Không tự làm video tiếp theo cho đến khi người dùng yêu cầu.
