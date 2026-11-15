# Video thử đã nâng cấp — r07

Xem [trang phát và đối chiếu lời–hình](index.html) hoặc [MP4 mới](r07/long/final.mp4): **3 phút25 giây,1920×1080,30fps,6150frame**. [Manifest r07](production-v7.json) giữ24mệnh đề, timing, nguồn và giới hạn. Các revision cũ được giữ nguyên.

Đã thêm khoảng một phút3D: giỏ nhận từng món, so một/hai hộp và tổng tiền, hành trình ở nhà → trên kệ → tại quầy. Ảnh siêu thị/chợ Việt Nam có chứng cứ địa điểm, tác giả và giấy phép; đọc [credit](r07/CREDITS.md). Một số ảnh tủ lạnh/đồ ở nhà vẫn là stock minh họa, không được gán địa điểm Việt Nam. Giá trên ảnh tư liệu không phải giá hiện nay;30k/50k/25k/+20k trong cảnh3D là ví dụ giả định riêng.

Phần **MIỄN TRỪ TRÁCH NHIỆM** tách riêng ngay sau hook ở18,53–27,17s. Giữ nguyên take Nhật Phong, script, alignment và mix của r04. Câu cuối và đuôi thoại được giữ đầy đủ.

## Kiểm tra và giới hạn

- Full MP4 giải mã đủ6150frame. [QA kỹ thuật](r07/long/qa/report.json) ghi hash video, đo âm lượng và tổng60,5s3D, trong đó53,73s hoạt ảnh đối tượng.
- Root mở24midframe,40mẫu chuyển động3D và frame c9 ở kích thước native. [Quan sát thực tế](r07/long/qa/RENDERED_VISUAL_REVIEW.md); [cảnh nhãn khuyến mại đã sửa](r07/SEMANTIC_CORRECTION.md). Đây là kiểm chọn mẫu, không phải lượt nghe/xem liên tục.
- r05 giữ lỗi cắt sát mép canvas và được sửa góc máy; r06 giữ lỗi giá kệ thường thay cho mức giảm. r07 dùng tag thật có giá cũ/mới rõ và ghi ngày tư liệu.
- Một số ảnh được dùng lại; các cảnh ảnh vẫn có pan/zoom nhẹ. h1b/c8 dùng khuyến mại như bối cảnh, phụ đề che một phần con số; c9 dùng crop lớn để đọc rõ mức giảm.
- Bản mới **chờ phản hồi người dùng**, chưa được tự đánh dấu đẹp/được duyệt.

## Quy trình dùng lại

`production.py` hỗ trợ policy ảnh Việt Nam có chứng cứ, disclaimer rõ và `object3d` với cue theo take thật. `production_repair.py` giữ nguyên thoại/timing khi sửa riêng cảnh; thêm resume kiểm snapshot, bundle và patch đã giải mã để tiếp tục sau lỗi dung lượng. `render_directions.py` ghi receipt atomically để giữ bản ghi trước khi đầy ổ. [Biên nhận r06](r06/long/repair-receipt.json), [biên nhận r07](r07/long/repair-receipt.json).

Vòng học ghi phản hồi người dùng và bài học theo bằng chứng; cải tiến code/profile không phải huấn luyện trọng số. Đọc [ghi chú sản xuất](PRODUCTION_NOTES.md) và các hồ sơ trong `learning/`. Không tự lên lịch hoặc đăng video.
