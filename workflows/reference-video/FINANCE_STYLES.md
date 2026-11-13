# Hai lựa chọn video đơn giản — 13/11/2026

> **Phản hồi mới nhất:** người dùng chê bản tối giản r02 giống slide và thấy nhân vật r03 chưa ưa mắt. Hai bản cần sửa, không phải baseline được duyệt. Người dùng đã chọn **“Comic biểu cảm mạnh, hơi hài hước”**. Dùng `cinematic/src/finance-flow/` cho chuyển động vật thể có nguyên nhân/kết quả và `finance-cast-v2/`, `finance-comic/` cho hai nhân vật comic mới. Giữ thư viện cũ; kiểm vài nhân vật trước khi nhân rộng30. Batch `videos/2026-11-13-hai-style-tiet-kiem-v2/` là proof18s của hai cảnh daily+dinner, dùng exact take/mix cũ; không phải phim đầy đủ hoặc phê duyệt tạo hình. Runner `finance_style_reset.py` snapshot trước bundle, preflight hình rồi render và QA. “Ít chi phí” vẫn phải có hành động diễn tiến theo lời, chuyển cảnh liên tục và bố cục phục vụ hành động; chỉ cho chữ xuất hiện rồi đứng yên không giải quyết góp ý.

Người dùng yêu cầu thêm **hai phong cách tùy chọn**, làm thử để xem trước: (1) nhân vật hoạt hình thiết kế riêng tương tác, tạo cảm xúc, nội dung tài chính, có thư viện khoảng 30 nhân vật dùng lại; (2) video tối giản, ưu tiên nội dung và chi phí. Đây là nhánh mới, không thay mặc định các explainer trước khi người dùng chọn.

## Nghiên cứu từ ảnh mẫu

Ảnh gốc được giữ tại `videos/2026-11-13-hai-style-tiet-kiem/reference/user-style-reference.png`. Quan sát được: hai người hoạt hình viền đậm, một người dang tay, người còn lại chỉ tay, biểu cảm rõ, các biểu tượng hạng mục tài chính và lưới tối. **Một ảnh không cho biết diễn biến, tốc độ dựng, thoại, nhạc, cách chuyển cảnh hay lip-sync.** Không ghi những điều đó là đã học từ video. Không sao chép mascot, logo, viền trang trí hoặc âm thanh nguồn.

Áp dụng: nhân vật gốc có dáng tóc/quần áo/phụ kiện khác nhau; một người nêu vấn đề, người kia giúp tính, phản ứng thay đổi theo kết quả; đạo cụ và con số chỉ xuất hiện để giải thích tình huống. Giữ nét và palette đồng nhất. Nội dung mới thay lưới tối bằng sân khấu giấy sáng để ưu tiên khả năng đọc.

## Chọn phong cách

| ID | Dùng khi | Cách dựng | Chi phí hình ảnh |
| --- | --- | --- | --- |
| `finance-cast` | Cần câu chuyện, đối thoại, hiểu lầm và phản ứng | SVG có bộ phận riêng, biểu cảm, tay, đầu, chớp mắt, đạo cụ chuyển động bằng frame | Dựng local, tái dùng thư viện, không cần API ảnh/video mỗi cảnh |
| `finance-minimal` | Ưu tiên lập luận, tốc độ sản xuất và ngân sách | Chữ, phép tính, sơ đồ nhỏ và chuyển động có chủ đích | Dựng local, không nhân vật/stock/3D |

Không gọi nhánh đơn giản này là footage, hoạt hình 3D hoặc video AI tạo sinh. Miệng nhấp theo khoảng có lời là chuyển động hoạt hình đơn giản, **không phải lip-sync âm vị đã xác minh**. Một giọng Nhật Phong kể và đọc lời nhân vật; không giả là hai diễn viên lồng tiếng khác nhau.

## Thư viện 30 nhân vật

Nguồn `cinematic/src/finance-cast/`, danh mục `finance-cast.json`. ID 1 Minh, ID 2 Lan là cặp demo. Mỗi nhân vật là người trưởng thành hư cấu. Có 15 nhóm tóc, 10 kiểu trang phục, 10 loại phụ kiện và 3 dáng người kết hợp thành 30 thiết kế. Đây là 30 thiết kế trong một hệ thống chung, không phải 30 bộ phim hay 30 rig vẽ tay hoàn toàn độc lập.

`Character` nhận id, x, y (điểm chân), scale, emotion, pose, frame, speaking, flip. Có 6 biểu cảm, 8 tư thế, khung đầu/tóc tới khoảng y=-485. Khi đổi bố cục phải kiểm cánh tay, đầu và phụ kiện trên khung render. `export-cast.cjs` xuất từng SVG trong suốt và roster, không gọi API. File SVG gốc vẫn sửa bằng mã, không dùng ảnh raster làm thay thế.

## Quy trình

1. Viết kịch bản gốc theo hook → miễn trừ ngắn → cơ chế/giới hạn → hành động cụ thể. Số tiền giả định ghi rõ và phép tính phải kiểm được. Nêu khả năng thay đổi chi thiết yếu; không áp mức chi hay tiết kiệm cố định cho mọi người.
2. Chọn style theo yêu cầu; không tự làm cả hai bản cho mọi chủ đề.
3. Khóa script, tạo một take Nhật Phong mới cho nội dung mới. Sửa hình giữ nguyên take; bản so sánh hai style dùng cùng take. `eleven_audio` giữ cache, receipt và unresolved intent để tránh gọi trả phí trùng khi gián đoạn.
4. Dùng exact character timestamps của take; giữ tốc độ 1.0 và câu cuối trọn vẹn. Lưu coverage từng đoạn; kiểm hình tại các mệnh đề thật.
5. Dùng nhạc đã có receipt/hash nếu phù hợp; cue ngắn có ý nghĩa và ưu tiên lời nói. Không tạo thêm nhạc/SFX chỉ để đổi style. Ghi nguồn tái sử dụng, thời gian render và provider cost header, không suy ra hóa đơn USD từ header.
6. Batch mới, public assets cô lập, snapshot mã và hash. Render tuần tự, kiểm đầy đủ frame/audio, lấy nhiều frame trong mọi cảnh. Xem frame không được ghi là đã xem/nghe liên tục hoặc đã duyệt chuyển động toàn video.
7. Chờ phản hồi thật của người dùng trước khi ghi style được duyệt. “Học” ở đây là lưu tri thức và mã tái sử dụng, không huấn luyện trọng số mô hình.

## Demo hiện tại

Batch `videos/2026-11-13-hai-style-tiet-kiem/`: cùng kịch bản **Lương tăng, vì sao tiền dư vẫn không tăng?**, 9 đoạn, 30 fps, khoảng 78s. `finance_demo.py` chuẩn bị script/timing/mix; `finance_demo_render.py` dựng tuần tự, snapshot và QA. Entry độc lập `cinematic/src/finance-demo-entry.tsx`; không sửa entry cũ.

Lệnh từ gốc dự án:

```powershell
python -X utf8 -B workflows/reference-video/finance_demo.py prepare
# voice là bước gọi speech trả phí; cache/intent bảo vệ khi chạy tiếp
python -X utf8 -B workflows/reference-video/finance_demo.py voice
python -X utf8 -B workflows/reference-video/finance_demo.py mix
python -X utf8 -B workflows/reference-video/finance_demo_render.py render
python -X utf8 -B workflows/reference-video/finance_demo_render.py qa
# Chọn một phong cách và revision mới sau khi sửa mã
python -X utf8 -B workflows/reference-video/finance_demo_render.py render --revision r02 --style toi-gian
python -X utf8 -B workflows/reference-video/finance_demo_render.py qa --revision r02 --style toi-gian
```

Không thay script/plan sau khi đã xuất rồi dùng lại silent.mp4 cũ. Thay nội dung hoặc sửa hình phải tạo revision mới và bundle lại; runner mới lưu dependency hash và chặn dùng bundle cũ khi source/plan/mix đổi. Bản nhân vật r01 có mũi tên đè số thu nhập trong hai cảnh ngân sách; r03 sửa vị trí và chỉ render lại khoảng frame 351–889, giữ take/mix. Bản tối giản r02 thêm lưu ý chi phí thiết yếu và cho đồng tiền tới đúng đích. Các bản cũ giữ nguyên. Hai bản giao xem thử là nhân vật r03 và tối giản r02, chưa có phản hồi duyệt của người dùng.
