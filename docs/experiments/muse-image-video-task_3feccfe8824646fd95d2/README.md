# Thử API tạo video từ một ảnh sản phẩm

Ngày: 27/10/2026. Repo: `czg86389-hub/muse2api`, commit `5b8bba9561fdbe6402fbc08012d144699760afd0`.

## Kết quả thực tế

Đã gửi một yêu cầu `POST /v1/videos` với ảnh máy xay Toshiba người dùng cung cấp, dưới dạng data URL trong `reference_image`. Đầu vào yêu cầu `duration=8`, `size=9:16`, `resolution=720p`; prompt yêu cầu một cảnh quay liên tục, camera di chuyển chậm và giữ nguyên nhận diện sản phẩm. Sau khi POST, chỉ polling `GET /v1/videos/{task_id}`, không gửi lại yêu cầu tạo.

Task `task_3feccfe8824646fd95d2` hoàn thành; server ghi thời gian xử lý 95,3 giây. File MP4 gốc có 4.248.009 byte. Kiểm tra media: 720 × 1280, 24 fps, 192 khung hình, đúng 8 giây, tỷ lệ 9:16. Giải mã toàn bộ bản xuất không phát hiện lỗi.

Upstream vẫn sinh audio dù prompt yêu cầu không âm thanh. Đã loại bỏ track audio bằng FFmpeg, sao chép nguyên video stream sang [toshiba-reference-video-silent.mp4](toshiba-reference-video-silent.mp4).

## Đánh giá hình ảnh

[Sáu khung hình mẫu](frames.jpg) cho thấy có chuyển động góc nhìn quanh máy xay trong căn bếp; kết quả là video mới dựa trên ảnh tham chiếu. Hình dáng tổng thể, cối, nắp đen, thân đen/bạc và tên Toshiba còn nhận diện được.

Tuy nhiên, ảnh tham chiếu không được tái hiện chính xác tuyệt đối: một số chi tiết thân/đế và tay cầm bị thay đổi, xuất hiện thêm chữ trên cối. Cần duyệt thủ công trước khi dùng quảng cáo sản phẩm thật. Chưa đánh giá toàn bộ video theo từng khung hình hoặc khẳng định không có sai lệch nhỏ ở chỗ chuyển động.

## Phạm vi kết luận

- API và tài khoản đã dùng có thể tạo video dọc từ một ảnh; một lần thử thành công.
- Có thể bảo đảm đầu ra không âm thanh bằng hậu xử lý, thay vì chỉ dựa vào prompt.
- Chưa chứng minh độ ổn định qua nhiều lần chạy, nhiều tài khoản hoặc qua thời gian dài.
- Chưa kiểm chứng video liền mạch 20 giây hay tính năng kéo dài video của Muse. Không lấy kết quả 8 giây này để kết luận hỗ trợ thẳng 20 giây.

`submission.json` lưu yêu cầu đã bỏ dữ liệu ảnh base64, `result.json` lưu trạng thái task cuối, và `media-check.json` lưu thông số file đã đo. Không lưu cookie hoặc API key vào các tài liệu này.
