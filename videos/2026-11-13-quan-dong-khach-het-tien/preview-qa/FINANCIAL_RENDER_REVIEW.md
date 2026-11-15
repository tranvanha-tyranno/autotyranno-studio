# Kiểm frame tài chính từ MP4 thực — 8 cảnh

Phạm vi: lấy 16 frame thật ở giữa và 90% của 8 cảnh từ các part MP4 đã hoàn tất trong attempt `20261113T035136Z`. Đã mở 2 contact sheets chứa đủ 16 frame; mở riêng 8 late frame 1920×1080 để đọc số, đơn vị, footnote/crop. So sánh cả mệnh đề của từng beat từ props snapshot đã đóng băng. Không rerender và không sửa code/manifest/audio/ledger.

**Kết quả có phạm vi:** không thấy lỗi phép tính, dấu âm, clipping hay mismatch tài chính cần chặn trong các frame đã mở. Đây không là duyệt toàn video, toàn chuyển động của cảnh, nghe AV liên tục hoặc người dùng chấp nhận. h02/p04cueissues được root xử lý riêng ở revision sau; không thuộc kết luận đạt của lượt này.

Ảnh và hai sheet nằm tại `financial-render/`; JSON frame receipt giữ global/local frame, SHA MP4 và SHA từng frame. Các mốc là frame 0-based/30fps. Dùng `part-02.mp4` cho breakeven, `part-04.mp4` cho discount và `part-05.mp4` cho cash; local frame=globalframe−chapterstart.

Props snapshot SHA-256: `132c24dff4d105bc5d43b8203a66bb9f1d771fb5862a86f66b12d69979d543ce`.

MP4 nguồn: `render-attempts/20261113T035136Z/part-02.mp4`; SHA-256 `f004d2478459e7edb88e9c77b4f4f24cfd655afc2691b42e858c282ca6d724dc` (đã tính từ file và khớp receipt của part).
MP4 nguồn: `render-attempts/20261113T035136Z/part-04.mp4`; SHA-256 `8f1e85185fbd89927c49b9c7699b711588c4aa25a7c073514a0c30932d34ccf7` (đã tính từ file và khớp receipt của part).
MP4 nguồn: `render-attempts/20261113T035136Z/part-05.mp4`; SHA-256 `00725e9b48c32c6db830ddc4c9ad2c10c744256cee92f53c2323ae3d0b036e09` (đã tính từ file và khớp receipt của part).

## b03 —b-paper

**Mệnh đề đầy đủ:** Mỗi ly đóng góp hai mươi nghìn, vậy cần bao nhiêu ly mới bù được bốn mươi tám triệu? Chia ra, ta được hai nghìn bốn trăm ly trong tháng.

**Quan sát actual frame:** Late frame hiện48.000.000đ fixed/tháng, dòng chia20.000đ đóng góp/ly và kết quả2.400ly/tháng. Headline có giả định và nêu đúng kết quả. Các dòng/đơn vị trong phiếu nguyên vẹn, không bị caption che. Mid frame chưa bung toàn hàng theo cue; kiểm kết quả dựa late frame đã mở riêng.

- Global 4345 / 144.833s; local643; xem qua contact sheet. File `preview-qa/financial-render/b03-g04345-l00643.jpg`; SHA-256 `d4c61945fdf340024b5f7e88661818622e8f7daae966d0d683aeb36a54eca3a8`.
- Global 4448 / 148.267s; local746; mở riêng native và xem trong sheet. File `preview-qa/financial-render/b03-g04448-l00746.jpg`; SHA-256 `5a4cb4b3328fe3a9dd867cbef5e87c608fe6963c0c314f5c916cd1cc656e1e84`.

## b05 —b-chart

**Mệnh đề đầy đủ:** Dưới mốc đó, phần đóng góp chưa đủ. Trên mốc đó, mô hình bắt đầu có dư. Đường hòa vốn giúp biến câu hỏi có vẻ cảm tính thành một giả thuyết có thể kiểm.

**Quan sát actual frame:** Đường đóng góp đi qua (40;24),(80;48),(120;72); trục ngang Ly/ngày·30ngày, trục dọc triệu đồng/tháng. Đường fixed 48 nằm ngang và giao đúng 80. Point80/48 được nhấn, không gọi đồ thị này là doanh thu. Không bị crop hay caption đè trục/đơn vị.

- Global 4913 / 163.767s; local1211; xem qua contact sheet. File `preview-qa/financial-render/b05-g04913-l01211.jpg`; SHA-256 `cfb31d58bc27741c134e9c8b8cc625a73f45244af55907b8136027ecd5307411`.
- Global 5036 / 167.867s; local1334; mở riêng native và xem trong sheet. File `preview-qa/financial-render/b05-g05036-l01334.jpg`; SHA-256 `66fc1090ff879b2b76da16734c565e00208ad0ce287bc66cfc8f5fc515b076e7`.

## b07 —b-chart

**Mệnh đề đầy đủ:** Trả tiếp bốn mươi tám triệu chi phí cố định, còn mười hai triệu. Cần gọi đúng: đây là phần dư của mô hình trước thuế, lãi vay và khấu hao, không phải lợi nhuận ròng đã chốt.

**Quan sát actual frame:** Waterfall số105, −45, −48 và cuối 12. Cột−45 rơi105→60;−48 rơi60→12; cột 12 riêng bắt đầu ởzero chứ không cộng tiếp. Header105−45−48=12triệu và footnote “Phần dư mô hình, trước thuế, lãi vay và khấu hao” đọc được; không ghi lợi nhuận ròng. Đơn vị triệu đồng phù hợp.

- Global 5537 / 184.567s; local1835; xem qua contact sheet. File `preview-qa/financial-render/b07-g05537-l01835.jpg`; SHA-256 `13a0c54b3a51e6ac80efdb8ab76c3362bfc082fb1d809c5e9ed63582ef557404`.
- Global 5669 / 188.967s; local1967; mở riêng native và xem trong sheet. File `preview-qa/financial-render/b07-g05669-l01967.jpg`; SHA-256 `0fdbe4b4bec5463efb2452664a3b94950523efaac640038ad2cff3977d09eb4f`.

## p03 —b-paper

**Mệnh đề đầy đủ:** Muốn giữ phần đóng góp sáu mươi triệu như tháng bán ba nghìn ly giá cũ, quán phải bán hơn bốn nghìn hai trăm tám mươi lăm ly ở giá mới. Làm tròn lên là bốn nghìn hai trăm tám mươi sáu.

**Quan sát actual frame:** Late frame có mục tiêu60.000.000đ, mỗi ly 14.000đ và 4.286ly, ghi Số ly làm tròn lên. Đúngceil(60.000.000/14.000); không hiển thị4.285 như đủ mục tiêu. Phiếu không crop hoặc đè số; ảnh cốc chỉ bối cảnh và có credit.

- Global 8592 / 286.400s; local710; xem qua contact sheet. File `preview-qa/financial-render/p03-g08592-l00710.jpg`; SHA-256 `4bdf2e1b12032d70733b266a4b2b46081de7f6d4aec28ef228097d8f680b4446`.
- Global 8720 / 290.667s; local838; mở riêng native và xem trong sheet. File `preview-qa/financial-render/p03-g08720-l00838.jpg`; SHA-256 `194a13e6b67c6ca1282e5cadacf02e5a41ea70f180750d1ef121398b6a25a406`.

## p05 —b-paper

**Mệnh đề đầy đủ:** Ngay cả mốc hòa vốn cũng đổi. Bốn mươi tám triệu chia mười bốn nghìn cần làm tròn lên ba nghìn bốn trăm hai mươi chín ly mỗi tháng, xấp xỉ một trăm mười lăm ly mỗi ngày.

**Quan sát actual frame:** Late frame có fixed 48triệu trong tiêu đề phiếu,14.000đ/ly, 3.429ly/tháng làm tròn lên và ≈115ly/ngày, ghi Bình quân 30 ngày. Đây là làm tròn 114,3 thành mức nguyên khoảng 115, không thay thành mức chính xác 115. Caption nằm ngoài phiếu, không che số/đơn vị.

- Global 9171 / 305.700s; local1289; xem qua contact sheet. File `preview-qa/financial-render/p05-g09171-l01289.jpg`; SHA-256 `a33f91793856b3d01f23a7c854e13889c4f982309adf501902ec0a76dd91dd14`.
- Global 9283 / 309.433s; local1401; mở riêng native và xem trong sheet. File `preview-qa/financial-render/p05-g09283-l01401.jpg`; SHA-256 `0da80a702ccb374e23c25b445aca72a6329cd4891571febcab20c8fa303b40ce`.

## m03 —b-paper

**Mệnh đề đầy đủ:** Chẳng hạn, mua nguyên liệu đủ dùng nhiều tuần khiến tiền ra ngay, trong khi một phần hàng vẫn còn trong kho. Không thể cứ nhìn khoản chuyển tiền mua hàng rồi gọi toàn bộ là chi phí của số ly đã bán.

**Quan sát actual frame:** Ảnh hạt rang ở trái được đặt cạnh phiếu cơ chế gốc: Trả tiền mua nguyên liệu/Hôm nay; Dùng nguyên liệu để bán/Dần nhiều tuần; Hàng còn lại/Cần theo dõi. Lời nhắc tiền chi không đồng nhất toàn bộ chi phí ly bán được hỗ trợ bằng phiếu thật trên render, không dựa vào việc đoán ảnh hạt là kho đã mua. Không giả hóa đơn hay số hàng thực tế.

- Global 11480 / 382.667s; local871; xem qua contact sheet. File `preview-qa/financial-render/m03-g11480-l00871.jpg`; SHA-256 `69a291bba9030b71643fcf13b2ddb5995f64e65590dd5344e53b64791399cb8d`.
- Global 11628 / 387.600s; local1019; mở riêng native và xem trong sheet. File `preview-qa/financial-render/m03-g11628-l01019.jpg`; SHA-256 `2aa6e26a8796b1df114c0da218eee24236d7febc0aedb961bc5e2f57ea8ff18c`.

## m06 —b-split

**Mệnh đề đầy đủ:** Ngay cả tiền bán hàng cũng có lịch. Khách có thể trả tại quầy, hoặc một kênh bán đối soát và chuyển về sau. Lịch thực tế tùy thỏa thuận, không nên tự coi mọi doanh thu là tiền sẵn dùng.

**Quan sát actual frame:** Hai panel có label TẠI QUẦY/Tiền thu ngay/Khi thực sự được thanh toán và KÊNH ĐỐI SOÁT/Tiền chuyển về sau/Tùy thỏa thuận cụ thể. Header “Doanh thu chưa chắc đã sẵn dùng”. Ảnh cốc/bánh chỉ minh họa nền; không có ngày đối soát giả hoặc nói hai món thực có cùng lịch thanh toán. So sánh là card cơ chế gốc, không suy ngân hàng từ ảnh/POS.

- Global 12454 / 415.133s; local1845; xem qua contact sheet. File `preview-qa/financial-render/m06-g12454-l01845.jpg`; SHA-256 `bc9d4f76e914b272691098d06a46d9c0615d07f3a984f4010e0f8a4a22bddcc2`.
- Global 12596 / 419.867s; local1987; mở riêng native và xem trong sheet. File `preview-qa/financial-render/m06-g12596-l01987.jpg`; SHA-256 `773684091c76006f7378ed42d542b8d7427d39dcca158658c5642e328a049fb8`.

## m07 —b-chart

**Mệnh đề đầy đủ:** Thử một tình huống riêng: đầu tuần có hai mươi triệu, trong tuần thu mười lăm triệu, nhưng các khoản đến hạn cần bốn mươi triệu. Thiếu năm triệu trước khi bàn tới mục tiêu tăng trưởng.

**Quan sát actual frame:** Late frame chart có 20 đầu kỳ,15 thu,−40 đến hạn và−5 còn thiếu. Cột thu 15 bắt đầu từ20 lên35; cột chi −40 rơi35→−5; final −5 nằm dưới đường zero, không đụng caption. Đơn vị triệu đồng, header thiếu 5 triệu và note tình huống tuần riêng/không ghép tháng đầy đủ. Đây là gap mô hình nếu chi đủ, không bằng chứng overdraft thực. Tick trục có−10/3,8/17,5/31,3/45 và đường zero nhưng không ghi tick 0; có thể tinh gọn tick ở lần thiết kế khác, chưa gây sai dấu/số trong mẫu đã xem.

- Global 12786 / 426.200s; local2177; xem qua contact sheet. File `preview-qa/financial-render/m07-g12786-l02177.jpg`; SHA-256 `3a92e423fcdc0760c46157dac9d8abaad843cb0a2673c7060a5188112019bac8`.
- Global 12909 / 430.300s; local2300; mở riêng native và xem trong sheet. File `preview-qa/financial-render/m07-g12909-l02300.jpg`; SHA-256 `b2c60b5a781994a65ee646c83023b4c3972bee46522acaad2172097976bdd9cd`.

## Giới hạn đối chiếu

Không dùng caption chunk làm chứng cứ đã nghe từ nào đúng thời điểm; timing âm/giọng từng từ chưa được nghe trong lượt này. Các phiếu lộ dần theo cue, nên midframe chưa đủ hàng không tự đồng nghĩa thiếu số của cả cảnh; kết quả/độ đọc được kiểm từ late frame và số phiếu khớp toàn mệnh đề. Muốn kết luận toàn cảnh phải xem chuyển động/âm tương ứng.

Nhãn mô hình giả định hiện rõ trong b03/b05/b07/p03/p05/m03/m07. m06 có nội dung cơ chế và source note mô hình minh họa; ảnh hai món không được gán là hợp đồng/lịch thực của quán thật. Không suy đóng cửa, thất bại hay thiếu tiền của doanh nghiệp/nhân vật nguồn.

Ghi chú nhỏ: m07 có đường zero với bar âm đúng nhưng không có nhãn tick 0; đây là gợi ý độ đọc trục, không phải lỗi đảo dấu hoặc phép tính. Không yêu cầu đổi take hay mở rộng render từ quan sát này.

Không thêm acceptance/verification event. Review chỉ nhận diện đúng part/frame đã mở; khi ghép bản cuối hoặc sửa chapter, phải đối chiếu output cuối và phạm vi thay đổi tương ứng.
