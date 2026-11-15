# Kiểm hình độc lập — r02

**Không phát hiện thêm lỗi hình/nội dung trọng yếu cần chặn trong các mẫu đã xem.** Bản video mới vẫn chờ phản hồi người dùng.

MP4 thực `../final.mp4`: SHA-256 `7e980f8be5758d0dff49ee28a477643fb48c62d8612317c7674285dbf68b8b1e`, đã tính từ file và khớp report. Timeline 17848 frame/30fps=594,933 giây.

## Phạm vi thực sự đã xem

- Mở đủ 7 keyframe sheets: **58/58 midframes** của 58 beat, đối chiếu ý của toàn mệnh đề trong timeline/script đã đọc.
- Mở đủ 23 three-second sheets: **199/199 thumbnail**, từ 0s/f0 đến 594s/f17820, cách 3 giây.
- Mở riêng 1920×1080 midframes h01/f142, d01/f1002, u02/f1533, a02/f14129; thêm 4 lateframe từ MP4 cuối b06/f5347, p01/f8116, p03/f8726, p05/f9289, cùng last-frame/f17847. Tổng 9 frame mở riêng.

File/mốc đầy đủ ở `capture-plan.json`; file/hash 4 frame bổ sung ở `independent-extra/receipts.json`. Last-frame SHA-256: `474117e7a8b648b37ace73fe0c20224720b78368b3f7b10e30e0ea0b6ce0b226`.

## Quan sát

**Hook/disclaimer:** nhãn “QUÁN GIẢ ĐỊNH / TƯ LIỆU MINH HỌA” đã có ở frame 0, còn thấy trong native h01 khi lời kể chủ thiếu tiền. h02 đủ 3 card sau cue; d01 nêu rõ miễn trừ, giá/chi phí giả định và giới hạn thuế/lãi vay/khấu hao. Không gán tình trạng tiền mặt cho quán nguồn.

**Nguồn khớp vật thể:** hình thực có máy xay/portafilter ở 48 giây, rót sữa/cốc ở 51 giây, terminal/receipt ở quầy, người pha và bàn có khách/trống. Không thấy ảnh ngoài chủ đề được thay cho những vật thể này. Nguồn được dùng lại thấy rõ; cảnh đông/vắng khác quán chỉ là bối cảnh, không là cùng doanh nghiệp trước/sau thất bại. Ảnh các món ở u07/m06 không chứng minh cùng SKU hay lịch đối soát thực; phần giải thích nằm ở card gốc.

**Giá/tổng:** các mẫu cho 35−15=20 nghìn;18+22+8=48 triệu;2.400 ly/80lyngày; đường đóng góp cắt fixed 48 tại 80; waterfall 105/−45/−48/12 cùng footnote. Phiếu p01 late có29.000/−15.000/14.000; p03 late đủ60.000.000/14.000/4.286ly; p04 hai cột3.000/4.286; p05 late đủ3.429ly/≈115lyngày. b06 late5347 thấy60 triệu đang fade-in: các hàng lộ dần, không phải mất tổng do crop. Không thấy caption che các giá/tổng đã kiểm.

**Tiền và thời điểm:** m03 có phiếu hôm nay/dần nhiều tuần/hàng còn lại, không đoán tồn kho từ ảnh hạt. m04 hai dòng thuê/cọc có đủ ở 396 giây. m06 hai card có điều kiện thanh toán/đối soát. m07 âm −5dưới đường zero ở 429 giây và ghi tuần riêng. a02 native nhắc phí/trợ giá tính một lần; a07 đủ 3 dòng ở 528 giây. Kiểm tài chính 8 cảnh/16 frame part thực trước đó còn ở `../../preview-qa/FINANCIAL_RENDER_REVIEW.md`.

**Không nhận diện kênh:** không quan sát thấy tên/logo/watermark kênh bị cấm trong 58 midframes,199 thumbnail và 9 frame mở riêng. Nhận xét dựa trên pixels đã mở, không từ đường dẫn/tên người dùng hoặc decode. Intrinsic nhãn máy/cốc/giày/ảnh nguồn có thể còn.

**Kết:** mốc 585–594 giây còn câu hỏi/CTA; last-frame giữ câu hỏi và phụ đề từ cuối “hành.”.

## Giới hạn

Đây là xem mẫu hình tĩnh, không xem mọi transition, mọi pixel hoặc toàn bộ 17848 frame. Chưa nghe AV liên tục/âm cuối/Foley trong lượt này; thấy caption không chứng minh đã nghe trọn câu. Không xác nhận thẩm mỹ toàn video hoặc người dùng chấp nhận. Không ghi acceptance/verification vào ledger; không sửa renderer, đầu vào hoặc MP4. Không có phát hiện mới đòi đổi take hoặc thiết kế lại.
