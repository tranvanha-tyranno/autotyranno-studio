# Vì sao quán cà phê đông khách vẫn hết tiền?

Bản cuối: [xem video](index.html) hoặc [MP4 r02](r02/final.mp4), **9phút55giây / FullHD /30fps**.

Video giáo dục kinh doanh nguyên bản, khoảng10phút. Một quán giả định giúp lần theo doanh thu, phần đóng góp, hòa vốn, khuyến mại và lịch tiền mặt. Ảnh/clip của các cơ sở thật chỉ minh họa bối cảnh; không mô tả họ đang thiếu tiền hoặc kinh doanh thất bại. Không có nhận diện kênh, logo hoặc watermark do bản dựng thêm.

Giọng Nhật Phong,8take chương riêng, tốc độ1,0. Lời dài593,42giây; timeline17848frame/30fps, tương ứng594,93giây với khoảng nghỉ cuối. Giữ nguyên câu cuối, không cắt hoặc kéo giãn lời.

Hình kết hợp footage, ảnh thật, phiếu thu/giấy động, chữ nhấn, biểu đồ, đối chiếu và ly cà phê3D. Nguồn có20ảnh và13clip, trong đó22asset được dùng; nguồn chụp Việt Nam được phân biệt với địa điểm chưa được xác minh. Các khoảng lặp lại nguồn clip dùng trim khác nhau, không lặp đoạn để kéo dài.

Âm thanh gồm5bản nhạc mới, một nhạc cầu nối được giữ từ preset,10loại hiệu ứng ở18cue và hai nhịp hạ nhạc. Tất cả được phối dưới lời dẫn. Phép đo khoảng−16LUFS là kiểm kỹ thuật, không thay cho nghe duyệt.

Đọc [nguồn nghiên cứu và bản quyền](RESEARCH_AND_CREDITS.md), [lời dẫn](script.txt), [kiểm nội dung](sources/CONTENT_REVIEW.md), [kiểm frame tài chính](preview-qa/FINANCIAL_RENDER_REVIEW.md) và hồ sơ QA của bản cuối. Bản đầu được giữ; revisionr02 sửa thứ tự cue ba ý mở đầu, cue biểu đồ và đoạn extraction mở đầu.

Quy trình tái sử dụng nằm trong `workflows/reference-video/business.py`, `business_audio.py`, `business_render.py`, `business_refine.py`, `business_qa.py`, `business_review.py` và renderer `cinematic/src/business/`. Phản hồi/bài học được ghi trong `learning/`; cải tiến code và hồ sơ không phải huấn luyện trọng số hoặc tự duyệt bản mới.

Trạng thái: **đã xuất r02 và QA toàn17848frame,24targetedtests đạt; chờ phản hồi người dùng**. Root đã mở58midframe/lastframe cùng một số strip chuyển động; xem [quan sát bản cuối](r02/qa/ROOT_VISUAL_OBSERVATIONS.md). Ghi rõ phạm vi frame chọn mẫu và giới hạn nghe trong QA; không suy thẩm mỹ hoặc duyệt người dùng từ decode thành công.


Lượt kiểm hình độc lập cuối đã mở58/58midframe qua7sheet,199/199ảnh chọnmẫu3giây qua23sheet và9frame native. Xem [nhận xét độc lập](r02/qa/INDEPENDENT_VISUAL_REVIEW.md). Không ghi nhận lỗi mới cần chặn trong phạm vi chọn mẫu; không đồng nghĩa đã nghe/xem liên tục hay được người dùng duyệt.
