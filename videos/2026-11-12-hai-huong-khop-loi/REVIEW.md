# Dựng lại phần hình theo từng câu

Lý do: người dùng bác cả hai mẫu trước vì ảnh không khớp lời. Những ảnh công sở chung đã được thay bằng một tình huống minh họa nhất quán: email chào hàng cho Đèn bàn Mẫu A, nội dung nháp sai, bảng nguồn để đối chiếu, yêu cầu cụ thể của khách và phần sửa. Mẫu A, tính năng, giá và thời gian đều là dữ liệu giả định do tác giả đặt để giải thích công việc; không xác nhận thông số hay hiệu quả của một sản phẩm thật.

Giọng Nhật Phong và mix từng hướng được copy nguyên bytes từ batch trước, hash đã đối chiếu. Không gọi TTS/music/SFX mới, không đổi tốc độ hoặc câu kết. Cấu trúc hook → miễn trừ → nội dung → CTA giữ đủ.

## Học lại và sửa nguồn tái dùng

Audit xem 20 cặp lời/frame nguồn và 13 cặp từ MP4 bị bác, phân biệt đúng vật thể/thao tác/trạng thái với chỉ cùng bối cảnh. Không khẳng định mọi cảnh tham chiếu đều khớp. `source-snapshot/RELEARN.md` và `evidence.json` giữ phạm vi, URL, media và timestamp. Quy trình mới có hợp đồng chủ thể–hành động–đối tượng–trạng thái, toàn bộ câu đang nói, điều phải thấy, hình thay thế bị cấm và proof cần kiểm.

Trước render đã kiểm 75 cặp câu/frame thực: 38 Long, 37 Hidden. Vòng một phát hiện thẻ 3D rỗng, phần thiếu bối cảnh chưa thể hiện nhu cầu, kết quả chỉ có tick xanh, so sánh chỉ có tên cột, chưa đồng bộ người nhận và so tổng thời gian thiếu baseline. Đã giữ `proofs-v1`, sửa trong mã dùng lại và xem lại toàn bộ proof v2. Không lấy tsc/đúng frame làm bằng chứng khớp nghĩa.

## Kết quả xuất

| Bản | Thời lượng / decoded frame | Kích thước | Âm lượng trên MP4 |
|---|---|---|---|
| long/final.mp4 | 82s / 2460 | 1920×1080, 30fps | -16,08 LUFS / -4,81 dBTP |
| hidden/final.mp4 | 83s / 2490 | 1920×1080, 30fps | -16,05 LUFS / -4,84 dBTP |

Render dài ban đầu bị thiếu chỗ ổ C. Đã giữ log và dùng NTFS compression không mất nội dung trong thư mục dự án, sau đó render đoạn 3 giây không tiếng, ghép thứ tự frame rồi mux bản mix gốc. Không lặp hình hoặc tăng tốc. MP4 cuối giải mã đủ toàn bộ frame; QA trích cặp lời/frame trực tiếp từ file ghép cuối và các chuỗi thao tác. Báo cáo thực tế từng bản ở `VISUAL_REVIEW.md`; chi tiết mỗi câu trong `qa/semantic-review.json`.

Root đã mở ba sheet 1fps toàn thời lượng của từng MP4 cuối và các chuỗi thao tác. Reviewer độc lập kiểm các cặp câu/frame từ chính MP4, kiểm điểm nối và ghi giới hạn. Chuyển động nhập yêu cầu/bình luận, nhấn vùng kiểm tra và đổi bước 3D nhìn thấy ở chuỗi mẫu. So sánh giọng điệu dùng bố cục trước/sau; không tuyên bố quay thao tác người thật. Bộ đếm thời gian là count-up minh họa trên số giả định, không phải thử nghiệm đo người dùng thật. Các thẻ 3D là sơ đồ biểu tượng có chiều sâu; mô hình đèn thể hiện dây/nguồn/trạng thái tắt trong ví dụ.

Ảnh internet chỉ dùng hỗ trợ chỗ thực sự có hành động/vật thể tương ứng. Không giữ quota ảnh hoặc lấy người họp, headset, kệ tài liệu để thay email/nút gửi/phép so sánh. Đã loại ảnh 31726764 vì file thật là máy chiếu dù metadata ghi đèn; giữ ảnh và ghi quyết định ở `rejected-source-images.json`. Không lấy ảnh đèn stock làm bằng chứng về pin/nguồn/giá giả định.

Chưa tuyên bố nghe bằng tai hoặc xem liên tục từng frame. Kiểm nghĩa cốt lõi ở frame mẫu không chứng nhận thẩm mỹ; cả hai bản mới chờ phản hồi người dùng. Mọi bản trước vẫn được giữ nguyên.
