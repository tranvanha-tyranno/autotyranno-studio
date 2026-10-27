# Repository và thiết lập trên máy mới

Mã nguồn, dashboard, bộ workflow/prompt, tài liệu và các batch ảnh/video/voice được lưu trong repository. Ảnh/video/âm thanh dùng Git LFS. Muse2API nằm trong Git submodule `experiments/muse2api-czg86389`, được ghim commit để không trộn lịch sử/mã nguồn upstream với ứng dụng Studio.

## Clone đầy đủ

```powershell
git lfs install
git clone --recurse-submodules <repository-url>
cd <repository-folder>
git lfs pull
```

Nếu đã clone mà chưa có submodule:

```powershell
git submodule update --init --recursive
git lfs pull
```

Sau đó cài Python dependency của `backend/requirements.txt`, dependency Muse2API theo README upstream và `npm ci` trong `frontend`. Build frontend bằng `npm run build` và chạy `start-studio.ps1` từ project root. Xem `docs/studio-web.md` và `docs/muse2api-evaluation.md` về cấu hình.

## Dữ liệu chỉ nằm trên máy hiện tại

- `.secrets/`, `.env`, cookie/account pool và profile Chrome không được commit.
- `data/studio/` là dự án web, ảnh upload, preferences, gợi ý AI và task state đang vận hành; không đưa phiên làm việc này lên GitHub. Có thể tải gói từng dự án bằng nút Xuất ZIP nếu muốn sao lưu riêng.
- `.cache/`, log, SQLite, virtualenv, `node_modules` và `.next` không được commit.
- Key DPAPI chỉ dùng với tài khoản Windows đã tạo key; máy khác cần nhập lại qua Kết nối AI. Pool Muse cũng cần nhập lại phiên đăng nhập hợp lệ.

Batch xuất trước đây trong `videos/`, tài liệu và ảnh demo ở `docs/`, các thử nghiệm media/scripts trong `data/` được giữ để xem lại. Các manifest lịch sử có đường dẫn máy cũ; với sản phẩm mới hãy tạo batch mới bằng workflow, không chạy lại nguyên xi đường dẫn cũ.
