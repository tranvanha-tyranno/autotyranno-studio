# QA — video mũ xe đạp 30 giây

- Thành phẩm: **30,00 giây**, **720 × 1280**, **30 fps**, H.264 + AAC.
- 5 nguồn độc lập × 10 giây. Không lặp hoặc kéo chậm. Bốn cảnh dùng 9 giây ở 1,5×; cảnh đội thử dùng 8 giây ở 1,33× để giữ trọn đỉnh mũ.
- Lời đọc: Adam / Eleven v3, tiếng Việt; 5 đoạn căn vào từng cảnh 6 giây. Đã bỏ mô tả chưa chắc chắn về lưới, thay bằng dáng mũ/khe thoáng. Lời cuối tại `LOI-DOC.txt` và `dialogue-final.txt`.
- Đã kiểm tra giải mã toàn bộ video, âm thanh có tín hiệu, thời lượng và contact sheet của từng nguồn + bản cuối. Không phát hiện đoạn đen hoặc đứng hình liên tục trên 1 giây theo bộ phát hiện FFmpeg.
- Không dùng hình, giọng hoặc người mẫu từ clip mũ hồng làm thành phẩm. Video mẫu chỉ tham khảo cách kể và bố cục.

## Hạn chế thấy được

1. Chữ nhỏ trên vỏ và chi tiết khe/vân bề mặt vẫn có sai khác khi AI chuyển động, không phải bản sao tuyệt đối của sản phẩm.
2. Một vài đoạn cận mũ sát hoặc hơi vượt mép ngang; vẫn nhận ra sản phẩm nhưng bố cục chưa hoàn hảo.
3. Dáng đội và các góc không có trong ảnh gốc do AI suy diễn; không chứng minh độ vừa thực tế hay tính năng bảo vệ.
4. Người mẫu đôi lúc mấp máy môi; đây là voice-over Adam riêng, không phải đồng bộ khẩu hình.

Đã sửa riêng ảnh cận mất chữ, lỗi prompt logo, cảnh mở đầu xoay quá xa và cảnh chốt đổi khe. Giữ bản thử/lỗi và task ID trong batch để kiểm tra, không che các lần thử. Chưa đăng video lên nền tảng nào.
