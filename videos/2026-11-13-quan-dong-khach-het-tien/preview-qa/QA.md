# Kiểm hình dựng thật lần đầu

Đã mở trực tiếp 13 still: h02, h03, d01, u03, b05, b07, p03, p05,
m03, m06, m07, v02, e04. Hash từng file được lưu trong
`inspected-stills.json`. Đây là kiểm từng ảnh, không xác nhận chuyển động trọn
video, chất lượng nghe hoặc chấp thuận của người dùng.

## Lỗi phát hiện lần đầu và kiểm lại sau sửa

**Cập nhật:** đã mở trực tiếp `m07-corrected.jpg`. Đường0 được nâng lên,
hai thanh đi xuống dừng trước vùng nhãn, cả “Khoản đến hạn” và “Còn thiếu”
đọc được, không còn đè chữ ở still này. Hash và phạm vi xác nhận được thêm
vào `inspected-stills.json`. Lỗi bố cục dưới đây là lịch sử của bản đầu.

**m07: biểu đồ có số âm đè nhãn trục ngang.** Thanh chi −40 và số dư −5 đi
xuống dưới đường 0 hiện tại tại y766; vùng dưới thanh trùng nhãn “Khoản đến
hạn” / “Còn thiếu” khoảng y809. Số học 20 + 15 − 40 = −5 đúng, nhưng cách
chia miền tọa độ chưa dành chỗ cho giá trị âm. Cần miền dọc thấp hơn 0 (ví dụ
−7 tới45), nâng vị trí đường0 trong vùng vẽ, giữ nhãn trục bên dưới vùng vẽ.
Không đổi số liệu để chữa bố cục. Giữ ảnh gốc ở
`m07-before-negative-domain-fix.jpg` và kiểm still sửa lại trước khi kết luận.

## Quan sát còn lại

| Still | Quan sát trực tiếp |
| --- | --- |
| h02 | Đủ3 câu chuyện, chữ3 cột không bị cắt; ảnh là bối cảnh cà phê, không chứng minh sản lượng hay lịch thanh toán. |
| h03 | Cốc3D có thành/quai/mặt cà phê và bóng nằm trọn khung; ảnh extraction bên trái rõ. Có dải nền do giữ toàn khung nguồn, không che hành động. Giá35.000đ ghi rõ giả định. |
| d01 | Phần “MIỄN TRỪ TRÁCH NHIỆM” riêng, chữ chính và giới hạn thuế/lãi vay/khấu hao đọc được; không cắt mép. |
| u03 | Phiếu35.000−15.000=20.000đ đủ cả đầu vào và phần đóng góp; không tràn khung. |
| b05 |40/80/120 ly mỗi ngày tương ứng24/48/72 triệu mỗi tháng; giao điểm48 với chi phí cố định rõ; đơn vị và30 ngày hiện đầy đủ. |
| b07 | Waterfall105−45−48=12 đúng độ cao tương đối; footnote nêu trước thuế/lãi vay/khấu hao, không gọi là lợi nhuận ròng. |
| p03 | Mục tiêu60triệu và phần đóng góp14.000đ hiện rõ; headline4.286ly đúng làm tròn lên. Phiếu không bị cắt. |
| p05 |14.000đ/ly,3.429ly/tháng và khoảng115ly/ngày nhất quán với ví dụ; phiếu vừa khung. |
| m03 | Chữ dài trên phiếu vẫn vừa: trả tiền hôm nay / dùng dần nhiều tuần; hình hạt chỉ minh họa nguyên liệu, không chứng minh tồn kho thực tế. |
| m06 | Hai cột thu ngay / chuyển về sau và giới hạn tùy thỏa thuận rõ. Ảnh cà phê/bánh là bối cảnh đơn hàng, không phải bằng chứng đối soát hay giao dịch. |
| v02 |60+10=70 và mốc80 rõ; không đè nhãn. |
| e04 | Cảnh nền ấm khác cảnh kem, ba khái niệm đọc được. Ảnh cà phê có báo/giày ở nền chỉ tạo bối cảnh, không làm bằng chứng cho mô hình. |

Không thấy tên kênh được thêm, logo hoặc watermark của dự án trong13still này.
Không tự coi13still là kiểm hết58beat hoặc mọi crop/đoạn clip trong toàn video.

## Hiệu ứng âm thanh

Đã sửa cue milk-steam từ m05+0,3s sang **u06+0,3s** để đi cùng actual clip
đánh sữa được root chỉ định. m05 hiện dùng extraction/thiết bị nên không đặt
tiếng steam ở đó. Cue grinder vẫn tại u02+0,15s, root chỉ định clip grinder
thật cho slot đầu. Hai kiểm tra liên kết cue đã pass; chưa nghe thực tế bản mix
sau sửa.

Bản mix/stem/report/cue-stems đầu được giữ nguyên dưới
`audio/first-mix-before-cue-review/`, có hash trong archive-receipt. Root sẽ
chuẩn bị lại media rồi mix lại. Lưu nguồn âm được tạo ban đầu, không gọi tạo
lại vì việc thay vị trí cue.

## Gate âm thanh trên dữ liệu thật sau sửa cue

`audio-integrity-gates.json` ghi các kiểm tra chỉ đọc đã thực hiện:

- Cả8 chapter có request hash đúng nguyên lời và đúng Nhật Phong /
  eleven_v3 / vi / speed1, stability0,5, similarity0,8; MP3 khớp provider receipt.
- Alignment phủ đúng toàn lời của từng chapter và toàn video; không sửa lời
  để né kết quả timing.
- PCM narration lắp từ đúng PCM của8 chapter cùng7 đoạn nghỉ0,5s, bằng nhau
  ở cấp byte PCM:28.484.160 frame48kHz =593,42s. Không time-stretch.
-58shot liền nhau, timeline17.848frame =594,933s, còn1,513s sau từ cuối.
-17nguồn âm giữ đúng hash/request/receipt:5nhạc mới,10Foley,2nhạc giữ lại.
- Mix mới có milk-steam chỉ tại u06, đủ18cue và2quietpivot p09/m08;
  hash của final/public copy/2stem/18snippet đều đúng. Đo−15,99LUFS,
  true peak−2,56dBTP, độ dài594,93s.

Full data hash trong mix receipt khác bản data hiện tại sau prepare hình/cue
đồ thị. Không sửa receipt lịch sử. Đã kiểm riêng **toàn bộ đầu vào ảnh hưởng
âm thanh**: duration, narration hash, generation receipt hash,18cue gồm thời
điểm/độ dài/gain/asset và2quietpivot; tất cả bằng bản current. Gate này xác lập
tương đương đầu vào âm thanh, không tự khẳng định mọi field hình ảnh khác ở đâu.

Các kiểm tra này không phải nghe liên tục, không chứng minh phát âm tự nhiên,
chất lượng chuyển nhạc cảm nhận hay đồng bộ âm/hình ở mọi frame.
