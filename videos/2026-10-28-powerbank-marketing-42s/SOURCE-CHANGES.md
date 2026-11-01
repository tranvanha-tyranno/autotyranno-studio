# Cập nhật tái sử dụng trong repo

- `AGENTS.md`: lưu yêu cầu marketing mặc định — hook mạnh trong 3 giây đầu, lợi ích cụ thể, CTA cuối để chốt đơn; thông số cần nguồn, không bịa giảm giá/khan hiếm.
- `workflows/product-video/run.py`: nhận storyboard nhiều cảnh; chuẩn hóa upload PNG thật; giữ runner cũ tương thích.
- `workflows/product-video/storyboard.py`: ảnh mở đầu theo cảnh, khóa sản phẩm bằng hai ảnh, tùy chọn ảnh thứ ba để giữ nhân vật khi ảnh cận không có mặt, thư mục revision giữ lần sửa riêng, hash QA ảnh trước video, cache/plan đầy đủ, thoại riêng từng cảnh, kiểm tra hook/CTA nằm trong lời đọc, chữ tiếng Việt ghép bằng code, chặn thoại cũ, render/đo âm lượng/đen/đứng hình và contact sheet toàn thời lượng.
- `WORKFLOW.md` và `README.md`: lưu bài học mũ và hướng dẫn schema mới.
- `example-powerbank-storyboard.json`: manifest 42 giây của batch này, có nguồn và phạm vi thông số.
- `test_workflow.py`: 14 bài kiểm tra đã qua, gồm chuẩn hóa WebP/PNG, đủ nguồn không kéo chậm/lặp, resume không POST lặp, cache, duyệt ảnh theo hash, hook/CTA, thứ tự hai ảnh tham chiếu, render nhiều cảnh với thoại/chữ và chặn thoại cũ.

Không sửa hoặc ghi đè các batch đã có. Thay đổi sẵn có trong submodule Muse và runner trước phiên này được giữ lại.
