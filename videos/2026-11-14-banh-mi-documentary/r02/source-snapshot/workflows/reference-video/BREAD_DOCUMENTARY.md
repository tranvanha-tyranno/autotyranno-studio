# Làm lại toàn bộ bài bánh mì — 14/11/2026

Người dùng yêu cầu viết/dựng lại toàn bộ sau khi nhận xét nội dung thiếu trục, cầu nối và khai thác ví dụ; hình giống slide, chậm, nhân vật hoạt hình không cần thiết, voice ngang, subtitle nhỏ/thấp, thiếu video thực tế. Yêu cầu mới này cho phép lời và take mới, bỏ subtitle và đoạn miễn trừ riêng ở đầu. Nó ghi đè việc giữ nguyên audio của các lần chỉ sửa hình trước đó.

Nhánh riêng: `bread_documentary_content.py`, `bread_documentary.py`, `bread_documentary_assets.py` và `cinematic/src/bread-documentary/`. Batch `videos/2026-11-14-banh-mi-documentary/` giữ script/map, raw nguồn, license/hash, narration/alignment/receipt, timeline, render và QA. Các bản bánh mì cũ được giữ.

Trục duy nhất theo tiệm Hạnh: hai nghìn tiền bán → chi phí → nghĩa của chữ giảm → khi nào chi phí giảm có thể dẫn đến giá giảm → cùng chiếc bánh nhìn từ tiền lương → trả câu hỏi mở. Mô hình lương dùng lại bánh 20.000/22.000, không mở thêm mô hình giỏ 100 phần hay shrinkflation. Khung giỏ chi tiêu chỉ để nêu phạm vi phép so; không gọi sức mua bằng bánh là sức mua cả gia đình.

Tình huống Hạnh vẫn là hư cấu trong lời minh họa; không có nhân vật hoạt hình. Người và cơ sở xuất hiện trong stock là bối cảnh, không phải Hạnh thật, không chứng minh khoản chi hoặc hành vi kinh doanh hư cấu. Phép tính được ghi “Ví dụ minh họa” khi hiện số; nguồn và giới hạn đầy đủ lưu trong hồ sơ/mô tả thay cho một đoạn đọc dài ở đầu.

Nhịp nhanh hơn đến từ bớt nhắc/lạc đề, tình huống mới có mục đích, cảnh thật có hành động và nhấn đúng luận điểm. Không kéo dài lời cho đủ mười phút, không dùng zoom tấm ảnh làm footage, không tăng tốc audio sau tổng hợp để che cách viết. Lời mới có câu hỏi, tương phản và độ dài câu thay đổi. Không đánh giá chất giọng chỉ bằng ASR hoặc số liệu loudness.

## Giọng thay thế được người dùng cho phép — 15/11/2026

ElevenLabs đã tạo được hai take Nhật Phong đầu nhưng dừng ở chương ba vì quota. Người dùng sau đó nói rõ: **“Dùng giọng Việt khác cho bản mới”**. Với riêng phim này, cả năm chương final dùng cùng `vi-VN-NamMinhNeural` qua Microsoft Edge online TTS, `rate=+8%` ở bước tổng hợp, không dùng `atempo`/time stretch sau đó và không ghép lẫn hai giọng. Đây là ngoại lệ của batch này; Nhật Phong vẫn là mặc định các explainer khác.

`bread_documentary_voice.py` lưu MP3, provider word boundaries, alignment, hash và receipt ở `audio/nam-minh/`; `active-generation-plan.json` là kế hoạch take thực sự dùng cho timeline. `generation-plan.json`, hai take Nhật Phong hợp lệ và `audio/03-hoa-don-nao-giam.error.json` được giữ nguyên. Timing bên trong từng từ được nội suy từ word boundaries, không phải phoneme alignment hoặc lip-sync đã kiểm chứng. Không dùng no-audio retry để gọi ElevenLabs thêm; runner Edge có timeout/retry hữu hạn cho dịch vụ không trả lời.

Kiểm đủ năm take: hash khớp receipt, ký tự alignment khớp nguyên lời yêu cầu, word boundaries kết thúc trong MP3 và giải mã audio toàn thời lượng đều đạt. Bằng chứng tại `review/alternative-voice-integrity.json`; đây là kiểm kỹ thuật, chưa phải nghe giọng hoặc người dùng duyệt. `bread_documentary_asr.py` ưu tiên active plan, kiểm tuần tự từng take bằng Whisper base cục bộ; số và câu cuối là chẩn đoán nhận dạng, không xác lập biểu cảm tự nhiên.

FFmpeg xử lý các khoảng footage thuần; Remotion dựng những đoạn nhấn/chứng minh ngắn rồi ghép cùng chuẩn fps/size/SAR/màu. Đây là cùng một timeline exact-take, không lấy clip lặp lấp thời lượng. Mỗi source interval lưu rõ, không chồng khi dùng lại. Giữ frame cuối/câu kết trọn vẹn. Kiểm các cảnh hoàn chỉnh đầu/giữa/cuối trước xuất đầy đủ; review kỹ thuật và quan sát hình tách khỏi việc đã nghe liên tục và phản hồi người dùng.
