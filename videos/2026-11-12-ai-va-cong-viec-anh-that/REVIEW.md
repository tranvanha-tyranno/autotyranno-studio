# Bản dựng lại theo hướng ảnh thật — 12/11/2026

Yêu cầu mới: ảnh internet minh họa sát lời kể thay cho việc dùng 3D làm hình chính. Giữ bản 5 phút trước và bản 50s đã duyệt nguyên vẹn.

## Thay đổi

Đã tải/giải mã 27 ảnh Pexels, xem contact sheet và chọn 25 ảnh để sử dụng cùng 4 clip Mixkit có nguồn sẵn. 88 shot theo exact phrase alignment: 252,23s ảnh, 43,37s footage, 4,40s biểu đồ dự báo 170/92. Ảnh/clip khoảng 98,53% thời lượng, nhưng đây là kết quả biên tập bản này, không phải tỷ lệ cố định áp cho mọi đề tài.

Các ảnh thể hiện cụ thể ghi chép, bảng nhiệm vụ, trao đổi với khách, headset, xem bảng số/calculator, phỏng vấn, kỹ sư mặt trời, học máy tính và review tài liệu. Ảnh dọc có contain trên nền mờ để giữ người/bàn tay/hồ sơ thay vì cắt ngang máy móc. Chuyển động ảnh là pan/zoom, không phải chuyển động người thật trong ảnh. Chữ nhấn ngắn ở một số mốc; phụ đề ở vùng đáy. Giảm mạnh số lần phủ chữ lớn lên ảnh.

Giọng và phối âm copy nguyên SHA-256 từ bản 5 phút trước; không gọi API mới cho lần sửa hình. Nguồn hình và giấy phép trong image-sources.json/credits.html; nguồn lập luận trong RESEARCH.md/sources.json. Stock chỉ minh họa, không gán sự kiện sa thải/endorsement cho người trong ảnh.

## Kiểm tra trước render

Đã xem toàn bộ contact sheet ảnh nguồn; kiểm tra frame lớn của kỹ sư mặt trời, headset và bốn người trong trung tâm chăm sóc khách hàng với nhãn ILO. Chữ và ảnh rõ trong ba frame đó. TypeScript pass. Phát hiện last-shot opacity có hai mốc bằng nhau làm Remotion từ chối; đã sửa mốc và kéo shot cuối qua transition để tránh lộ nền đen. Các lệnh still chạy đồng thời làm Rspack cache lock race: đã hoàn thành các still còn lại tuần tự, không coi lỗi cache là lỗi ảnh. Việc nhìn ảnh nguồn không thay kiểm tra final.

Chờ kiểm tra MP4 xuất cuối và phản hồi người dùng. Không suy ra đã được duyệt thẩm mỹ từ yêu cầu đổi hướng.


## Vòng sửa crop sau khi xem MP4

Bản xuất đầu đã decode đủ 9000 frame; đã xem sáu sheet 1fps toàn 300s. Phát hiện ảnh review-team có khoảng tường trống quá lớn, làm hai người và thao tác xem giấy nhỏ. Đã giữ nguyên ảnh nguồn, tạo review-team-detail.jpg với crop pixel [0,1250,2400,3500], xem frame 4600 sau sửa: cả hai đầu, tay và giấy nằm rõ trong khung, không còn phần tường thừa. Lưu derived-assets.json và source snapshot cập nhật. Bản trước crop giữ ở review-before-detail-crop.mp4 và qa-before-detail-crop/. Render lại final từ source đã sửa; không gán các QA của bản trước cho final mới.


## Bản giao cuối sau sửa crop

File mới giải mã đủ **9000 frame / 30fps / 300,00s / 1920×1080**. Đã xem bốn trang keyframe (36 frame), hai sheet lấy mẫu xuyên 150–200s và 250–300s, cùng một trang chuỗi chuyển động trên chính final mới. Bản trước crop đã xem đủ sáu sheet toàn 300s và giữ riêng; không gộp hai phạm vi thành tuyên bố đã xem toàn bộ playback.

Các lần xuất hiện ảnh review-team nay thấy rõ hai người/tay/giấy, không còn vùng tường lớn. Ảnh/headset/giấy/calculator/phỏng vấn/kỹ sư/đào tạo minh họa các ý tương ứng. Biểu đồ chỉ giữ 4,40s; chữ không chiếm cả khung trong phần lớn các shot. Đã xem các dòng cuối/crop và fade; phụ đề nằm đáy, không phát hiện chữ tràn ở các frame kiểm tra. Ảnh dọc có nền mờ và ảnh chính rõ; chuyển động là pan/zoom ảnh tĩnh.

Audio từ exact mix cũ có hash khớp; đo lại trên MP4 **-16,10 LUFS / -4,35 dBTP**, không clipping. Không gọi TTS/music/SFX mới, không tuyên bố đã nghe thủ công. Bản mới chờ phản hồi thẩm mỹ người dùng; hướng ảnh internet đã được lưu làm mặc định theo chỉ thị mới.
