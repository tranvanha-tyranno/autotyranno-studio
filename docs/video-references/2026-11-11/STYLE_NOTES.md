> Cập nhật tiếp theo sau phản hồi người dùng: hướng footage thật đã được ghi nhận, nhưng mic/waveform cố định gây nhàm. Default mới là Lăng Kính / Tyranno, nhiều bố cục trong một video và cue-based SFX. Xem workflows/reference-video/WORKFLOW.md và lang-kinh.profile.json.

> Ưu tiên bản sửa mới: đọc `RELEARN_AUDIT.md`. Nhận định cũ coi cả 17 là cùng một style là sai. Có 9 podcast, 4 bản tin Giao lộ và 4 bình luận. Không dùng renderer hình tĩnh cũ. Chỉ ghi audio/video đã tải đủ khi `local_av.full_decode` trong evidence là passed.

# Hồ sơ học phong cách video tham chiếu — 11/11/2026

## Phạm vi và bằng chứng

Đã lập catalog cho 17 URL YouTube người dùng cung cấp. Lưu từng video theo ID tại `docs/video-references/2026-11-11/<video-id>/` với `evidence.json`, tiêu đề, thời lượng, phụ đề tiếng Việt khi YouTube cho phép, `transcript.txt` và một số `reference.mp4` tải được ở 144p/360p để xem nhịp hình. `analysis.json` chứa đoạn mở/đóng và thuật ngữ nổi bật của từng transcript. Phụ đề tự động có thể sai dấu, tên riêng và con số; mọi dữ kiện thời sự/tài chính/pháp lý phải kiểm tra bằng nguồn độc lập trước khi dùng.

Một số lượt tải media/phụ đề bị YouTube giới hạn HTTP 429 hoặc chỉ cung cấp stream tách hình/tiếng; các lỗi được giữ trong `evidence.json`, không coi là đã xem toàn bộ. Vì vậy hồ sơ dưới đây tách rõ điều đã đo từ transcript/khung mẫu và điều cần kiểm tra khi sản xuất.

## Hai lựa chọn cho mỗi video mới

- **Tự đề xuất:** hệ thống đọc nhóm chủ đề và tín hiệu xu hướng, đề xuất 3 ý tưởng có góc nhìn khác nhau, sau đó chọn một theo tiêu chí mới mẻ, có nguồn và phù hợp độ dài.
- **Chủ đề người dùng nhập:** giữ chủ đề, đối tượng và mục tiêu; hệ thống viết lại hook, luận điểm, shotlist và nguồn cần kiểm chứng.

Cả hai lựa chọn đều đi qua: ý tưởng → research brief có nguồn → luận đề → kịch bản → shotlist → prompt hình/video → asset manifest → voice take → dựng → QA → báo cáo. Video tham chiếu chỉ học cấu trúc/nhịp kể, không sao chép câu chữ, thumbnail, logo, nhân vật hay footage.

## Mẫu số chung đã học

### Xác nhận bằng khung hình trực tiếp — 11/11/2026

Đã xem lại contact sheet lấy từ bản media cục bộ của `29B8-FtuC6U`, `5uTC396kCs4`, `UA7yZNRmZYY` và `5_7IDQEU5OI`, rồi đối chiếu các video còn lại. Mẫu thực tế là video **ngang 16:9 1920×1080**, tông tối và tương phản thấp kiểu documentary/podcast. Hình thay đổi liên tục theo lời dẫn: phố đêm, nhà máy, tay viết trên giấy, điện thoại, biểu đồ, bản đồ, đám đông, chân dung và cảnh đời thường. Trên hình có một lớp nhận diện podcast màu trắng: micro ở giữa, đường/waveform âm thanh và thanh điều khiển tối giản; caption nhỏ nằm sát đáy. Một số mẫu có logo/chữ nhận diện riêng và card quảng bá ở giữa/cuối.

Nhịp đúng của mẫu là voice-over dẫn chuyện + B-roll cắt theo ý, không phải sáu poster đứng yên. Hook thường là câu hỏi nghịch lý, sau đó dùng ẩn dụ đời thường, mở rộng sang cơ chế kinh tế, rồi kết bằng một câu hỏi hoặc kết luận có dư âm. Khi tái tạo cho Auto Tyranno, chỉ học bố cục và nhịp; dùng nhận diện riêng, footage/đồ họa mới và không sao chép logo, watermark hay card bán hàng của kênh mẫu.

1. **Hook 0–10 giây:** câu hỏi hoặc nghịch lý lớn, thường đặt đối lập “có X nhưng thiếu Y”, rồi trả lời sớm bằng một luận đề ngắn. Mẫu mạnh dùng một hình ảnh đời thường để làm mô hình (nhà hàng đầy bếp nhưng vắng khách) trước khi mở ra vấn đề vĩ mô.
2. **Lời hứa:** nói rõ người xem sẽ hiểu nguyên nhân, cơ chế hoặc hệ quả nào; tránh mở đầu chung chung. Hook phải đúng với dữ liệu đã kiểm tra.
3. **Cấu trúc thân bài:** bối cảnh → định nghĩa khái niệm → cơ chế nhân quả → số liệu/ví dụ → phản biện hoặc rủi ro → hệ quả cho người xem → kết luận. Mỗi đoạn trả lời một câu hỏi và chuyển bằng câu treo.
4. **Tạo hình dung:** dùng ẩn dụ không gian/đời sống (nhà hàng, dòng tiền, căn phòng, chiếc ví) để giải thích khái niệm trừu tượng; sau đó quay lại biểu đồ, bản đồ, ảnh tư liệu hoặc B-roll có nguồn.
5. **Nhịp:** lời dẫn liên tục, câu ngắn xen câu dài; nhấn từ khóa bằng ngắt nhịp và âm nhạc. Dựng B-roll thay đổi theo ý, không lạm dụng zoom/quay camera chỉ để tạo chuyển động.
6. **Giọng:** bình luận tiếng Việt nam/trung tính, chắc và điềm tĩnh; tò mò ở hook, nghiêm ở rủi ro, chậm hơn khi kết luận. Nhạc nền làm nhịp cảm xúc nhưng phải nhường lời.
7. **Kết:** quay lại luận đề bằng một câu cô đọng, mở rộng hệ quả dài hạn hoặc hành động người xem nên làm. CTA nên mời xem phần tiếp/đọc nguồn/để lại góc nhìn, không hứa lợi nhuận hay dùng khan hiếm giả.
8. **Chữ/hình:** chữ trên màn hình chỉ để định danh khái niệm, số liệu và nguồn; không làm phụ đề dày đặc. Bất kỳ số liệu nào hiện lên phải có nguồn, ngày và phạm vi.

## Các cụm chủ đề trong 17 mẫu

- **Trung Quốc, cầu nội địa và dòng vốn:** `29B8-FtuC6U`, `5uTC396kCs4`, `5zqAMK2qsfM`, `NCl_PG00oa4`.
- **Kinh tế thế giới, lãi suất, suy thoái, lạm phát:** `5_7IDQEU5OI`, `Glw9YcOMw2s`, `L0uNZyvCAxE`, `ERI4I4V4sBs`, `9I2suK0eob4`.
- **Bất động sản, ngân hàng, đất đai và luật:** `bm5q0e4MXhg`, `v74IRBimBk0`, `njD0SI3TNxg`, `X2Uadb-AKTw`.
- **Năng lực cá nhân, tiêu dùng, cơ hội:** `UA7yZNRmZYY`, `ggxRI_1u0_4`, `BOD_6bf_6pM`.
- **Bẫy thu nhập trung bình:** `96eyTrbH-ak`.

## Luật sản xuất đã cập nhật

- Có hai đầu vào: `auto_idea` hoặc `user_topic`; không tự dựng khi chưa có brief sản phẩm/chủ đề và phạm vi kiểm chứng.
- Với video phân tích dài, dùng scene theo luận điểm, không dùng profile review sản phẩm 20 giây. Mỗi cảnh cần `claim`, `source_refs`, `visual_asset`, `narration_range` và trạng thái QA.
- Không bịa số liệu, dự báo, giá, lợi nhuận, trải nghiệm hoặc nhận định pháp lý. Tách `verified_fact`, `source_claim`, `analysis/inference`, `uncertainty` trong research brief.
- Không coi thay presenter/background là đủ để tạo nội dung nguyên bản; phải viết luận điểm, ví dụ và hình minh họa mới.
- Giữ bản gốc, prompt, script, audio, task ID, final MP4, contact sheet, transcript và QA trong từng thư mục `videos/<batch>/`.
- Đối với presenter nói, phải chốt take và timing trước khi lip-sync. Muse hiện không nhận audio đầu vào; không tuyên bố remux voice hoặc prompt miệng là lip-sync khách quan.

## Ghi chú theo từng video

Chi tiết máy và transcript đã phân tích nằm trong `analysis.json`. `evidence.json` của từng ID giữ lỗi tải, hash và phạm vi bằng chứng. Khi chọn video mới, đọc hồ sơ ID liên quan trước, rồi research nguồn chính thức mới nhất.
