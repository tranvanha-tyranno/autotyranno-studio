# Học lại cấu trúc nội dung từ các video đã tải

Đợt nghiên cứu bắt đầu ngày 14/11/2026. Sau đó người dùng yêu cầu làm lại toàn bộ phim bánh mì; các phát hiện đang được áp dụng trong nhánh riêng `bread_documentary.py`, không xóa các nghiên cứu hoặc bản phim cũ.

Đọc [LIBRARY_REVIEW.md](LIBRARY_REVIEW.md) để xem kiểm kê 23 ID không trùng, kênh thật, video/audio đang có và phạm vi kiểm của từng nguồn. Không gọi việc đã có file hoặc giải mã được file là đã xem/nghe nó. Bản tải chỉ dùng nghiên cứu; không đưa footage/nhạc/mascot của các kênh vào phim mới.

## Chín mẫu đã đọc lại toàn caption và chia đoạn lập luận

| Kênh | Bài | Phân tích |
|---|---|---|
| Lóng | Châu Âu | [w3z43Hlzq3c](analyses/w3z43Hlzq3c.md) |
| Lóng | Vĩnh Hưng/quy hoạch | [1OGwWLvasIk](analyses/1OGwWLvasIk.md) |
| Lóng | Thẻ bài TCG | [gNznfzAUiLw](analyses/gNznfzAUiLw.md) |
| Lóng | Huấn Hoa Hồng/kinh tế chú ý | [3JUxxp2sIDM](analyses/3JUxxp2sIDM.md) |
| Lóng | AI và việc làm | [JlfAd_OaFek](analyses/JlfAd_OaFek.md) |
| Lóng | Shein | [podWgLH4b3M](analyses/podWgLH4b3M.md) |
| THE HIDDEN SELF | Trung Quốc | [29B8-FtuC6U](analyses/29B8-FtuC6U.md) |
| THE HIDDEN SELF | Mẫu 5zqAMK2qsfM | [5zqAMK2qsfM](analyses/5zqAMK2qsfM.md) |
| THE HIDDEN SELF | Mẫu 5uTC396kCs4 | [5uTC396kCs4](analyses/5uTC396kCs4.md) |

Mỗi bản JSON cạnh Markdown ghi nguồn/hash, phạm vi đọc, mốc chương, câu hỏi, luận điểm, ví dụ, cơ chế, chuyển ý và payoff. Phân biệt chapter do người xuất bản khai báo với ranh giới do agent suy luận từ caption. Các source còn lại giữ đúng phạm vi trong inventory và báo cáo bổ sung; phần đọc dở không được cộng thành full-read. Caption có thể sai tên/số/năm; các phát biểu của nguồn được nghiên cứu như cách lập luận, chưa tự thành sự thật đã kiểm độc lập.

Đã mở một số contact sheet ở các mốc ghi cụ thể trong từng analysis. Chưa xem/nghe liên tục toàn bộ chín MP4. Không dùng mẫu ảnh để suy ra nhấn giọng, SFX, mọi cut hoặc hiệu quả giữ chân đã được đo.

## Những gì thực sự đổi trong cách viết

Vĩnh Hưng không chỉ xếp danh sách mô hình: bài đặt câu hỏi nhà ở dày hơn thì đi lại thế nào, rồi mới sang giao thông và tiện ích gần nhà. TCG khoảng 09:39–09:53 chốt các câu vừa giải rồi mở nghịch lý tiếp: in hàng tỷ thẻ, vì sao vẫn hiếm? Mẫu Huấn có một chương bản lề chỉ khoảng 16 giây (04:20–04:36) để chuyển từ lượng người theo dõi sang cách đổi thành tiền. Độ dài chương theo chức năng, không chia đều.

Những thủ pháp này không phải công thức bảo đảm retention. Nguồn cũng có đoạn lặp, sponsor đổi hướng, nhảy cấp khái quát, số/hình/caption chưa chắc khớp. Báo cáo ghi cả điểm yếu; không sao chép mọi lựa chọn vì kênh đã đăng nó.

Áp dụng có thể đọc ngay:

- [Chẩn đoán toàn script bánh mì cũ](OWN_SCRIPT_DIAGNOSIS.md): có tám chapter dữ liệu nhưng nhiều đoạn đang xếp nhóm kiến thức, chưa tạo diễn tiến.
- [Bài tập dàn ý và đoạn viết thử](REWRITE_EXERCISE.md): đã sửa sau phản biện về việc trả hết câu hỏi quá sớm. Đây là bài tập, không phải bản script cuối của phim mới.
- [Quy trình nội dung dùng lại](../../../workflows/reference-video/CONTENT_FIRST.md): một câu hỏi chính; mỗi chương có câu hỏi, cơ chế, ví dụ, điểm nhấn, kết luận và cầu nối có lý do.
- [Nhánh làm lại toàn bộ](../../../workflows/reference-video/BREAD_DOCUMENTARY.md): dùng footage thật, bỏ cartoon/subtitle và đoạn miễn trừ riêng ở đầu theo yêu cầu mới.

`editorial_gate.py` kiểm đủ/đúng thứ tự lời, review còn khớp script và map trước timed TTS mới. Việc kiểm bằng máy không đánh giá được văn hay, sự thật toàn nguồn, chất giọng hoặc người dùng đã duyệt. Review của agent là đọc phản biện kịch bản; lưu tri thức dự án không phải huấn luyện trọng số mô hình.
