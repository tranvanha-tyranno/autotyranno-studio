# Hướng explainer kinh doanh — 13/11/2026

Phản hồi gần nhất về pilot siêu thị r07 là “kháổnđỉnh”: giữ hướng ảnh thật Việt Nam kết hợp chuyển động 3D có ích và miễn trừ trách nhiệm rõ. Đây là nhận xét về pilot; không phải duyệt trước chất lượng chuyên nghiệp của video tiếp theo.

Người dùng đã yêu cầu làm bản đầy đủ khoảng 10 phút, chủ đề kinh doanh, phối hợp ảnh/footage thật, biểu đồ 2D, chữ động và 3D; âm thanh giàu ngữ cảnh và trình bày chuyên nghiệp. **Không hiển thị bất kỳ thương hiệu kênh, tên, logo hoặc watermark kênh nào.** Yêu cầu này thay cho nhận diện kênh trước đây trong hướng explainer kinh doanh; không thay các workflow sản phẩm/mica.

## Bản đang thực hiện

Batch: `videos/2026-11-13-quan-dong-khach-het-tien/`.

Chủ đề: “Vì sao quán cà phê đông khách vẫn hết tiền?”. Một quán giả định giúp phân biệt doanh thu, phần đóng góp, chi phí cố định và lịch tiền mặt. 58 beat, 8 chương; take Nhật Phong đã chốt phải được giữ chính xác, tốc độ 1,0. Timeline hiện 17848 frame/30fps≈594,93giây, gồm đuôi lời cuối. Giữ hook→miễn trừ ngắn→nội dung chính→CTA có hành động; disclaimer là nội dung người dùng yêu cầu.

Ảnh/clip quán thật chỉ là bối cảnh, không bằng chứng doanh nghiệp ấy thiếu tiền hoặc kinh doanh kém. Ghi tình huống giả định từ hook nếu lời dẫn kể chủ quán thiếu tiền trước lúc lời nêu mô hình. Cảnh đông/vắng thuộc các quán khác nhau không được kể thành cùng một quán trước/sau thất bại. Giá 35k/15k/29k và 48 triệu là số giả định; chart tự tạo phải giữ đầy đủ đơn vị, dấu âm và phạm vi mô hình.

## Phần tái sử dụng

- `business.py`: validate nội dung; voice/assemble theo take chương; prepare ánh xạ đủ 58 beat, exact-take captions, source/hash/giấy phép, clip duration và trim không trùng, chặn nhận diện kênh trong trường nhìn/lời đọc.
- `business_audio.py`: plan/generate/mix theo batch, cache receipt để không gọi lại nguồn trả phí chỉ vì sửa hình; nhạc nền theo chương, cue ngữ cảnh, duck dưới lời và đo mix thật. Cue không thay cho nghe; không nhận đo loudness là đã nghe liên tục.
- `business_render.py`: snapshot đầu vào, dựng phần có thể tiếp tục rồi ghép; chỉ nhận thành công khi kiểm frame/output. Không sửa manifest/source đang đóng băng giữa một lần render; thay đổi cần attempt/revision mới.
- `cinematic/src/business/` và `cinematic/src/business-entry.tsx`: composition riêng `BusinessPreview`, các cảnh photo/paper/question/chart/split/coffee/closing. Dùng nhiều layout theo ý, giữ palette và narrator thống nhất; không biến nội dung thành dashboard rối.

Ảnh/footage phải khớp chủ thể/hành động/vật thể từng câu. Phép tính, tồn kho, phân biệt tiền chi/chi phí kỳ và đối soát cần đồ họa cơ chế gốc; hạt cà phê không tự chứng minh đã mua/tồn kho, clip POS không chứng minh tiền đã về ngân hàng. Dùng máy xay espresso thật khi có cue máy xay; footage xưởng rang không được đổi nhãn thành xay một liều. Cue Foley gắn chuyển động nhìn thấy; âm gốc stock mặc định tắt khi chưa kiểm quyền/nghe.

Ưu tiên ảnh Việt Nam có nguồn xác nhận địa điểm; nguồn khác hoặc chưa rõ vị trí giữ nhãn đúng, không suy từ ngoại hình/tên tác giả. Lưu ảnh gốc, sourceURL, tác giả, ngày, license, hash, ghi crop/fit/trim và attribution đầy đủ; bản ảnh chỉnh giữ điều kiện CC BY-SA tương ứng. Đồ họa/kịch bản gốc là thành phần riêng. Không đưa giấy phép hay code vào luồng xem chính trừ ghi chú tư liệu ngắn hữu ích.

## Tài liệu batch và kiểm chất lượng

`content.json`/`script.txt`: lời và mô hình; `sources-candidates.json`: thư viện 33 nguồn; `source-receipts.json`: 22 nguồn dùng và 36 biến thể public; `clip-intervals.json`: trim theo 30fps; `sources/CONTENT_REVIEW.md`: kiểm 58 beat/phép tính/nguồn; `RESEARCH_AND_CREDITS.md`: nguồn chính phủ, giả định, attribution/giấy phép/thay đổi từng nguồn.

Kiểm bản MP4 thật: đủ frame/thời lượng/tail, loudness, caption/crop/biểu đồ, nhãn giả định, độ khớp nguồn với câu, chuyển động và cue âm. Phân biệt xem contact sheet/frame, xem chuyển động, nghe đoạn và xem/nghe toàn bản; chỉ ghi việc đã làm. Duyệt kỹ thuật, nhận xét biên tập có phạm vi và phản hồi người dùng là ba loại khác nhau.

**Trạng thái bản kinh doanh 10 phút: đang dựng/QA, chờ phản hồi người dùng.** Không gán phản hồi pilot cho video mới, không coi render thành công là user-approved và không tạo lesson verified trước khi có bản sửa cùng bằng chứng kiểm tương ứng. Cải tiến được lưu vào code/profile/tài liệu tái sử dụng và ledger có chứng cứ; đó không phải huấn luyện trọng số mô hình. Không tạo lịch chạy nền hoặc video mới khác chỉ từ tài liệu này.
