from pathlib import Path
import hashlib,json
B=Path(__file__).parent
manifest=json.loads((B/'manifest.json').read_text(encoding='utf-8'))
observations=[
'Ô giao việc hiển thị yêu cầu viết email chào hàng cho đèn Mẫu A, nút Tạo bản nháp và con trỏ. Ảnh tay gõ bên cạnh hỗ trợ thao tác, không thay đối tượng email.',
'Email nháp xuất hiện đầy đủ với người nhận khach@vidu.invalid, tiêu đề Mẫu A, lời Mua ngay!, lời sai không dây/120.000; nhãn chưa kiểm tra và Gửi khóa. Danh tính nay khớp caseFacts.',
'Lời Dùng không dây tô đỏ đứng sát mô hình đèn có dây và nguồn USB-C có dây/Không pin. Không còn credit Pexels gán cho mô hình 3D. Toàn khung ghi dữ liệu giả định.',
'Câu hỏi khách về pin/ra ngoài mang nhãn phản hồi giả định nếu gửi; trách nhiệm xác nhận lại thuộc người gửi; hộp trả lời còn chưa gửi/đang xác minh.',
'Thời gian viết 2 phút cạnh baseline12; kiểm tra+sửa chờ đo, tổng chưa có. Không gọi bản nháp nhanh là toàn bộ việc xong.',
'Bản nháp trông hoàn chỉnh bên trái vẫn có hai lỗi; bốn ô kiểm tính năng/giá/nhu cầu/trách nhiệm bên phải chưa tick. Trạng thái chưa đối chiếu nguồn rõ.',
'Luồng AI tạo nháp → Bạn kiểm tra; chính câu không dây được gạch bỏ và dòng nguồn có dây/không pin đặt cạnh, cho thấy người nhận lại một lỗi cụ thể để xử lý.',
'Disclaimer hiển thị rõ đèn/tính năng/giá/thời gian giả định, chỉ bàn phần việc và không dự báo nghề nghiệp cá nhân.',
'Cùng email nháp, người nhận khach@vidu.invalid, lời Mua ngay!, tính năng/giá sai và Gửi khóa; đúng đối tượng phân tích, không còn headset thay email.',
'Hồ sơ Mẫu A giả định có USB-C có dây, không pin và giá1.200.000; mô hình đèn giữ dây nguồn nhìn thấy. Chỉ xác nhận tính nhất quán nội bộ, không thông số sản phẩm thật.',
'Lời khách cần dùng nơi không có ổ cắm đứng cạnh nguồn USB-C có dây/không pin và cảnh báo chưa thể mặc định phù hợp. Nhu cầu với hạn chế nguồn điện nhìn thấy cùng khung.',
'Cam kết được phép là nguồn USB-C có dây/không pin; lời Dùng không dây bị gạch. Mối quan hệ nguồn giả định→giới hạn lời hứa trực tiếp.',
'Giá nguồn1.200.000 được tô sáng bên trái, giá nháp120.000 bên phải có trạng thái chưa khớp. Cặp số cùng sản phẩm đọc được, không coi dữ liệu minh họa là giá bán thật.',
'Mua ngay! trong bản nháp ban đầu được đối chiếu Mời bạn tham khảo. ở bản sửa. Mua ngay! đã xuất hiện tại L02/L09; nhãn nay là Giọng thúc ép, không còn gọi bản thân mệnh lệnh là hứa tính năng.',
'Hội thoại khách hỏi không có nguồn USB dùng được không; vùng Cần trả lời ghi đang chờ xác minh nguồn điện và trạng thái chưa trả lời/tiếp tục theo dõi.',
'Cùng email Mẫu A và khach@vidu.invalid với Mua ngay!/không dây/120.000; AI tạo nháp, chưa kiểm tra và khóa gửi. Khớp ý hỗ trợ bản nháp, không gán cả quy trình hoàn tất.',
'Ba bước trước gửi gồm tính năng/giá/giọng điệu và khóa CHƯA ĐƯỢC GỬI biểu đạt bản nháp chưa phải kết quả. Không hiện dấu đã duyệt.',
'Nhu cầu nơi không có ổ cắm, khách cần không dây và Mẫu A cần dây USB-C nằm cạnh câu trơn tru Phù hợp mọi góc làm việc. Có cảnh báo chưa đáp đúng nhu cầu; mâu thuẫn bối cảnh nay nhìn thấy cụ thể.',
'Nguồn Mẫu A ghi có dây/không pin/1.200.000 cạnh tóm tắt sai không dây/120.000, với trạng thái chưa khớp và chỉ dẫn đối chiếu nguồn giả định.',
'Ba mặt phẳng nay có nội dung: phong bì Tạo bản đầu, checklist Kiểm tra, người với dấu xác nhận Quyết định; cùng nhãn Mẫu A và tuyến ba bước. Đây là sơ đồ biểu tượng có chiều sâu, không phải ảnh tài liệu email.',
'Cùng ba bước, thẻ phong bì Tạo bản đầu được tô coral/nâng lên, hai thẻ sau giữ trung tính. Trọng tâm khớp mệnh đề tạo bản đầu.',
'Thẻ giữa checklist Kiểm tra được tô coral/nâng, thẻ tạo nháp và quyết định giữ trung tính; chữ phụ nói đối chiếu thông tin gốc. Đủ phân biệt bước kiểm tra trong sơ đồ.',
'Thẻ người+check Quyết định được tô coral/nâng, hai bước trước giữ nguyên; chữ phụ nhắc trách nhiệm trước gửi. Chưa biểu diễn thao tác bấm một lựa chọn thật.',
'Ba bước tính năng/giá/giọng điệu cạnh khóa CHƯA ĐƯỢC GỬI, không gộp tất cả thành AI tự gửi. Email vẫn ở trạng thái chưa gửi trong câu chuyện.',
'Viết bản nháp2phút cạnh viết+kiểm+sửa15phút và nhãn nhanh hơn một phần/chưa chắc năng suất cao hơn. Phân biệt phần việc với toàn nhiệm vụ; đây là số giả định.',
'Hai lỗi không dây/120.000 hiện cạnh nguồn có dây/không pin/1.200.000 trước khi có gửi; trạng thái chưa khớp, mô tả phát hiện sớm chứ chưa tuyên bố đã sửa.',
'Chọn nhiệm vụ nháp email Mẫu A; hai lựa chọn đối chiếu bảng/trả lời khách mờ. Có con trỏ và dấu chỉ chọn một việc kiểm tra được.',
'Thẻ dữ liệu giả định ghi Mẫu A và domainvidu.invalid, không dùng dữ liệu khách thật. Domain nay thống nhất với email khach@vidu.invalid; đây là khung nhắc phạm vi dữ liệu chứ chưa phải màn hình nhập brief.',
'Thời gian viết2phút trong sổ theo dõi; baseline12, hàng kiểm/sửa chờ đo và tổng chưa có. Phần đo viết được tách khỏi phần đo sửa.',
'Thời gian kiểm+sửa13phút, dònglog13 và tổng2+13=15 xuất hiện, baseline12 vẫn hiện. Không suy ra một phiên làm việc thực kéo dài13phút từ dữ liệu minh họa.',
'Mục Lỗi còn sót liệt kê không dây/120.000 và trạng thái chưa đạt do chưa khớp nguồn, chưa gửi; không biến lỗi còn lại thành dấu đạt.',
'Tổng AI15phút=2+13 được đặt sát baseline tự làm12. Tổng dùngAI dài hơn ở ví dụ, phép tính nhất quán và nhãn dữ liệu giả định hiện.',
'Khung chưa đủ căn cứ xác minh có cam kết chưa có nguồn, ô Chưa kiểm được và trạng thái Chặn duyệt/Chưa gửi. Không tự duyệt một lời hứa chưa kiểm chứng.',
'Prompt mới giới thiệu Mẫu A yêu cầu chỉ dùng thông tin gốc, thiếu hãy hỏi lại; có nhãn sản phẩm/người đọc/không hứa ngoài nguồn. Khớp hành động đổi cách giao việc.',
'Cùng toàn nhiệm vụ tự làm12phút đứng cạnh viết+kiểm+sửa15phút=2+13; dòng so cùng nhiệm vụ/cùng tiêu chuẩn nguồn và nhu cầu đã được thêm. Không còn chỉ so2phút phần việc với15phút tổng.',
'Ba thẻ nhiệm vụ có biểu tượng/nhãn thật trong3D; trên khung phân AI hỗ trợ ban đầu với Bạn kiểm tra nguồn và duyệt gửi. Giải thích vai trò bằng sơ đồ, không có cảnh kéo thẻ thật trong proof.',
'Ô nhập bình luận có ví dụ Tôi muốn thử nháp email cho khách và nút Để lại một ví dụ. Đúng nơi/hành động CTA, không thao tác tài khoản thật.',
'Endcard TYRANNO với nút đăng ký, ba bước tạo nháp/kiểm tra/quyết định và thẻ nhắc email Mẫu A/nguồn/giá/nhu cầu/người quyết định. Phụ đề cuối còn hiện ở proof.'
]
assert len(observations)==len(manifest)==38
v1dir=B.parent/'proofs-v1'
out=[]
for item,observed in zip(manifest,observations):
    p=B/item['file'];digest=hashlib.sha256(p.read_bytes()).hexdigest();old=v1dir/item['file']
    oldhash=hashlib.sha256(old.read_bytes()).hexdigest() if old.exists() else None
    out.append({'id':item['id'],'status':'pass','observed':observed,'issues':[], 'evidence':item['file'],'frame':item['frame'],'evidenceSHA256':digest,'previousProofSHA256':oldhash,'proofChanged':oldhash!=digest if oldhash else None})
scope={'date':'2026-11-12','revision':'v2 independently re-opened all38 proof frames in10pairedsheets, not copied prior statuses',
    'reviewedAllShots':38,'openedPairSheets':[{'file':f'pairs-{i:02}.jpg','sha256':hashlib.sha256((B/f'pairs-{i:02}.jpg').read_bytes()).hexdigest()}for i in range(1,11)],
    'openedFullFrames':['L03-202.jpg','L07-393.jpg','L14-933.jpg','L18-1180.jpg','L22-1428.jpg','L35-2107.jpg'],
    'method':'Compared actual v2 rendered pixels with spoken clause and requiredVisual. About75% shot frame sampled. No continuous playback/action progression checked.',
    'passMeaning':'Core spoken meaning is visibly represented at this sampled state, including explicit diagrams for abstract clauses. Pass does not claim every planned pointer/transition/click or full authored layout contract is implemented.',
    'contractDeviations':[{'shots':['L20','L21','L22','L23','L36'],'observed':'3D uses meaningful icons+step labels with highlighted focus, not full email/source documents or an actual review-choice action.'},{'shots':['L01','L28'],'observed':'Prompt/dummy-data panels carry clause meaning; no attached source file or entire brief form is visible in sampled frame.'}],
    'hypotheticalFactPolicy':'All feature/price/time values remain labelled dummy illustration. This review does not validate actual lamp specs, measured AI performance or a real user outcome.',
    'unverified':['Within-shot animation progression','Audio listening','FinalMP4 after v2render','User aesthetic acceptance'],
    'requiredBeforeDelivery':'Review actual finalMP4 clauseframes and transitions; this report only clears static semantic proofs for rendering.'}
report={'shots':out,'scope':scope,'summary':{'pass':38,'fix':0,'mandatoryStaticSemanticDefects':[]}}
(B/'semantic-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report['summary']))
