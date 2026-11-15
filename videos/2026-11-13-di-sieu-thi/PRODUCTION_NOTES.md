# Bản thử quy trình sản xuất — 13/11/2026

Chủ đề: **Vì sao mua một món lại mang về cả giỏ?** Người dùng yêu cầu nâng cấp quy trình và chọn để agent tự chọn một chủ đề đời sống. Mục tiêu là kiểm cả quy trình có thể dùng lại và một bản dựng cụ thể; không phải xác nhận đã đạt chất lượng như kênh mẫu hoặc đã được người dùng duyệt.

## Bản hiện tại

Manifest `production-v4.json`, batch `r04/long/`, 716 từ tách theo khoảng trắng, take Nhật Phong dài khoảng 203 giây; timeline 205 giây, 30 fps, 1920×1080. Lời cuối có khoảng đệm, không tăng tốc giọng. Có 24 cảnh theo bốn phần hook → lưu ý ngắn → nội dung → CTA. Giao diện ảnh/gallery3D cũ được giữ, bổ sung clip thật trong chính bố cục đó và vài hình giải thích gọn có nhãn giả định.

Kho nguồn có 16 ảnh thật,3 clip thật, bản gốc và bản 720p/30 fps, poster và nguồn/license/hash. Bản dùng chọn 19 tài sản, gồm ảnh/clip và hình minh họa nguyên bản. Không gán việc mua thừa, ý định, địa điểm Việt Nam hay hậu quả thật cho người trong stock. Không dùng tài sản của kênh Lóng trong video mới.

Nhạc nền ghép các stem đã có theo hướng âm thanh được giữ; lời nổi, nhạc duck theo lời. Một cue xử lý túi/đồ mua nhỏ được tạo riêng, đặt thấp dưới cảnh lấy đồ khỏi giỏ. Không thêm tiếng quét máy/thanh toán khi hình không cho thấy thao tác đó. Chất lượng nghe chưa được đồng nhất với phép đo loudness; trạng thái nghe cần ghi theo bằng chứng thực tế.

## Các lần sửa được giữ

- `production.json`: kế hoạch đầu với 23 cảnh; phát hiện vài chỗ hình còn quá rộng so với mệnh đề.
- `production-v2.json`, `r02/`: tách câu nhắc bảng giá ra đúng hình, tách nhãn nghiên cứu với ảnh stock, gọi lại hai hộp bằng chính ví dụ, bổ sung nguồn hỗn hợp. Take không đổi, chưa render final.
- `production-v3.json`, `r03/`: sửa chữ “TỔNG CHI:+20.000đ” thành “CHI THÊM 20.000đ” trong hình mới, giữ hình cũ; chọn nhạc/cue có hash. Bản xuất này được giữ để đối chiếu.
- `production-v4.json`, `r04/`: sau khi mở MP4 r03, sửa c12 bị crop mất số bên trái và a1 bị tiêu đề che dòng danh sách. Hai hình trong panel dùng `fit: contain`, giữ trọn nội dung; bỏ headline thừa. Chỉ render lại hai khoảng, có thêm bảy frame đuôi chuyển cảnh, sau đó ghép và QA toàn bản. Take, mix, caption và timing giữ nguyên; video được encode lại nên không khẳng định pixel ngoài vùng sửa giống byte.
- Lỗi kỹ thuật chuẩn bị: tên asset clip trùng raw MP4 khi compiler cố giữ nguồn theo ID. Đã sửa mã tái dùng giữ filename nguồn và kiểm hash; raw và 720p tồn tại riêng. Regression case được thêm vào test.

## Điều đang được học

Giá đơn vị, tổng chi và chênh lệch chi là ba đại lượng khác nhau. Lời nói, hình vật thể, số, nhãn và mốc xuất hiện phải cùng nghĩa. Khi một mệnh đề nói bảng giá, đổi sang bảng giá ở chính mốc đó thay vì giữ ảnh giỏ rồi chờ câu kế tiếp. Ảnh có nghiên cứu trích dẫn không được làm người xem hiểu là ảnh người tham gia nghiên cứu. Khi nguồn trộn ảnh stock và đồ họa gốc, ghi nhận đủ hai loại.

Các lỗi này được lưu trong `long/PRE_RENDER_REVIEW.md`; lesson được ghi riêng bằng `learning.py`, giữ nguồn và phạm vi xác minh. Kiểm kỹ thuật không tự duyệt thẩm mỹ. Phản hồi người dùng của video mới vẫn pending.

## Kiểm bản xuất

R03 và R04 đều giải mã đủ 6.150 frame / 205 giây. R04 đo âm lượng toàn MP4 khoảng -16 LUFS. Root đã mở toàn bộ 24 keyframe từ R03, ảnh native các cảnh lỗi, ảnh đã sửa R04 và giữ nhận xét độc lập. Agent kiểm hình đối chiếu 24 keyframe và bảy trang chọn mẫu mỗi giây của R03; hai cảnh sửa được kiểm lại từ MP4 R04. Đây là kiểm theo mẫu phủ timeline, chưa phải lượt nghe/xem liên tục toàn video. Âm thanh giữ preset và take gốc, chất lượng nghe chưa được xác nhận bằng tai trong phiên này.

Kho có hàng đợi tuần tự, bước resume kiểm hash, giới hạn bộ nhớ tùy chọn và công cụ sửa riêng cảnh. Điều đó hỗ trợ làm nhiều tập nhưng không bỏ bước nghiên cứu, xem nguồn, đối chiếu lời–hình và nhận phản hồi. Chưa đo năng suất hàng loạt hoặc khẳng định số video/ngày.

## Nguồn nghiên cứu

Đọc `long/research.json` và `long/RESEARCH.md`. Phần lời nói dùng nghiên cứu Inman–Winer–Ferraro (2009) như bằng chứng liên hệ giữa cách chuẩn bị/bối cảnh và quyết định ngoài kế hoạch, không gọi là thử nghiệm nhân quả. Nghiên cứu Gravert–Mormann (2025) được giữ làm nền nghiên cứu giá mua nhiều, không đưa tỷ lệ của tám cửa hàng Thụy Điển thành quy luật Việt Nam. Không dùng các claim lãng phí thực phẩm hoặc khoa học thần kinh không cần thiết.

Giá 30.000đ/một hộp và 50.000đ/hai hộp là ví dụ giả định được viết mới. Số 50.000đ là tổng trả, 25.000đ là giá mỗi hộp, 20.000đ là phần tổng chi tăng so với mua một hộp. Không ghép các số này lên nhãn giá nước ngoài như thể cửa hàng thật đang bán mức đó.


## r05–r07 / Ảnh Việt Nam và hoạt ảnh3D

r05 là lượt still-review giữ lỗi cắt canvas. Góc máy được sửa trong Shopping3D.tsx. r06 giữ take nhưng thay17shot và thêm7object3d/1gallery; lỗi đầy ổ khiến render dừng ở patch02, sau đó resume kiểm2976frame hoàn tất và chỉ xuất1229frame còn lại. State được ghi atomically; patch hỏng và biên nhận failed được giữ. r07 sửa riêng c9 (giá kệ thường không minh họa mức giảm) bằng tag khuyến mại thật crop lớn. Cả r06/r07 đều giải mã6150frame; xem QA và ghi chú chọn mẫu. Giọng, mix, caption, timing và câu cuối giữ nguyên. Bản r07 chờ phản hồi, không gọi các lần render là duyệt thẩm mỹ.
