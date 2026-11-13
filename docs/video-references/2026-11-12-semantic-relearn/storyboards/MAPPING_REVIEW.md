# Review thiết kế ánh xạ lời → hình

Phạm vi: đã đọc toàn bộ hai script, đối chiếu 287 từ của bản Long và 295 từ của bản Hidden với exact-take word alignment, chia theo mệnh đề thành 38 và 37 shot. Đây là kiểm tra storyboard; chưa xem output mới nên không gắn trạng thái đạt về hình ảnh.

Lỗi cần sửa không chỉ là hai ảnh headset/sổ ghi. Kho ảnh công sở cũ chủ yếu chỉ cho biết “đang làm việc”, trong khi lời mô tả email cụ thể, cam kết sai, một số không khớp, thao tác sửa và tiêu chí hoàn thành. Mỗi cảnh mới phải làm lộ đúng **đối tượng + hành động + trạng thái** đó. Nếu cần giữ ảnh thật làm bối cảnh, phần email/nguồn/tương tác được nói phải vẫn là đối tượng chính nhìn thấy.

## Độ phủ

- Hai manifest giữ đủ hook → disclaimer → content → CTA.
- `narratedText` ghép lại bằng đúng toàn bộ script, không thêm lời hoặc làm mất câu cuối.
- Mốc cắt lấy từ chính aligned-words.json của take cũ. Timeline liên tục 0–2460 và 0–2490 frame, không có vùng trống.
- Mỗi shot có yêu cầu có thể kiểm trên hình, có ví dụ bị cấm dùng thay và trạng thái proof đang chờ render.

## Các quyết định cụ thể

1. Một đèn Mẫu A xuyên suốt, dây nguồn và trạng thái không pin dễ quan sát. Nguồn/cam kết/giá đều giả định, không gán thông số cho một listing thật hoặc người trong ảnh stock.
2. Email có người nhận/chủ đề/nội dung và trạng thái Nháp chưa gửi. Mở bài cho thấy câu “Dùng không dây” mâu thuẫn nguồn có dây; câu hỏi khách được ghi là phản hồi giả định nếu gửi.
3. Số 120.000đ được so với 1.200.000đ, thay vì chỉ nhìn ảnh calculator/tờ giấy. Nếu đã sửa, không làm nó sai lại ở cảnh sau trừ khi ghi Nháp ban đầu.
4. Thời gian viết/sửa/tổng là một bảng log cùng ví dụ, có 2 + 13 = 15 phút so với mốc giả định 12 phút. Không mô tả đó là thống kê hiệu năng thực nghiệm.
5. Nhu cầu khách là dùng nơi không có nguồn điện. Lời trả lời lịch sự vẫn chưa đủ nếu không nói rõ đèn cần nguồn qua dây và chưa phù hợp nhu cầu đó.
6. Nhịp sửa giọng điệu một giây chỉ thay “Mua ngay!” bằng “Mời bạn tham khảo.”; không có hai đoạn văn dài người xem không kịp đọc.
7. Các nhịp ngắn 0,6–1 giây chỉ soi một bước trên giao diện đã giới thiệu. Không đổi sang một ảnh mới hoặc intro toàn màn hình ở mỗi từ.

## Điều phải kiểm tiếp trên output

Mở frame thực tại các mốc cam kết sai, giá không khớp, câu trả lời bỏ sót nhu cầu, tổng thời gian và bản cuối đã kiểm. Kiểm từng nội dung yêu cầu có thật trên frame, đọc được và xuất hiện cùng thời điểm nói. Frame count, caption khớp ASR, nhiều ảnh hoặc texture 3D đầy đủ đều không thay được phép kiểm này. Cần giữ cả lỗi và bằng chứng sửa; không tự chuyển thành được người dùng duyệt.
