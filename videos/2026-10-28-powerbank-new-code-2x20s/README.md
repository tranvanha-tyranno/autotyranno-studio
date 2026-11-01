# Hai video review sạc dự phòng tím — 28/10/2026

Đầu ra: hai bản 20 giây, 9:16, 720 × 1280, 30 fps, giọng Việt Adam / eleven_v3. Mỗi bản ba nguồn độc lập 10 giây ở tốc độ hình 1,5×; giọng căn riêng. Không chèn chữ, không loop hoặc kéo chậm.

## Nội dung

Bản 1 mở bằng “Nhìn như hộp phấn, hóa ra sạc dự phòng!”; bản 2 mở bằng “Sạc dự phòng mà tím như kẹo!”. Thoại dựa trên hình dáng, màu tím, quai đồng màu và ô báo mức pin thấy trong ảnh, kết bằng CTA giỏ hàng và chọn đúng phiên bản. Không thêm giá/dung lượng/công suất chưa kiểm chứng.

## Hình thực tế

Sau QA, chuyển sang các cảnh cận để giữ sản phẩm đúng góc chéo; hai nhân vật hư cấu có áo kem/tóc cột thấp và áo xanh/tóc bob. Các nguồn medium bị xoay đứng hoặc làm xám ô đen đã bị loại và giữ nguyên trong các revision.

Bản 1 tái dùng hai cảnh cận đã duyệt của mẫu tím khớp ngoại hình từ batch trước, có `reuse-provenance.json`, và dùng một nguồn cận mới. Bản 2 dùng ba nguồn cận mới từ ảnh của nhân vật áo xanh. Không mô tả các nguồn cache là sinh mới. Ảnh gốc của lần này và crop sản phẩm vẫn được lưu riêng.

## QA

Chân dung tách riêng được kiểm tra trước ảnh cảnh. Ảnh mở đầu được kiểm tra trước khi gọi video. Nguồn được xem bằng 20 khung/10 giây; final có giải mã toàn thời lượng, đo âm lượng, tìm đoạn đen/đứng hình, contact sheet toàn video, khung cuối và đo độ sáng sau hiệu chỉnh.

Số/ký tự nhỏ trên ô đen vẫn do AI tái dựng và có thay đổi. Độ nghiêng và nhịp dừng không được xác nhận chính xác bằng số. Các cử chỉ miết vỏ và dáng sản phẩm được xem trực tiếp trong QA; không có cam kết sao chép tuyệt đối từng chi tiết nhỏ.

## Kịch bản

### variant-01

[surprised] Nhìn như hộp phấn, hóa ra sạc dự phòng! [playful] Tím pastel, bo góc xinh ghê, mấy ní!

[upbeat] Vỏ trơn, quai đồng màu, có ô báo mức pin. [explaining] Liếc nhanh để chủ động chuẩn bị trước khi ra ngoài.

[encouraging] Thích kiểu gọn xinh này? Bấm giỏ hàng, kiểm tra thông số, chọn đúng phiên bản rồi chốt đơn nha!

### variant-02

[excited] Sạc dự phòng mà tím như kẹo! [playful] Bo góc, có quai đồng màu; đặt cạnh đồ đi làm nhìn hợp ghê.

[upbeat] Xoay nhẹ, chạm lớp vỏ trơn nè. [explaining] Ô báo mức pin ở mặt trước giúp mình tiện theo dõi.

[encouraging] Mê màu tím này thì bấm giỏ hàng, xem kỹ thông số, chọn đúng phiên bản rồi đặt mua nha!

## File hoàn tất

- `01-sac-du-phong-tim-20s.mp4` — 20 giây, nhân vật áo kem, một nguồn mới + hai nguồn cache đã duyệt.
- `02-sac-du-phong-tim-20s.mp4` — 20 giây, nhân vật áo xanh, ba nguồn mới.
- `FINAL-QA.json` — duration, resolution, fps, audio, sáu hash nguồn khác nhau, hash final và giới hạn còn lại.

Hai final đã giải mã toàn thời lượng, không báo đen/đứng hình; ảnh toàn timeline và khung cuối đã xem sau hiệu chỉnh sáng. Bộ kiểm tra workflow: 17 bài qua.
