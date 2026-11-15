# R02 — sửa riêng heading o03

QA bản đầu phát hiện heading “Bốn câu hỏi để đọc Trung Quốc” đặt trên ba thẻ chủ đề. R02 đổi thành **“Ba góc nhìn để đọc Trung Quốc”**; không sửa lời đọc, caption, thời lượng hoặc thiết kế cảnh khác.

Đã mở frame thật `review/o03-corrected-mid.jpg`, frame793 /26,433giây trích từ r02final: heading mới đọc đầy đủ, ba thẻ giữ nguyên và phụ đề nằm riêng bên dưới. Đây là quan sát một frame để kiểm lỗi đếm thẻ, không xác nhận nghe/xem liên tục toàn bản hoặc người dùng chấp nhận.

Chỉ render366frame `[614,980)`, gồm o03 và7frame cảnh tiếp để kiểm seam bảo thủ. ChinaFilm hiện hardcut, không có dissolve chồng cảnh. Dùng nguyên frozenbundle và props mới; bytehash của final/data/mix bản đầu được kiểm giữ nguyên trước–sau. Toàn video được normalize/re-encode khi ghép, nên không khẳng định pixel ngoài đoạn sửa giống byte.

Kết quả kỹ thuật: đủ17.913frame,30fps,1920×1080; audio giải mã phủ tới từ cuối. Toàn lượt sửa149,640giây, không có API trả phí. Chi tiết nguồn/guard/timing/SHA trong `repair-receipt.json`. Bản final mới SHA256: `7a6257701b5a6998118d6ce3572b14a5e9066489a6327bebd55f429506c986c1`. QA toàn bản và nghe/đánh giá của người dùng tách riêng.
