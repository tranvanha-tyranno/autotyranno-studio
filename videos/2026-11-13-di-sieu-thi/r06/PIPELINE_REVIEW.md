# R06 — kiểm pipeline và cue, 13/11/2026

Đã đọc `long/preflight.json`, `data.json`, `aligned-words.json`, `image-sources.json`, manifest và source `Shopping3D.tsx`; không chạy render/test nặng, không sửa renderer đang đóng băng. Đây là kiểm hồ sơ/timing và hai ảnh preview có sẵn, chưa phải xem/nghe liên tục hoặc duyệt bản xuất cuối.

- Timeline cấu hình: **205 giây, 6150 frame, 30 fps, 24 shot**. Take dài 203,15 giây; từ cuối kết thúc 203,12 giây. Chưa dùng các con số này làm bằng chứng số frame giải mã của MP4 cuối đang render.
- Miễn trừ riêng `d1`: **[556, 815)**, tức **18,533–27,167 giây**, dài 8,633 giây. Heading đúng `MIỄN TRỪ TRÁCH NHIỆM`; body nêu tính minh họa, mua thêm không luôn lãng phí và bố trí cửa hàng khác nhau.
- **7 tài sản có hồ sơ địa điểm VN**, hiện diện theo slot ảnh trong **117,433 giây** (57,285% timeline). Đây không phải thời gian phủ toàn màn hình, diện tích ảnh hay đo thời điểm reveal. Cảnh giá thuần hình học không bị tính thành ảnh VN; ảnh bếp/Pexels không bị gán VN theo tên tác giả.
- Tổng cảnh Three.js: **60,5 giây**, gồm `object3d` **53,733 giây** và gallery 6,767 giây.
- Cả **18 bản ghi nguồn** khớp SHA-256 file được giữ. Manifest v6 khớp snapshot. `Shopping3D.tsx` hiện tại khớp source snapshot của attempt `20261113T015112.536110Z-repair-fb1f0a`, SHA-256 `539458c3a9881851c8e2e3abcbdbfab1111a759788d3f09594eee538d1cabbf2`.

## Cue đối chiếu take

Tất cả 21 cue trong 7 cảnh `object3d` đều là frame cục bộ tăng dần và nằm trong shot. Các cue cơ chế chính đối chiếu được với từ thực trong alignment:

| Shot | Frame cục bộ | Thời điểm toàn phim | Mốc lời |
|---|---|---|---|
| c10 — 1 hộp / 2 hộp / giá đơn vị | 48 / 99 / 195 | 110,667 / 112,367 / 115,567 s | “một” / “hai” / “hai [mươi lăm]”; lệch điểm đầu từ tối đa 0,014 s |
| c11 — chi thêm | 107 | 120,033 s | Trước từ “thêm” 0,015 s |
| c14 — nhà / kệ / trước thanh toán | 52 / 95 / 150 | 147,100 / 148,533 / 150,367 s | “đồ” / “lựa” / “rồi [tổng tiền]”; dẫn trước 0,007–0,020 s |

Hook `h1a` thả các hộp từ 0 / 0,533 / 1,100 s, là hành động mở đầu có chủ đích; không phải ba món cụ thể được người nói liệt kê. Tương tự, các lần thả hộp ở c5/c13 minh họa giỏ tăng dần, không chứng minh ba quyết định hay hành vi của người trong ảnh. Source ghi rõ hình khối gốc và ngữ cảnh ảnh.

Source c14 đưa hộp từ đúng vị trí/scale của món dưới kệ sang giỏ; hai điểm nối dùng cùng phép nội suy. Quan sát preview c14 thấy ảnh mở tủ lạnh / kệ mì / hàng đợi quầy tương ứng ba chặng, không biến cảnh chợ thành thanh toán. Preview c10 thấy đầy đủ 1–2 hộp, 30.000đ/50.000đ, 30.000đ/25.000đ mỗi hộp và nhãn giả định. Hai still không xác nhận độ mượt toàn đoạn.

## Nguồn và phạm vi cần giữ rõ

Ảnh VN là tư liệu 2007–2022; nhãn giá Coca-Cola, sốt và hạt không phải giá hiện hành hay cặp giá giả định 30k/50k. Ảnh hạt ghi “from Russia” chỉ xuất xứ hàng hóa; hồ sơ địa điểm chụp là siêu thị Việt Nam. c7 tách credit ảnh khỏi “Nghiên cứu: Inman và cộng sự (2009)”, tránh coi ảnh là bằng chứng nghiên cứu. c16 là chợ Huế, chỉ hỗ trợ lời tổng quát về mua đồ; không được gọi thành checkout siêu thị.

Credit c14 hơi lặp “Ảnh bối cảnh: Ảnh:”, nhưng phần `VN:` chỉ áp cho Kham Tran/Groupe Casino; Pew Nguyen/Pexels vẫn là bối cảnh nhà không xác nhận địa điểm. URL, giấy phép và tác giả riêng từng ảnh nằm trong `image-sources.json`; nguồn nhiều ảnh trên một dòng là credit tổng hợp, không phải phép gán giấy phép chung. Không phát hiện gán nhầm nước trong hồ sơ đã đọc.

## Âm thanh và trạng thái

So byte trực tiếp với r04: `narration-original.mp3`, alignment, receipt, `final-mix.wav` và `script.txt` **đều giống nguyên vẹn**. SHA-256 narration: `3cc0a086878e8ac3a687d318ae1e46b028e92947eb692704ef7bdb1a8100b5d6`; mix: `535115a6a2adc17b56a0eccb68af43af9f775cac98e10b0979e649ac6e2d2bb6`.

Không thấy lỗi cue vượt shot hay mâu thuẫn phép tính trong phạm vi kiểm này. Cần QA MP4 hoàn tất để kiểm giải mã, chuyển cảnh, motion và phần kết; chưa thiết lập việc nghe liên tục hoặc người dùng chấp nhận.
