# Hai bản xem thử: hoạt hình tài chính và tối giản

- Nhân vật: `r03/nhan-vat/final.mp4`.
- Tối giản: `r02/toi-gian/final.mp4`.
- Bảng 30 nhân vật: `cast-library/contact-sheet.png`; từng SVG và roster trong cùng thư mục.
- Trang so sánh: `index.html`, phục vụ qua HTTP localhost để phát/tua video.

Cùng kịch bản gốc và một take Nhật Phong, 77,77 giây, 2333 frame, 1920×1080, 30 fps. Nội dung tài chính là giả định minh họa, không phải số liệu điều tra hoặc mức chi khuyến nghị. Giữ disclaimer riêng và CTA xem lại một khoản chi của mình. Không có channel branding.

Một lời đọc mới trả phí được dùng chung. Không gọi mới API ảnh, video, nhạc hoặc SFX. Nhạc tái dùng có receipt/hash; cue pluck ngắn tổng hợp tại máy. Header usage của voice là 462 theo provider, không suy ra hóa đơn USD. Tính cả thời gian dựng và điện/máy khi so tổng chi phí; hình local không có nghĩa toàn bộ video miễn phí.

Thời gian render hình đo riêng: bản nhân vật gốc 544,671s (~9,1 phút), bản tối giản 331,157s (~5,5 phút), chưa tính bundle, sửa/ghép và QA. Đây là số đo lần chạy này, không cam kết mọi video sau có tốc độ đó. Thời gian sửa hai cảnh nằm ở `r03/timings.json`.

R01 nhân vật giữ lại lỗi mũi tên đè số để đối chiếu; r03 chuyển mũi tên xuống dưới số và chỉ render lại hai cảnh. R02 tối giản sửa rõ lưu ý chi phí thiết yếu và điểm đến chuyển khoản. Bản r01 tối giản đã dừng trước khi xuất để không render lặp bản cần sửa.

QA: giải mã đủ video/audio, giữ câu cuối, cùng audio giữa hai phong cách; ảnh chọn mẫu ở 18%, 50%, 84% mỗi cảnh. Agent xem contact sheet và một số frame đủ độ phân giải; đây **không phải** xem/nghe liên tục toàn bộ và không xác lập người dùng đã duyệt. Chuyển động miệng là hoạt họa đơn giản, không xác nhận lip-sync âm vị.

Mã dùng lại và các lựa chọn: `workflows/reference-video/FINANCE_STYLES.md`, `finance-styles.profile.json`, `cinematic/src/finance-cast/`, `finance-demo/`, `finance-simple/`. Nghiên cứu ảnh mẫu chỉ khẳng định hình tĩnh quan sát được, không suy ra âm thanh/chuyển động của video nguồn. Không thay những hướng cũ trước khi người dùng chọn.
