# Prompt mica v2 — nhịp rõ, 6 giây

Đây là bản phát triển từ bộ gốc, chưa phải kết quả tạo ảnh/video. Dùng mẫu ảnh với tên/tính năng đã được cấp; xem WORKFLOW.md về độ chính xác sản phẩm, chữ và đo 4K.

## Ảnh mở đầu — template

Tạo MỘT ảnh chân thực dọc 9:16, mục tiêu 2160 × 3840 pixel. Đây là ảnh {image_order}/{image_total} của sản phẩm {product_order}, bối cảnh {scene_name}. Không collage, không chia ô, không trộn với sản phẩm khác.
Nguồn nhận diện duy nhất của sản phẩm này: {reference}. Tên được cấp: {name}. Đặc điểm được cấp: {description}.
ƯU TIÊN NHẬN DIỆN: giữ đúng hình dáng, tỷ lệ, màu, vật liệu, logo, từng chữ, nút, màn hình và số, nắp, cổng, đường viền, phụ kiện và số lượng như ảnh tham chiếu. Không tự thiết kế lại, thêm hay bớt. Không lấy tên hoặc chi tiết của sản phẩm khác.
Đặt đúng sản phẩm đó trong {box}. Hộp mica sáng trong, vừa vặn, đế mỏng hợp lý chịu lực, không xuyên cắt hay làm méo sản phẩm. Vật bên trong cố định tương đối với hộp.
Một cẳng tay nữ TRƯỞNG THÀNH đi NGANG vào từ cạnh {arm_side} khung hình. Chỉ thấy một bàn tay và đoạn cẳng tay, móng sơn {nails}; cổ tay ở tư thế tự nhiên, bàn tay nắm chắc quai và nâng cả hộp lơ lửng trước camera ở độ cao ngang ngực của người cầm ngoài khung. Không mặt, tóc, thân, chân hoặc phản chiếu của người. Không tay thừa hoặc ngón thừa. Không đưa tay từ trên xuống. Thấy nguyên quai, hộp và đáy; hộp không chạm bàn, sàn, bục hoặc bất kỳ giá đỡ nào.
Hộp ở giữa, chiếm 55–65% chiều cao ảnh, mặt trước gần song song camera, còn tối thiểu 8% khung trống dưới đáy và 5% phía trên quai/hai cạnh. Camera nhìn ngang, không cắt quai hoặc đáy. Phần sản phẩm luôn rõ nét; hậu cảnh là {background}, mờ nhẹ để vẫn nhìn ra đúng không gian. Ánh sáng trắng trung tính, màu thật, mica phản xạ nhẹ không lóa che sản phẩm.
Nhãn tên và tính năng ở vùng chân/cạnh hộp được dành riêng, nền nhãn gọn, không đè lên sản phẩm; dùng đầy đủ CHÍNH XÁC nội dung sau, giữ dấu tiếng Việt và thứ tự:
{label_text}
Không thêm claim. Không logo/tên hãng/biển quảng cáo trên toàn bộ hậu cảnh hoặc hàng hóa phụ; GIỮ logo gốc trên sản phẩm chính và nhãn hộp. Không watermark. {staging}

## Video — 10 prompt đầy đủ

PROMPT 11 — Bước qua cửa hàng

NHỊP: Video POV 9:16 dài 6 giây. Hành động xuất hiện từ giây đầu, tốc độ đời thường dứt khoát và có chủ đích; hoàn toàn không slow-motion. Camera có chuyển động theo hành động, hậu cảnh tạo parallax rõ; không rung quá đà. Không giữ gần đứng hình nhiều giây. Chuyển động bàn tay/quai và trọng lực phải liền mạch, có tăng/giảm tốc ngắn tự nhiên.

0–0,3s bắt đầu bước ngay; 0,3–4,8s đi 3–4 bước tự nhiên, dứt khoát qua đúng lối cửa có trong ảnh, camera theo nhịp bước, hậu cảnh trôi rõ. Hộp nhún theo bước khoảng 1–3 cm, không lắc mạnh; cổ tay bù để mặt hộp hướng camera. 4,8–6s tiếp tục đi thêm một bước ổn định, không dừng tạo dáng. Không thêm cửa mới.

Đúng MỘT tay nữ trưởng thành giữ quai; không có tay thứ hai.

KHÓA NHẬN DIỆN VÀ KHUNG: Dùng đúng ảnh opening của chính clip này; giữ sản phẩm, hộp mica, quai, số lượng, logo, từng chữ/nhãn, số hiển thị, tỷ lệ, màu móng, phía tay vào và hậu cảnh. Hộp cứng, sản phẩm không trượt bên trong; mặt hộp luôn hướng camera, không xoay lật, không orbit rộng, không thay background. Thấy trọn quai và đáy, khoảng trống dưới đáy tối thiểu 8% chiều cao; không mặt/thân/phản chiếu người, không đặt hộp lên mặt đỡ. Không rung giật, biến dạng, chữ trôi, thêm props/chữ hoặc watermark. Không nhạc/thoại/hiệu ứng âm thanh; voice-over ghép riêng nếu được yêu cầu.

---

PROMPT 12 — Dừng lại quan sát

NHỊP: Video POV 9:16 dài 6 giây. Hành động xuất hiện từ giây đầu, tốc độ đời thường dứt khoát và có chủ đích; hoàn toàn không slow-motion. Camera có chuyển động theo hành động, hậu cảnh tạo parallax rõ; không rung quá đà. Không giữ gần đứng hình nhiều giây. Chuyển động bàn tay/quai và trọng lực phải liền mạch, có tăng/giảm tốc ngắn tự nhiên.

0–3,5s đi ngay 2–3 bước rõ ràng với nhún hộp nhỏ theo bước; 3,5–4,5s dừng chân tự nhiên. 4,5–5,3s hộp đung đưa một nhịp nhỏ giảm dần, camera ổn định theo. 5,3–6s giữ chắc để thấy sản phẩm; không phóng đại dao động hoặc đứng yên phần lớn clip.

Đúng MỘT tay nữ trưởng thành giữ quai; không có tay thứ hai.

KHÓA NHẬN DIỆN VÀ KHUNG: Dùng đúng ảnh opening của chính clip này; giữ sản phẩm, hộp mica, quai, số lượng, logo, từng chữ/nhãn, số hiển thị, tỷ lệ, màu móng, phía tay vào và hậu cảnh. Hộp cứng, sản phẩm không trượt bên trong; mặt hộp luôn hướng camera, không xoay lật, không orbit rộng, không thay background. Thấy trọn quai và đáy, khoảng trống dưới đáy tối thiểu 8% chiều cao; không mặt/thân/phản chiếu người, không đặt hộp lên mặt đỡ. Không rung giật, biến dạng, chữ trôi, thêm props/chữ hoặc watermark. Không nhạc/thoại/hiệu ứng âm thanh; voice-over ghép riêng nếu được yêu cầu.

---

PROMPT 13 — Chuyển hộp sang giữa khung hình

NHỊP: Video POV 9:16 dài 6 giây. Hành động xuất hiện từ giây đầu, tốc độ đời thường dứt khoát và có chủ đích; hoàn toàn không slow-motion. Camera có chuyển động theo hành động, hậu cảnh tạo parallax rõ; không rung quá đà. Không giữ gần đứng hình nhiều giây. Chuyển động bàn tay/quai và trọng lực phải liền mạch, có tăng/giảm tốc ngắn tự nhiên.

Nếu ảnh mở đầu đã giữa khung, 0–1,2s chuyển hộp sang phải khoảng 8–10% bề ngang khung, vẫn thấy trọn hộp; nếu đã hơi lệch phải thì bắt đầu ngay bước tiếp. 1,2–3,2s đưa hộp ngang về chính giữa với cổ tay tự nhiên, không xoay hộp. 3,2–5,5s camera tiến một nhịp nhỏ khoảng 5% để thấy rõ hơn, vẫn dư khung; 5,5–6s ổn định. Không đứng yên chờ chuyển động.

Đúng MỘT tay nữ trưởng thành giữ quai; không có tay thứ hai.

KHÓA NHẬN DIỆN VÀ KHUNG: Dùng đúng ảnh opening của chính clip này; giữ sản phẩm, hộp mica, quai, số lượng, logo, từng chữ/nhãn, số hiển thị, tỷ lệ, màu móng, phía tay vào và hậu cảnh. Hộp cứng, sản phẩm không trượt bên trong; mặt hộp luôn hướng camera, không xoay lật, không orbit rộng, không thay background. Thấy trọn quai và đáy, khoảng trống dưới đáy tối thiểu 8% chiều cao; không mặt/thân/phản chiếu người, không đặt hộp lên mặt đỡ. Không rung giật, biến dạng, chữ trôi, thêm props/chữ hoặc watermark. Không nhạc/thoại/hiệu ứng âm thanh; voice-over ghép riêng nếu được yêu cầu.

---

PROMPT 14 — Hạ hộp nhẹ xuống

NHỊP: Video POV 9:16 dài 6 giây. Hành động xuất hiện từ giây đầu, tốc độ đời thường dứt khoát và có chủ đích; hoàn toàn không slow-motion. Camera có chuyển động theo hành động, hậu cảnh tạo parallax rõ; không rung quá đà. Không giữ gần đứng hình nhiều giây. Chuyển động bàn tay/quai và trọng lực phải liền mạch, có tăng/giảm tốc ngắn tự nhiên.

0–0,3s bắt đầu hạ ngay; 0,3–2s hạ cả hộp khoảng 8–10 cm bằng cẳng tay, không đổi chiều dài quai hay hình hộp. Giữ đáy trong khung với khoảng trống. 2–4,8s camera lùi một bước ngắn hoặc mở khoảng cách nhẹ để giữ trọn hộp, góc nhìn vẫn ngang; 4,8–6s bàn tay nắm chắc cho hộp ổn định. Không chĩa xuống đất hay chạm mặt đỡ.

Đúng MỘT tay nữ trưởng thành giữ quai; không có tay thứ hai.

KHÓA NHẬN DIỆN VÀ KHUNG: Dùng đúng ảnh opening của chính clip này; giữ sản phẩm, hộp mica, quai, số lượng, logo, từng chữ/nhãn, số hiển thị, tỷ lệ, màu móng, phía tay vào và hậu cảnh. Hộp cứng, sản phẩm không trượt bên trong; mặt hộp luôn hướng camera, không xoay lật, không orbit rộng, không thay background. Thấy trọn quai và đáy, khoảng trống dưới đáy tối thiểu 8% chiều cao; không mặt/thân/phản chiếu người, không đặt hộp lên mặt đỡ. Không rung giật, biến dạng, chữ trôi, thêm props/chữ hoặc watermark. Không nhạc/thoại/hiệu ứng âm thanh; voice-over ghép riêng nếu được yêu cầu.

---

PROMPT 15 — Đi ngang kệ trưng bày

NHỊP: Video POV 9:16 dài 6 giây. Hành động xuất hiện từ giây đầu, tốc độ đời thường dứt khoát và có chủ đích; hoàn toàn không slow-motion. Camera có chuyển động theo hành động, hậu cảnh tạo parallax rõ; không rung quá đà. Không giữ gần đứng hình nhiều giây. Chuyển động bàn tay/quai và trọng lực phải liền mạch, có tăng/giảm tốc ngắn tự nhiên.

0–0,3s bắt đầu bước; 0,3–5,5s đi ngang 3–4 bước qua kệ hàng có sẵn, tốc độ đi bình thường dứt khoát. Hậu cảnh trôi ngang rõ, camera đi cùng tay cầm; hộp giữ ở giữa, mặt hộp hướng camera, nhún nhỏ theo chân. 5,5–6s vẫn chuyển động, không dừng lâu. Không sinh thêm thương hiệu/biển quảng cáo trên kệ.

Đúng MỘT tay nữ trưởng thành giữ quai; không có tay thứ hai.

KHÓA NHẬN DIỆN VÀ KHUNG: Dùng đúng ảnh opening của chính clip này; giữ sản phẩm, hộp mica, quai, số lượng, logo, từng chữ/nhãn, số hiển thị, tỷ lệ, màu móng, phía tay vào và hậu cảnh. Hộp cứng, sản phẩm không trượt bên trong; mặt hộp luôn hướng camera, không xoay lật, không orbit rộng, không thay background. Thấy trọn quai và đáy, khoảng trống dưới đáy tối thiểu 8% chiều cao; không mặt/thân/phản chiếu người, không đặt hộp lên mặt đỡ. Không rung giật, biến dạng, chữ trôi, thêm props/chữ hoặc watermark. Không nhạc/thoại/hiệu ứng âm thanh; voice-over ghép riêng nếu được yêu cầu.

---

PROMPT 16 — Camera lùi một bước

NHỊP: Video POV 9:16 dài 6 giây. Hành động xuất hiện từ giây đầu, tốc độ đời thường dứt khoát và có chủ đích; hoàn toàn không slow-motion. Camera có chuyển động theo hành động, hậu cảnh tạo parallax rõ; không rung quá đà. Không giữ gần đứng hình nhiều giây. Chuyển động bàn tay/quai và trọng lực phải liền mạch, có tăng/giảm tốc ngắn tự nhiên.

Một shot do người đứng đối diện giữ camera quay ngang ngực, chỉ tay người cầm xuất hiện. Tay giữ hộp ổn định ở vị trí cũ trong không gian; 0–2,5s camera lùi một bước khoảng 30–40 cm theo trục thẳng, bù góc nhìn để hộp còn giữa khung. 2,5–5,5s camera dịch ngang rất nhỏ 5–10 cm, tay bù tư thế để mặt hộp luôn hướng camera; 5,5–6s ổn định. Hộp thu nhỏ theo phối cảnh tự nhiên, không scale riêng sản phẩm hoặc biến độ dài tay.

Đúng MỘT tay nữ trưởng thành giữ quai; không có tay thứ hai.

KHÓA NHẬN DIỆN VÀ KHUNG: Dùng đúng ảnh opening của chính clip này; giữ sản phẩm, hộp mica, quai, số lượng, logo, từng chữ/nhãn, số hiển thị, tỷ lệ, màu móng, phía tay vào và hậu cảnh. Hộp cứng, sản phẩm không trượt bên trong; mặt hộp luôn hướng camera, không xoay lật, không orbit rộng, không thay background. Thấy trọn quai và đáy, khoảng trống dưới đáy tối thiểu 8% chiều cao; không mặt/thân/phản chiếu người, không đặt hộp lên mặt đỡ. Không rung giật, biến dạng, chữ trôi, thêm props/chữ hoặc watermark. Không nhạc/thoại/hiệu ứng âm thanh; voice-over ghép riêng nếu được yêu cầu.

---

PROMPT 17 — Bước chéo sang trái

NHỊP: Video POV 9:16 dài 6 giây. Hành động xuất hiện từ giây đầu, tốc độ đời thường dứt khoát và có chủ đích; hoàn toàn không slow-motion. Camera có chuyển động theo hành động, hậu cảnh tạo parallax rõ; không rung quá đà. Không giữ gần đứng hình nhiều giây. Chuyển động bàn tay/quai và trọng lực phải liền mạch, có tăng/giảm tốc ngắn tự nhiên.

0–2s người cầm bước chéo trái một bước rõ khoảng 30–40 cm trong đúng lối đi; camera theo cùng chuyển động, hộp giữ giữa và thẳng mặt camera. 2–4,8s bước tiếp một nhịp ngắn về phía trước để hậu cảnh đổi góc tự nhiên. 4,8–6s ổn định dần với nhún nhỏ; không lắc mạnh hoặc xoay hộp, không thêm lối đi mới.

Đúng MỘT tay nữ trưởng thành giữ quai; không có tay thứ hai.

KHÓA NHẬN DIỆN VÀ KHUNG: Dùng đúng ảnh opening của chính clip này; giữ sản phẩm, hộp mica, quai, số lượng, logo, từng chữ/nhãn, số hiển thị, tỷ lệ, màu móng, phía tay vào và hậu cảnh. Hộp cứng, sản phẩm không trượt bên trong; mặt hộp luôn hướng camera, không xoay lật, không orbit rộng, không thay background. Thấy trọn quai và đáy, khoảng trống dưới đáy tối thiểu 8% chiều cao; không mặt/thân/phản chiếu người, không đặt hộp lên mặt đỡ. Không rung giật, biến dạng, chữ trôi, thêm props/chữ hoặc watermark. Không nhạc/thoại/hiệu ứng âm thanh; voice-over ghép riêng nếu được yêu cầu.

---

PROMPT 18 — Tay chỉnh lại quai xách

NHỊP: Video POV 9:16 dài 6 giây. Hành động xuất hiện từ giây đầu, tốc độ đời thường dứt khoát và có chủ đích; hoàn toàn không slow-motion. Camera có chuyển động theo hành động, hậu cảnh tạo parallax rõ; không rung quá đà. Không giữ gần đứng hình nhiều giây. Chuyển động bàn tay/quai và trọng lực phải liền mạch, có tăng/giảm tốc ngắn tự nhiên.

Tay thứ nhất giữ quai từ đầu đến cuối, không buông hoặc đổi tay. 0,3–1,5s tay thứ hai đi ngang vào từ mép đối diện; 1,5–3s đặt ngón tay nhẹ lên phần quai còn trống và chỉnh vị trí nắm một đoạn rất nhỏ, không bẻ quai, không đẩy ngón tay xuyên tay chính. 3–4s tay thứ hai rút hết ra. 4–5,5s camera tiến khoảng 5%, giữ trọn quai/đáy; 5,5–6s ổn định. Hộp luôn được nâng chắc.

Tối đa ĐÚNG HAI tay nữ trưởng thành: một tay giữ quai liên tục, tay phụ chỉ vào làm động tác đã chỉ định rồi rút ra. Không có tay thứ ba; mỗi tay đúng giải phẫu.

KHÓA NHẬN DIỆN VÀ KHUNG: Dùng đúng ảnh opening của chính clip này; giữ sản phẩm, hộp mica, quai, số lượng, logo, từng chữ/nhãn, số hiển thị, tỷ lệ, màu móng, phía tay vào và hậu cảnh. Hộp cứng, sản phẩm không trượt bên trong; mặt hộp luôn hướng camera, không xoay lật, không orbit rộng, không thay background. Thấy trọn quai và đáy, khoảng trống dưới đáy tối thiểu 8% chiều cao; không mặt/thân/phản chiếu người, không đặt hộp lên mặt đỡ. Không rung giật, biến dạng, chữ trôi, thêm props/chữ hoặc watermark. Không nhạc/thoại/hiệu ứng âm thanh; voice-over ghép riêng nếu được yêu cầu.

---

PROMPT 19 — Đưa hộp ngang cửa kính

NHỊP: Video POV 9:16 dài 6 giây. Hành động xuất hiện từ giây đầu, tốc độ đời thường dứt khoát và có chủ đích; hoàn toàn không slow-motion. Camera có chuyển động theo hành động, hậu cảnh tạo parallax rõ; không rung quá đà. Không giữ gần đứng hình nhiều giây. Chuyển động bàn tay/quai và trọng lực phải liền mạch, có tăng/giảm tốc ngắn tự nhiên.

0–0,3s đi ngay; 0,3–5,5s đi 3 bước bình thường ngang đúng khu cửa kính có sẵn, hậu cảnh dịch ngang thấy rõ. Camera đi cùng người cầm, mặt hộp giữ hướng lens; ánh trắng và phản xạ mica thay đổi nhẹ có lý do theo vị trí, không lóe sáng giả. 5,5–6s còn chuyển động ổn định. Không tạo cửa kính/cảnh mới hay phản chiếu mặt người.

Đúng MỘT tay nữ trưởng thành giữ quai; không có tay thứ hai.

KHÓA NHẬN DIỆN VÀ KHUNG: Dùng đúng ảnh opening của chính clip này; giữ sản phẩm, hộp mica, quai, số lượng, logo, từng chữ/nhãn, số hiển thị, tỷ lệ, màu móng, phía tay vào và hậu cảnh. Hộp cứng, sản phẩm không trượt bên trong; mặt hộp luôn hướng camera, không xoay lật, không orbit rộng, không thay background. Thấy trọn quai và đáy, khoảng trống dưới đáy tối thiểu 8% chiều cao; không mặt/thân/phản chiếu người, không đặt hộp lên mặt đỡ. Không rung giật, biến dạng, chữ trôi, thêm props/chữ hoặc watermark. Không nhạc/thoại/hiệu ứng âm thanh; voice-over ghép riêng nếu được yêu cầu.

---

PROMPT 20 — Bước đi rồi chỉ sản phẩm

NHỊP: Video POV 9:16 dài 6 giây. Hành động xuất hiện từ giây đầu, tốc độ đời thường dứt khoát và có chủ đích; hoàn toàn không slow-motion. Camera có chuyển động theo hành động, hậu cảnh tạo parallax rõ; không rung quá đà. Không giữ gần đứng hình nhiều giây. Chuyển động bàn tay/quai và trọng lực phải liền mạch, có tăng/giảm tốc ngắn tự nhiên.

0–4s tay chính xách hộp đi ngay 3 bước rõ, camera theo chân, hộp nhún nhỏ và vẫn thẳng mặt lens. 4–4,3s dừng gọn; 4,3–4,8s tay thứ hai vào từ cạnh đối diện, ngón trỏ hướng vào sản phẩm qua khoảng mica trống mà không che logo/chữ. 4,8–5,3s chỉ ngắn rồi 5,3–6s rút tay ra. Tay chính luôn giữ quai; không chạm/kích hoạt nút hoặc buông hộp.

Tối đa ĐÚNG HAI tay nữ trưởng thành: một tay giữ quai liên tục, tay phụ chỉ vào làm động tác đã chỉ định rồi rút ra. Không có tay thứ ba; mỗi tay đúng giải phẫu.

KHÓA NHẬN DIỆN VÀ KHUNG: Dùng đúng ảnh opening của chính clip này; giữ sản phẩm, hộp mica, quai, số lượng, logo, từng chữ/nhãn, số hiển thị, tỷ lệ, màu móng, phía tay vào và hậu cảnh. Hộp cứng, sản phẩm không trượt bên trong; mặt hộp luôn hướng camera, không xoay lật, không orbit rộng, không thay background. Thấy trọn quai và đáy, khoảng trống dưới đáy tối thiểu 8% chiều cao; không mặt/thân/phản chiếu người, không đặt hộp lên mặt đỡ. Không rung giật, biến dạng, chữ trôi, thêm props/chữ hoặc watermark. Không nhạc/thoại/hiệu ứng âm thanh; voice-over ghép riêng nếu được yêu cầu.
