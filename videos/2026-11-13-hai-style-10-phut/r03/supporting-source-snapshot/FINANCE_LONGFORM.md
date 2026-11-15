# Hai video tài chính dài, cùng lời kể — 13/11/2026

Người dùng yêu cầu hai video khoảng mười phút theo hai dạng tài chính gần nhất. Batch mới là `videos/2026-11-13-hai-style-10-phut/`. Đây là hai phim đầy đủ theo hai cách thể hiện, không phải hai chủ đề khác nhau hoặc hai đoạn proof cũ kéo dài. Các bản demo, thư viện và bản bị bác trước đây được giữ nguyên.

## Nội dung và phạm vi

Chủ đề gốc: **Lương tăng mà vẫn hết tiền: sửa dòng tiền trong 30 ngày**. `finance_long_content.py` chứa 10 chương, 50 beat và 2.050 đơn vị tách bằng khoảng trắng. Timeline đo từ take thật là **17.743 frame ở 30fps = 591,433 giây, khoảng 9 phút 51 giây**. Giữ tốc độ lời 1.0; không kéo giãn lời hay lặp cảnh để ép đủ mười phút.

Mạch kể đi từ nghịch lý tăng lương → miễn trừ riêng sau hook → so hai ngân sách → cộng khoản chi nhỏ theo tháng → kiểm giao dịch → dịch vụ lặp lại và dự trù năm → ngày nhận tiền/ngày đến hạn → giới hạn của việc cắt chi thiết yếu → giao việc cho khoản dư → kiểm lựa chọn mua → kế hoạch bốn tuần và CTA.

Minh và Lan là người trưởng thành hư cấu. Mọi mức lương, giá, chi phí và số tiền đều là tham số minh họa, không phải thống kê về Việt Nam. Ví dụ chính giữ phép tính 12 − 10 = 2 triệu và 14 − 12 = 2 triệu; 60.000 × 30 + 200.000 = 2 triệu. Kịch bản bớt 20.000 mỗi ngày cho 30 ngày giải phóng 600.000; mức dư 2,6 triệu chỉ đúng khi khoản chi khác không đổi. Dịch vụ 120.000/tháng và khoản dự trù 1,2 triệu/năm là ví dụ riêng, không cộng nhầm vào ngân sách chính. Chuyển tiền giữa tài khoản của mình không tự thành chi tiêu hoặc lợi nhuận.

Nguồn CFPB đã ghi trong `sources.json` chỉ hỗ trợ phương pháp giáo dục chung: theo dõi chi tiêu, lịch hóa đơn, thời điểm dòng tiền, khoản đệm phụ thuộc hoàn cảnh và chuyển tự động có kiểm số dư. Không chuyển quy định tài khoản/pháp lý của Mỹ thành quy định Việt Nam. Không đưa lời hứa lợi nhuận, lãi suất hoặc phương án cá nhân hóa.

## Hai cách thể hiện

| Bản | Composition | Mã nguồn | Yêu cầu hình |
| --- | --- | --- | --- |
| Comic biểu cảm, hơi hài hước | `FinanceLongComic` | `cinematic/src/finance-long-comic/` và rig `finance-cast-v2/` | Hai nhân vật tương tác với đạo cụ thật trong cảnh; phản ứng phục vụ lời kể; kiểm tay cầm và vị trí đạo cụ |
| Tối giản chuyển động liên tục | `FinanceLongFlow` | `cinematic/src/finance-long-flow/` | Tiền, hóa đơn, phong bì và lịch có hành động nguyên nhân/kết quả; tránh chuỗi slide chữ đứng yên |

Entry là `cinematic/src/finance-long-entry.tsx`. Hai phim dùng chính xác cùng các take chương Nhật Phong, cùng timestamp và cùng final mix để so phong cách. Một người kể đọc cả chuyện; không giả là hai diễn viên lồng tiếng. Chuyển động miệng theo mức có lời, nếu có, là hoạt hình đơn giản, chưa phải lip-sync âm vị đã kiểm chứng. Không có tên kênh hoặc branding.

## Chạy từ gốc dự án

```powershell
python -X utf8 -B workflows/reference-video/finance_long.py prepare
# Chỉ voice gọi speech trả phí. Dùng cache/receipt/intent để chạy tiếp, không retry trả phí mù.
python -X utf8 -B workflows/reference-video/finance_long.py voice
# timeline có thể dựng lại từ take đã có; không gọi provider.
python -X utf8 -B workflows/reference-video/finance_long.py timeline
python -X utf8 -B workflows/reference-video/finance_long.py mix

python -X utf8 -B workflows/reference-video/finance_long_render.py preflight --revision r03
python -X utf8 -B workflows/reference-video/finance_long_render.py render --revision r03 --style both
python -X utf8 -B workflows/reference-video/finance_long_render.py qa --revision r03
```

`voice` tạo tối đa 10 take chương mới cho cả hai phim, không tạo lại riêng theo style. Giọng Nhật Phong `6adFm46eyy74snVn6YrT`, `eleven_v3`, tiếng Việt, speed 1.0, stability 0.5 và similarity_boost 0.8. `timeline` dùng character alignment đúng take, nối chương với khoảng nghỉ 0,45 giây, tạo caption và cue thật theo câu. Không dùng timing của demo 78 giây.

`mix` tái dùng sáu nhạc có receipt từ batch café, kiểm hash và ghép bằng crossfade; phải đo đủ độ dài theo take thật. Cue giấy, nút chọn ngày và tiếng chạm nhẹ được tổng hợp local, giữ ưu tiên lời kể. Không cần gọi thêm API ảnh, video, nhạc hoặc SFX cho nhánh này. Số `character-cost` là đơn vị nhà cung cấp báo trong header, không phải hóa đơn USD; thời gian render local cũng không đồng nghĩa miễn phí hoàn toàn.

## Ghi nhận thực tế của batch hiện tại

Đã tạo 10 take chương dùng chung cho cả hai phim. Tổng `newRequestCredits` trong `audio/voice-runs.json` là **3.791 đơn vị theo header nhà cung cấp**. Đây không phải hóa đơn USD hoặc phép đổi credit sang tiền. Số lượt gọi trả phí mới cho ảnh, video, nhạc và SFX đều bằng **0**; nhạc được tái dùng có receipt, cue được tổng hợp local.

ASR local `faster-whisper-small / CPU int8` đã chạy trên toàn bộ final mix, mất **668,25 giây** theo `audio/asr-review.json`. Đoạn cuối nhận dạng được câu kết tới khoảng **590,1 giây**, nằm trong timeline 591,433 giây. Đây là kiểm tra bằng nhận dạng tiếng nói, có thể có lỗi ASR; không ghi là đã nghe thủ công hoặc nghe liên tục cả phim.

Các preflight `r01/` và `r02/` được giữ lại. Những sửa hình đã áp dụng gồm: chờ đúng cụm lời để bộ đếm đạt kết quả cuối, giữ chính xác số thập phân **11,4 / 2,6 triệu**, đặt `stroke="none"` cho chữ SVG, và sửa nhãn/vị trí/crop theo frame thực tế. Hồ sơ r02 gồm 100 mẫu comic trong `r02/comic/review/verification-r02.json` và 100 mẫu flow trong `r02/flow/review/subagent-flow-preflight-review.json`. Các ghi nhận này có phạm vi khung hình chọn mẫu; chúng chưa xác nhận chất lượng chuyển động toàn phim.

Revision **r03 đang render**. So guard r02 với r03 xác nhận chỉ `cinematic/src/finance-long-flow/index.tsx` thay đổi, để nâng một dòng giải thích ở footer b11 khỏi vùng bị crop. Hash plan và mix vẫn giống nhau. Ảnh sửa có ở `r03/b11-crop-fixed.png`; comic và các cảnh flow khác giữ nguyên nguồn đã kiểm trong r02. Chưa ghi final QA đã pass cho r03 cho tới khi decode/kiểm file cuối thực sự hoàn tất.

## Dựng và kiểm tra

Runner chụp snapshot và khóa dependency, plan, mix trước khi bundle. Nếu đổi mã hoặc hình sau khi khóa, dùng revision mới. Thay đổi hình không được tạo lại narration. Phim được render tuần tự theo style, chia đoạn tối đa 1.800 frame để chạy tiếp; mỗi đoạn cần receipt hash và số frame decode đầy đủ trước khi được dùng. Ghép các đoạn đã chuẩn hóa, giữ một final mix chung.

Preflight lấy cue và trạng thái sau cue của từng beat; mở ảnh thật để kiểm trước khi render dài. QA sau render decode đủ toàn thời lượng mỗi phim, kiểm 1920×1080/30fps, số frame thật, độ dài audio, câu cuối trọn và PCM hash audio giống nhau. Lấy ba mẫu mỗi beat, lưu sheet, loudness và báo cáo. Không kết luận hình khớp lời chỉ từ ID, loại cảnh hoặc số file; phải đối chiếu chủ thể, đạo cụ, hành động và số liệu của từng câu với frame thật.

Đếm đủ frame, đo âm lượng, render thành công và xem khung hình chọn mẫu là các bằng chứng khác nhau. Chúng không xác nhận đã xem/nghe liên tục hoặc tự chứng minh chất lượng mỹ thuật/chuyển động. Ghi rõ phần nào thực sự quan sát được trong báo cáo.

Trạng thái của hai phim mới là **chờ phản hồi người dùng**. Yêu cầu làm bản dài không có nghĩa nhân vật mới, motion mới hay toàn bộ video được người dùng duyệt. Chỉ lưu bài học đã áp dụng và có bằng chứng; không gọi việc cập nhật mã/quy trình là huấn luyện trọng số mô hình.

## Kết quả xuất r03

Hai file `r03/comic/final.mp4` và `r03/flow/final.mp4` đã xuất đầy đủ: 1920×1080, 30 fps, mỗi bản 17.743 frame, 591,433 giây. QA giải mã toàn bộ hai video, audio PCM trùng hash, câu cuối kết thúc ở 590,21 giây; âm thanh giải mã dài 591,445 giây. `r03/qa-report.json` ghi technical passed, tách riêng khỏi thẩm mỹ và phản hồi người dùng.

Đã kiểm mẫu từ MP4 cuối: 150 frame cho mỗi style, phủ 50 beat; giữ báo cáo và hash trong các thư mục `r03/*/review/`. Đây là kiểm hình lấy mẫu, không phải xem/nghe liên tục. Một vài chữ phụ sát mép bàn/lọ trong comic vẫn được ghi nhận; số liệu và thông tin chính đọc được trong mẫu.

Render các chunk hoàn tất mất tổng 916,608 giây cho comic và 903,804 giây cho flow, khoảng 19,36 và 19,63 fps. Các số này loại trừ chuẩn bị, thao tác biên tập, attempt hỏng, mux và QA; không phải tổng thời gian làm dự án. Comic chunk thứ chín từng lỗi thư mục tạm trong bước FFmpeg fast-start, được chạy lại local một lần từ bundle đã đóng băng; tám chunk trước giữ nguyên. Log hỏng và hồ sơ phục hồi được giữ trong r03; không lặp API trả phí.

`finance_long_review.py --revision r03 --serve --port 8879` mở trang xem hai style, chuyển tiếp ở cùng thời điểm và chọn 10 chương/50 beat. Hai đường MP4 đã kiểm HTTP byte-range 206. Trang này chỉ phục vụ local. Hồ sơ chi phí, timing và giới hạn đo nằm ở `r03/benchmark.json`.
