# Lăng Kính / Tyranno — video editorial 50 giây

Bản nâng cấp từ batch documentary-50s đã được người dùng nhận xét bắt đầu đúng hướng. Giữ footage chuyển động và mạch giải thích; thay hệ mic/waveform cố định bằng 7 kiểu bố cục dùng cùng bộ màu.

## Nhận diện và cách dựng

Tên: LĂNG KÍNH · TYRANNO. Than đậm / giấy ngà / hổ phách / mint. Dấu ngoặc lệch và đường kẻ mảnh, chữ lớn chỉ khi cần nhấn ý. 11 đoạn hình: hero số liệu → footage sạch với cú dừng ý → panel biên tập → chia đôi → ba cửa sổ chuyển động → footage gõ phím → chia đôi → inset → panel giấy ngà → footage với luận điểm → kết bằng câu hỏi. Không có micro hoặc waveform chạy xuyên video. Footage quốc tế chỉ là minh họa, không giả là quay ở Việt Nam.

## Giọng

ElevenLabs eleven_v3, Thùy Tiên / Vietnamese Narrator sẵn trong tài khoản. Giữ thêm hai sample ngắn Adam và Thùy Tiên tại audio/. Lựa chọn giọng dựa trên native-Vietnamese metadata và đối chiếu nhận dạng lời, không tuyên bố đã thực hiện nghe thử thủ công. Take gốc 49,79 giây; căn rất nhẹ về 49 giây, giữ nhịp nghỉ cuối. Subtitle dùng character alignment do provider trả về cho đúng take, không tái dùng timestamp từ giọng cũ.

## Sound design

Sáu asset ElevenLabs SFX v3: whoosh, impact nhẹ, giấy, bàn phím, UI tick và ambience cảng. 10 cue chính, hai đoạn ambience liên quan mở/kết. Lưu bus effects.wav và sound-cue-sheet.json. Nhạc nền tổng hợp nguyên bản được giảm tự động dưới lời bằng sidechain. Không dùng tiếng nổ/còi để giật chú ý. Cue và âm lượng được đo, không gọi là đánh giá nghe khách quan.

## Kiểm tra

Giải mã toàn bộ, đếm 1500 frame/30fps, đo 50 giây, LUFS/true peak. Duyệt contact sheet 1fps trải cả video và khung lớn của mọi kiểu bố cục. Whisper small độc lập nhận được trọn câu kết; ASR có thể sai tên/số và không chứng nhận giọng hay. Giữ trạng thái user_acceptance pending.

## Lưu để dùng lại

workflows/reference-video/lang-kinh.profile.json
workflows/reference-video/editorial.py
workflows/reference-video/eleven_audio.py
workflows/reference-video/audio_stages.py

Khóa chỉ nằm trong cơ chế local DPAPI/env, không có trong batch/profile/prompt. Xem provider-usage.json để biết đơn vị dùng do provider báo; các lần đổi hình dùng cache giọng/SFX. Batch trước được giữ nguyên.
