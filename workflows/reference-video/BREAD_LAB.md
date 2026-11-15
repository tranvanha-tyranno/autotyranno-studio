# Nâng thông tin, mô phỏng và âm thanh — 15/11/2026

Người dùng cho rằng bản footage r02 hiển thị quá ít thông tin, chưa có đủ mô phỏng, yêu cầu nâng cấp mạnh hơn, đổi sang giọng OpenAI và tải thêm nhiều hiệu ứng âm thanh trên mạng. Đây là thay đổi được phép cho chính bài bánh mì, không trở về nhân vật hoạt hình hoặc phụ đề bị bác.

Nhánh cô lập `cinematic/src/bread-lab/`, entry `bread-lab-entry.tsx`/`BreadLab`, `bread_lab.py`, `bread_openai_voice.py` và `bread_openai_align.py`. Batch mới `videos/2026-11-15-banh-mi-mo-phong-openai/` giữ content, source note, các request/receipt không chứa credential, raw SFX/giấy phép, timeline, plan và render. Không sửa renderer hoặc phim đã đóng băng của batch cũ.

Tám nhóm mô phỏng có công việc khác nhau: chia tiền bán thành đầu vào/cố định/khoảng dư; tách mức giá với tỷ lệ; tiêu thụ lô tồn trước khi dùng bột mới; cộng chi phí và phản ví dụ tổng giảm; lựa chọn nơi mua/cạnh tranh; cùng tiền lương đổi thành số bánh; một chiếc bánh khác toàn giỏ chi; tổng hợp ba phía. Từng nhóm cần trạng thái đầu → hành động → kết quả. Dữ liệu là mô hình minh họa; không gọi khoảng dư là lãi ròng hoặc giả định dùng cả lương mua bánh. Kho/cạnh tranh là cơ chế định tính, không tự thêm thống kê thị trường.

Thông tin trên video là từ khóa, quan hệ, số/đơn vị và phạm vi cần thiết. Không chép toàn bộ lời thành subtitle. Giữ footage thật ở mở bài, các cầu nối, ví dụ đời sống và CTA; mô phỏng có thể chiếm nhiều hơn bản cũ khi nó làm rõ lời. Tỷ lệ cảnh hoặc số family không phải bằng chứng tự động rằng hình đa dạng/hay.

16 SFX mới đã tải từ các trang Freesound có giấy phép CC0 riêng, HTML nguồn, license và hash ở `research/sfx-sources.json`. File là HQ MP3 công khai do Freesound cung cấp, không phải WAV gốc cần đăng nhập. Chọn cue theo hành động và phép tính, hạ dưới lời; không rải âm beep/woosh vào mọi cut. Bed chợ có hội thoại nước ngoài và bản bread-cooling có tiếng quạt/quần áo được ghi giới hạn, không tự coi là Foley sạch. Đo waveform/giải mã không thay lượt nghe thực.

OpenAI Docs đã được kiểm tại `https://developers.openai.com/api/docs/guides/text-to-speech`; chọn `gpt-4o-mini-tts`, voice `cedar`, chỉ dẫn đọc tiếng Việt tự nhiên, nhấn tương phản/câu hỏi và số, không đổi tốc độ sau tổng hợp. API speech không trả exact-word alignment trong workflow này; khi có audio thật dùng local Small ASR word timestamps và known-text mapping, ghi rõ từ nội suy và giới hạn. Không gọi đó là phoneme/forced alignment khi chỉ khớp ASR.

Hai khóa người dùng đưa đã bị API chính thức trả401 `invalid_api_key`; biên nhận lỗi được lưu không chứa khóa. Không có take OpenAI thành công. Chỉ tiếp tục hình/SFX bằng bản preview giữ take Nam Minh cũ khi chờ khóa dùng được, ghi rõ trạng thái này ở manifest/viewer/đường dẫn. Không dùng nội dung giọng khác để tuyên bố đã đáp ứng yêu cầu OpenAI. Không tự retry request trả phí chưa rõ kết quả.
