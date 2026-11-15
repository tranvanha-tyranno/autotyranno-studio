# Làm lại vì hình không khớp lời — 12/11/2026

Người dùng bác cả hai mẫu: **“hình ảnh chả khớp lời thoại quá tệ làm lại và học lại đi”**. Đây là lỗi hệ thống chọn hình và kiểm tra, không phải hai ngoại lệ nhỏ. Không lấy lời khen về giọng trước đây làm chấp thuận phần hình của hai bản này.

Đọc audit mới tại `docs/video-references/2026-11-12-semantic-relearn/RELEARN.md`: đối chiếu từng cụm lời với frame thật của video tham chiếu và các bản bị bác. Kiểm tra timing, số frame, số ảnh, độ sáng hoặc chữ không tràn không chứng minh hình có nghĩa phù hợp.

## Cách chọn hình bắt buộc

Mỗi câu/tiểu ý phải nêu được **chủ thể, thao tác, vật thể và trạng thái** cần thấy. Viết ra điều người xem sẽ nhìn thấy để hiểu câu đó, rồi mới tìm ảnh hoặc dựng minh họa. Không đi từ kho ảnh công sở có sẵn rồi viết lý do khớp ngược lại.

- Nói email/bản nháp: phải thấy email đang soạn, chủ đề/nội dung và trạng thái chưa gửi.
- Nói hứa sai tính năng: phải thấy lời hứa cụ thể và thông tin nguồn trái với nó trong cùng mạch hình.
- Nói kiểm tra số: cho hai giá trị đọc được, nguồn gốc và thao tác đối chiếu; một người cầm giấy/calculator chưa đủ.
- Nói sửa giọng điệu: cho câu trước/sau, phần sửa và ý nghĩa thay đổi.
- Nói phản hồi/khách có nhu cầu: cho yêu cầu và câu trả lời; ảnh người đeo headset không tự diễn đạt vấn đề.
- Nói tổng thời gian/năng suất: ghi riêng viết, sửa, tổng và chất lượng; không dùng đồng hồ trang trí hoặc người ghi sổ để thay kết quả đo.
- Nói gửi/bình luận: phải thấy đúng thao tác và trạng thái liên quan, không dùng ảnh họp/phỏng vấn.

Ảnh thật chỉ hỗ trợ phần nó thực sự thể hiện. Metadata có thể sai: ảnh Pexels 31726764 được mô tả là đèn bàn nhưng file thật là máy chiếu, đã loại và giữ bằng chứng. Ảnh đèn không xác minh nguồn điện, pin hoặc giá của tình huống. Màn hình minh họa và số liệu do tác giả đặt phải có nhãn dễ thấy, không giả làm tư liệu sự kiện hoặc thông số thật.

## Bản làm lại

Hai hướng vẫn riêng: Lóng tham chiếu nhịp ví dụ trực diện; The Hidden Self tham chiếu mạch phân tích. Giữ cấu trúc hook → miễn trừ → nội dung → CTA, giọng Nhật Phong và exact mix của từng bản. Phần hình được dựng lại từ đầu theo một tình huống giả định nhất quán: email giới thiệu Đèn bàn Mẫu A, lời hứa dùng không dây mâu thuẫn thẻ nguồn có dây/không pin. Mọi tính năng, giá và thời gian của ví dụ đều là dữ liệu giả định, không phải video review sản phẩm.

`semantic-profiles/` ghi toàn bộ câu được nói trong từng khoảng, word index, anchor, ý nghĩa, điều bắt buộc phải thấy, hình thay thế bị cấm và kiểm tra cần làm. `semantic_rebuild.py` kiểm tra không bỏ/lặp từ, timeline phủ đủ và hash audio. `cinematic/src/semantic/` thực hiện thao tác bằng hình email, bảng nguồn, lời phản hồi, sửa câu và bảng thời gian có chuyển động; Three.js dùng cho vật thể và mối quan hệ thật sự cần giải thích.

Không cố đạt một số lượng ảnh. Đổi ảnh nhiều mà không diễn đạt ý vẫn là lỗi. Các bước rất ngắn phải giữ cùng không gian thao tác để người xem theo dõi, không liên tục bật lại hiệu ứng vào cảnh.

## Kiểm tra có bằng chứng

Trước render cuối, mở từng cặp **toàn bộ câu nói ↔ frame thực** và kiểm từng điều trong visibleFacts. Trạng thái thiết kế trong profile luôn là chờ kiểm tra; không tự đổi thành passed nhờ schema/timing đúng. Cần ghi điều thực thấy, trạng thái đạt/sửa, đường dẫn frame và giới hạn cho từng shot.

Sau render, giải mã đủ frame, đối chiếu các cặp trên chính MP4 mới, mở chuỗi frame thể hiện thao tác đổi trạng thái, đo mix và kiểm câu kết. Nếu mismatch còn tồn tại phải sửa trước bàn giao; không hạ thành ghi chú “stock theo ngữ cảnh” để cho qua. Không suy ra thẩm mỹ đã được người dùng duyệt hoặc đã nghe bằng tai từ kiểm tra kỹ thuật.

Batch mới: `videos/2026-11-12-hai-huong-khop-loi/`. Giữ nguyên mọi batch bị bác để đối chiếu. “Học lại” ở đây là sửa cách chọn hình, nguồn, mã và kiểm tra; không phải huấn luyện trọng số mô hình.

## Chạy và phục hồi xuất file

`semantic_render.py` tạo bundle/public riêng; proof phải được người kiểm tra ghi quan sát thật theo từng shot và hash ảnh trước khi render. Khi máy thiếu dung lượng, dùng action `chunks` để xuất video không tiếng theo đoạn frame ngắn, ghép đúng thứ tự rồi mux nguyên mix. Không lặp hình, không thay đổi tốc độ, không cắt lại lời. Chạy `semantic_qa.py` trên file ghép cuối để kiểm số frame, toàn bộ cặp lời/hình, chuỗi thao tác và âm lượng.

Ổ C gần đầy đã gây hai lần xuất dài thất bại ở batch này; giữ log. Nén lưu trữ NTFS không mất dữ liệu đã được dùng cho các tệp dự án để giảm chỗ trên đĩa, không sửa nội dung file. Các MP4/mix/bằng chứng cũ giữ nguyên; không coi lần render dừng giữa chừng là sản phẩm hoàn tất.
