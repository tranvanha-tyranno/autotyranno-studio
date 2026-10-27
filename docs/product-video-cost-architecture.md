# Kiến trúc tiết kiệm chi phí cho video sản phẩm

Pipeline được chia thành hai lớp.

## LLM/provider trả phí

- ElevenLabs chỉ nhận phần thoại cuối cùng. Nếu người dùng đã đưa kịch bản, không cần LLM viết lại. Cùng nội dung + voice + model + settings dùng lại file TTS trong `.cache/product-video/tts`.
- Muse2API chỉ nhận ảnh/prompt tạo opening và các cảnh video. Mỗi request có hash ổn định gồm endpoint, prompt, model, thông số và hash ảnh. Kết quả thành công được lưu trong `.cache/product-video/muse`; chạy lại cùng input không gửi job mới.
- LLM tùy chọn chỉ dùng cho việc có giá trị ngôn ngữ: phát triển hook, biến thể thoại, CTA, tóm tắt claim có trong ảnh và tạo prompt. Không dùng LLM để crop, resize, ghép cảnh, đo thời lượng hoặc kiểm tra file.

## Code/local miễn phí

Python xử lý manifest, chuẩn hóa request, hash, cache hit/miss, retry/resume an toàn, giới hạn số cảnh, copy input, tạo crop và báo cáo. FFmpeg xử lý concat, tăng tốc hình 1,5×, giữ giọng độc lập, encode, sample frames và decode check. Đây là các bước xác định, rẻ và lặp lại được.

## Thứ tự chạy ít tốn nhất

1. `init`: tạo batch và copy ảnh, chưa gọi provider.
2. `cache`: index các voice/media cũ trong batch, không gọi provider.
3. `plan`: đếm TTS, opening image và scene video sẽ gọi; báo cache hit; ghi `cost-plan.json`.
4. `images`: tạo opening và kiểm tra ảnh. Sửa prompt ở đây nếu framing sai trước khi tạo cảnh.
5. `voices`: tạo Adam một lần cho mỗi kịch bản chưa có cache.
6. `videos`: tạo đúng số cảnh cần thiết; task id được lưu trước polling, không POST lại sau gián đoạn.
7. `render`: chỉ chạy local, không phát sinh API call.

Khi muốn một biến thể mới, thay prompt/bối cảnh hoặc đặt `cache.muse`/`cache.tts` thành `false` cho batch đó. Không xóa cache chung để sửa lỗi một batch; điều đó làm mất khả năng tái sử dụng của các batch khác.

## Kiểm soát chất lượng và chi phí

Không kéo một cảnh ngắn để che thiếu footage hoặc lặp cảnh. Manifest 1,5× yêu cầu ba cảnh mười giây; runner từ chối thiếu cảnh trước khi encode. `verification.json` ghi số cảnh nguồn, tốc độ hình, thời lượng audio, cache hit và decode. Các giá provider không được hard-code vì thay đổi theo tài khoản/model; plan chỉ báo số call, còn hóa đơn là dữ liệu của provider.
