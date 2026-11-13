# Học lại cách khớp hình với lời — sau khi hai bản mẫu bị từ chối

Người dùng nói **“hình ảnh chả khớp lời thoại quá tệ làm lại và học lại đi”**. Hai bản `videos/2026-11-12-hai-huong/{long,hidden}/final.mp4` bị từ chối về nội dung hình. Không tiếp tục gọi những sai lệch này là hai hạn chế nhỏ của ảnh stock. Chọn ảnh cùng bối cảnh công sở đã thay thế việc thực sự diễn đạt câu nói trong phần lớn các ví dụ thao tác cụ thể.

Các kiểm tra số frame, font, loudness, cắt theo phrase và số lượng ảnh đã kiểm được tính toàn vẹn kỹ thuật; chúng không kiểm được nghĩa. 52 shot trong hai manifest không lưu hợp đồng chủ thể–hành động–đối tượng–trạng thái hoặc bằng chứng nhìn thấy tương ứng. Đó là chỗ quy trình đã để sai lọt qua. Viết thêm “minh họa” vào ảnh không làm email biến thành headset hoặc làm một cuốn sổ trở thành số đo thời gian.

## Phạm vi kiểm tra mới

Đã trích **20 cặp mệnh đề–frame thực, 10 cặp mỗi kênh**, từ bốn video nguồn, gồm mở đầu và ví dụ trong nội dung chính. Đã mở cả bốn sheet `long-phrase-pairs-*.jpg`, `hidden-phrase-pairs-*.jpg`. Đã trích và mở thêm **13 cặp lời–frame trực tiếp từ hai MP4 bị từ chối** trong bốn sheet `rejected-pairs-*.jpg`. File `evidence.json` lưu quan sát, giới hạn, đường dẫn, URL, thời gian trích và SHA-256.

Mốc lời tham chiếu lấy từ caption YouTube có các đoạn chồng thời gian. `frameTime` là vị trí trích frame; không gọi đó là word timestamp được forced alignment. Lời của hai bản bị từ chối được đối chiếu với aligned words của chính take. Không tuyên bố đã nghe bằng tai hoặc xem liên tục toàn bộ bốn video nguồn. Audit này không xác minh các số liệu kinh tế/kinh doanh trong lời tham chiếu.

## Nhìn lại hình tham chiếu đúng thời điểm lời

Các URL dưới đây dẫn tới video gốc; thời gian cụ thể nằm trong bảng và `evidence.json`. Đây là quan sát chức năng dựng, không phải tài sản để sao chép vào video mới.

**Lóng — [AI và công việc](https://www.youtube.com/watch?v=JlfAd_OaFek)**

| Mốc | Ý đang được nói | Frame thật cho thấy | Điều nên học / giới hạn |
|---|---|---|---|
| 3,8s | Thực đơn quán ăn dùng hình AI | Ô menu có ảnh món ăn và chữ MENU | Đưa đúng đồ vật lên hình ngay khi nhắc. Không thể xác thực nguồn AI của ảnh từ frame. |
| 8,5s | Chuyển sang ứng dụng trong học tập | Thêm ô người dùng laptop/tài liệu vào hai ô ví dụ trước | Đối tượng mới xuất hiện theo ví dụ mới. Màn hình quá nhỏ để khẳng định hoạt động học cụ thể. |
| 405,8s | Nhân viên xử lý dữ liệu và làm báo cáo | Nhân vật hoạt hình ngồi trước máy tại bàn | Chỉ khớp ngữ cảnh nghề; không có báo cáo nhìn thấy. Không lấy mức này làm chuẩn cho câu thao tác cụ thể. |
| 410,7s | Con người kiểm chứng và đánh giá | Cùng nhân vật, tư thế tay cạnh mặt | Không có cặp nguồn/kết quả hoặc hành động kiểm tra. Không gọi là minh họa trực tiếp. |
| 452,8s | Ví dụ kỹ sư xem/sửa mã | Nhóm nhân vật bên đường, xe/tank tiền cảnh | Không thấy code ở mốc này. Tham chiếu cũng có đoạn yếu; không học lại điểm yếu đó. |

**Lóng — [Shein](https://www.youtube.com/watch?v=podWgLH4b3M)**

| Mốc | Ý đang được nói | Frame thật cho thấy | Điều nên học / giới hạn |
|---|---|---|---|
| 4,5s | Mua sắm quần áo online với nhiều lựa chọn | Giao diện Shein, lưới sản phẩm, giá, điện thoại và màn hình | Đúng đối tượng cụ thể; không thay bằng người cầm laptop bất kỳ. |
| 127s | Quy mô các mẫu hàng mới trong ngày | Quần áo/kiện hàng + icon áo + số và đơn vị theo ngày | Ảnh giữ đối tượng, đồ họa bổ sung quan hệ số lượng. Audit không xác nhận con số ấy. |
| 200,3s | Hạn mức áp cho một kiện nhỏ | Hộp hàng + quy tắc/hạn mức ngay cạnh | Đồ họa giải thích một quy tắc gắn với đúng vật thể. Không dùng như thông tin thuế hiện hành. |
| 215s | Hàng được gửi theo kiện tới người mua | Hộp hàng Shein trên bậc cửa nhà | Đúng vật thể và đích đến. Frame không chứng minh động tác giao nhận. |
| 274,8s | Một nhóm hàng được phân biệt với các nhóm khác | Icon khăn, giỏ hàng và váy nữ; thông tin hiện theo nhóm | Lên hình theo danh mục cụ thể và diễn tiến lời; không phải ba ảnh người họp không rõ chức năng. |

**THE HIDDEN SELF — [Nhu cầu và sản xuất](https://www.youtube.com/watch?v=29B8-FtuC6U)**

| Mốc | Ý đang được nói | Frame thật cho thấy | Điều nên học / giới hạn |
|---|---|---|---|
| 7,8s | Năng lực làm ra hàng | Tay robot/dây chuyền công nghiệp | Đúng lớp hoạt động sản xuất; không chứng minh quy mô toàn nền kinh tế. |
| 10,5s | Thiếu nhu cầu mua | Kệ/hàng trong kho | Cùng bối cảnh hàng hóa nhưng chưa thể hiện người mua hay sức mua yếu. Không coi tự động là khớp. |
| 27,8s | Ẩn dụ đầu bếp đang nấu | Người ở quầy bếp thao tác với thực phẩm | Hành động nhìn thấy khớp lời. Không suy ra đủ số lượng đầu bếp từ frame. |
| 36,5s | Nhà hàng có ít khách so với món đã làm | Khung hàng ăn/chợ có nhiều người dưới đèn lồng | Chưa thể hiện trạng thái vắng khách, bàn trống. Cùng chủ đề ăn uống chưa đủ để diễn đạt đối lập cung–cầu. |
| 456s | Người từ nông thôn ra đô thị làm việc | Người ngồi làm việc trong xưởng may | Có ngữ cảnh lao động; không xác nhận người trong hình là lao động di cư. |

**THE HIDDEN SELF — [Xuất bản giá trị](https://www.youtube.com/watch?v=5zqAMK2qsfM)**

| Mốc | Ý đang được nói | Frame thật cho thấy | Điều nên học / giới hạn |
|---|---|---|---|
| 3,8s | Lưu nội dung trên điện thoại | Màn hình laptop/trình duyệt | Sai thiết bị/hành động ở mốc này; không nhìn thấy nhấn lưu. |
| 11,5s | Sách chất trên kệ | Kệ sách thật và gáy sách | Đúng đồ vật, người xem nhận ra đối tượng mà không cần phụ đề giải thích hộ. |
| 391,8s | Tự viết một bài sau khi đọc | Bàn tay viết vào giấy/sổ | Đúng động tác viết. Chưa chứng minh bài đó đã được đăng lên mạng. |
| 517s | Đưa suy nghĩ ra giấy | Tay, giấy và ghi chép | Hành động chính rõ hơn ảnh người trong một phòng làm việc chung. |
| 647s | Chuẩn bị trình bày cho người khác | Người đọc/viết tại thư viện | Không thấy trình bày hoặc người nghe; không lấy câu này để hợp thức hóa stock cùng ngành. |

Kết luận học lại: dùng cơ chế mạnh như **đúng vật thể → đúng hành động → thay đổi trạng thái/quan hệ xuất hiện theo lời**. Không khẳng định kênh tham chiếu khớp mọi câu, và không dùng các frame yếu của họ để hạ tiêu chuẩn sau phản hồi trực tiếp của người dùng.

## Những sai lệch thực tế trong hai bản bị từ chối

| Bản / frame | Lời cần được diễn đạt | Hình thực tế | Cảnh thay thế cần làm được |
|---|---|---|---|
| Long 1,0s | Giao AI viết email | Người gõ laptop, trang web nhiều hình/cột; không có email hay yêu cầu AI | Thấy yêu cầu soạn email và composer có người nhận/tiêu đề/nội dung. |
| Long 3,8s | Bản nháp xuất hiện trên màn hình | Viết vào sổ giấy | Bản nháp hiện trên màn hình; giữ cùng thư đang kể. |
| Long 19,8s | Đang nhìn một email | Tay cầm headset | Cận email, chỉ đúng phần sẽ được phân tích. |
| Long 31,3s | Sửa giọng điệu rồi theo dõi phản hồi | Người xem giấy và nhóm đeo headset | Hai trạng thái trước/sau của một câu, sau đó thread phản hồi cùng tình huống. |
| Long 49,5s | Không gộp ba bước vào nút gửi | Nhóm người họp bàn | Ba bước riêng, nút Gửi có trạng thái phù hợp với việc đã/chưa kiểm tra. |
| Long 61,2s | Ghi thời gian viết/sửa và lỗi còn lại | Hai ảnh người ghi sổ | Một nhật ký với ba trường đọc được, không chỉ tấm ảnh có bút. |
| Long 75,5s | Bình luận một công việc cụ thể | Giấy note trên tường | Ô nhập bình luận và một ví dụ nhiệm vụ. |
| Hidden 0,8s | Một thao tác nhanh hơn không làm cả nghề biến mất | Ảnh như cuộc phỏng vấn | Chức danh gắn với các nhiệm vụ; chỉ một nhiệm vụ đổi tốc độ, phần trách nhiệm còn lại vẫn hiện. |
| Hidden 40,5s | Công cụ gợi ý cấu trúc | Giấy note | Yêu cầu và dàn ý có đề mục cụ thể thực sự xuất hiện. |
| Hidden 43,5s | Một số không khớp, cần quay về nguồn | Calculator/giấy nhỏ không đọc được cặp số | Hai giá trị của cùng một mục, nguồn gốc được tô sáng, trạng thái sửa sai rõ. |
| Hidden 48,5s | Lời đáp lịch sự chưa giải quyết đúng vấn đề | Bốn người đeo headset | Nội dung khiếu nại, lời đáp bỏ sót yêu cầu và trạng thái vấn đề chưa được giải quyết. |
| Hidden 69,8s | Đo thời gian sửa | Viết vào sổ | Đồng hồ hoặc cột thời gian sửa được ghi nhận. |
| Hidden 77s | Để ví dụ dưới bình luận | Phỏng vấn ở văn phòng | Ô bình luận minh họa đang nhập ví dụ nhiệm vụ. |

Đây là 13 lỗi đại diện được trích từ MP4 và mở xem, không phải kết quả chấm mọi frame của toàn bộ hai video. Tuy nhiên chúng trải từ hook tới thân bài và CTA; không thể coi vấn đề chỉ nằm ở hai hình riêng lẻ. Phần chữ lớn/phụ đề trong bản cũ đang làm công việc giải thích thay cho hình.

## Quy tắc chọn và dựng hình mới

1. **Tách mệnh đề trước khi tìm ảnh.** Ghi ai/cái gì, đang làm gì, tác động vào vật nào, trạng thái hoặc quan hệ nào đổi. Một câu có sửa lời rồi phản hồi cần hai biến đổi trong cùng cảnh hoặc hai cảnh; không lấy một ảnh họp để che cả câu.
2. **Hình phải chứa điều người xem cần nhận ra.** Với vật thể số, hình phù hợp thường là email, bảng tính, tài liệu, thread hoặc thao tác trên màn hình. Ảnh người cầm laptop không tự thể hiện tác vụ trên laptop. Với nấu ăn/viết tay/giao hàng, dùng đúng hành động hoặc vật thể và bối cảnh có thể nhìn thấy.
3. **Giữ tính liên tục của ví dụ.** Nếu kể một email, giữ cùng người nhận giả định, tiêu đề, nội dung và dữ liệu nguồn qua tạo nháp → phát hiện sai → sửa → quyết định. Thay cả bối cảnh/nhân vật/đạo cụ mỗi vài giây làm mất quan hệ nhân quả.
4. **Không ép mọi câu thành ảnh stock.** Khi không có ảnh/footage được phép dùng thể hiện đúng thao tác số, dựng màn hình minh họa có nhãn rõ. Màn hình tái dựng không được gọi là screenshot của sản phẩm thật hoặc bằng chứng kết quả AI thật. Ảnh thật vẫn dùng khi có vai trò cụ thể; số lượng ảnh không phải thước đo mức khớp.
5. **Số và so sánh phải đọc được.** Thấy hai giá trị, mục dữ liệu và nguồn đối chiếu; thấy cột thời gian viết/sửa nếu lời nói đo hai khoản ấy. Số giả định phải được ghi là minh họa và nhất quán giữa các cảnh, không trở thành bằng chứng năng suất hay lời hứa hiệu quả.
6. **3D phải mang đúng đối tượng và quan hệ.** Đưa chính email, dòng nguồn, bản sửa hoặc các nhiệm vụ vào không gian 3D. Ba ảnh gõ máy–xem giấy–họp bàn không tự giải thích được kiểm chứng hay quyết định. Sự chuyển trạng thái có giá trị hơn một quỹ đạo camera trang trí.
7. **Đặt biến đổi đúng lời đang nói.** Chỉ đúng đoạn sai khi nói tới sai; hiện nguồn khi nói đối chiếu; đo/gộp tổng khi nói tổng thời gian; nhập ví dụ khi mời bình luận. Không chỉ canh đầu shot với từ đầu tiên rồi để hình chung chung kéo qua các động từ còn lại.
8. **Không suy diễn thuộc tính con người từ stock.** Ảnh một người ở văn phòng không chứng minh họ lo mất việc, đã bị sa thải, dùng AI hoặc là người trả lời một email cụ thể. Nếu dựng tình huống giả định, toàn bộ trình bày phải giữ đúng phạm vi giả định.

## Hợp đồng bắt buộc cho từng shot

```json
{
  "spokenClause": "mệnh đề thực tế lấy từ take",
  "start": 0,
  "end": 0,
  "subject": "ai hoặc đối tượng chính",
  "action": "động tác/biến đổi đang được nói",
  "object": "vật mà hành động tác động vào",
  "stateOrRelation": "điều người xem phải nhận ra",
  "mustShow": ["các chi tiết bắt buộc nhìn thấy và đọc được"],
  "mustNotShow": ["các thay thế chung chung dễ nhầm"],
  "assetRole": "documentary | illustrative_stock | labelled_reconstruction | explanatory_graphic",
  "sourceAndLicense": "URL, creator, license hoặc nguồn tác phẩm tự dựng",
  "observedEvidence": "mô tả điều đã thực sự mở xem trong asset/crop",
  "semanticVerdict": "pending | direct | explicit_analogy | reject",
  "finalEvidence": {"frameTime": 0, "file": "frame lấy từ MP4 cuối"}
}
```

`explicit_analogy` chỉ dùng khi hình diễn tả đúng quan hệ và người xem có thể nối nó với lời; không phải tên mới cho `context-only`. Với câu gọi đích danh vật/hành động, thiếu vật/hành động đó là `reject`. Metadata đúng tên không chứng minh hình thật có nội dung ấy.

Trước render: mở asset/crop hoặc storyboard đang có chính lời tương ứng; ghi một câu bằng chứng nhìn thấy. Nếu bỏ hết tiêu đề/phụ đề mà hình không thể hiện được tác vụ/trạng thái chính, đổi hình hoặc dựng lại thao tác. Không dùng nhãn “minh họa” để duyệt hình sai.

Sau render: kiểm từng mệnh đề có vật/hành động/trạng thái cụ thể trên **MP4 cuối**, kể cả đoạn đầu và cuối shot khi có đổi ý. Lưu frame cạnh lời và quyết định theo nghĩa, riêng với decode/font/loudness. Cảnh không đạt phải sửa; không gộp vào câu “không phát hiện lỗi kỹ thuật”. Phản hồi từ người dùng phủ quyết các nhận xét nội bộ trước đó; bản mới chỉ được gọi là bản sửa chờ phản hồi.
