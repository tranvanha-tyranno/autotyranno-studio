# Kiểm riêng cách gọi chênh lệch giá — pilot siêu thị

Ngày 13/11/2026. Người kiểm: Codex learning_loop, độc lập với người sửa đồ họa.

## Phạm vi thực sự đã kiểm

Đã mở riêng cả hai file đồ họa total-example.jpg và total-change.jpg ở kích thước nguồn 1920×1080. Đã đọc mệnh đề c11 trong production.json, production-v3.json và script.txt của r03; đã đọc báo cáo PRE_RENDER_REVIEW.md của lượt trước. Hồ sơ này chỉ kiểm câu chữ/nhãn và phép tính của ví dụ gốc. Không xem MP4 cuối, không nghe tiếng, không duyệt crop/chuyển động/âm thanh và không ghi người dùng đã chấp nhận video.

## Bản gốc r01 cần sửa nhãn

Đồ họa gốc thể hiện một hộp với tổng 30.000đ, hai hộp với tổng 50.000đ; đơn giá tương ứng 30.000đ/hộp và 25.000đ/hộp. Thanh dưới ghi “TỔNG CHI: +20.000đ”. Dấu cộng gợi một phần tăng, nhưng danh từ “tổng chi” có thể bị hiểu là số tiền cuối. Trong cùng ví dụ, số tiền cuối của phương án hai hộp là 50.000đ; 20.000đ là chênh lệch so với mua một hộp. Báo cáo độc lập trước render đã chỉ ra đúng điểm mơ hồ ở c11 và đề xuất “CHI THÊM” hoặc “TỔNG CHI TĂNG”. Đây là đề nghị sửa độ rõ nghĩa, không phải nói phép trừ 50.000−30.000 đã sai.

## Bản sửa r03 đã kiểm lại trên source graphic

Đồ họa mới vẫn có đúng một hộp bên trái, hai hộp giống nhau bên phải. Tổng 30.000đ và 50.000đ, đơn giá 30.000đ/hộp và 25.000đ/hộp được giữ nguyên. Thanh dưới đổi thành “CHI THÊM 20.000đ”. Mệnh đề nói “số tiền phải trả đã tăng thêm hai mươi nghìn”, phù hợp nhãn mới. Phép tính được kiểm riêng: 50.000−30.000=20.000; 50.000÷2=25.000. Header vẫn ghi “VÍ DỤ GIẢ ĐỊNH · KHÔNG PHẢI GIÁ BÁN”, nên không trình bày các giá này như giá thật ở một cửa hàng.

Kết luận phạm vi script/nhãn: chấp nhận cách gọi chênh lệch mới để dùng cho c11. Điều này không phải chấp nhận toàn video hoặc xác nhận nhãn luôn đọc rõ trong bản MP4. Cần tiếp tục kiểm frame/crop/thời lượng trên r03 sau render.

## Mốc tham chiếu

Timeline exact take của r03 đặt c11 từ frame 3494 tới 3742, tức 116.4667–124.7333giây ở 30 fps. Mốc này chỉ giúp định vị chính mệnh đề khi kiểm bản xuất; r01 chưa có bản MP4 trong hồ sơ kiểm này nên không khẳng định r01 từng hiển thị ở cùng một cut.

## Bài học có thể dùng lại

Mọi số trong đồ họa cần tên đúng đại lượng: tổng cuối, đơn giá hoặc chênh lệch. Khi một số là phần tăng, dùng “chi thêm/tăng thêm/chênh lệch” và giữ hai mốc so sánh nhìn thấy được. Đối chiếu phép tính, số lượng vật thể, đơn vị và câu nói trước render; sau render vẫn phải kiểm độ đọc được.
