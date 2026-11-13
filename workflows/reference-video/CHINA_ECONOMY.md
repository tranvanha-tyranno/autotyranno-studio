# Explainer kinh tế bằng đồ họa nguyên bản — Trung Quốc

Nhánh này đáp ứng yêu cầu riêng về video kinh tế khoảng mười phút: bản đồ, biểu đồ, sơ đồ truyền dẫn và mô phỏng có chuyển động làm chính; ảnh/footage đúng bối cảnh bổ trợ. Không ép hướng ảnh/gallery của bài siêu thị lên mọi chủ đề quốc tế. Giữ giọng Nhật Phong, hook → miễn trừ ngắn → nội dung → CTA, không thêm nhận diện kênh hay chữ thương hiệu bị cấm. Video mới **chờ phản hồi**; kiểm kỹ thuật không tự nâng thành duyệt.

## Mã và dữ liệu

- `china.py`: manifest `china-economy/1`, chương/beat nguyên bản, ghép take đúng tốc độ tự nhiên, căn lời theo alignment của chính take, compile `data.json`/`props.json` và namespace riêng `production-public/china/`.
- `cinematic/src/china/` và `china-entry.tsx`: composition `ChinaPreview`; `c-map`, `c-flow`, `c-chart`, `c-sim`, `c-compare`, `c-question`, `c-photo`, `c-closing`. Xem [hợp đồng và giới hạn hình](cinematic/src/china/README.md). Các chuyển động SVG/2D không được gọi thành footage thật hoặc Three.js 3D.
- `china_audio.py`: lời mới được đo chi phí theo request; nhạc/SFX liên quan công nghiệp–cảng–đường sắt–giấy/số liệu, không dùng mặc định máy pha cà phê. Xem [âm thanh và usage](CHINA_AUDIO.md).
- `china_render.py`: bundle bất biến, checkpoint từng chương, resume có hash/frame check, ghép nhanh có kiểm tham số và fallback encode. Xem [render và benchmark](CHINA_RENDER.md).
- `china_qa.py` / `china_review.py`: kiểm toàn thời lượng và trang xem media–lời–nguồn–các kết quả đo; quan sát biên tập và trạng thái người dùng tách khỏi decode pass.

Mỗi đề tài/revision ở thư mục riêng dưới `videos/`, giữ script, raw take/receipts, nguồn, crop, bundle/source snapshot, mọi lần render và QA. Batch hiện tại là `videos/2026-11-13-kinh-te-trung-quoc/`: tám chương, 51 beat, narration ghép 595,58 giây; timeline có đệm 597,1 giây / 17.913 frame. Đây là số của bản này, không phải hằng số cho mọi bài.

## Cổng kiểm nội dung và nguồn

Viết câu hỏi trung tâm và chuỗi nguyên nhân trước, rồi chọn cách lên hình cho từng mệnh đề. Với số liệu, giữ nguồn sơ cấp, ngày chốt, kỳ đo, đơn vị, mức/tốc độ, giá hiện hành/so sánh, cùng giới hạn suy luận. Không đổi tăng so cùng kỳ thành tăng so quý trước; không dùng đầu tư bất động sản thay mức giá mọi căn nhà; không tráo mốc tuổi 60+ và 65+. Các số được pin trong compiler là cổng cho bản đã nghiên cứu, không phải nguồn sự thật vĩnh viễn: đề tài/ngày mới phải kiểm nguồn và cập nhật đồng bộ lời, biểu đồ và phép kiểm.

Biểu đồ số liệu có nguồn khác mô phỏng cơ chế: thông số giả định, độ rộng ribbon hay tốc độ băng chuyền phải ghi rõ minh họa, không giả thành tỷ trọng hoặc dự báo đo thực. GDP/xuất nhập khẩu không tự chứng minh lợi nhuận, thu nhập hay hành vi của người trong ảnh. Ảnh Trung Quốc cần hồ sơ địa điểm thực; không suy từ khuôn mặt hoặc tên tác giả. Giữ URL, tác giả, giấy phép, hash và crop đã mở. Nguồn địa lý Natural Earth cần receipt/ghi chú ranh giới; các đường nối thương mại chỉ là sơ đồ, không phải tuyến tàu hoặc khối lượng thực.

## Trình tự sản xuất

1. Lưu brief, nội dung tám chương hoặc cấu trúc mới và nguồn nghiên cứu; kiểm toàn bộ mệnh đề/đơn vị/giới hạn, tránh gán câu chuyện không quan sát cho stock.
2. Chốt text, tạo take qua `china_audio.py --phase voice` để ghi cache, thời gian và usage; không sửa text rồi tái dùng alignment cũ. Ghép/compile qua `china.py`; không tăng tốc để ép thời lượng.
3. Thiết kế cảnh/crop/cue từ exact alignment. Mở still của cảnh khó, kiểm chữ/đơn vị/nguồn và trạng thái đầu–giữa–cuối; ảnh gốc hoặc source SVG đúng chưa chứng minh crop cuối đúng.
4. Phối âm bằng cue-plan có beat/role cụ thể; nhạc nhường lời, SFX là minh họa âm thanh, không phải bản ghi từ tư liệu. Sửa hình thuần túy có cùng dependency/timing giữ nguyên mix.
5. Render tuần tự từ bundle đã pin. Nếu lỗi, giữ partial/log và resume đúng attempt; không ghi đè batch cũ. Chỉ ghép stream copy khi H264/FPS/SAR/màu phù hợp và vẫn phải giải mã đủ frame sau ghép.
6. Kiểm frame toàn thời lượng, lời cuối, caption/crop/claim và chuyển động; đo audio trên final. Chỉ ghi đã nghe khi thật sự nghe. Duyệt agent theo phạm vi không là duyệt toàn bản của người dùng.

## Đo thời gian và chi phí

Pin thời điểm bắt đầu bằng đồng hồ thực. Tách thời gian gọi provider cộng dồn, mix cục bộ, bundle, từng chương, join/decode và wall time toàn tác vụ. Không lấy FPS một chương để khẳng định tốc độ cả phim. Khi final chưa xong, giờ kết thúc và tổng thời gian cuối để `null`/đang chờ.

Chỉ cộng credits có header usage của request mới thuộc tác vụ; cache/copy không tính lại phí lịch sử, header thiếu giữ chưa biết. Chênh account count có thể chứa việc khác và không phải hóa đơn riêng. Giá USD niêm yết là ước tính có ngày/nguồn, tách khỏi tiền thực trả, credits và chi phí token/máy/điện chưa đo. Không đặt khoản chưa biết thành 0. Batch lưu `benchmark/audio-cost-summary.json`, `audio-stage-measurements.json`, `mix-stage.json`, `render-stage.json` sau hoàn tất và báo cáo đọc được `benchmark/report.md` / `report.json`.

Sau phản hồi, dùng `learning.py` theo [vòng cải tiến](LEARNING_LOOP.md): đề xuất → áp dụng có evidence snapshot → kiểm lại đúng phạm vi. Một request nâng cấp hoặc số frame đạt không tự trở thành bài học verified hay model-weight training.
