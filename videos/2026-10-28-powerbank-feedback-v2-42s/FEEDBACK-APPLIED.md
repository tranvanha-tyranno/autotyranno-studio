# Phản hồi người dùng và bản sửa

## Vấn đề xác nhận ở bản trước

Đã xem ảnh mở đầu và khung 0/3/6/9 giây của sáu nguồn. Cảnh 1: mean luma cuối/ảnh mở đầu khoảng 0,875; cảnh 3 khoảng 0,887. Chỉ số toàn hình có ảnh hưởng bố cục nhưng khung đối chiếu cũng cho thấy nền/áo/sản phẩm tối đi. Hook trước chỉ nêu tình huống pin yếu, không có cú bất ngờ. Các động tác chủ yếu chỉ cạnh vỏ, không phải chạm. Video có card chữ trái với yêu cầu mới.

## Thay đổi đang áp dụng

1. Chân dung nhân vật trưởng thành hư cấu riêng được tạo/duyệt **trước** ảnh sản phẩm. Dùng chân dung này trong tất cả ảnh/video.
2. Không chèn chữ: `text_overlays: false`; không tạo hoặc nạp caption card khi render. Giữ ký tự vật lý vốn có trên sản phẩm.
3. Hook nói: “Tưởng hộp phấn? Sạc dự phòng đó!”; kiểm tra khoảng nghỉ đầu cho thấy hook hoàn tất trước khoảng 2,2 giây trong take gốc. Giá ấm inox trong ví dụ người dùng không được gán sang sạc.
4. Hành động có mốc nguồn: đưa lên → dừng tự nhiên 0,5–0,6s → xoay 5–8° → tay kia chạm/miết phần vỏ trống → trở về. Không dùng freeze-frame hoặc loop để giả nhịp dừng.
5. Ánh sáng studio cố định, camera ít dịch. Thêm khóa exposure/white balance vào video prompt. Đo độ sáng ROI so với ảnh mở đầu, nội suy bù luma nhẹ có giới hạn, sau đó phải xem lại thành phẩm.
6. Không đánh dấu hoàn hảo chỉ vì decode/âm lượng đạt. Xem bảng hành động 2 khung/giây và ghi rõ hạn chế còn thấy.

## Source

`AGENTS.md`, `WORKFLOW.md`, `README.md` cập nhật preference. `storyboard.py` thêm chân dung chuẩn, cổng QA nhân vật, mặc định không chữ, bảng hành động, QA video bắt buộc và căn giọng theo khoảng lặng đã đo. `quality.py` đo/hiệu chỉnh tối dần. `test_workflow.py` có 16 bài đã qua, gồm chế độ không chữ và clip thử fade-to-dark. Template mới `example-powerbank-portrait-first.json` không mang mốc cắt giọng của một take cụ thể.

## Sửa ảnh thử

Ảnh cảnh 1 lần đầu giữ mặt nhưng tự thêm quai dài thứ hai; đã loại trước video. Dùng scene-01-r02 với một quai đúng kiểu, giữ ảnh lỗi ở scene-01 để đối chiếu.

## Lần sửa chuyển động

Hai cảnh cận đầu tiên có chạm vỏ nhưng model dựng đứng/lật sản phẩm và đổi ô đen thành xám, nên đã loại cả hai. `scene-02-r02` và `scene-03-r02` dùng cùng ảnh mở đầu/giọng, khóa ô đen dưới-phải và quai trên-phải, tay đỡ đứng yên, chỉ cho nghiêng rất nhỏ theo chiều sâu. Không lấy việc có chạm làm lý do bỏ qua sai thiết kế.
