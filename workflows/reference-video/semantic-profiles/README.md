# Storyboard theo nghĩa từng mệnh đề

Hai manifest này thay phần chọn hình của hai bản mẫu bị người dùng từ chối ngày 12/11/2026. Dùng lại đúng lời đọc, alignment và mix; không gọi giọng mới, không đổi tốc độ.

| Manifest | Exact take | Từ đã ánh xạ | Shot |
|---|---|---|---|
| long.json | 82s / 2460 frame | 287/287 | 38 |
| hidden.json | 83s / 2490 frame | 295/295 | 37 |

`allNarrationWordsCovered` chỉ xác nhận không bỏ lời khi chia shot. Nó không chứng minh hình đúng. `proof.status` của mọi shot còn là `requires_render_inspection`; chỉ đổi sau khi xem frame/video và ghi bằng chứng cụ thể.

## Hợp đồng hình ảnh

Mỗi shot có `scene` và `mode` cho renderer, `start/end` frame, `startWordIndex/endWordIndexExclusive`, `phrase` và toàn bộ `narratedText` trong khoảng đó. `narratedMeaning`, `requiredVisual`, `visibleFacts` và `forbiddenSubstitute` là yêu cầu nội dung hình, không phải từ khóa tìm ảnh chung chung.

- Nói tạo email: phải thấy email và thao tác nhập/tạo nháp. Laptop, bàn phím hoặc người ghi sổ chỉ là bối cảnh, không thay được điều này.
- Nói hứa sai tính năng: phải thấy lời hứa sai đặt cạnh căn cứ đối chiếu, cùng chỉ về một sản phẩm.
- Nói kiểm số: phải thấy hai số/nguồn và trường được kiểm. Calculator không có phép so không đủ.
- Nói sửa giọng điệu: phải thấy câu trước/sau ngắn, ở đúng chỗ trong cùng email.
- Nói chưa giải quyết nhu cầu: phải thấy câu hỏi khách và lời trả lời còn bỏ sót, không suy diễn từ vẻ mặt một người mẫu.
- Nói năng suất: phải có tổng thời gian viết + sửa và trạng thái chất lượng. Đồng hồ hay thanh 3D trang trí không thể chứng minh điều đó.
- Nói bình luận/đăng ký: giao diện minh họa lời mời hành động liên quan; không có tương tác hay bình luận thật được tạo.

`photoIntent` là yêu cầu tìm ảnh cụ thể, chưa phải asset đã được duyệt. Chỉ map sang ảnh đã mở xem, có URL/license/hash và đúng vật thể/thao tác. Giữ một đèn nhận diện nhất quán trong cùng tình huống; không thay nhiều mẫu đèn khác nhau để tăng số ảnh. Không có quota ảnh cần lấp cho đủ.

## Tình huống và trạng thái

Đèn bàn Mẫu A, thông số USB-C có dây/không pin, giá, số phút và hội thoại đều là **dữ liệu giả định**. Nhãn này phải hiện trong các cảnh có lời hứa, số liệu và kết quả. Ảnh nguồn chỉ minh họa vật thể; không chứng minh những thông số do tác giả đặt là thông số của đơn vị sản phẩm trong ảnh.

Bản nháp có thể hứa “Dùng không dây” hoặc sai giá để minh họa khâu kiểm tra. Nháp chưa gửi. Câu hỏi khách trong hook phải ghi “Phản hồi giả định nếu gửi”, tránh tạo mâu thuẫn với nút gửi bị chặn ở thân bài.

Không cho lỗi tự xuất hiện lại sau khi đã sửa: nếu quay lại bản lỗi phải ghi **Nháp ban đầu**. Ở bản Hidden, kiểm số sửa giá trước; so sánh hình thức sau đó phải giữ giá đã sửa hoặc phân biệt rõ cột nháp cũ. Hoàn thành thật còn cần sửa cam kết và trả lời đúng nhu cầu dùng xa nguồn điện.

## Nhịp hiển thị

Các mệnh đề ngắn “kiểm tra”, “trao đổi”, “hiểu bối cảnh” chỉ dài 0,6–1 giây. `continuityGroup` và `displayPolicy` yêu cầu giữ giao diện/camera đã được giới thiệu, chỉ đổi highlight hoặc trạng thái. Không fade toàn cảnh, chạy intro hay đòi đọc đoạn văn mới trong từng nhịp đó. Một số ô có thể ghim qua nhiều shot để người xem có thời gian đọc.

Bản giải thích đầy đủ theo thời gian: `docs/video-references/2026-11-12-semantic-relearn/storyboards/long.md` và `hidden.md`.
