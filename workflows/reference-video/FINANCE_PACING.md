# Nhịp cảnh nhanh hơn và CTA đăng ký — 13/11/2026

Người dùng đã bác cả hai phim tài chính r03 vì vẫn giống slide, sau đó yêu cầu rõ: **“style chuyển động quá lâu, chuyển cảnh nhanh hơn nâng cấp hơn đi cho tôi rồi cuối video còn đăng ký kệnh đồ nữa”**. Yêu cầu mới này cho phép dựng lại cả comic và tối giản với diễn biến nhanh hơn, thêm lời mời đăng ký/bật chuông/bình luận ở cuối. Nó không chuyển các phim cũ thành mẫu được duyệt.

Batch mới: `videos/2026-11-13-hai-style-nhip-nhanh/`. Giữ nguyên batch bị bác `videos/2026-11-13-hai-style-10-phut/`, các MP4, nguồn, take và hồ sơ kỹ thuật. Chỉ dùng giọng Nhật Phong đã chốt, không tự đặt tên kênh, không thêm branding Tyranno.

## Phần lời giữ nguyên và đoạn kết mới

`finance_pace.py` đọc plan cùng final mix của batch cũ. Toàn bộ **50 beat, 2.050 từ căn chỉnh, 289 caption và 17.743 frame phần chính** giữ nguyên thời gian. Không tăng tốc tiếng để tạo cảm giác dựng nhanh.

Phần kết mới được người dùng yêu cầu:

> Nếu thấy video hữu ích, hãy đăng ký kênh và bật chuông để đón xem những nội dung tiếp theo. Bạn muốn xem lại khoản chi nào trong tháng này? Hãy để lại bình luận nhé.

Một request speech mới dùng Nhật Phong `6adFm46eyy74snVn6YrT`, `eleven_v3`, tiếng Việt, speed 1.0, stability 0.5, similarity_boost 0.8. Receipt ghi **66 đơn vị theo header nhà cung cấp**, không phải hóa đơn USD. Không tạo lại lời phần chính; không gọi mới API ảnh, video, nhạc hoặc SFX cho thay đổi này.

Đã đối chiếu PCM thực tế: **28.388.800 mẫu stereo / 113.555.200 byte** đầu của WAV mới giống hệt toàn bộ PCM phần cũ; SHA-256 của phần PCM này là `b85810d9907319176d5980a930df9a4d90ab44950f8895c958c0fbc9fa34217a`. Đây là tính nguyên vẹn phần âm thanh, không phải kết luận về cách đọc hay thẩm mỹ.

Đoạn kết gồm tiếng mới, một đoạn nhạc có receipt đã giữ và cue tổng hợp local; nối sau phần mix cũ đầy đủ. Timeline mới đo **18.070 frame / 30fps = 602,333 giây**, khoảng **10 phút 02 giây**. Đoạn nối dài 10,9 giây; từ cuối kết thúc ở 601,433 giây, còn 0,9 giây đệm. Chi tiết nằm trong `audio/mix-receipt.json` và `audio/outro-generation.json`.

## Cắt cảnh và diễn biến

`finance_pace_plan.py` cung cấp `build_shots(plan)` và `audit_shots(plan, shots)`. Các cut ở ranh giới beat cũ hoặc điểm bắt đầu từ của chính take, ưu tiên dấu câu và mệnh đề; giữ các cụm số tiền và cụm từ gắn nghĩa. Không dùng độ dài ký tự để đoán thời gian đọc.

Plan hiện có **186 shot / 51 beat**, trung bình **3,238 giây/shot**, ngắn nhất 1,733 giây và dài nhất 4,567 giây. Có 170 shot trong khoảng ưu tiên 2,2–4,4 giây; 182 điểm đầu shot ở ranh giới beat hoặc dấu câu. Tất cả từ có đúng một shot sở hữu, toàn bộ timeline phủ liên tục không chồng/lỗ. `part` bắt đầu từ 0; `parts` là tổng shot của beat. Trường `stage` mô tả vai trò setup/action/result/reaction/outro.

Đây chỉ là kế hoạch nhịp và tính liên tục. **186 shot không tự chứng minh đã hết slide.** Cảnh phải có hành động xảy ra sớm, nguyên nhân/kết quả, tương tác và thay đổi trạng thái đúng lời; vật thể bay vào, số chạy, zoom nhẹ rồi giữ vẫn là lỗi đã bị bác. Các shot trong một beat cần tiếp nối trạng thái, tránh khởi động lại cùng hoạt ảnh hoặc thay nhãn trên một khung cố định. Không duy trì dải tiêu đề, sân khấu và footer lớn xuyên toàn video như bản bị bác.

Mã hình mới nằm riêng trong `cinematic/src/finance-pace-comic/` và `finance-pace-flow/`, entry `cinematic/src/finance-pace-entry.tsx`. Có thể tái dùng nhân vật/primitive phù hợp, nhưng không chỉ bọc lại renderer cũ bằng một crop hay pan. Tiêu chuẩn chống slide trong `AGENTS.md` và `FINANCE_STYLES.md` vẫn áp dụng.

## Lệnh từ gốc dự án

```powershell
# Bước này đã có take/receipt; cache/intent bảo vệ việc chạy tiếp.
# Chỉ voice-outro có khả năng gọi speech trả phí nếu chưa có take phù hợp.
python -X utf8 -B workflows/reference-video/finance_pace.py voice-outro

# Chỉ dựng plan/mix từ tài sản đã có, không gọi provider.
python -X utf8 -B workflows/reference-video/finance_pace.py prepare

python -X utf8 -B workflows/reference-video/finance_pace_render.py bundle --revision r04
python -X utf8 -B workflows/reference-video/finance_pace_render.py proof --revision r04
python -X utf8 -B workflows/reference-video/finance_pace_render.py preflight --revision r04

# Chỉ chạy render dài sau khi kiểm các cảnh chuyển động trọn vẹn của revision.
python -X utf8 -B workflows/reference-video/finance_pace_render.py render --revision r04 --style both
python -X utf8 -B workflows/reference-video/finance_pace_render.py qa --revision r04
```

Không thay source/plan/mix sau khi đã khóa dependency rồi dùng lại bundle cũ. Giữ revision trước và tạo revision mới cho thay đổi hình. Chỉ sửa hình không tạo lại voice/outro hoặc mix.

## Kiểm chuyển động trước bản dài

Runner chuẩn bị proof đầy đủ các beat **b01, b15, b26, b42 và subscribe** cho cả hai style, phủ hook, phép tính, lịch dòng tiền, lựa chọn mua và đoạn kết. Proof scale 0,6 cho khung 1152×648, giữ 30fps và đúng âm thanh của khoảng đó. Chụp still theo từng shot hỗ trợ kiểm chữ, bố cục và phép tính, nhưng không thay việc kiểm diễn biến trọn cảnh.

Hồ sơ motion review cần gắn với dependency của bundle và các proof clip thực tế. Chỉ có tệp JSON hay hash bundle không tự chứng minh đã xem, không được coi trạng thái pending/rejected là đạt. Cần ghi đúng những gì đã quan sát theo thời gian, thao tác nào diễn ra sớm, cảnh có tiếp tục phát triển sau entrance hay không, và vấn đề nào còn tồn tại. Đây là QA nội bộ, không thêm vòng xin phép người dùng.

Sau render, giải mã đủ cả hai file, kiểm 1920×1080/30fps và 18.070 frame, audio trọn câu cuối và PCM audio hai style giống nhau. Kiểm lại prefix PCM phần chính cùng receipt/hash trước khi ghi đã giữ nguyên lời cũ. Kiểm mẫu theo từng shot và kiểm chuyển động/âm thanh là các bằng chứng có phạm vi khác nhau.

Runner hiện giải mã mỗi proof để kiểm đúng **1152×648, 30fps và toàn bộ frame của beat**. Cổng render dài yêu cầu quyết định `ready_for_long_render`, phương pháp `temporal_scene_review`, quan sát có nội dung, hash dependency đúng revision và hash của đủ năm proof cho style được chọn. Một review pending/rejected hoặc clip thay byte sẽ bị chặn. QA cuối tính lại prefix PCM của WAV mới đối với mix cũ thực tế, thay vì chỉ ghi một cờ khẳng định.

## Revision hình đang kiểm r04

Các revision r01–r03 được giữ. Revision r04 tiếp tục sửa font chữ/diễn giải hành động trong comic; so dependency r03→r04 cho thấy chỉ ba file `finance-pace-comic/art.tsx`, `decisions.tsx` và `money-scenes.tsx` thay đổi. Entry, tất cả mã flow, plan và mix giữ nguyên hash. Scoped TypeScript của entry chung đã qua; hai renderer có cấu trúc plan/shot tương thích.

Năm proof flow r04 được giữ nguyên byte từ r03, có đối chiếu source, entry, plan, mix và SHA-256 của từng MP4 trong `r04/flow/proof-equivalence.json`. Đây là chứng cứ không đổi của đúng nhánh flow, không phải phê duyệt thẩm mỹ hoặc bằng chứng rằng comic r04 đã được kiểm chỉ nhờ flow không đổi. Comic r04 có bộ proof được dựng lại theo nguồn mới và cần quan sát chuyển động của chính bộ đó.

Đối chiếu lặp lại khi kiểm r04 vẫn xác nhận phần PCM cũ giống hệt, timeline 602,333 giây và từ cuối 601,433 giây. Không tạo thêm voice, nhạc hoặc clip trả phí chỉ vì đổi revision hình.

## Trạng thái

Plan, phần âm thanh và các phép đối chiếu trên đã chuẩn bị; r04 đang ở bước kiểm proof/preflight. **Final QA chưa được ghi nhận đạt trong tài liệu này.** Việc tăng nhịp/chọn chuyển cảnh mới chưa phải người dùng duyệt tạo hình hay toàn video. Giữ trạng thái phản hồi người dùng pending cho bản sửa, và giữ trạng thái rejected của hai phim cũ.
