# muse2api: kiểm tra, đánh giá và thử nghiệm trước khi tích hợp

Ngày khảo sát: 27/10/2026.

**Trạng thái: cần thử nghiệm; chưa chọn làm provider chính thức.** Phải kiểm tra mã nguồn, đánh giá khả năng đáp ứng và chạy thử bằng tài khoản thật trước khi triển khai tích hợp vào pipeline Affiliate Auto Tyranno.

Đã đọc README và các phần mã nguồn liên quan đến API, trình duyệt, tài khoản, tác vụ và media của hai repo. Sau khảo sát ban đầu, đã cài và kiểm thử offline repo `czg86389-hub`; một lần thử tạo video từ ảnh bằng tài khoản thật đã thành công. Xem [báo cáo video Toshiba 8 giây](experiments/muse-image-video-task_3feccfe8824646fd95d2/README.md). Các checklist bên dưới vẫn cần đánh giá đầy đủ; chưa kết luận ổn định hoặc đáp ứng video liền mạch 20 giây.

## Hai repo cần đánh giá

| Nội dung | www222fff/muse2api | czg86389-hub/muse2api |
| --- | --- | --- |
| Nguồn | https://github.com/www222fff/muse2api | https://github.com/czg86389-hub/muse2api |
| Commit đã đọc | `618aeb0d569e71a8e57d3e4724015b0e18d3ac03` | `5b8bba9561fdbe6402fbc08012d144699760afd0` |
| Phiên bản trong mã | `0.3.0` trong `pyproject.toml` | `1.6.4` trong `version.json` và `app.py` |
| Cấu trúc | Tách protocol, service, account pool và driver; có mock để phát triển offline | Phần lớn logic nằm trong `app.py`, `engine.py`, `store.py`; có dashboard vận hành |
| Cách gọi Muse thực tế | Chromium/CDP; driver HTTP trực tiếp chưa triển khai chức năng sinh nội dung | Chromium/CDP; HTTP dùng cho kiểm tra/duy trì phiên và đánh thức VM |
| Ảnh | Tạo ảnh, ảnh tham chiếu, edits; có tùy chọn xóa nền bằng mô hình chạy cục bộ | Tạo ảnh, edits, tối đa 4 ảnh tham chiếu có thứ tự; kiểm tra xác nhận upload và chọn đúng media mới |
| Video | Từ văn bản hoặc một ảnh đầu tiên | Từ văn bản hoặc tối đa 4 ảnh tham chiếu; ảnh đầu tiên là ảnh khởi đầu chính |
| Tác vụ ảnh | Chế độ async và polling | `/v1/images/tasks`, polling, `Idempotency-Key` chống tạo trùng cho luồng tác vụ ảnh |
| Tài khoản | Nhiều chiến lược phân phối; cấu hình số tab đồng thời trên mỗi tài khoản | Nhiều tài khoản chạy song song; khóa tránh cùng tài khoản bị hai tác vụ chiếm dụng; mặc định tổng đồng thời là 2 |
| API văn bản | Chat Completions và Responses đã có trong mã | Chat Completions và Responses cho văn bản; tool protocol thử nghiệm mặc định tắt |
| Ưu tiên thử đề xuất | Đối chiếu khả năng mở rộng, API và xóa nền | Thử trước cho luồng ảnh sản phẩm → ảnh/video do đã có xử lý tác vụ, nhiều ảnh tham chiếu và các sửa lỗi media cụ thể |

Hai repo có cấu trúc và API khác nhau; không suy ra quan hệ fork hay repo nào ổn định hơn chỉ từ tên, số sao hoặc số phiên bản. Ưu tiên thử là đánh giá ban đầu dựa trên mã nguồn, chưa phải quyết định lựa chọn.

## Những điểm đã xác định cần kiểm chứng

- Cả hai là cầu nối đến web Muse qua phiên đăng nhập, phụ thuộc trình duyệt, giao diện và khả năng của tài khoản upstream.
- Tên như `gpt-5`, `claude-sonnet-4`, `sora`, `veo` chỉ được ánh xạ sang chức năng Muse. Không xem đó là bằng chứng được chọn đúng model của nhà cung cấp tương ứng.
- Tỷ lệ khung hình và thời lượng video được đưa vào prompt; phải đo kích thước và thời lượng file thực tế. Không coi thông số đầu vào là bảo đảm đầu ra.
- Repo `czg86389-hub` tự thêm yêu cầu xóa chữ, watermark và logo khi tạo ảnh từ ảnh tham chiếu (`build_image_prompt`). Điều này có thể làm mất nhãn hiệu, chữ trên bao bì hoặc đặc điểm nhận diện sản phẩm. Cần thử đối chiếu và sửa yêu cầu này trong bản thử nếu làm sai sản phẩm.
- Ảnh đầu vào cho chat ở repo `czg86389-hub` hiện được chuyển thành ký hiệu văn bản `[图片]` trong `_content_text`, không được chuyển thành upload ảnh thật qua luồng chat đã đọc. Không nhầm với hỗ trợ ảnh tham chiếu ở API tạo ảnh/video.
- Repo `czg86389-hub` có mô phỏng tool calling bằng prompt và phân tích JSON, mặc định tắt. Responses hiện trả nội dung văn bản. Chưa có cơ sở coi đây là backend đầy đủ cho agent cần gọi công cụ.
- Tuyên bố về độ trễ 2–3 giây hay duy trì phiên 48 giờ của repo `czg86389-hub` cần đo ở môi trường triển khai. Mã đọc cookie do upstream trả về; không bảo đảm tự gia hạn thành công hoặc dùng vô hạn.
- Cần kiểm tra quota và khả năng tạo video bằng chính tài khoản và đường mạng triển khai; phản hồi giới hạn vùng, hết quota và lỗi phiên phải được ghi riêng.
- README/TODO của repo `www222fff` có phần chậm cập nhật: Responses và image edits đã có mã dù một số bảng còn ghi chưa triển khai. Xác nhận bằng mã ở commit được thử.

## Trình tự thử nghiệm bắt buộc trước khi làm tích hợp

### 1. Kiểm tra offline và chuẩn bị bản thử

- [ ] Chốt commit của từng repo, chạy trong môi trường riêng với cấu hình và dữ liệu riêng.
- [ ] Chạy các kiểm thử sẵn có liên quan đến API, ảnh tham chiếu, chọn media, tác vụ async, đồng thời, quota và duy trì phiên; lưu lệnh, môi trường và kết quả thực tế.
- [ ] Xác minh dịch vụ, Chromium, API key và dashboard hoạt động; phân biệt rõ mock với driver thật.
- [ ] Giữ phiên bản cố định trong đợt đo; kiểm tra cơ chế nâng cấp/thử khôi phục trước khi sử dụng nút cập nhật trực tiếp của repo `czg86389-hub`.

### 2. Chạy thử bằng tài khoản thật

Dùng cùng bộ sản phẩm, ảnh đầu vào và mục tiêu đầu ra cho hai repo. Bộ mẫu khởi đầu đề xuất: 3 sản phẩm có màu sắc, logo/chữ và hình dáng dễ đối chiếu; mỗi ca quan trọng chạy lặp 3 lần nếu quota cho phép. Ghi rõ số mẫu đã chạy, kể cả trường hợp thất bại.

| Ca thử | Bằng chứng cần lưu |
| --- | --- |
| Chat và kịch bản tiếng Việt | Prompt, kết quả, độ trễ; đánh giá đúng thông tin sản phẩm |
| Tạo ảnh từ văn bản | Ảnh gốc đầu ra, tỷ lệ, kích thước, thời gian chờ |
| Tạo ảnh từ 1 và nhiều ảnh tham chiếu | Màu, hình dáng, logo/chữ, bao bì; xác minh không trả ảnh upload hoặc ảnh lịch sử |
| Tạo video từ ảnh sản phẩm | File video thật có chuyển động; không nhầm ảnh bìa; giữ đúng sản phẩm |
| Video dọc 9:16 và thời lượng yêu cầu | Kích thước, thời lượng đo từ file; lỗi méo/cắt, viền đen, chuyển động sai |
| Tác vụ async, polling và gửi lại yêu cầu | ID và trạng thái; riêng luồng ảnh hỗ trợ idempotency phải xác minh gửi lại cùng khóa không tạo thêm tác vụ |
| Lỗi và khởi động lại dịch vụ | Hết quota, phiên hết hạn, từ chối tạo nội dung, timeout; trạng thái tác vụ và khả năng lấy lại file đã hoàn thành |
| Chạy đồng thời | Bắt đầu 1 tác vụ, sau đó 2 tác vụ nếu đủ tài khoản/quota; xác minh không lẫn tài khoản, prompt hoặc kết quả |
| Duy trì phiên và đánh thức VM | Theo dõi ít nhất qua mốc 48 giờ; lưu trạng thái thật và cookie hết hạn đã che giá trị; phân biệt yêu cầu wake được nhận với VM đã `RUNNING` |

### 3. Đánh giá rồi mới quyết định tích hợp

- [ ] Báo cáo số thành công/thất bại, tỷ lệ đạt chất lượng, thời gian trung vị và trường hợp chậm nhất, CPU/RAM, quota tiêu thụ và chi phí quan sát được. Không suy ra chi phí bằng 0 chỉ vì mã nguồn miễn phí.
- [ ] Kiểm tra file trả về dùng được ở bước dựng video tiếng Việt, ghép giọng đọc/phụ đề và lưu media của dự án.
- [ ] Chỉ đề xuất tích hợp chức năng có bằng chứng chạy được, file đầu ra hợp lệ, sản phẩm được giữ đúng và lỗi có thể xử lý rõ ràng.
- [ ] Nếu ca giữ logo/bao bì, chọn đúng media hoặc tạo video thật còn thất bại chưa giải thích được, giữ trạng thái thử nghiệm và ghi việc cần sửa trước khi tích hợp chức năng đó.
- [ ] Ghi kết luận riêng cho từng repo: tiếp tục thử / cần sửa rồi thử lại / đủ điều kiện làm adapter thử / không phù hợp; kèm giới hạn và kết quả mẫu.

Khi có kết quả đủ tốt, bước tiếp theo là làm adapter thử qua interface provider hiện có, có cấu hình lựa chọn provider. Các phần dựng clip, TTS, phụ đề và xuất bản vẫn cần được đánh giá riêng trong pipeline của dự án.

## Nhật ký kết quả

## Bản clone để tiếp tục thử

Bản clone nằm tại [experiments/muse2api-czg86389](../experiments/muse2api-czg86389) ở commit `5b8bba9561fdbe6402fbc08012d144699760afd0`. Để chạy lại trên Windows:

```powershell
cd C:\Users\tyranno\Documents\Project\AffilateAutoTyranno\experiments\muse2api-czg86389
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:MUSE2API_KEY = "tự-đặt-một-key-thử-nghiệm"
$env:MUSE2API_CHROMIUM = "C:\Program Files\Google\Chrome\Application\chrome.exe"
python -m uvicorn app:app --host 127.0.0.1 --port 18610
```

Đã thiết lập `.venv` và `.env` cục bộ để chạy thử, với key tự sinh, Chrome trên máy và mức đồng thời ban đầu là 1. Dịch vụ lắng nghe tại `127.0.0.1:18610`. Key và profile được giữ ngoài các file Git theo dõi. Đã có tài khoản Muse được nhập và dùng cho một lần thử video từ ảnh thành công.

Khởi động lại và mở trang quản trị có sẵn key bằng PowerShell từ thư mục gốc dự án:

```powershell
.\experiments\start-muse2api.ps1 -OpenAdmin
```

Script mở server chạy nền, lưu log tại `experiments/muse2api-czg86389/data/server-stdout.log` và `server-stderr.log`. Đã xác minh health `ok`, trang quản trị HTTP 200 và API quản trị chấp nhận key đã lưu. Trạng thái `no_account` là bình thường khi chưa nhập tài khoản thật. Bốn bản ghi giả `one/two` do test để lại đã được xóa sau khi đối chiếu đúng dữ liệu fixture trong `tests/test_refusal_rotation.py`.

| Ngày | Repo / commit | Môi trường, tài khoản đã ẩn danh | Ca thử / số lần | Kết quả, file bằng chứng | Kết luận |
| --- | --- | --- | --- | --- | --- |
| 27/10/2026 | Hai commit nêu trên | Chỉ đọc tài liệu và mã nguồn | Chưa chạy offline/live | Các nhận xét trong tài liệu này | Cần kiểm tra, đánh giá và thử nghiệm trước khi tích hợp |
| 27/10/2026 | `czg86389-hub/muse2api` @ `5b8bba9` | Windows, Python 3.11.9, virtualenv riêng; chưa có cookie | Clone và cài dependency thành công; `py_compile` đạt; `pytest --ignore` 15 passed, 19 subtests passed, 12 warnings | Server khởi động; `/healthz` trả `ok`; `/readyz` trả `no_account`; `/v1/models` trả 3 model; test quota, VM wake, session health và API error đạt. 4 file test bị lỗi khi pytest thu thập do `spec_from_file_location` không nhận đường dẫn; 3 file chạy trực tiếp với `engine.py` đạt. | Chạy được phần offline và smoke test; chưa chứng minh tạo ảnh/video thật |
| 27/10/2026 | `czg86389-hub/muse2api` @ `5b8bba9` | Cùng môi trường; Chromium chưa có trong PATH; Docker daemon chưa chạy | `tests/test_media_selection.py engine.py` dừng với `Chromium required`; `docker compose config` hợp lệ nhưng `docker info` không kết nối được Docker Desktop | Chưa kiểm tra browser/CDP, Docker image hoặc tạo media thật | Cần cài Chromium và bật Docker rồi thử lại |
| 27/10/2026 | `czg86389-hub/muse2api` @ `5b8bba9` | Windows, Chrome `C:\Program Files\Google\Chrome\Application\chrome.exe` chỉ dùng cho test offline | `MUSE2API_CHROMIUM=...\\chrome.exe .venv/Scripts/python.exe tests/test_media_selection.py engine.py` đạt | Ảnh upload bị loại khỏi kết quả; media cũ bị loại; chọn đúng video có `vSrc`; ảnh tham chiếu nhiều ảnh được xử lý; fallback video sai và ảnh bìa bị từ chối | Phần CDP/media-selection offline đạt; chưa tạo media trên Muse thật |

Không lưu cookie, API key hoặc URL quản trị có key vào docs hay file kết quả dùng chung.

## Nguồn đối chiếu

- www222fff: [README](https://github.com/www222fff/muse2api/blob/618aeb0d569e71a8e57d3e4724015b0e18d3ac03/README.md), [models](https://github.com/www222fff/muse2api/blob/618aeb0d569e71a8e57d3e4724015b0e18d3ac03/src/muse2api/core/models.py), [browser driver](https://github.com/www222fff/muse2api/blob/618aeb0d569e71a8e57d3e4724015b0e18d3ac03/src/muse2api/drivers/browser/driver.py), [Responses](https://github.com/www222fff/muse2api/blob/618aeb0d569e71a8e57d3e4724015b0e18d3ac03/src/muse2api/api/routes/responses.py).
- czg86389-hub: [README](https://github.com/czg86389-hub/muse2api/blob/5b8bba9561fdbe6402fbc08012d144699760afd0/README.md), [app.py](https://github.com/czg86389-hub/muse2api/blob/5b8bba9561fdbe6402fbc08012d144699760afd0/app.py), [engine.py](https://github.com/czg86389-hub/muse2api/blob/5b8bba9561fdbe6402fbc08012d144699760afd0/engine.py), [config.py](https://github.com/czg86389-hub/muse2api/blob/5b8bba9561fdbe6402fbc08012d144699760afd0/config.py), [version.json](https://github.com/czg86389-hub/muse2api/blob/5b8bba9561fdbe6402fbc08012d144699760afd0/version.json), [tests](https://github.com/czg86389-hub/muse2api/tree/5b8bba9561fdbe6402fbc08012d144699760afd0/tests).
