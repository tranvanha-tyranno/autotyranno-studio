# Hai hướng kể chuyện — bản mẫu mới

Đối chiếu ba mẫu Lóng và ba mẫu THE HIDDEN SELF bằng media, các frame mở/thân/kết và transcript theo thời gian. Không tuyên bố đã nghe hoặc xem liên tục toàn bộ sáu nguồn. Audit và URL tại source-snapshot/REFERENCE_AUDIT.md.

Hai bản dùng chủ đề AI/công việc để so sánh hướng kể, không phải hai video dài năm phút. Mỗi bản đủ hook → miễn trừ ngắn → nội dung → CTA, có kịch bản riêng, giữ giọng Nhật Phong, timing từ chính take mới ở tốc độ 1.0 và công thức phối âm speech-first.

| Bản | Thời lượng / frame thực | Ảnh riêng / shot / lượt đặt ảnh | Gallery ảnh 3D | Âm lượng MP4 |
|---|---|---|---|---|
| long/final.mp4 | 82s / 2460 | 23 / 26 / 33 | 7,70s | -16,07 LUFS / -4,96 dBTP |
| hidden/final.mp4 | 83s / 2490 | 24 / 26 / 33 | 10,27s | -16,03 LUFS / -4,83 dBTP |

Cả hai 1920×1080, 30fps; giải mã đủ từng frame. Đây là kiểm tra kỹ thuật, không phải chứng nhận thẩm mỹ.

## Quan sát hình thực tế

Root đã mở ba sheet 1fps toàn thời lượng của từng MP4 cuối. Bản Lóng còn mở chuỗi chuyển động hai gallery và keyframe kết; reviewer độc lập xem thêm frame lớn/giấy/disclaimer/gallery. Bản Hidden đã xem lại cả ba sheet sau sửa font và frame lớn 1311/2253 trên chính MP4 mới. Phạm vi và giới hạn chi tiết tại long/VISUAL_REVIEW.md và hidden/VISUAL_REVIEW.md.

Ảnh người, viết, giấy, calculator, headset, trao đổi và học tập làm phần hình chính; gallery dùng các plane có texture trong Three.js, không phải gọi ảnh phẳng thành footage. Bản Lóng dùng cream/coral và chữ sans; bản Hidden navy/teal và chữ serif. Ảnh dọc giữ chủ thể trên nền mờ. Các frame đã xem giữ tiêu đề/caption ở hai vùng riêng, không thấy texture mất hoặc khoảng đen bất thường.

Vẫn có hình minh họa bối cảnh chung: khoảng 3,73s của bản Lóng dùng sổ ghi cạnh laptop cho câu nói bản nháp trên màn hình; khoảng 20s dùng headset để dẫn vào ví dụ email. Chúng chưa trực tiếp bằng hình email thực tế. Chuyển động 3D là gallery có chiều sâu với dịch chuyển nhẹ; phần lớn thời lượng vẫn là ảnh tĩnh pan/zoom. Không gán sự cố AI hoặc lời bảo chứng cho người trong ảnh stock.

## Những lần sửa được giữ lại

Lần xuất đầu báo Chrome thiếu bộ nhớ/dung lượng tạm; job đọc bundle tạm của job đó cũng mất asset khi thư mục bị dọn. Đã chuyển sang ảnh render nhỏ hơn có hash/kích thước dẫn xuất, bundle bền vững và render tuần tự concurrency 1. Có log lỗi trong mỗi thư mục; ảnh nguồn không đổi.

Bản Hidden đầu có font Georgia thiếu ký tự tiếng Việt, làm dấu rời chữ. Đã giữ review-before-vietnamese-font-fix.mp4 và qa-before-vietnamese-font-fix/, thay bằng Times New Roman có đủ cmap, chuẩn hóa NFC và xuất lại. Hai still kiểm tra trước render và hai frame lấy từ MP4 mới đều hiện đúng “Quay về nguồn”, “Nhiệm vụ nào tiếp theo?”. Font hashes/glyph proof tại hidden/font-validation.json.

Nguồn ảnh/giấy phép/hash trong từng image-sources.json và credits.html; bản render dẫn xuất trong render-assets.json; stem, receipt và alignment trong audio/. Không có credentials trong source snapshot. Không tuyên bố đã nghe bằng tai dựa trên đo loudness/timestamps. Hai mẫu mới chờ phản hồi người dùng; các batch trước vẫn được giữ nguyên.
