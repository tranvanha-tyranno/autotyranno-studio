from pathlib import Path
import hashlib,json
B=Path(__file__).parent
manifest=json.loads((B/'manifest.json').read_text(encoding='utf-8'))
notes=[
('pass','Ô giao việc ghi yêu cầu viết email giới thiệu đèn bàn Mẫu A; nút Tạo bản nháp và con trỏ hiện, ảnh tay gõ chỉ hỗ trợ thao tác.',[]),
('fix','Email có chủ đề, người nhận, nội dung nháp, nhãn chưa gửi và nút Gửi khóa.',['Người nhận trong pixel là khachhang@example.test, khác caseFacts/visibleFacts yêu cầu khach@vidu.invalid; đồng bộ một danh tính giả định cho toàn ví dụ.']),
('fix','Cụm Dùng không dây tô đỏ bên trái; mô hình đèn có dây và dòng USB-C có dây/Không pin bên phải tạo mâu thuẫn trực tiếp.',['Credit Artem Podrez/Pexels đang gắn dưới mô hình thủ tục 3D; bỏ credit đó tại cảnh không hiển thị ảnh của tác giả. Không coi mô hình/nhãn này là xác minh thông số sản phẩm thật.']),
('pass','Bong bóng phản hồi được ghi rõ giả định nếu gửi; câu hỏi về pin/ra ngoài cùng hộp trả lời người gửi, trạng thái chưa gửi/đang xác minh.',[]),
('pass','Số thời gian viết 2 phút, baseline tự làm 12 phút, hàng kiểm tra chờ đo và tổng chưa có cùng xuất hiện; dữ liệu giả định hiện rõ.',[]),
('pass','Bản nháp còn lời không dây và giá 120.000; bên phải checkbox tính năng/giá/nhu cầu/trách nhiệm đều chưa được tick.',[]),
('fix','Sơ đồ AI tạo nháp → Bạn kiểm tra và ba câu hỏi tính năng/giá/nhu cầu biểu đạt phần việc còn lại.',['Không có hành động sửa hay email đang sửa như contract; mới chuyển từ công việc chung sang ba câu hỏi. Thêm cùng email với một sửa đổi hoặc vùng cần kiểm tra để lời ngồi sửa có vật thể cụ thể.']),
('pass','Thẻ disclaimer nói rõ đèn/tính năng/giá/thời gian đều giả định và không dự báo nghề nghiệp cá nhân.',[]),
('fix','Cùng email nháp và nút Gửi khóa xuất hiện, đúng đối tượng email thay cho headset.',['Người nhận pixel khachhang@example.test khác danh tính caseFacts khach@vidu.invalid; đồng bộ trước final.']),
('pass','Hồ sơ sản phẩm giả định có cùng Mẫu A, USB-C có dây, không có pin, giá 1.200.000; mô hình đèn giữ dây nhìn thấy.',[]),
('pass','Nhu cầu khách dùng nơi không có ổ cắm đứng cạnh thông tin USB-C có dây/không pin và cảnh báo không mặc định phù hợp.',[]),
('pass','Thông tin được phép nói là USB-C có dây/không pin; câu dùng không dây gạch bỏ. Đây là chọn cam kết theo nguồn giả định, không phải chứng thực spec thật.',[]),
('pass','Bảng nguồn giả định giá 1.200.000 và bản nháp 120.000 cùng hiện; hàng giá nguồn tô sáng, bản nháp đánh dấu chưa khớp.',[]),
('fix','Hai câu Mua ngay! → Mời bạn tham khảo. thể hiện thay đổi giọng điệu bằng nội dung thật.',['Mua ngay! không xuất hiện trong các email ban đầu L02/L09/L16 nhưng được gọi Bản nháp ban đầu ở đây; thêm vào bản nháp hoặc ghi rõ đây là một câu đề xuất riêng.','Nhãn Hứa quá mức không được chứng minh bởi Mua ngay!; đó là lời thúc ép chứ chưa hứa tính năng. Dùng nhãn Giọng thúc ép, giữ sai tính năng ở cảnh riêng.']),
('pass','Lời khách cần mang đèn tới nơi không có ổ cắm và lời đáp lịch sự nhưng bỏ qua nhu cầu hiện trong hai hộp hội thoại, có trạng thái chưa giải quyết.',[]),
('fix','Email nháp tái hiện cùng tiêu đề và hai lỗi tính năng/giá; AI tạo nháp chưa kiểm tra, Gửi khóa.',['Người nhận pixel chưa đồng bộ caseFacts.','Hình tĩnh cho biết bản nháp có mặt, không chứng minh tiến trình gõ hoặc cột tạo nháp được tick; không báo đã kiểm chuyển động từ proof này.']),
('pass','Đầu ra có dùng không dây và 120.000, bên cạnh ghi chưa đạt do tính năng/con số chưa khớp và chưa gửi. Giữ trạng thái lỗi, không tự chuyển sang duyệt.',[]),
('fix','Hai panel nêu yêu cầu viết email, hai câu hỏi bối cảnh và lời dùng không dây.',['Thiếu chính yêu cầu khách nơi không có ổ cắm đứng cạnh câu trơn tru để cho thấy mâu thuẫn bối cảnh; hiện tại phần lớn là nhãn kể rằng thiếu bối cảnh. Thêm yêu cầu khách từ L11/L15 và quan hệ chưa được đáp ứng.']),
('pass','Nguồn Mẫu A với USB-C/không pin/1.200.000 đứng sát bản tóm tắt sai không dây/120.000, sự khác biệt đọc được và nguồn được ghi giả định.',[]),
('fix','Ba mặt phẳng xám cùng đường nối và một câu mô tả bằng chữ.',['Ba plane trắng/xám không có email, nguồn, quyết định hoặc nhãn bước. Ý nghĩa chỉ tồn tại ở câu chữ dưới hình; phải hiện tài liệu/thao tác thật trên các plane.']),
('fix','Plane đầu đổi sang cam, hai plane sau xám; chữ nói AI tạo bản đầu.',['Không có email/bản nháp/nội dung; màu cam không đủ biểu đạt tạo nháp. Tài liệu đúng tình huống phải nhìn thấy.']),
('fix','Plane giữa cam, hai plane ngoài xám; chữ nói đối chiếu nguồn.',['Không có nguồn hay dữ liệu cần kiểm tra và không có quan hệ đối chiếu. Cần hiện dòng gốc/bản nháp và liên kết cụ thể.']),
('fix','Plane cuối cam, các plane còn lại xám; chữ nói chịu trách nhiệm trước khi gửi.',['Không có người duyệt/trạng thái lựa chọn hay email bị chặn. Cần hiện các lựa chọn hoặc quyết định thật, không chỉ tô màu một hộp.']),
('pass','Ba bước tính năng/giá/giọng điệu cùng biểu tượng khóa và CHƯA ĐƯỢC GỬI. Phân biệt được phần viết với kiểm tra trước gửi.',[]),
('pass','Một thao tác viết nháp 2 phút và toàn nhiệm vụ viết+kiểm+sửa 15 phút được đặt cạnh nhau, nhãn chỉ nhanh một phần. Các số được ghi giả định toàn khung.',[]),
('pass','Nguồn và bản nháp sai hiện cạnh nhau, tính năng lẫn giá sai được nhìn thấy trước khi có gửi. Đủ để minh họa phát hiện lỗi, chưa nhận là đã sửa.',[]),
('pass','Một nhiệm vụ soạn email Mẫu A được chọn; hai nhiệm vụ khác mờ, con trỏ ở vùng lựa chọn. Thể hiện chọn việc nhỏ cụ thể.',[]),
('fix','Thẻ chỉ dùng dữ liệu giả định, Mẫu A, Khách vidu.invalid và không dùng dữ liệu thật.',['Danh tính khách/domain không đồng bộ với email trước khachhang@example.test và storyboard khach@vidu.invalid. Dùng một ví dụ nhất quán.','Không có brief/email đang nhận thông tin, mới là nhãn dữ liệu giả định; thêm dữ liệu ví dụ vào chính ô giao việc nếu muốn đạt đầy đủ contract.']),
('pass','Thời gian viết 2 phút được hiển thị trong sổ theo dõi cùng baseline 12, phần kiểm tra chờ đo và tổng chưa có.',[]),
('pass','Thời gian kiểm tra+sửa 13 phút, hàng log 13 và phép cộng 2+13=15 cùng hiện; dữ liệu giả định. Proof không chứng minh đã thao tác sửa 13 phút thật.',[]),
('pass','Hai lỗi còn nguyên không dây/120.000 với trạng thái chưa đạt và chưa gửi, đúng lời lỗi còn sót.',[]),
('pass','Baseline tự làm 12 phút so với 2 phút viết+13 phút kiểm/sửa=15; tổng AI chưa được gọi thành tiết kiệm. Phép tính nhìn thấy và nhất quán.',[]),
('pass','Đầu ra sai tính năng/giá và trạng thái chưa đạt, chưa gửi; việc không đủ kiểm chứng không được đổi thành duyệt.',[]),
('pass','Prompt đã được sửa thành chỉ dùng nguồn gốc, thiếu thì hỏi lại; có sản phẩm/người đọc/không hứa ngoài nguồn, phù hợp đổi cách giao việc.',[]),
('fix','2 phút viết nháp được so với 15 phút toàn nhiệm vụ và nhãn chưa chắc năng suất cao hơn.',['Đang so phần với tổng chứ chưa trực tiếp cho thấy phương án cũ; contract yêu cầu 12 phút tự làm cạnh 15 phút dùng AI cùng tiêu chuẩn chất lượng/lỗi còn lại. Thêm baseline 12 như L32.']),
('fix','Ba plane xám, hai nhãn trên chia AI hỗ trợ ban đầu/Bạn kiểm tra nguồn và duyệt gửi.',['Các nhiệm vụ trên plane không hiện; không thể thấy cái gì được giao/giữ hoặc thao tác phân công. Cần nội dung ba bước/tài liệu và trạng thái người chịu trách nhiệm.']),
('pass','Ô bình luận có ví dụ Tôi muốn thử nháp email cho khách, nút Để lại một ví dụ và con trỏ. Đúng CTA; không phải thao tác đăng bình luận thật.',[]),
('pass','End card TYRANNO có nút Đăng ký, ba bước tạo nháp/kiểm tra/quyết định và thông điệp thử/kiểm tra, phụ đề câu cuối vẫn hiện ở proof.',[]),
]
assert len(notes)==len(manifest)==38
out=[]
for item,(status,observed,issues) in zip(manifest,notes):
    out.append({'id':item['id'],'status':status,'observed':observed,'issues':issues,'evidence':item['file'],'frame':item['frame'],'evidenceSHA256':hashlib.sha256((B/item['file']).read_bytes()).hexdigest()})
scope={'date':'2026-11-12','reviewedAllShots':38,'openedPairSheets':[f'pairs-{i:02}.jpg' for i in range(1,11)],
    'openedFullFrames':['L03-202.jpg','L13-884.jpg','L14-933.jpg','L20-1360.jpg','L28-1773.jpg','L35-2107.jpg'],
    'method':'Compared actual rendered pixels with full narrated clause and requiredVisual. Each proof samples about75% of its shot; no animation or continuous playback verified.',
    'passMeaning':'Static proof carries core spoken meaning without an unrelated stock substitute. Pass does not verify every planned motion/layout detail or external facts.',
    'hypotheticalFactPolicy':'Prices/features/times are authored dummy data explicitly labelled illustrative. No real product specifications, AI performance or user outcome accepted as evidence merely because they appear in a panel.',
    'unverified':['Motion timing/progression within shot','Actual audio listening','Final MP4 after repairs','User aesthetic acceptance'],
    'requiredBeforeFinal':'Fix all flagged semantic/continuity issues, regenerate affected proofs, then review actual final MP4 clause frames. Current blank3Dplanes are not accepted.'}
report={'shots':out,'scope':scope,'summary':{'pass':sum(s['status']=='pass' for s in out),'fix':sum(s['status']=='fix'for s in out)}}
(B/'semantic-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report['summary']))
