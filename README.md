# Affiliate Auto Tyranno

**Studio web mới:** chạy `./start-studio.ps1 -Open` sau khi cài dependency/build frontend. Tạo dự án, upload ảnh, sửa prompt với Muse Chat hoặc Gemini, chạy pipeline và xem kết quả tại `http://127.0.0.1:3000`. Xem [hướng dẫn Studio](docs/studio-web.md). Dashboard mock cũ nằm ở `/mock`.

MVP cho hệ thống tạo video AI bán hàng tự động bằng tiếng Việt. Backend cung cấp API để nhập sản phẩm, tạo video từ ảnh, kiểm tra policy, thu thập trend, xếp lịch và mô phỏng xuất bản. Frontend là dashboard Next.js tối giản.

## Chạy nhanh backend

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

Mở `http://localhost:8000/docs` để thử API. Dữ liệu mặc định nằm trong `data/app.db`, media nằm trong `data/media`.

## Chạy dashboard

```powershell
cd frontend
npm install
npm run dev
```

Dashboard mặc định gọi backend tại `http://localhost:8000`; có thể đổi bằng biến `NEXT_PUBLIC_API_URL`.

## Tạo video mẫu

Quy trình review sản phẩm bằng Muse2API và Adam V3 đã lưu tại [workflows/product-video/WORKFLOW.md](workflows/product-video/WORKFLOW.md). Mặc định hai clip với người mẫu hoặc chỉ tay và bối cảnh khác nhau, nhịp hình nhanh 1,5× từ ba cảnh mới; mỗi batch nằm trong `videos/`.

Chạy `python workflows/product-video/run.py cache --batch <batch>` rồi `plan` trước khi tạo để dùng lại TTS/media và xem số lần gọi provider dự kiến.

Bộ [prompt hộp mica POV 6 giây](workflows/product-video/mica/WORKFLOW.md) lưu nguyên bản và phiên bản nhịp nhanh 11–20. Compiler offline tạo prompt theo N × 3 ảnh, tách khỏi runner review 20 giây.

Gửi `POST /products/import`, sau đó dùng `POST /video-jobs` với `product_id`. Pipeline sẽ tạo script tiếng Việt, poster và MP4 dọc nếu có ffmpeg (backend dùng binary của `imageio-ffmpeg`). Provider AI/TTS hiện là provider mô phỏng, được tách interface để thay bằng API thật.

## Công nghệ cần đánh giá trước khi tích hợp

[muse2api: kiểm tra, đánh giá và thử nghiệm](docs/muse2api-evaluation.md) ghi nhận hai repo ứng viên cho tạo ảnh/video. Cần hoàn thành thử nghiệm bằng tài khoản thật và đánh giá kết quả trước khi quyết định tích hợp vào pipeline.

## Lưu ý

Adapter đăng TikTok hiện chỉ mô phỏng idempotent publish. Trước khi bật đăng thật cần thêm OAuth/token vault và chỉ dùng API chính thức của nền tảng. Nội dung có claim nhạy cảm hoặc dữ liệu sản phẩm thiếu sẽ bị chặn.
