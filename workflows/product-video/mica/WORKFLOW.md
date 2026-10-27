# Bộ mica — N ảnh → N × 3 ảnh và clip POV 6 giây

Bộ gốc người dùng cung cấp được giữ trong [original-prompts.txt](original-prompts.txt). Phiên bản phát triển do code sinh thành [optimized-prompts.md](optimized-prompts.md). Dùng bộ này khi yêu cầu **hộp mica xách tay**; không tự đổi mọi yêu cầu video sang mica. Chế độ này thay thế quy tắc review 20 giây/3 cảnh khi được chọn.

## Quy tắc ảnh mở đầu

Mỗi ảnh sản phẩm đầu vào là một mục riêng, theo thứ tự tải lên. Mỗi mục xuất **ba ảnh riêng**, lần lượt: **trung tâm thương mại → siêu thị gia dụng/điện máy → xưởng sản xuất**. Không collage. Không trộn sản phẩm giữa các ảnh, không thêm bản sao hoặc tự nhân phụ kiện. Với mỗi mục, chỉ dùng ảnh tham chiếu của chính mục đó.

Mục tiêu ảnh dọc **2160 × 3840**. Phải đo file đầu ra; nếu provider trả nhỏ hơn thì ghi rõ kích thước gốc và bản upscale. Chữ “4K” trong prompt không xác nhận chất lượng hay kích thước thực.

Giữ sản phẩm đúng ảnh: hình, tỷ lệ, màu, vật liệu, logo, chữ, nút, màn hình, nắp, cổng, đường viền và phụ kiện. Đây là yêu cầu ưu tiên và tiêu chí kiểm tra, **không phải khả năng giữ đúng tuyệt đối của mô hình sinh ảnh**. Nếu chữ/chi tiết quan trọng bị đổi: ưu tiên compositing vùng sản phẩm gốc và nhãn bằng code; không chấp nhận chỉ vì ảnh trông đẹp. Camera mặt trước giúp giảm mặt khuất phải suy diễn.

Hộp mica vừa vặn, đế mỏng nhưng có cảm giác chịu lực, không xuyên cắt sản phẩm. Ba kiểu hộp/quai và màu móng khác nhau; cùng một ảnh khi chuyển sang video phải giữ đúng kiểu hộp và màu móng đã chọn. Hộp chiếm khoảng 55–65% chiều cao, nằm hoàn toàn trong khung, còn ít nhất 8% khoảng trống phía dưới, 5% phía trên quai và hai cạnh. Cẳng tay nữ trưởng thành vào ngang từ mép bên; chỉ bàn tay và cẳng tay, không mặt, không phần thân/reflection của người. Bàn tay giữ chắc quai, trọng lực và cổ tay hợp lý. Hộp treo ở tầm ngực của người cầm ngoài khung; không để tay từ trên xuống hoặc đặt hộp trên mặt đỡ. Mỗi scene giữ cố định phía tay vào.

Nhãn có đúng tên và toàn bộ tính năng/công dụng **được cung cấp**; không đoán từ kiểu dáng. Nhãn ở vùng đế hoặc cạnh dành riêng, không đè lên sản phẩm. Chữ nhiều thì chia nhãn ở các cạnh trống hoặc mở rộng phần chân nhãn hợp lý; nếu không đủ chỗ thì đánh dấu cần chỉnh layout, không bỏ tính năng âm thầm. Giữ logo gốc trên sản phẩm và nhãn. Không logo/nhãn hãng/biển quảng cáo ở toàn bộ nền, kể cả nhãn trên đồ trưng bày; không xóa logo sản phẩm chính. Không watermark. Ánh sáng trắng trung tính, nền mờ nhẹ, màu trung thực.

**Cách ổn định chữ:** lưu `label_text` riêng trong JSON, tạo chữ tiếng Việt bằng PIL/SVG theo font có dấu rồi compositing/tracking lên vùng nhãn khi cần. Không giao cho LLM nhiệm vụ căn chữ hoặc sửa từng frame. Nếu chưa thực hiện compositing thì phải ghi “chữ sinh bởi AI, chưa kiểm chứng”, không tuyên bố khóa chữ.

## Nhịp chuyển động mới

`final4.mp4` được kiểm tra qua contact sheet và các mẫu ảnh, metadata container là 20 giây, 720 × 1280, 30 fps. Các mẫu cho thấy ấm đứng trên bàn với các động tác tay tương tự và camera dịch góc ít; tăng tốc thôi không tạo được hành động mới. Báo cáo ở `docs/video-review/final4/` ghi phép đo thay đổi pixel để tham khảo, không dùng nó thay đánh giá cảm giác tốc độ.

Clip mới **6 giây**, hành động bắt đầu trong **0–0,3 giây**, có khoảng dịch rõ trong 1–2 giây đầu, hoàn tất chính trong khoảng 3–4,5 giây, giữ đoạn nghỉ cuối tối đa 0,5–1 giây khi hành động cho phép. Tránh “đi chậm”, “từ từ”, “cực nhẹ”, “slow cinematic”, “micro-orbit”, “long hold” trong phiên bản nhanh. Bước đi tự nhiên dứt khoát, không chạy, không rung máy bừa hoặc làm hộp lắc mạnh. Nhún vật lý khoảng 1–3 cm, không biến thành vật thể quay 3D. Không xoay hộp, lật sản phẩm hoặc orbit rộng: **mặt hộp luôn hướng camera**.

Quãng dịch theo từng prompt chỉ là chỉ dẫn tạo chuyển động; không báo là số đo thực tế nếu chưa tracking. Không bắt buộc áp cùng tốc độ hậu kỳ 1,5× cho mọi cảnh. Kiểm tra hành động trước; nếu provider trả 10 giây cho yêu cầu 6 giây, chọn 6 giây có động tác tốt. Chỉ tăng tốc nếu không làm tay/hộp giật; không kéo chậm hoặc giữ ảnh cuối để lấp đủ 6 giây. Nếu không đủ chuyển động thì sửa đúng cảnh lỗi, tối đa một lần sinh lại tự động cho một bản prompt, rồi báo giới hạn thay vì lặp tốn quota.

Prompt 11/19 cần cửa/cửa kính có sẵn trong ảnh. Prompt 15 cần kệ. Prompt 17 cần lối đi bên trái. Nếu ảnh thiếu điều kiện, compiler bỏ qua prompt đó và ghi lý do; không biến đổi cửa hàng hoặc thêm cửa giữa video. Prompt 18 và 20 cho phép **đúng hai tay**: một tay luôn giữ quai, tay kia vào làm động tác rồi ra; các prompt khác **đúng một tay**. Không dùng một khóa “chỉ một tay” mâu thuẫn cho tất cả.

## Vận hành tiết kiệm

1. Agent/LLM đọc ảnh một lần, xác định tên và claim được cấp, viết manifest nhỏ (mẫu `example.json`). Không tự bổ sung claim sản phẩm.
2. `python workflows/product-video/mica/compile.py --config workflows/product-video/mica/example.json --output videos/mica-prompts-demo` tạo **gói prompt offline**, đếm N × 3, lưu nhãn chính xác và đánh số. Không có API call. Output phải là thư mục mới để không trộn với lần trước.
3. Tạo ba ảnh opening cho mỗi sản phẩm bằng Muse2API, cache theo ảnh + prompt. Xem ảnh rồi cập nhật `capabilities` của từng bối cảnh đúng nội dung ảnh. Không gọi cả 10 video khi người dùng chỉ yêu cầu lưu prompt hoặc chỉ muốn một vài clip.
4. Chọn prompt phù hợp ảnh: đi bộ/kệ cho biến thể rõ chuyển động, đổi tâm/hạ hộp cho động tác đơn giản dễ giữ chữ. Tạo clip 6 giây từ đúng ảnh opening. Chưa có runner API mica riêng; gói compiler là prompt/plan, **không phải video đã tạo**. Không truyền trực tiếp vào `run.py` review 20 giây vì schema và staging khác nhau.
5. FFmpeg/code đo duration, fps, resolution; trích mẫu 0,5/1/2/4/5,8 giây và khung cuối. Kiểm tra toàn hộp/quai/đáy trong khung, không mặt, chữ/nhãn ổn định, số tay đúng, hoạt động bắt đầu sớm. Cần xem playback để xác nhận nhịp; contact sheet chỉ hỗ trợ kiểm tra hình. LLM/vision tập trung vào lỗi hình học/hành động khi có nghi vấn; không polling hoặc đọc log liên tục bằng LLM.

Giữ nguyên file người dùng đưa. Chỉ tạo video/gọi provider trong lần người dùng yêu cầu thực thi, không coi prompt được lưu là quyền tự chạy cả N × 3 × 10 video.
