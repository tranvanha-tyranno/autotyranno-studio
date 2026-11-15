# Thời gian và chi phí bản sửa hình r03

**R03 sẵn sàng xem lúc14:03:57 13/11/2026 (UTC+7). Tổng thời gian thực của revision:50phút12giây (3.012giây).** Người dùng chưa duyệt bản sửa.

Mốc đầu**13:13:45 /06:13:45Z**, mốc sẵn sàng**14:03:57 /07:03:57Z**, đều ngày13/11/2026. Mốc đầu là lần đọc đồng hồ ghi nhận sau phản hồi lặp kiểu, không phải giờ gửi tin nhắn chưa biết. Mốc cuối do root đọc sau QA, hash/server/link và báo cáo kiểm chuỗi cảnh độc lập. Tổng là hiệu hai mốc đồng hồ, không cộng các stage lồng nhau. Đây là lần dựng lại hình gồm thiết kế/mã từng cảnh, preview, xuất và kiểm mẫu cuối; không phải cam kết tốc độ cho mọi đề tài sau.

## Chi phí phát sinh của revision này

- **0request provider mới** cho giọng, nhạc và SFX; mix, take, caption và timing được pin nguyên từ bản trước, có [biên nhận tái dùng](../audio-reuse-receipt.json).
- Không cộng lại phí tạo âm thanh lịch sử. [Báo cáo gốc](../../benchmark/report.md) giữ17request mới của lần đầu:4.366credits có header xác nhận, usage3bản nhạc chưa biết;1,7732USD chỉ là ước tính theo giá API có ngày/nguồn, không phải hóa đơn.
- Chi phí Codex/model, máy, điện và phần thuê bao chưa được đo riêng; không quy0request API mới thành tổng hóa đơn sản xuất0USD.

## Render toàn phim — số đo đã hoàn tất

Bản MP4 r03 đã giải mã đủ**17.913frame /30fps /1920×1080 /597,1giây**. Dung lượng**90,235,394bytes** (~90,2MB). SHA256`dbbb016a2a57107d4bc943059fa8e3eb41ff0f087f67604e399c370cab59620e`.

Lượt xuất bắt đầu `2026-11-13T06:41:57.169450+00:00`, kết thúc `2026-11-13T06:56:55.774388+00:00`; tổng**898,605giây**, khoảng**14phút59giây**, gồm bundle, xuất tám chương, normalize/join và kiểm giải mã. Dùng**concurrency2**, cache media**256MiB**; cache không phải giới hạn toàn bộ RAM.

- Cộng thời gian render tám chương:**811,878giây**; tốc độ thực tổng số frame chia tổng thời gian chương:**22,064fps**.
- Ghép **stream-copy**:**35,063giây**.
- Giải mã toàn video cuối:**14,109giây**; audio:**0,734giây**.
- Audio dài**597,12giây**, phủ từ cuối tại**595,58giây**. Không tăng tốc take, không cắt câu kết. Giải mã không đồng nghĩa đã nghe.

| Chương | Frame | Render (giây) | FPS render |
|---|---:|---:|---:|
| opening | 1330 | 60,188 | 22,097 |
| factory | 2698 | 125,079 | 21,57 |
| property | 2641 | 114,406 | 23,084 |
| households | 2753 | 120,594 | 22,829 |
| trade | 2339 | 101,61 | 23,019 |
| demography | 2093 | 100,266 | 20,874 |
| policy | 2494 | 110,5 | 22,57 |
| ending | 1565 | 79,235 | 19,751 |

[Receipt render đầy đủ](render-stage.json) · [Báo cáo cấu trúc](report.json).

## Kiểm cuối

QA hoàn tất lúc`2026-11-13T06:59:42.625011Z`, mất**140,344giây**: đủ17.913frame;51midframes,200thumbnail ba giây và255mẫu temporal cho51cảnh. Caption/font, nguồn/publichash, single-use media và âm thanh đạt cổng kỹ thuật; đo trên MP4**−15,98LUFS /−1,93dBTP**.

Root đã mở đủ51ảnh giữa cảnh và6dải temporal. Kiểm độc lập đã mở23contactsheet (200mẫu ba giây),15dải temporal×5mẫu và khung cuối native; không phát hiện blocker trong phạm vi quan sát, đồng thời ghi giới hạn về phong cách chung. Đây là kiểm ảnh lấy mẫu thực tế, không phải xem/nghe liên tục và không thay người dùng duyệt. Module/mechanic không tự chứng minh đa dạng.

[Báo cáo kiểm độc lập](../qa/independent-diversity-review.json) · [Quan sát root](../qa/editorial-review.json) · [QA kỹ thuật](../qa/report.json).
