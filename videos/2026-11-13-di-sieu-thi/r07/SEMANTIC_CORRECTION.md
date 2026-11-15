# r07 c9 — kiểm nguồn sửa khớp lời

**Trạng thái: đã kiểm asset/cấu hình; chờ frame render cuối của c9.** Chưa đánh dấu r07 accepted hoặc sửa này verified.

Đã mở trực tiếp `production-public/directions/long/vn-promotion-close.jpg` và đọc c9 trong `../production-v7.json`. Crop `[0, 0.63, 1, 1]` giữ phần chai, nhãn **KHUYẾN MẠI**, giá cũ **19.600 đ/CHAI** bị gạch đi, giá mới **15.400**, cùng timestamp **2022.04.20 10:29**. Đây là mức giảm nhìn thấy thật trên ảnh, giải quyết thiếu sót ở frame r05/c9: hai ảnh giá thường trước đó không thể hiện giảm giá khi lời đọc nói “Nhìn một mức giảm”.

c9 mới đặt crop khuyến mại bên trái, ảnh sốt/giá/khối lượng bên phải; cả hai dùng contain. Source note nêu Phat14082005 / Lcsnes, CC BY-SA 4.0, tư liệu 2022/2020 và không phải giá hiện tại. Asset mới giữ nguồn gốc ảnh VinMart tại Việt Nam; chi nhánh cụ thể chưa được nguồn xác nhận.

Giới hạn: nhãn này là tư liệu lịch sử, không là giá bán hiện hành, không liên quan trực tiếp tới ví dụ giả định 30k/50k của c10. Ảnh sốt bên phải hỗ trợ bối cảnh đọc giá/khối lượng; các sản phẩm/khối lượng khác nhau không phải bằng chứng mức giảm. Không ảnh nào chứng minh tổng tiền một giỏ, ý định hay quyết định của khách hàng. Phép tính tổng tiền vẫn cần được giải thích bằng cảnh cơ chế/số giả định kế tiếp.

Khi c9 render xong, phải mở frame đúng cụm “Nhìn một mức giảm” để kiểm nhãn giảm giá thực sự hiện rõ, giá cũ/mới còn đọc được, source note/phụ đề không che tag, và hai ảnh tách khỏi phép tính giả định. Kiểm source crop này không thay cho QA motion/full video hoặc phản hồi người dùng.

SHA-256 crop public: `63d00833dcd7517dfc93ec064bc6c9c20e9bb67795d85a581ce84b62ae788e68`

SHA-256 ảnh nguồn nguyên: `a43c24b279cb3798e06f0c0bcab217c28826bcc75dbf6ce93ac6ea5e61e19697`

Phương pháp: xem ảnh crop thật và đọc manifest; chưa xem frame cuối r07/c9, chưa nghe/xem AV toàn bản. Không sửa manifest, renderer hoặc ledger.

Ghi nhận dung lượng: lần ghi đầu gặp C: đầy. Query-cache do agent tạo `../vietnam-sources/research-search.json` đã được nén lossless thành `research-search.json.gz` (1,383,624→102,999bytes); giải nén đã đối chiếu toàn byte. SHA-256 nội dung JSON gốc: `71a40eeeb281167994b54da29eee1bd3437448d400a083a795ed617b01501d01`. Ảnh, metadata các nguồn đã chọn, catalog và render được giữ nguyên.

## Cập nhật sau render cuối — chỉ c9

Đã mở riêng **frame03121,104.03s** từ `long/qa/frame-03121.jpg` (1920×1080) của MP4 cuối r07; đây là frame thực, không phải preview/source crop. Phụ đề tại frame đọc “Nhìn một mức giảm, ta rất dễ chỉ hỏi”.

Panel trái hiện trọn nhãn **KHUYẾN MẠI**, giá cũ **19.600 đ/CHAI** có gạch, giá mới **15.400** lớn và timestamp **2022.04.20 10:29**. Nhãn cùng các số nằm trên credit và phụ đề, không bị hai dòng này che. Panel phải vẫn có sản phẩm/khối lượng và thẻ giá sốt; không gán khác biệt kích cỡ thành giảm giá. Source note đọc được, gồm Phat14082005 / Lcsnes, CC BY-SA4.0 và “Không phải giá hiện tại”.

**Kết luận đúng phạm vi:** thiếu vật thể “mức giảm” đã được sửa trong frame c9 được mở; nguồn khuyến mại thật nay hiển thị đồng thời với cụm lời tương ứng. Nhận xét này thay trạng thái chờ frame ở phần kiểm source phía trên cho đúng một frame/đối chiếu này. Nó không duyệt thẩm mỹ toàn video, không chứng minh mọi frame của c9 đều giống nhau, không xác nhận nghe AV liên tục và không là người dùng chấp nhận r07. Giữ nguyên giới hạn giá lịch sử/không liên quan phép tính giả định ở phần trên.

SHA-256 frame cuối đã mở: `e60d52dcd59eb86bb911e35308be64f6cf9710257fe08a9382864fc75a61ea6a`

SHA-256 MP4 cuối r07: `2cc81a55ab125afaa38cee6dc9e1d96ef7dc69b3016f9ba04a80126e1fd0f861`

Không sửa manifest, renderer hoặc ledger; chỉ nối quan sát actual-render vào ghi chú này.
