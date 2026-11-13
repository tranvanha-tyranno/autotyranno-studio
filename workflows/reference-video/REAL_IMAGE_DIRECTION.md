# Hướng mặc định mới: ảnh thật minh họa lời kể — 12/11/2026

Người dùng chê bản 5 phút thiếu ảnh bên ngoài và dùng 3D quá nhiều, đã cho phép lấy ảnh internet và yêu cầu đổi toàn bộ hướng làm. Chỉ thị này **ưu tiên hơn** mẫu hình 3D được duyệt trước đó. Giọng Nhật Phong và hướng âm thanh đã được duyệt vẫn là chuẩn; không cần tạo lại giọng khi chỉ thay hình.

## Cách lên hình

1. Viết lời kể có luận điểm, ví dụ và chi tiết cụ thể. Tách từng câu/ý thành nhu cầu hình ảnh: người đang làm gì, công cụ gì, vật thể gì, bối cảnh nào.
2. Tìm ảnh/footage internet để thể hiện nhu cầu ấy. Ưu tiên ảnh thật và clip thực có nguồn dùng được. Nhắc chăm sóc khách hàng cần người/headset/cuộc trao đổi; nhắc sửa bảng số cần giấy/bảng/calculator; nhắc chuyển đổi xanh có kỹ sư/pin mặt trời; nhắc học lại cần người đang được hướng dẫn. Không lấy một ảnh laptop cho mọi ý.
3. Xem file thật trước khi đưa vào video. Kiểm tra chủ thể, hành động, nét, tỉ lệ ảnh và crop. Ảnh dọc giữ phần quan trọng bằng contain hoặc bố cục phù hợp; không cắt trán/tay/bảng giấy cho vừa khung ngang một cách máy móc.
4. Đặt cut theo phrase từ exact narration alignment. Dùng chuyển khung/pan/zoom có chủ đích; đó là chuyển động của ảnh tĩnh, không gọi là footage chuyển động hay ảnh AI sinh.
5. Dùng chữ động ngắn ở các mốc cần nhớ, để chủ thể ảnh vẫn rõ. Không che ảnh bằng panel/đoạn chữ dài ở mọi cảnh. 3D/biểu đồ chỉ dùng khi giúp hiểu khái niệm hoặc so sánh số liệu; không để các khối hình thay thế câu chuyện thực tế.
6. Ảnh stock là minh họa; không gán câu chuyện sa thải, phát ngôn hay quảng cáo/endorsement cho người trong ảnh. Ghi nguồn URL, creator khi biết, license, file và SHA-256. Lưu nguồn nghiên cứu riêng với nguồn ảnh.

Tỷ lệ ảnh/video không phải công thức cứng. Bản sửa hiện tại có 88 lần đổi hình, 25 ảnh nguồn được sử dụng, 4 clip stock, 252,23s ảnh + 43,37s clip + 4,40s biểu đồ. Các số đó đo bản dựng, không phải lời hứa mọi chủ đề đều cần 98% ảnh.

## Source và renderer tái dùng

- `web_images.py`: tải bộ ảnh đã chọn qua CDN nguồn, verify decode, giữ manifest nguồn và tạo contact sheet. Catalog hiện thuộc câu chuyện AI/công việc; chủ đề khác cần bộ nguồn mới.
- `visual_story.py`: mỗi shot ghi exact phrase, asset, mục đích hình và crop; canh từ lời đã tạo, giữ audio nguyên vẹn. PLAN hiện biên tập theo câu chuyện này, không phải hệ thống hiểu mọi chủ đề tự động.
- `cinematic/src/visualstory/`: composition `WorkAIVisual5min`, CanvasImage / Video làm chính, pan/zoom deterministic theo frame, brief chart. Public asset namespace `visual-story/` giữ riêng với các bản cũ.
- Batch: `videos/2026-11-12-ai-va-cong-viec-anh-that/`; bản gốc `videos/2026-11-11-ai-va-cong-viec-5phut/` còn nguyên.

Không render nhiều lệnh Remotion dùng chung Rspack persistent cache cùng lúc: lần kiểm tra song song gây cache lock race. Chạy bundle/still/render tuần tự hoặc dùng bundle riêng, không chạy lại các lệnh fail vô hạn. Kiểm tra opacity input ranges luôn tăng nghiêm ngặt; last-shot extension không được tạo hai mốc thời gian bằng nhau. Ảnh cuối mỗi chapter phải kéo qua vùng transition để không ló nền đen.

## QA và bàn giao

Kiểm tra đủ 9000 frame / 300s trên MP4 mới, không coi ảnh nguồn đẹp là đủ. Xem sheet lấy ảnh xuyên suốt thời lượng, keyframe/chuyển động, crop của người và thao tác; đối chiếu cut với lời. Giữ exact mix bằng hash khi chỉ thay hình; đo audio trên MP4 sau mux. Những phép đo không tự chứng nhận thẩm mỹ. Bản hình mới vẫn chờ phản hồi người dùng; việc họ yêu cầu hướng này không đồng nghĩa đã duyệt file chưa xem.

Bài học crop thực tế: contain ảnh dọc không tự động là bố cục tốt. Bản xuất đầu của review-team vẫn còn quá nhiều tường, người nhỏ. Sau xem MP4, bỏ vùng tường thừa bằng crop được lưu riêng và ghi bounding box; vẫn giữ đủ hai đầu, tay và giấy. Kiểm tra vùng hành động, không chỉ tiêu chí không cắt mặt.
