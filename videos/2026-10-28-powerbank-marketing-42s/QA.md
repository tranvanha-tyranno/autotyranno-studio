# QA video sạc dự phòng — 42 giây

- Thành phẩm **42,00 giây**, dọc **720 × 1280**, **30 fps**, H.264 + AAC.
- Sáu nguồn khác nhau (SHA-256 khác nhau), mỗi nguồn dài 10 giây; lấy 9,8 giây ở 1,4× thành 7 giây/cảnh. Không lặp hoặc kéo chậm để bù thời lượng.
- Sáu đoạn Adam / Eleven v3, tiếng Việt, căn vào timeline riêng với mức tăng tốc giọng tối đa khoảng 1,11×. Không cắt mất đoạn âm thanh để vừa hình.
- Hook chữ xuất hiện 0–3 giây; hai câu mở ngắn đi trước khoảng nghỉ ở khoảng 2,47 giây trong bản giọng gốc. CTA chữ có từ 35–42 giây và hành động mua nằm ở cuối lời đọc.
- Chữ được vẽ bằng code, đủ dấu tiếng Việt; thẻ dung lượng và công suất luôn gắn điều kiện nguồn/phiên bản. Không bịa giảm giá, tồn kho hoặc trải nghiệm đã sử dụng.
- Kiểm tra giải mã toàn bộ file qua FFmpeg: đạt. Âm lượng trung bình -16,5 dB, đỉnh -1,5 dB; không phát hiện đoạn đen hoặc đứng hình liên tục trên 1 giây theo bộ phát hiện đã chạy.
- Đã xem sáu ảnh mở đầu, contact sheet của sáu nguồn được chọn, 21 khung của bản cuối từ 0 đến 40 giây, cùng ảnh cuối ở 41,8 giây. Các ô đen trống cuối contact sheet là ô chưa dùng của bố cục 5 × 5, không có trong video.
- Cảnh 5 lần đầu bị loại vì camera mở rộng, AI tạo tóc/gương mặt khác và đưa sạc sát mép. Bản sửa dùng ảnh nhân vật thứ ba, giữ camera vào sản phẩm, không lộ mặt; giữ lần đầu trong scene-05 và dùng scene-05-r02 cho thành phẩm.

## Giới hạn thấy được

Ký tự rất nhỏ trên ô báo pin thay đổi nhẹ khi AI tạo chuyển động, không phải số đo pin thực tế. Người mẫu đôi lúc mấp máy môi; đây là voice-over Adam riêng, không đồng bộ khẩu hình. Hình AI không chứng minh chính xác kích thước, cổng hoặc vật liệu ở các mặt không có trong ảnh. Thông số dung lượng/công suất là thông tin nhà cung cấp mẫu cùng kiểu, chưa xác minh tem của chiếc trong ảnh. Nguồn, ảnh đối chiếu và phạm vi claim nằm trong research.json và research-primary-check.json.

Không đăng hoặc gửi video sang ứng dụng khác. 14 bài kiểm tra source đã qua; git diff --check sạch.
