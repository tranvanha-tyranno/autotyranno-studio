# Đo thời gian và chi phí — video kinh tế Trung Quốc

**Bản r02 sẵn sàng xem lại lúc 13:09:35 13/11/2026 (UTC+7). Tổng thời gian thực ghi nhận: 1 giờ 14 phút 22 giây (4.462,000 giây).** Người dùng chưa duyệt video.

Mốc đầu: **11:55:13 13/11/2026 (UTC+7)** / `2026-11-13T04:55:13Z`. Mốc sẵn sàng `06:09:35Z` do root đọc từ đồng hồ UTC thật sau khi kiểm server/hash/QA/link và delta review bản sửa; không dùng thời gian tương lai hay giờ render xong thay giờ bàn giao. Thời điểm gửi tin nhắn gốc không được cung cấp.

Đây là lần sản xuất đầu gồm nghiên cứu/kịch bản gốc, chọn nguồn, xây workflow và cảnh mới, tạo/phối âm, kiểm still, render toàn bản, QA và sửa một lỗi. **Không xem thời gian này là cam kết năng suất cho mọi video sau.**

Bản bàn giao: `r02/final.mp4`, **64.372.346 bytes (~64,4 MB)**, **17.913 frame / 30 fps / 1920×1080 / 597,1 giây** (9 phút 57,1 giây). QA cuối đạt; đo **−15,98 LUFS / −1,93 dBTP**. Lời cuối giữ nguyên; không tăng tốc take.

## Các chặng có số đo

| Chặng | Thời gian thực | Phạm vi |
|---|---:|---|
| Gọi provider audio | 259,673 giây cộng dồn | 17 request mới; không phải wall time toàn dự án |
| Phối âm cục bộ | 96,672 giây | Chuẩn bị stem, mix và đo |
| Render toàn bản lần đầu | 1.173,484 giây — 19 phút 32,881 giây | Bundle/chapter/check/ghép/giải mã |
| Trong đó: xuất tám chương | 1.059,188 giây | 16,912 frame/giây thực |
| Trong đó: ghép stream copy | 58,812 giây | Nằm trong thời gian render, không cộng lần hai |
| QA bản đầu | 187,703 giây | Đủ 17.913 frame; tạo chứng cứ và đo âm thanh |
| Sửa o03 thành r02 | 149,640 giây — 2 phút 29,640 giây | Chỉ render lại 366 frame rồi ghép normalize; không gọi API |
| QA toàn bản r02 | 184,593 giây | Đủ 17.913 frame, kiểm âm thanh bản cuối |

**Tổng wall time lấy từ hai mốc đồng hồ**, không cộng máy móc các dòng có phần lồng nhau hoặc diễn ra trong lúc làm việc khác. Các khoảng nghiên cứu, phát triển cảnh, chọn tư liệu và kiểm mẫu nằm trong tổng nhưng chưa có phép đo riêng đủ để phân bổ chính xác.

## Âm thanh: gọi mới và tái dùng

| Hạng mục | Gọi API mới | Độ dài nguồn mới | Thời gian gọi cộng dồn | Credits có header xác nhận |
|---|---:|---:|---:|---:|
| Lời Nhật Phong | 8 | 592,41 giây | 199,437 giây | 3.954 |
| Nhạc | 3 | 360,24 giây | 41,548 giây | Chưa biết — 3 request thiếu header |
| Hiệu ứng âm thanh | 6 | 41,38 giây | 18,688 giây | 412 |

Tổng **17 lần gọi mới**, **4.366 credits được xác nhận** từ header từng request (3.954 lời + 412 SFX). Usage của **3 request nhạc vẫn chưa biết**; không thay giá trị thiếu bằng số 0. Có tái dùng **3 bản nhạc / 350,22 giây** và **2 hiệu ứng chung / 3,17 giây** với file/hash/receipt cũ; chúng không phát sinh lần gọi tạo mới trong tác vụ này.

Thời gian provider cộng dồn: **259,673 giây**. Đây là tổng thời gian của các lần gọi, không phải thời gian từ bắt đầu tới kết thúc toàn tác vụ. Phối âm cục bộ mất **96,672 giây**, cho mix dài **597,1 giây**, 18 cue, 6 đoạn nhạc; giữ giọng tự nhiên và không loop nhạc để bù thời lượng. Chưa xác nhận nghe liên tục.

## Chi phí được biết và phần còn thiếu

**$1,7732 là ước tính theo giá niêm yết, không phải hóa đơn hay số tiền thực trả.** Tính theo trang [ElevenAPI Pricing](https://elevenlabs.io/pricing/api), kiểm ngày 13/11/2026: v3 $0,08/1.000 ký tự đầu vào, nhạc $0,15/phút, SFX $0,12/phút; chỉ tính 17 request mới, chưa thuế. Không quy đổi credits thành USD theo phép tính này.

Ảnh chụp tài khoản được lọc thông tin nhạy cảm: đầu lượt còn **18.499**, cuối lượt audio còn **9.633 credits**. Chênh bộ đếm tài khoản là **8.866**, nhưng không thể quy toàn bộ cho tác vụ: có thể chứa việc khác, điều chỉnh hoặc thay đổi hạn mức. Tổng có chứng cứ riêng từng request vẫn là **4.366 + usage nhạc chưa biết**.

Chưa có số tiền hóa đơn, chi phí token/model của phiên làm việc, điện/máy hay phần phân bổ thuê bao. Không gán các khoản chưa đo bằng 0 và không bịa tổng tiền thực trả.

## Render và sửa lỗi được giữ bằng chứng

Render đầu hoàn tất `2026-11-13T05:55:52.701835+00:00`; từ mốc bắt đầu tới đó là 1 giờ 0 phút 39 giây. Bản đầu giữ nguyên ở `final.mp4`. QA phát hiện o03 có heading “Bốn câu hỏi” trên ba thẻ; r02 sửa thành **“Ba góc nhìn để đọc Trung Quốc”**.

Chỉ render đoạn `[614,980)` — 366 frame, gồm bảy frame đệm seam. Caption, thời gian, take/mix và dữ liệu cảnh khác giữ nguyên; khi ghép toàn video được encode lại nên không khẳng định pixel giống byte. So sánh 50 midframe ngoài đoạn sửa đạt PSNR tối thiểu 47,30277 dB và MAE tối đa 0,47604.

Kiểm thực tế đã gồm toàn bộ 51 midframe bản đầu và o03 sửa ở độ phân giải gốc; lượt độc lập lấy 200 mẫu mỗi ba giây cùng 15 strip năm frame. Đây là kiểm mẫu hình, **không phải xem/nghe AV liên tục**. Kết quả kỹ thuật/agent không thay phản hồi người dùng.

SHA-256 final r02: `7a6257701b5a6998118d6ce3572b14a5e9066489a6327bebd55f429506c986c1`.

Xuất hình dùng concurrency2, cache media256MiB. CPU ghi trong receipt chỉ thuộc tiến trình Node/FFmpeg trực tiếp trên Windows, không bao gồm toàn bộ Chrome/encoder con. Không quy thời gian máy thành USD khi chưa có phép đo/đơn giá.

## Chứng cứ

- [Bảng đo có cấu trúc](report.json)
- [Chi phí/request âm thanh](audio-cost-summary.json)
- [Tách thời gian các nhóm audio](audio-stage-measurements.json)
- [Thời gian phối âm](mix-stage.json)
- [Bundle/chương/ghép/giải mã đầu](render-stage.json)
- [QA bản đầu](qa-stage.json)
- [Sửa riêng o03](r02-visual-repair-stage.json)
- [QA bản cuối r02](qa-r02-stage.json)
- [QA đầy đủ r02](../r02/qa/report.json)

17 request mới vẫn là tổng số cuối: tám lời, ba nhạc, sáu SFX; sửa/QA không phát sinh thêm phí provider. Credits còn thiếu và tiền hóa đơn chưa biết vẫn giữ nguyên trạng thái chưa biết.

Trang xem cục bộ: [Bản r02 và chứng cứ](http://127.0.0.1:8883/?revision=r02). Thời điểm ghi báo cáo sau đó không làm tăng thời gian sẵn sàng đã kiểm.
