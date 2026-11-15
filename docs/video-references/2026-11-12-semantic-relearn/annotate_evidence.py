from pathlib import Path
import hashlib,json
B=Path(__file__).parent
refs=json.loads((B/'reference-pairs.json').read_text(encoding='utf-8'))
annotations=[
('direct_object','Hiện một ô thực đơn có ảnh món ăn và chữ MENU đúng lúc nhắc thực đơn.','Không thể xác thực nguồn AI của ảnh chỉ bằng frame.'),
('object_context','Ô hình thứ ba là người dùng laptop/tài liệu học; hai ô trước vẫn giữ menu và điện ảnh.','Công dụng học tập chủ yếu do lời kể, nội dung màn hình nhỏ chưa đọc rõ.'),
('context_only','Nhân vật hoạt hình ngồi trước máy tính tại bàn làm việc.','Không thấy dữ liệu hoặc một bản báo cáo cụ thể.'),
('context_only','Vẫn là nhân vật ngồi trước máy tính, tay cạnh mặt.','Không thấy nguồn đối chiếu hoặc trạng thái kiểm tra thay đổi.'),
('action_mismatch','Nhóm nhân vật hoạt hình đứng bên đường với xe/tank trong tiền cảnh.','Không thấy mã, thao tác kiểm tra hay sửa code tại mốc này.'),
('direct_object','Điện thoại và màn hình Shein với lưới ảnh quần áo, giá và lựa chọn.','Học cách đưa đúng đối tượng mua sắm lên hình, không lấy lại ảnh nguồn.'),
('explicit_graphic','Kho quần áo/kiện hàng, biểu tượng áo và số mẫu theo ngày cùng hiện.','Hình số diễn đạt quy mô; audit dựng hình không xác minh số liệu kinh doanh.'),
('explicit_graphic','Hộp hàng và hạn mức miễn thuế được ghi cạnh nhau.','Đối tượng và quy tắc liên hệ trực tiếp; không dùng như tư vấn thuế hiện hành.'),
('direct_object_state','Những hộp Shein xếp ngay bậc cửa nhà.','Đúng kiện hàng và đích đến; frame tĩnh không chứng minh thao tác giao nhận.'),
('staged_category_graphic','Ba loại hàng được phân biệt bằng icon, váy nữ là nhóm đang được đưa lên.','Nhóm xuất hiện theo lời; đây là minh họa danh mục, không phải ảnh người bất kỳ.'),
('direct_class','Cánh tay robot và dây chuyền đang xử lý vật thể công nghiệp.','Cho thấy sản xuất, không chứng minh toàn bộ quy mô kinh tế.'),
('context_only','Giá/kệ và hàng trong nhà kho, chưa có hành động người mua.','Cùng bối cảnh hàng hóa nhưng chưa thể hiện sức mua yếu.'),
('direct_action','Người mặc đồ bếp đang thao tác tại quầy bếp, thấy tay và thực phẩm.','Khớp hành động nấu; không nhìn thấy đầy đủ số lượng đầu bếp được kể.'),
('state_mismatch','Khung hàng ăn/chợ dưới đèn lồng, có nhiều người trong vùng nhìn thấy.','Không thể hiện rõ nhà hàng vắng khách, bàn trống hay lượng khách ít.'),
('work_context_only','Nhiều người ngồi làm việc với bàn/máy may trong xưởng.','Không suy ra tình trạng di cư của người trong hình từ nghề hoặc trang phục.'),
('device_action_mismatch','Cận cảnh màn hình laptop với nội dung trên trình duyệt.','Không thấy điện thoại hoặc thao tác nhấn lưu bài tại mốc này.'),
('direct_object','Kệ đầy sách với gáy sách nhìn thấy.','Đúng đồ vật được nhắc; không dùng thêm laptop chung chung để thay.'),
('direct_action','Tay cầm bút viết vào giấy/sổ.','Đúng hành động viết; chưa chứng minh nội dung ấy đã được đăng công khai.'),
('direct_action','Tay và giấy ghi chép hiện rõ khi nói đưa suy nghĩ ra giấy.','Hành động là trục minh họa; không cần cảnh nhóm họp để giải thích.'),
('action_mismatch','Một người cúi đọc/viết tại bàn thư viện.','Không thấy người trình bày, khán giả hay tài liệu trình chiếu.'),
]
for r,(match,observed,limit) in zip(refs,annotations):
    r.update({'matchAssessment':match,'observedVisual':observed,'limit':limit,'frameSHA256':hashlib.sha256((B/r['file']).read_bytes()).hexdigest()})
rejected=json.loads((B/'rejected-pairs.json').read_text(encoding='utf-8'))
fixes=[
('Người gõ trên laptop; màn hình là trang web nhiều hình/cột, không thấy composer email hay prompt AI.','Sai đối tượng và trạng thái giao việc.','Prompt viết email và cửa sổ soạn thư có Tới/Tiêu đề/Nội dung; nhãn tình huống minh họa.'),
('Tay viết vào sổ giấy cạnh laptop.','Lời nói bản nháp trên màn hình nhưng hình chính là giấy viết tay.','Bản nháp email xuất hiện trong cửa sổ màn hình; giữ cùng tiêu đề và nội dung qua các cảnh.'),
('Hai tay cầm headset trước ngực.','Đổi email thành vật dụng gọi điện; không còn đối tượng đang phân tích.','Giữ cận cảnh email và chỉ rõ các phần cần xử lý.'),
('Hai người xem giấy bên trái và nhóm đeo headset bên phải.','Không thấy sửa câu chữ, giọng điệu trước/sau hoặc một phản hồi khách hàng.','Tách theo hai mệnh đề: sửa một câu email cụ thể rồi hiện thread phản hồi liên quan.'),
('Ba người trao đổi tài liệu ở bàn.','Không thấy nút gửi hoặc ba bước bị gộp.','Ba bước tạo nháp/kiểm tra/quyết định hiện riêng; nút Gửi chỉ mở khi các bước cần thiết hoàn tất.'),
('Hai ảnh người ghi sổ, có chữ nhấn nói tính thời gian sửa.','Không có thời gian viết, thời gian sửa hoặc số lỗi để đọc và so sánh.','Bảng nhật ký ba cột thời gian viết/thời gian sửa/lỗi còn sót; số minh họa phải ghi rõ và nhất quán.'),
('Ảnh giấy note dán trên tường bị mờ.','Dòng chữ CTA là phần duy nhất nói tới bình luận; ảnh không làm rõ hành động.','Ô bình luận của giao diện minh họa và một ví dụ nhiệm vụ cụ thể đang được nhập.'),
('Một phụ nữ đối diện người khác tại bàn như cuộc phỏng vấn.','Không thể hiện nghề gồm các nhiệm vụ hoặc một thao tác nhanh lên nhưng nghề còn tồn tại.','Một chức danh gắn với các nhiệm vụ; chỉ một nhiệm vụ thay đổi tốc độ, trách nhiệm còn hiển thị.'),
('Giấy note xanh/hồng trên tường.','Không thấy công cụ nhận yêu cầu hoặc sinh dàn ý.','Một đề bài và dàn ý có đề mục thực sự hiện ra, đúng loại việc đang nói.'),
('Tay chỉ giấy, calculator và tiêu đề Quay về nguồn.','Không nhìn thấy hai giá trị bất nhất hoặc trường dữ liệu gốc cần đối chiếu.','Hai giá trị khác nhau cho cùng một mục, hàng nguồn được tô sáng và thao tác sửa về giá trị nguồn.'),
('Nhóm bốn nhân viên đeo headset.','Không có câu trả lời lịch sự hoặc dấu hiệu vấn đề của khách chưa được giải quyết.','Thread có yêu cầu khách cụ thể, câu trả lời lịch sự nhưng bỏ sót yêu cầu, vấn đề vẫn được đánh dấu chưa xử lý.'),
('Tay đang ghi vào sổ, số đo không hiện.','Dùng đạo cụ ghi chép thay cho hành động đo thời gian.','Đồng hồ hoặc nhật ký với cột thời gian chỉnh sửa đang được ghi nhận.'),
('Người trong cuộc phỏng vấn ở văn phòng.','Không thể hiện nơi nhập bình luận hay ví dụ nhiệm vụ.','Ô bình luận minh họa với ví dụ nhiệm vụ; không gán câu chuyện AI cho người stock.'),
]
for r,(observed,failure,must) in zip(rejected,fixes):
    r.update({'observedVisual':observed,'semanticFailure':failure,'requiredReplacement':must,'verdict':'reject_for_semantic_mismatch','frameSHA256':hashlib.sha256((B/r['file']).read_bytes()).hexdigest()})
media={r['media'] for r in refs}
media.update(str(Path('videos/2026-11-12-hai-huong')/d/'final.mp4').replace('\\','/') for d in ['long','hidden'])
record={'date':'2026-11-12','trigger':'User explicitly rejected both demos because images do not match spoken narration',
    'scope':{'referencePhraseFramePairs':20,'referencePairsPerChannel':10,'rejectedPhraseFramePairs':13,'referenceVideos':4,
    'observed':'Opened all four reference phrase sheets and all four rejected phrase sheets. Frames extracted from actual MP4 files.',
    'notPerformed':['No continuous full playback','No manual audio listening','No verification of business/economic claims in reference narration'],
    'timingPrecision':'Reference anchors come from overlapping YouTube caption segments; frameTime/decodedFrameTime are exact extraction positions, not claimed forced-aligned word timestamps. Rejected samples use exact-take aligned words.'},
    'manifestAudit':{'shotsInspectedAsData':52,'storedSubjectActionObjectStateContracts':0,'semanticAcceptanceWasNotTestedByTechnicalQA':True},
    'referencePairs':refs,'rejectedPairs':rejected,
    'mediaHashes':[{'file':p,'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}for p in sorted(media)],
    'requiredGate':{'contract':['spokenClause','start/end','subject','action','object','state/relation','mustShow','mustNotShow','assetRole','source/license','actualObservedEvidence'],
    'reject':['Only the industry/setting matches','Named object or action absent','Wrong state or relationship','Meaning depends entirely on subtitle/title','Unverified personal/event identity inferred from stock'],
    'acceptancePolicy':'Technical decode/timing/legibility cannot imply semantic or aesthetic acceptance. User rejection overrides earlier internal review language.'}}
(B/'evidence.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print('ANNOTATED',len(refs),'reference pairs and',len(rejected),'rejected pairs')
