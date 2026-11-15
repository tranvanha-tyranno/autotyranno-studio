# Nguồn cho “Vì sao quán cà phê đông khách vẫn hết tiền?”

Catalog gốc `../sources-candidates.json` có 32 asset:20 ảnh và12 video thật,52.4MB.14 ảnh có nguồn xác nhận Việt Nam;3 ảnh được xác nhận nước ngoài;3 ảnh và toàn bộ 12 clip chưa có bằng chứng quốc gia. Không suy Việt Nam từ tên creator, khuôn mặt hay nhãn hiệu.

Đã kiểm 32/32 file và SHA; toàn bộ video giải mã đủ số frame, mỗi clip dưới 6.6MB, phần lớn 1280×720. Hai clip espresso 26.67s/36.60s và closing 21.96s cho phép chọn nhiều khoảng không trùng; các clip khác 7–15s nên không kéo dài bằng loop. Suggested intervals trong catalog là gợi ý biên tập, phải đối chiếu lời/crop trong render cuối.

## Chọn đúng câu và vật thể

- Hook “đông khách”: `clip-busy-cafe`, `clip-cafe-tables` thấy nhiều bàn có người; vẫn có ghế trống. Không nói quán trong ảnh thật hết tiền hoặc biết số đơn.
- Bối cảnh Việt Nam: `vn-rin-cafe-cup`, `vn-hue-cafe`, `vn-saigon-coffee-phin`, `vn-saigon-coffee-food`, `vn-cafe-cart-hanoi`. Không dùng ảnh cốc cận cảnh như bằng chứng quán đầy khách.
- Bàn vắng: `vn-cafe-oxy-tables` cho bàn trống tại thời điểm chụp; `clip-close-shift` là quy trình đóng ca có ghế úp. Các quán khác nhau, không kể như một quán trước/sau phá sản.
- Mỗi ly có nguyên liệu/bao bì: `clip-pour-milk` thấy sữa, cốc giấy và nắp; `clip-steam-milk`, `clip-espresso-flow`, `clip-espresso-extract` thấy làm đồ uống thật. Không suy định lượng hoặc chi phí từ cảnh; số liệu dùng chart/đồ họa nguyên bản ghi ví dụ giả định.
- Nhân công: `clip-serve-coffee` có phục vụ thật; `clip-pos-counter` thấy thao tác POS. Không suy lương, năng suất hay số nhân viên của quán giả định.
- Thanh toán: `clip-phone-payment` có điện thoại/terminal rồi receipt. Không khẳng định khoản đã về ngân hàng hoặc lịch settlement/khấu trừ. `clip-pos-counter` không đủ frame chứng minh card tap nên đổiID khỏi tên nội bộ card-payment.
- Nguồn cung: coffee cherries/drying/roaster chỉ cho vật thể cà phê và xử lý hạt. `clip-roaster-hands` không phải một liều xay cho espresso dù tên tải gốc là coffee-grind. Không gọi đây là nhà cung cấp hay hóa đơn của quán giả định.
- Thuê mặt bằng: storefront chỉ minh họa không gian/mặt tiền, không chứng minh đang cho thuê, giá thuê hoặc hợp đồng.

## Kiểm nhìn và giới hạn

Nhánhảnh đã mở 4 selected contact sheets và 4 ảnh quan trọng riêng (emptytables/occupiedtables/frothing/extraction); ghi rõ từngsource trong `photos/PHOTO_REVIEW.md`. Nhánhvideo mở 3 contact sheets × 5 frame phân bố mỗi clip; filedecode toàn bộ không thay xem/nghe liên tục. Không tuyên bố đã nghe source audio hoặc xem mọi frame. Clip audio mặc định tắt.

Không thấy Tyranno trong các ảnh/frame được mở. Có intrinsic brands như VÂNNAM/TheCart/Nescafé/Vsmart và một số thiết bị; người dựng phải tránh logo lớn nếu không phục vụ câu. `vn-hanoi-phone-patrons` có watermark máy ảnh Vsmart; cân nhắc không chọn khi cần hình sạch. `global-espresso-extraction` chỉ 500×500 nên dùng inset nhỏ, ưu tiên video HD khi cần hero.

Ảnh/clip thật chỉ làm ngữ cảnh. Doanh thu, lãi góp, chi phí cố định, hòa vốn và dòng tiền là case giả định, phải hiện phép tính gốc và không gán vào doanh nghiệp thật. Không thêm Tyranno branding trên video; metadata nguồn vẫn giữ tên tác giả/giấy phép đúng.

Bản render mới chưa tồn tại trong kiểm này. Chưa đánh dấu semantic/aesthetic accepted, chưa xem AV cuối và chưa có người dùng duyệt clip dài. Cần kiểm từng clause và crop thực sau dựng.
