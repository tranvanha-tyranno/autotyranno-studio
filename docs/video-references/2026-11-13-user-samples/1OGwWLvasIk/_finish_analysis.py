"""Authored continuation notes; preserves the first eight inspected blocks."""
import json
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

P = Path(__file__).resolve().parent
D = json.loads((P / 'analysis.json').read_text(encoding='utf-8'))
STUDY = json.loads((P / 'study-blocks.json').read_text(encoding='utf-8'))
BLOCKS = D['blocks'][:8]
for block, title in zip(BLOCKS, [
        'Vị trí thuận lợi, hiện trạng khó sống và lời hứa giải thích',
        'Nguồn gốc địa hình, sinh kế và phát triển manh mún',
        'Từ hiện trạng sang bốn điểm nghẽn: giao thông',
        'Ngập và cứu hộ: một chi tiết người thật làm điểm nhớ',
        'Không gian công cộng, số liệu và yêu cầu tái thiết',
        'Giới thiệu dự thảo bằng nguồn và số liệu đọc được',
        'So trước/sau và câu hỏi vì sao quỹ đất đủ',
        'Đô thị nén: phá hiểu nhầm bằng ẩn dụ hộp giấy']):
    block['title'] = title


def add(index, title, lesson, rows):
    beats = []
    for a, b, function, visual, relation, attention, transition, limit in rows:
        item = {'start': a, 'end': b, 'scriptFunction': function, 'visibleEvidence': visual,
                'visualWordRelationship': relation, 'teaching': relation,
                'attentionInference': attention, 'transition': transition}
        if limit:
            item['limit'] = limit
        beats.append(item)
    BLOCKS.append({'index': index, 'start': index * 60, 'end': min(index * 60 + 60, 1524),
                   'title': title, 'reviewedSheets': STUDY[index]['sheets'], 'beats': beats,
                   'reusableLesson': lesson})


add(8, 'Đô thị nén qua trường hợp quốc tế và lớp hạ tầng ngầm',
    'Đưa khái niệm về một trường hợp nhìn thấy rồi thêm giới hạn: chỉ nén nhà chưa đủ nếu đỗ xe và hạ tầng vẫn chiếm mặt đất. Hình phối cảnh phải được ghi là dự kiến/minh họa, không chứng cứ công trình đã xong.', [
    (480, 496, 'Khép ví dụ nén bằng việc trả mặt đất cho đường, quảng trường, hồ và tiện ích.',
     '08:00–08:14.5 là flycam nhà thấp, hồ và các khối cao hơn trong cùng vùng; mascot xuất hiện ở08:14.5–08:15.',
     'Toàn cảnh đối chiếu quy mô chiếm đất; hình bối cảnh chưa tự biểu diễn phép giữ nguyên tổng diện tích sàn như ẩn dụ hộp trước đó.',
     'Chốt phần giải nghĩa trước khi người xem mệt vì thuật ngữ.', 'Câu hỏi về thực tế mở trường hợpTokyo.', ''),
    (496, 520, 'DùngRoppongi làm ví dụ từ khu nhà cũ tới tổ hợp cao tầng có không gian công cộng.',
     '08:19.5–08:25 phố nhỏ với nhà gỗ;08:27.5–08:33 cảnh cao tầng nhìn từ trên;08:35 phố cây đèn sáng.',
     'Đối chiếu hình nhà gỗ/ngõ nhỏ với khối cao tầng và không gian đi bộ; diễn đạt trước/sau theo lời nguồn, không có hồ sơ chứng minh từng ảnh là cùng vị trí trước/sau.',
     'Ví dụ cụ thể trả câu hỏi liệu cơ chế có thể xuất hiện ngoài bản vẽ.', 'Quay lạiVĩnhHưng và vấn đề bãi đỗ/hạ tầng.', 'Không xác minh độc lập vị trí/ngày của tư liệuTokyo.'),
    (520, 540, 'Bổ sung điều kiện ngầm hóa bãi đỗ và kỹ thuật để mặt đất thực sự thoáng.',
     '08:40 góc trên khu nhà;08:42.5–08:46.5 bãi xe máy;08:48–08:50 hầm/bãi đỗ ôtô;08:52–08:53.5 kiến trúc ban đêm;08:55–08:58.5 phối cảnh đại lộ và ven hồ.',
     'Vật thể xe máy→bãi đỗ ngầm khớp ý chuyển chức năng xuống dưới đất. Phối cảnh đẹp hỗ trợ hình dung, không chứng minh đường điện/cáp đều đã nằm ngầm.',
     'Từ nguyên lý chung sang một trở ngại vẫn còn sau giải pháp đầu.', 'Nêu thách thức tái thiết vùng đang có người ở.', 'Góc phối cảnh có thể làrender; không gọi tất cả làfootage thực.')])

add(9, 'Giữ cấu trúc cũ và dùng khối mới tạo nguồn lực',
    'Một mô hình được giải thích tốt khi có hai phần cùng vai trò khác nhau. Chỉ dùng màu/nhãn để phân biệt phần mới và phần cải tạo; không biến hình đẹp của khu khác thành bằng chứng dự án đã thành công.', [
    (540, 555, 'Đặt câu hỏi mới: đất không trống, không thể xóa toàn bộ cộng đồng để dựng lại.',
     '09:00 còn phối cảnh ven hồ;09:03–09:05 flycam cầu/sông và nhà ven sông;09:06.5 khu cao tầng.',
     'Chuyển từ hình mong muốn sang hiện trạng có cư dân để nêu ràng buộc thực thi.',
     'Câu hỏi hạn chế giải pháp trước đó, mở nhu cầu mô hình tiếp theo.', 'Đưa trường hợpThượngHải.', 'Caption nhiều dòng ghi442ha trong khi các thẻ dự án ghi447ha; giữ rawASR, chưa coi442 là số chuẩn.'),
    (555, 578, 'Trường hợpThượngHải: giữ hẻm/kiến trúc cũ, xây cao tầng liền kề, dùng nguồn thu nuôi hạ tầng.',
     '09:10–09:16.5 cao tầng sau dãy mái thấp;09:20 cổng vòm gạch;09:24.5–09:33 flycam tháp quanh các dãy nhà thấp/không gian cây.',
     'Sự kề nhau của cao/tầng thấp làm rõ ý tái thiết đan xen. Không cần thêm đồ họa phức tạp để diễn đạt mối quan hệ không gian nhìn thấy.',
     'Một biến thể của câu trả lời giúp tránh cảm giác chỉ có phá bỏ hoặc giữ nguyên.', 'Áp lại hai phân vùngVĩnhHưng.', 'Tư liệu nhìn thấy chưa đủ xác nhận cơ chế dòng tiền trợ cấp chéo đã được vận hành đúng như lời.'),
    (578, 600, 'Áp mô hình về dự án bằng hai phân vùng và cách phần mới hỗ trợ phần cũ.',
     '09:34.5–09:58.5 flycam khu nhà thấp với tháp cao;09:39.5 thêmiconđất206,1ha;09:43.5 thêm240,9ha;mascot xuất hiện09:48 trở đi.',
     'Đặt hai diện tích cạnh nhau, mỗi phần chỉ một chức năng; giữ nền hiện trạng cùng hệ quy chiếu.',
     'Câu giải nghĩa gần gũi của nguồn biến phân bổ đất thành quan hệ hai phần có vai trò.', 'Gọi chuyên gia để hỏi tiền thực sự đến từ đâu.', 'Nhãn trênvideo chưa xác nhận ranh giới thu hồi của từng thửa đất.')])

add(10, 'Nguồn tài chính và vòng giá trị đất',
    'Thay vì coi đồ án đẹp là đủ, hỏi nguồn lực và mô tả chuỗi hạ tầng→giá trị→tái đầu tư. Giữ rõ đây là lập luận/quan điểm được nguồn dẫn, chưa tự xác minh lời trích hoặc số liệu.', [
    (600, 619, 'Dẫn ý chuyên gia: thiết kế và tầm nhìn cần cơ chế huy động vốn.',
     '10:00 nhân vật hoạt họa đại diện chuyên gia trên nền lưới;10:05–10:15 câu trích xuất hiện và cử chỉ thay đổi.',
     'Màn hình tách khỏi ảnh thành phố để tập trung một mệnh đề; hình nhân vật là đại diện, không phải cảnh phỏng vấn người thật.',
     'Mở phản đề với sự hưng phấn từ hình phối cảnh.', 'Câu hỏi nguồn tiền dẫn sang cơ chế.', 'Chưa truy tài liệu gốc để xác nhận câu trích; không xem hoạt họa làbằng chứngphỏngvấn.'),
    (619, 630, 'Giải thích giá trị đất tăng khi đường, công viên và dịch vụ tốt lên.',
     '10:20–10:25 iconđất, mũi tên lên, đường,cây,khối nhà được thêm quanh tâm;mascot ở10:25.',
     'Thêm từng đầu vào quanh một đối tượng trung tâm, làm rõ quan hệ bằng hình hơn là ảnh tiền đứng riêng.',
     'Một chuỗi nguyên nhân ngắn giúp khán giả theo được thuật ngữtài chính.', 'Ví dụ trong nước cho cơ chế.', ''),
    (630, 650, 'Ví dụĐàNẵng/PhúMỹHưng để kéo lý thuyết về địa danh quen.',
     '10:30–10:37.5 flycam bờ biển và caoốc;10:40 khu nhà quy hoạch;10:44–10:45 chuyên gia hoạt họa trên nền làm mờ.',
     'Địa danh được đi kèm hình đô thị thay vì icon; hình chỉ minh họa kết quả nhìn thấy, chưa đo giá đất hoặc tính nhân quả.',
     'Ví dụ gần người Việt thu hẹp khoảng cách với câu chuyện quốc tế.', 'Mở rộng sang đô thị hóa rồi nêu thước đo.', 'Không coi ảnh biển/caoốc tự xác nhận cơ chếtài chính của hai địa phương.'),
    (650, 660, 'So tỷ lệđô thị hóa và mở câu chốt nguồn lực đấtđai.',
     '10:50 hình bản đồTrungQuốc với65%;10:54.5 quay nền lưới và nhân vật;10:55 câu trích bắt đầu.',
     'Bản đồ và số giúp nhớ một đối chiếu, nhưng mẫu hình chưa cho thấy đủ hai nguồn dữ liệu để kiểm cùng năm/phương pháp.',
     'Nén phần so sánh để chuẩn bị một câu chốt có giá trị.', 'Nhắc thước đo cuối cùng là người dân.', 'Tỷ lệ65/50 là số nguồn nói, chưa kiểm nguồn/ngày; không tái dùng làm số hiện hành.')])

add(11, 'Khóa vòng tiền bằng quyền lợi dân, mởTOD từ vấn đề đi lại',
    'Mô hình sau phải giải đúng vấn đề mô hình trước tạo ra. Câu hỏi họ đi bằng gì là cầu nối nhân quả, mạnh hơn chuyển chương chỉ vì đến lịch đổi cảnh.', [
    (660, 682, 'Nhấn hạ tầng, môi trường và quyền lợi dân; tóm vòng hạ tầng–giá trị đất.',
     '11:00 câu trích trên nhân vật;11:05 baiconnhà,cây,người;11:10 haiiconcông trình/đất với mũi tên ngược chiều;11:15–11:20 mascot và nền làm mờ.',
     'Vòng hai mũi tên cho quan hệ tái đầu tư; thêmconngười khi nói thước đo cuối giúp giữ mục tiêu phục vụ dân.',
     'Chốt phần tài chính để không kéo bài thành câu chuyện đất tănggiá đơn thuần.', 'Nhà cao có đông người, chuyển câu hỏi sang đi lại.', ''),
    (682, 704, 'Định nghĩaTOD sau khi nêu nút thắt người đông/xe cá nhân.',
     '11:25–11:30 chữTOD,icon và diễn giải tiếngViệt trên flycam;11:33.5–11:40 đoàn xe máy chen đặc trên đường.',
     'Từ thuật ngữ vào hậu quả nhìn thấy; đoàn xe thể hiện quy mô di chuyển, không chỉ dùng toa tàu cho mọi câu.',
     'Câu hỏi nhu cầu khiến người xem muốn nghe mô hình tiếp.', 'Nêu quy mô dân số và nhu cầu chuyển phương tiện.', 'Cảnh xe đông có thể minh họa chung, chưa xác nhận chính tuyếnVĩnhHưng.'),
    (704, 720, 'Nêu mức tăngdân số và sự cầnthiết của vận tải khối lượnglớn, mở cơ sở pháp lý.',
     '11:42.5–11:45 iconngười với~80.000 rồi~186.896;11:48–11:55 đường/cầu vượt đang thi công;11:56.5 xuất hiện biểu tượng văn bản.',
     'Đổi số trên cùngicon làm rõ trước/sau; công trường minh họa đầu tư hạ tầng, chưa chứng minh tiến độ của bốn tuyếnmetro.',
     'Tăng độ lớn bài toán trước khi chuyển sang điều kiện triển khai.', 'Ba nền pháp lý ở phút12.', 'RawASR đọc186.896nghìn có thể saiđơn vị; hình là~186.896người. Không nhân thêm1000.')])

add(12, 'Khung thể chế và phân cấpTOD',
    'Phần nhiều định nghĩa cần ngôn ngữ hình ổn định, thêm từng cột, cùng đơn vị để so sánh. Đừng chuyển ảnh quá nhanh khi người xem đang đọc cấp/bán kính.', [
    (720, 735, 'Liệt kê ba nềnpháp lý/quyhoạch mà lời nguồn dùng để tạo tính khảthi.',
     '12:00–12:10 baiconvăn bản/bản đồ trên lưới đen;chữ hìnhghiLuậtThủđô2026,nghịquyết66/2026/NQ-HĐND và quyhoạch100năm.',
     'Baiconbiểu trưng gọn hơn scan nhiều trang nhưng không phải tài liệu gốc để xác minh hiệu lực hay nội dung pháp lý.',
     'Tạo cảm giác mô hình có nềnthểchế sau phần nguyên lý.', 'Từ văn bản tới quan hệ nhàga/phạmviđi bộ.', 'Caption đoạn này nhiều lần ghi2016 khác chữ2026 trênhình. Đánh dấu mâu thuẫn, không tự chọn năm nào làđúng hay coi chữ trênhình lànguồn luật.'),
    (735, 750, 'Giải thích khoảng đi bộ quanhnhàga gắn nhàở,vănphòng,thươngmại,khônggiancôngcộng.',
     '12:14–12:28.5 phối cảnh bờhồ,caoốc và đườngđi bộ,mascot từ12:23.',
     'Hình mô tả một môi trường có thể đi bộ, nhưng không vẽ vòng400–800m hay phépđo thời gian để xác nhận phạmvi.',
     'Cho khoảng thở sau văn bản, đổi từ danh mục pháp lý sang môi trường người dân hình dung.', 'Báo trước ba cấpTOD.', 'Đây là phối cảnh dự kiến/minh họa; không gọi là khu đã hoànthành hay thửnghiệm15phút.'),
    (750, 778, 'Phân ba cấpTOD theo sốtuyến và bánkínhảnhhưởng; cùng cấu trúc cột.',
     '12:30–12:50 nền trắng, cộtquốcgia xuất hiệntrước,thêm cấpđôthị rồi cấpkhuvực; icon, sốtuyến, bánkính đặt tại cùng vịtrí.',
     'Một mẫu so sánh lặp giúpđọc khácbiệt; không đổi background giữa từng số để tránh mất hệquychiếu.',
     'Người xem có mốc phânloại cho việc áp vàoVĩnhHưng.', 'Nhóm mục tiêu chung cho metro.', 'Không xácminh các bánkính/địnhnghĩacấp của thànhphố ngoài video này.'),
    (778, 780, 'Bắt đầu danh mục mục tiêu và dành đấtcôngcộng.',
     '12:55 nền phâncấp làm mờ, bullet đỏ và mục70%nhàgaTOD xuất hiện.',
     'Làm mờ phần vừa giải thích để đặt ýmới lên trên, không chồnghai tầng chữ đọc cùng lúc.',
     'Chuyển từ phânloại sangmục tiêu sau khi hoànthànhba cột.', 'Hoànthiện ba bullet ở13:00.', '')])

add(13, 'Valuecapture và hìnhmẫu rail+property, quay lạiVĩnhHưng',
    'Thuậtngữ kinh tế cần được giải thích bằng dònggiátrị và trườnghợp, sau đó áp trở về dựán. Đừng lấy một tuyếnmetro hiện hữu để nói nó chính là tuyến quyhoạch mới.', [
    (780, 801, 'Hoànthành mục tiêuTOD rồi giải thích giátrị đất quanhga quay lại gópphần vốnmetro.',
     '13:00 ba bullet;13:03–13:18.5 tàuđỏvàng trên đường trêncao,nhàga và cảnh di chuyển qua nhiều góc.',
     'Footagetàu/nhàga làm rõ phươngthức vận tải, nhưng chưa nhìn thấy cơ chế thu giátrị đất hay tỷlệ gópvốn.',
     'Cơ chế tạo một lợíích kép sau phầnquyđịnh.', 'Dẫn HồngKông làmvídụ.', 'Rawcaption ghi2đến30% có thể sainhận dạng; chưa xácminh sốđúng. Không coi đườngtàu hình làbốn tuyếnVĩnhHưng đãxây.'),
    (801, 824, 'TrườnghợpHồngKông: bấtđộngsản kết nối ga và nguồnthu táiđầutư đườngsắt.',
     '13:20–13:23 nhàga,ngườiđi lại,thangcuốn;13:25 chữRAIL+PROPERTY;13:30–13:40 caoốcHồngKông;13:41.5–13:43 cầuđibộ và xe buýt.',
     'Nhàga→thangcuốn→caoốc→kết nốiđi bộ cho thấy cùnghệsinhhoạt; chữ dịch đúngthuậtngữ lànhãn giải nghĩa, không phụđề toàncâu.',
     'MộttrườnghợpchâuÁ cụthểgiúp môhình bớttrừutượng.', 'Áp về bốn tuyếnmetro/BRT ởVĩnhHưng.', 'Hìnhcaoốc/nhàga không tự chứngminh lợi nhuận được phân bổra sao.'),
    (824, 840, 'VĩnhHưng được nguồn đặt trong mạngmetro/BRT và các cấpTOD.',
     '13:45–13:48.5 nhàga trêncao;13:50–13:52 metroiconnhãn4,8,10,15 rồi thêm xe buýtBRT trên nềnmờ;13:55 flycam;13:59.5 iconTODđôthị.',
     'Danh mục sốtuyến được gắn vàoicon, đủ đọc khi nền bịgiảmchi tiết; hình thực chỉminhhọaloại phươngtiện.',
     'Trảtiền đềquyhoạch chung về đềtài banđầu đểkhông lạc sang du lịchquốctế.', 'Tổchứckhốinhà quanhga ởphút14.', 'Đây là cách video nguồn diễn giải dựthảo, chưa xác nhận khảnăng hoặc tiếnđộ xâycác tuyến.')])

add(14, 'Từ đi lại liênvùng tới nhu cầuquanhnhà',
    'Một giải pháp được đánhgiá từ chuyện nhỏ còn chưa xửlý. Hỏi đưaconđihọc/đichợ có phải đi tàu không để dẫn môhình15phút; thay nội dungvì nhu cầu mới, không thaybố cụcvôcớ.', [
    (840, 864, 'Giải thích cụm caoốc quanhga, kết nối ngầm và lợiíchgiảm xe trênmặtđất.',
     '14:00 iconTOD;14:05–14:10 nhàga trêncao giữa nhà thấp;14:12–14:20 tháp cao cạnh tuyếnđường/đườngtàu.',
     'Tòa cao và tuyếnvận tải cùngkhunghình gợi quan hệvịtrí. Tuy nhiên không thấy một hànhtrình thangmáy→ga ngầm để chứngminh lời mô tả đó.',
     'Chốt lợíích môhình hai, rồi để một câu hỏi thực tế phá thế đãđủ.', 'Đi học/đichợ/khámbệnh mỗi ngày thì sao?', 'Không được gọifootagetàu trêncao là minhchứng trực tiếp kết nốingầm củadựán.'),
    (864, 883, 'Đặt nhu cầu lặtvặt hằngngày rồi gọi tên môhìnhđôthị15phút.',
     '14:22.5–14:29.5 cổngtrường,phụhuynh,xe đạp/họcsinh vàmascot;14:30–14:35 iconđôthị15phút,nhânvậtđạidiệnMoreno.',
     'Thấy đúngtrườnghọc/ngườiđóncon khi nhắc nhu cầuđưacon, tránh bám mãi ảnhmetro.',
     'Câu hỏi đời thường giúp người khôngchuyên quyhoạch vẫn theođược xâu giải pháp.', 'Dẫn kháiniệm và trườnghợpParis.', 'Hoạthọanhàkhoahọc làđạidiện; khôngphảicảnh ôngphátbiểu.'),
    (883, 900, 'Giải thích sựmệtmỏi của đôthị từ chức năngsống bịtáchrời.',
     '14:40 thápEiffel/venSông;14:45–14:50 nềnParis làm mờ và hai dòng hỏigiảiđáp;14:51.5–14:56.5 flycam nhànhỏdày;14:58 đườngxe/bụi.',
     'Địa danh địnhvị xuất xứkháiniệm; cặp hỏi–đáp tập trung mộtnguyênnhân, rồi quay về biểu hiệnđi xa.',
     'Mở vấn đềđộngcơ thay vì đọc thêm thuậtngữ.', 'Tác hạiđilạixa và sáunhucầucơbản ởphútsau.', 'Parisminhhọa không tự xácnhận môhìnhápdụngởmọikhu hay kếtquảcụthể.')])

add(15, 'Sáu nhu cầu trong bánkính tiếp cận',
    'Vẽ quanh một tâmnơiở và chỉthêm nhu cầuđangđược gọi. Tách mục tiêuquyhoạch, hìnhmôphỏng và hiệntình; khônghứa khảnăngtiếpcận từ ảnhđẹpmắt.', [
    (900, 916, 'Tóm cái giá củadi chuyển xa và liên hệtrực tiếp với ngườiđi làmHàNội.',
     '15:00–15:03 đườngbụi;15:04.5–15:11.5 luồngxe đông nhìn từcao vớimascot.',
     'Xe/bụi khớp vídụ thời gian,véxăng,tắcđường; chưa đo tiếngồn/phátthải/thờigian bằngframe.',
     'Cách xưng hô và tìnhhuống giờcaođiểm gọi kinhnghiệm khángiả.', 'Mở vòng15phút quanh nơiở.', ''),
    (916, 933, 'Giải thích sáu nhu cầu và phân biệt bộkhung vật lý với bộnão vận hànhthôngminh.',
     '15:15–15:20 sáuiconnhà,cặp,sách,y tế,giỏhàng,vui chơi xếp quanh tâm tròn;15:25–15:30 haiiconnằmngang ghi bộkhung/bộnão.',
     'Cùng tâm và cùng khoảngtrống cho sáu chức năng; phépẩn dụ bộkhung–bộnão được gắn haiđối tượngrõ.',
     'Gom sáunhóm thành một hìnhdễnhớ sau chuỗi việc hằngngày.', 'Áp mục tiêu dịchvụ vàoVĩnhHưng.', 'Vòngicon là sơđồkháiniệm, khôngphải bảnđồđườngđithựchoặc phépđothờigian.'),
    (933, 950, 'Giới thiệu phân bổ trường,y tế,thươngmại,thểthao và khônggianxanh trongdựthảo.',
     '15:33.5–15:36.5 flycamhiệntrạng;15:38–15:40 phối cảnhtrườnghọc;15:42.5–15:47 phố/côngviên nhiều người trong hìnhmôphỏng.',
     'Trườnghọc có sân/họcsinh đúng chủđềdịchvụ; cảnh môphỏng chỉ phục vụ hìnhdung mục tiêu.',
     'Chuyển thuyếtminhkhungchung thành lợíích nhìnrathấy.', 'Rút vềtrảinghiệm của người viết và khuônviênxanh.', 'Không ghi nhữnghình này làtư liệuVĩnhHưngsaudựán.'),
    (950, 960, 'Kể trải nghiệm về tiệníchgầnnhà ởnướcngoài, chuẩn bị tuađến tươnglai.',
     '15:49–15:58 đườngcây,côngviên và lốiđibộ thực có gócnhìn thayđổi.',
     'Côngviên hỗtrợ vídụ tiếpcậncâyxanh, chưa xácnhận chỗđóthuộcÚc hoặc có đủtrường/phòngkhám trong15phút.',
     'Giọng kể cá nhân tạo thayđổi giữa phần nhiềukháiniệm.', 'Thửhìnhdung năm2030 ở16:14.', 'Lời kể về trải nghiệm của người viết là lời nguồn, chưa được xác minh độc lập.')])

add(16, 'Tua tới tươnglai có điều kiện, biến chỉtiêu thành hìnhdung',
    'Phân biệt rõ tươnglaigiảđịnh với hiệntrạng. Với tỉlệ thu hồi/phạmviảnhhưởng, phải giữ mẫu số và điều kiện trong lời/chữ, tránh phóng đại thành70%toàn bộđấtphường.', [
    (960, 974, 'Khép trải nghiệm khuônviên gầnnhà bằng minh họa ngườiđi bộ.',
     '16:00–16:05 nhânvật2D trênphố;16:06.5–16:10 chuyển vào côngviên, ghế và cây.',
     'Giữ cùngnhânvật, đổi khônggian tạo ý di chuyển/tiếp cận gần; hoạt họa minh họa chứ không đoquãngđường.',
     'Nhânvật nhẹnhàng tạo nhịp đổi sau các bảngsố liệu.', 'Câu tua nhanh đến2030.', ''),
    (974, 995, 'Chuyển hiệntrạng sang tầmnhìn2030; giải thích phầnđất phục vụhạtầng/côngcộng.',
     '16:14 chồnglớphiệntrạngvàphối cảnh;16:15–16:20 flycam đượcthaybằngmôphỏng;16:22–16:34.5 chữ~70%diệntíchđất và côngviên/đường trên hìnhmôphỏng.',
     'Chuyểntừthực sangmôphỏng làm thấy khácbiệt; chữmàn hình rútgọn hơn lời vềdiệntíchtrongphạmviảnhhưởngcáchộ.',
     'Cho ngườixem thấy viễn cảnh để hiểu tại saophải làm, sauđó quay lạiđiềukiệncuối bài.', 'Cụthểhóamặt cắtđường.', 'Mẫu sốcủa70%khôngđược rútgọn sai; đây là lời phân tíchdựthảochứ chưa làquyết địnhthuhồihoànthành.'),
    (995, 1020, 'Hai trục đại lộ và đườngkhuvực làm khungxươnggiao thông.',
     '16:35–16:40 phối cảnhđại lộ;16:45 iconđường60m/10làn và40m/6làn,16:50thêmđường15m/21,5m;16:55–16:58.5 ngườiđạpxe/khối nhàvàhồ ởmôphỏng.',
     'Sốđo vàicon tạo nhóm đểđọc, nhưng phối cảnh khôngphảimặtcắttỷlệchínhxác chứngminhsốlàn.',
     'Chuyển từtỉlệđấttrừutượng đến cáchngườiởđi lại.', 'Về ngõ nhỏ, cứuhỏa và liênvùng.', 'Không nhận phối cảnh lànănglựchiện tại; khôngtự suy công cụdựng3D từmộtvideoexport.')])

add(17, 'Từ ngõnhà tới mạng liênvùng và cầu',
    'Đổi tỉlệ theo ý: ngõtrướcnhà→mạngnội khu→liênvùng→mộtcâycầu. Khi cầnquan hệđịalý phải có bảnđồ, khôngchỉcảnhđường đẹp.', [
    (1020, 1047, 'Mởrộng ngõ, thôngngõcụt và biếnlợiích đẹpđẽ thành antoàn tínhmạng.',
     '17:00 phối cảnhhồ;17:05–17:10 iconđườngvàchữ3–4m lên7–13,5m/ngõcụtthôngtuyến;17:15–17:25 đườngđibộ/đạilộmôphỏng vớimascot.',
     'Chữtrước/sau hỗtrợ sođộrộng; hìnhphốminhhọalợíích, không thấy actualxe cứuhỏađến từnghộ.',
     'Gọi lạistakesantoàn đãnêuphút3, đẩylợiích vượt yếu tốmỹquan.', 'Mởkếtnốiliênvùng.', 'Khônghứaxe chuyên dụngtiếp cậnmọihộchỉtừmặtcắt hayrender; cầnkiểm thiết kếthực.'),
    (1047, 1064, 'Giải thích bốn hướngkếtnốitrục,hànhlangven sông vàchuỗicầu.',
     '17:27–17:35 bảnđồgiao thông có mũitênxanh vàcáctuyếnmàu;17:39.5–17:40 bảnđồcơcấusửdụngđất.',
     'Bảnđồgánh quan hệhướng/tuyến; legendnhỏ ở360p chưa đủđọc mọi tên nếu khôngphóngtừngvùng.',
     'Mở khungrađôthịlớn sau phầnngõnhà đểnâng tầmđềtài.', 'MộtcâucầuCựKhốilàm điểmnhấn.', 'Không xácminh kếhoạchkhởicông/hoànthànhcác cầu/tuyến ngoài nguồn.'),
    (1064, 1080, 'Giới thiệu cầuCựKhối và tácdụngkếtnốirồi mở sanghồ/câyxanh.',
     '17:44–17:55 bảngphối cảnhcầuhoànghôn,mộtnhịplớn,chúthíchvàcácảnhnhỏ;17:57 bắtđầubảnđồtiện íchcôngcộng.',
     'Một tài liệuphối cảnh cụthểphụchọatêncầuvàhìnhdáng; maptrướcđóđãđịnhhướngkhônggian.',
     'Điểmnhấnkiếntrúcđổi hình nhưng vẫn phụcvụmạch kết nối.', 'Côngviên,mặt nước vàlợííchmôi trường.', 'Phối cảnhcầukhông làảnhcầuthựctế; captiontênđơnvịtưvấn có thểsaiASR.')])

add(18, 'Biến vùngtrũng thành hệsinhtháivàthoátnước',
    'Cùngmộtđặctínhcóthểlàđiểmyếuhaynguồnlực. Cần cảbảnđồquan hệ, hìnhtrải nghiệm và sơđồcơchế; hìnhhồđẹpkhôngtựchứngminh hếtnhập.', [
    (1080, 1093, 'Tăngđấtxanh/mặtnướcvàtậndụng hồtựnhiên thayvì sanlấp.',
     '18:00–18:07.5 bảnđồPublicAmenities với hànhlangxanhcôngviên;18:10 hồhiệntrạng có bèo/câynhàvenbờ.',
     'Cho thấy yếu tốhồcósẵn trước khichuyểnsang ýthiếtkế; bảnđồđánh quan hệcôngviênvàsông.',
     'Giảiquyết trực tiếp nhượcđiểmvùngtrũng đãnêuđầubài.', 'Hìnhdung môi trườngsống và ba côngviên.', 'Không lấyviệcnhìnthấyhồ làm xácnhậnthểtíchtích trữhoặckếthoạchkỹthuật.'),
    (1093, 1128, 'Mô tả bacôngviên,dảixanh,khônggiangiađình vàkhoảngđibộ.',
     '18:15–18:22 phố/hồphốicảnh;18:23.5–18:28.5 ngườitậptháicựcquyền venhồ;18:30–18:35 lốiđibộ vàcây;cảnhbốconchơidiều/nhạcnước18:39–18:45.',
     'Tư liệu/môphỏngđều cóhànhđộngnghỉngơi,tập,vui chơikhớploạitiện ích;khôngphảitoànbộ làfootagethậtcủadựán.',
     'Đổi từbảnđồtổngthểsangngườiđượchưởnglợitạocảmgiácmongmuốncuộcsống.', 'Giảithích haichứcnăngkỹthuật.', 'Khungngườitậpthểdụccó thểlàmôphỏng/quảngbá; nguồntừngcảnhchưaxácđịnhđộc lập.'),
    (1128, 1140, 'Tómchứcnăngvi khíhậu/lọcbụi vàhồđiềuhòakết nốicống.',
     '18:50 trênnềnphốicảnhlàiconlọcbụi;18:55 thêmhồchứanướcmưavàmiệngống/nhãnhạtầngngầm.',
     'Thêmđúngđốitượngchohai cơchế,cùngnhau chứkhôngchỉhìnhcôngviênđẹp.',
     'Trảlời nỗikhổquét nướccủanhânvậtđầubài bằngchuỗicơchế.', 'Callbackcáichổi vàhạtầngxãhội.', 'Hìnhminhhọacơchếkhôngthaymôtínhthủyvăn/khảnăngthoátnướcthật.')])

add(19, 'Callback, hạtầngxãhội rồi câu hỏi nhàtôithìsao',
    'Câuchuyệnsẽmấtgần gũinếuchỉdừngởđường/hồ/trường. Dùngmộtcallbackkhépvấnđềcũrồichuyểncâu hỏi sangquyềnlợicủangườisốngởđó.', [
    (1140, 1150, 'Lờigọilạicáichổicủangườiquétnước, nêulợííchthoátnước cóđiềukiện.',
     '19:00 vẫn làbaiconchứcnăngthoátnướctrên nềnmờvớimascot;19:03.5–19:10 quayflycamkhu nhàhiệntại.',
     'Đây làcallbackbằnglờiđến hànhđộngquétở03:32–03:35; mẫu19:00 KHÔNGcho thấyphátlạiclipngườiquét.',
     'Chi tiếtngườithậtgiúpkhớplợííchkỹthuậtvớivấnđềđầubài.', 'Tăngquỹđấthạtầngxãhội.', 'Giữcụmnếumọithứđúngkếhoạch, khôngbiếnthànhcam kếthếtnhập.'),
    (1150, 1179.5, 'Tăngđấthạtầngxãhội,hướngđếntrường,y tế,văn hóa vàdịchvụ.',
     '19:15 số23,88ha→83,68ha;19:20–19:30 flycamcôngtrườngnềnsàn/cầucẩu;19:33.5–19:35 khu nhànhỏ nhìn từcao.',
     'Cặpsốchotăngquỹđất; cảnhcôngtrườngminhhọaxâydựngchưađủnhậndiệnđó làtrườnghaybệnhviệncủadựán.',
     'Từhồvàđườngđếndịchvụngườixemcầnhằngngày.', 'Câuhỏivềconngười vànhàtôithìsao.', 'Tăngdiệntíchđấtkhôngtựchứngminhđủgiáoviên/bácsĩhaychấtlượngvậnhành.'),
    (1179.5, 1200, 'Chiadâncưthànhhaiphần:di dời vàgiữchỗở, nêutáiđịnhcưtạichỗ.',
     '19:39.5 nềntrắngchiađôi;19:45–19:55 số25%/7250hộ/20000người và75%/60000ngườiđược thêm;19:56.5–19:59.5 khu đôthịnhìn từcao.',
     'Haicộttheocùngđơnvịphânbiệtnhómảnhhưởng,rõhơnđámđôngchung. Mẫusốcủahộvàngườiphảighi riêng.',
     'Câuhỏitrựctiếpđếntàisản/giađìnhlàmngườixemcảmnhậnstakessátmình.', 'Nỗisợbịđẩyđixavàlờigiải tạichỗ.', 'Tỷlệ/phươngánlàlờinguồnvềdựthảo,chưalàquyềnđãđượcphêduyệtchotừnghộ.')])

add(20, 'Táiđịnhcưtạichỗ và cách cuốnchiếu',
    'Giảithích thờigian/trìnhtự xâytrước–chuyểnsau bằngảnhcó trạngtháirõ. Mộtlogođơnvịthiếtkếkhôngchứngminhkếhoạchantoànhaykhảnăngthựchiện.', [
    (1200, 1215, 'Nêunỗisợtáiđịnhcưxatrungtâm rồiđốichiếuphươngántạichỗ.',
     '20:00–20:06.5 khu biệtthự/nhàliềnkề nhìn từcao;20:08–20:14.5 côngtrườngđường/cầuvượt.',
     'Hìnhminhhọamôitrườngnhàở/hạtầngkhácnhau, nhưngkhôngthấybảnđồđo độxatrungtâmhayhộdânthựcđượcchuyểntạichỗ.',
     'Lợííchđặtthànhcâutrảlờimộtnỗisợcụthể.', 'Quỹđấttáiđịnhcưvàlờigiảithíchchuyêngia.', 'Khôngdùngkhubiệtthựđẹpđểhứaloạinhà/ngân sách bồithườngcủatừngngười.'),
    (1215, 1240, 'Dẫnchuyêngiaquỹđấttáiđịnhcư/côngcộng,caoốcvàchuẩnhạtầng.',
     '20:15–20:25 nhânvậthoạthọatrongnhà;20:27–20:40 flycamnhà thấpvàhồ.',
     'Nhânvậtđạidiệnchongườidẫnýkiến; hìnhnềnhiệntrạngnhắcđây làcộngđồngđangcó, khôngvẽmỗicâuthànhmộtbảng.',
     'Tăngtrọnglượnglờigiảibằngnguồnchuyêngia,giữgầnhiệntrạng.', 'Nhắcnhàthiếtkếvàtrìnhtựcuốnchiếu.', 'Hoạthọakhônglàphỏngvấn; khôngkiểmđộchuẩncáccon sốhađượclờinêu.'),
    (1240, 1260, 'LogoMVRDVvàýnghĩaxâyxongtrướcrồimớichuyểndânsau.',
     '20:42–20:50 nhânvậtgắnlogoMVRDVtrênflycam;20:55 nềnkhu nhàvẽ2D vàsântrống,chuẩnbịthêmnhânvậtởphútsau.',
     'Logođịnhdanhtưvấn; chuỗihoạthọacộngđồngcóthểgiảithíchtrìnhtự, nhưngmẫuchưaphảitimelinethi côngđãdiễnra.',
     'Dịchthuậtngữcuốnchiếuthànhcuộcsốngítxáotrộn.', 'Trẻconcòntrường/ngườigiàcònlánggiềng.', 'Khôngkếtluậnmôhìnhđãđượcthựchiệnhoặcbảođảmkhôngxáotrộntừmộtphốicảnh.')])

add(21, 'Từ chỗở tới nghềnghiệp',
    'Trảlờiquyềnlợicưtrúxongphải hỏi sinhkế. Cảnhcửa hàng/người làmviệccụthểgiúpngườixemhiểuvìsao mộtcăn hộmớichưađủ.', [
    (1260, 1287, 'Lợííchcuốnchiếuvớitrẻem/ngườigià/cộngđồngvànhómkhôngphảididời.',
     '21:00–21:05 hoạthọabốngười khác lứa;21:10–21:25 trẻ,ngườigiàvàphụnữtrongphốnhàcũvẽ2D.',
     'Giữnhânvậtvàphốquenđểminhhọamốiquanhệcộngđồng, thayvìchỉchophòngkháchmớisangtrọng.',
     'Lợííchđượckểtheonhómngườigiúpnhiềukhángiảtìmthấymình.', 'Nhàởđãcó,cònkiếmsốngthìnào?', 'Khônghứa100%trẻkhôngchuyểntrường/ngườigiàkhôngbịxáotrộnvìchỉlàphươngánnguồnnói.'),
    (1287, 1310, 'Nêurủirokhinghềcũchuyểntừlàngxóm/mặtngõlêncaoốc.',
     '21:27–21:35 nhómngườingồiquánvỉahè;21:38.5–21:45 cửa hàngnhỏ/gánhbán;21:46.5–21:48 phốcóhàngquánvàxemáy.',
     'Thấyhoạtđộngkiếmsống/mặtngõkhớplời, mạnhhơnảnhmộtngườibậnáovestbấtkỳ.',
     'Thêmràngbuộcmớigầnngườixem,giữbàikhôngtrôithànhvideoquảngbáphốicảnh.', 'Dẫnphảnhồicủachínhquyền.', 'Ngườitrongảnhkhôngtựxácnhậnhọthuộcdânsốảnhhưởngcụthểcủadựán.'),
    (1310, 1320, 'Dẫnýkiếnđịaphươngvềtiếpnhậnnguyệnvọng,sinhkế/thươngmại.',
     '21:50–21:57.5 cảnhbànhọpngườithậtvớinhãnNguồnHTV–ĐàiHàNội.',
     'Cónguồntưliệuhọpthậttáchkhỏicáchoạthọachuyêngia;khungđượcchọntheochức năngphảnhồi.',
     'Cho thấyngườicótráchnhiệmđượcđặtcạnhvấnđềthựctế.', 'Nêuphươngánmặtbằngkinhdoanh.', 'Chưanghetrựctiếptừngphátbiểunênkhôngxácnhậntríchdẫnkhớpđủaudio.')])

add(22, 'Hứa về sinhkế rồi tựđặtgiớihạn bảnvẽ',
    'Học thủpháp hãmđàlạcquan sauphầnlợíích. Dùngdanhmụcđầuvàođểgiảithíchlogic, rồi phânbiệtlogicdựkiếnvớikếtquảviệclàmđãcó.', [
    (1320, 1347, 'Nêuphươngánưu tiênkhônggianthươngmạimới cho ngườibáncũ.',
     '22:00 cảnhhọp;22:05–22:15 ngườibánrauvẽ2D trướcphố;22:17–22:26 ngõcóxe,biểnshop/ngườibánthực.',
     'Giữđúngchủthểngườibánvàđịađiểmbuônbántronglờinhưnghìnhhoạthọakhônglàbằngchứngđiềukiệngiáthuê/sởhữu.',
     'Trảđúngnỗilosinhkếvừamở, chưakếtnội dungngay.', 'Mởcơcấudịchvụvàdukhách.', 'Cácchi phíưuđãilàphươngánđượcnguồnnêu,chưaxácnhậnápdụngchonhàcụthể.'),
    (1347, 1366.5, 'Tổhợpcôngviên,metro,khách vànhucầutiêudùngđượckểnhưnguồn lựcviệclàm.',
     '22:30icon3côngviên18,5ha;22:35thêm4tuyếnmetro/dukhách;22:40–22:45thêmgiỏhàngnhucầutiêudùng.',
     'Bốnđầuvàocủalogicxuấthiệntừngbước,cùngnềnlưới. Hìnhkhôngđođượclượngkháchhaydoanhthutươnglai.',
     'Ngườixemnhìnđượcvìsaonguồnđềxuấtsựchuyểnnghềcóthểhoạtđộng.', 'Chuyểnphảnđề:đâyvẫnchỉlàlờihứabảnvẽ.', 'Khônglấyiconlogicđểkhẳngđịnhdòngtiền/việclàmthựcđãsẵnsàng.'),
    (1366.5, 1380, 'Nhắcbảnvẽkhôngtựxâyđược,vốn lớn vàdânđangsốnglàbàitoánthựcthi.',
     '22:46.5–22:50 bảndựthảoquyhoạchchitiếtvớimascot;22:55 số447ha,186000tỷ,80000ngườiquanhnềnplanlàmmờ.',
     'Trảvềgiấytờthựccủadựthảorồinhấnbathamsốgiớihạn;ẩn dụphẫuthuậtcơthểsốngởlờikhôngbịvẽthànhcảnhgâynhiễu.',
     'Đảogiọngtừhấpdẫnsangcầnđiềukiện, tạocâuhỏigiữđếnphầncuối.', 'Bađiềukiệnbắtbuộcởphút23.', 'Giấydựthảolàchứngcứđồánđangtồntại,khôngphảibằngchứngđãđượcduyệttoànbộ.')])

add(23, 'Điềukiện1: hạtầng; điềukiện2: vốn vàphốihợp',
    'Một videođềxuấtthuyếtphụcphải cókịchbảnthấtbạivàđiềukiệnngănnó. Dùngmũitênlên/xuốngvàtrìnhtựđểthấyquan hệ, khôngchỉđọclạiphầnlợíích.', [
    (1380, 1391.5, 'Khóthựcthi,nângthànhbađiềukiệnquyếtđịnh.',
     '23:00–23:10 thẻ447ha/186000tỷ/80000ngườiquanhmascot, giữnềnplan.',
     'Giữbaconsốnhắcquymôvàtháchthức, khôngthaybằngảnhcôngtrườngkhôngliênquan.',
     'Nhấnnợlờigiảibằngbathửtháchtrước khiđưacáclờikiếnnghị.', 'Thẻđiềukiện1.', ''),
    (1391.5, 1420, 'Hạtầngtrướchoặccùngnhàở; trìnhbàynguycơnhàlêntrướcvàđường/trườngchậm.',
     '23:11.5tiêuđềđiềukiện1;23:15–23:20iconcaoốc mũitênlên,đườngvàtrườngmũitênxuống;23:25icongiao thôngtắc;23:30–23:35iconvănbảnvàcâugiámsát.',
     'Quan hệnhàtăng, tiệníchchậmlà trạngtháinhìnthấyđượcquađồhọa. Văn bảniconchỉminhhọacam kết,khôngphảiscantài liệuchứngminh.',
     'Dùngkịchbảnxấurõđểngườixemhiểuvìsaophảiđòitiếnđộ.', 'Vốntưnhâncầnnănglựcvàkhớpcông.', 'Khôngkiểmnghiệmnănglựcthi côngtừđồhọa/camlờinguồn.'),
    (1420, 1440, 'Vốn tưnhânphảikhớpvốncông; nêunănglựcquảntrịvàphụthuộchạtầngngoàiranh.',
     '23:40tiềnvà186000tỷ;23:45thêmví/gear;23:50nhânvậtgắnlogoSunGroup;23:55mascotnềntrắngchuẩnbịbốnảnhhạtầng.',
     'LogođịnhdanhnhàđầutưkhônglàCTA/sponsorriêng;iconví/gearbiểudiễntàichínhvàquảntrị.',
     'Tựđặtđiềukiệnchologiclợííchtrướcđó,giảmviệctinrằngcứvốnlớnlàđủ.', 'Bốnhạngmụckết nốivàđiềukiệnminhbạch.', 'Khôngkhẳngđịnhcó/khôngcótàitrợchỉtừlogo; chỉghinhậnkhôngpháthiệnđoạnquảngbáriêngtrongcaption.')])

add(24, 'Điềukiện3: minhbạch vàđồngthuận cóhànhđộngthật',
    'Thayvìnóiminhbạchbằngiconbắttay, chothấyniêmyếtbảnvẽ,ngườixem,quétQRvàđốithoại. Đồngthờinêutrạngtháidựthảovàđiềuchưachốt.', [
    (1440, 1449, 'Khépphốihợpcông–tưqua các trụchạtầngngoàiranhrồi thẻđiềukiện3.',
     '24:05bốnảnhnhỏgắnnhãntrụcsông,cầuCựKhối,QL1A,metro;24:06.5chữĐiềukiện3minhbạch/đồngthuận.',
     'Nhómhạngmụcngoàidựánchotínhphụthuộckhônggian, rồiđổi nềnđểtáchđiềukiệnquảntrị.',
     'Từđủtiền/đủđườngsangcâu hỏiaiđượcbiếtvàđượcgópý.', 'Phạmvipháplýchưahoànthành.', 'Ảnhphốicảnhhạtầngkhôngchứngminhngânsáchcônghoặctiếnđộđãchốt.'),
    (1449, 1472, 'Nêudựthảođanglấyýkiến,chưaquyếtđịnhcuốitừngthửa/giáđền bù; côngkhaihồsơvàQR.',
     '24:09–24:25 ngườiđứngtrướcbảngghiỦYBANNHÂNDÂNPHƯỜNGVĨNHHƯNG/hồsơniêmyết;24:30haiđiệnthoạichĩavàomãQRvới nhãnđườngdẫntàiliệu.',
     'Chủthểđọc/quét,đồvậtbảnvẽ/điệnthoại,trạngtháiniêmyếtđúngýlời. Đây làvídụkhớphànhđộngđặcbiệtrõcủanguồn.',
     'Quyềnlợidânđượctrảbằngquytrìnhcóthểnhìnthấy, khôngchỉlờihứatrừutượng.', 'Đốithoạivàcácýkiếngópý.', 'Khôngtríchluật/giáđền bùtừphân tíchnày;khôngscanQRđểhứanội dunghiệnnayvẫnnhưnguồn.'),
    (1472, 1493.5, 'Nêugópý/đốithoạivàthờigianlấyýkiến,rồitómbabađiềukiện.',
     '24:35ngườingồibàntraođổi;24:40–24:45biểnthờigianniêmyếtghi12/10/2026→01/11/2026;24:50mascottrướcthẻlàmmờ.',
     'Biểnngàythậthỗtrợmốcthờigian;ngườigópýthấyđượchoạtđộngnhưngkhôngđếmđược300ýkiến.',
     'Khépnợbađiềukiệnthựcthitrướckếtbài,mỗinhánhcómộtbằngchứngthịgiác.', 'MởrộngtừmộtphườngsangtầmnhìnHàNội.', 'Giữngàytheonguồn, khôngnóilàthờihạncònhiệulựcởngàyngườixemđọc.'),
    (1493.5, 1500, 'Đặtdựántạithiếttrongtầmnhìnthủđôdàihạn.',
     '24:53.5–24:59.5 flycamcầuvượt/đôthịvàtháp.',
     'Mởrộngtỉlệkhônggianchonộidungkếtvĩmô.',
     'Trảýnghĩalớnhơnsaukhigiải cácnỗilođờisống.', 'Mục tiêuhạnhphúc/thu nhậpvàCTA.', 'Tầmnhìn/dựbáokhôngphảikếtquảđãcó.')])

add(25, 'Tầmnhìnlớn, mờiýkiến vàđăngký',
    'CTA nênkhớpkiểubài: đềtàichínhsáchmờibìnhluậnquanđiểm,tráchnhiệmhơnlàbiếnlờikếtthànhquảngcáobấtđộngsản. Trảxongcâuhỏi/tranhluậnrồimờitheodõi.', [
    (1500, 1511.5, 'Nêuđịnhhướnghạnhphúc/thu nhậpvàvai tròVĩnhHưngtrongtầmnhìnlớn.',
     '25:00–25:03flycamkhu nhà;25:05icontrái tim/top10;25:10thêmví/thu nhậpvớimascottrênnềnthànhphốmờ.',
     'Chữ/biểutượngtómmụctiêutươnglaichứkhôngminhhọasốđothựctế. Nhắc lại vịtrí chiếnsượccủa hook.',
     'Kếtbằnghìnhdungquymôlớnsaunhữngđiềukiệncụthể.', 'Mờingườixemnêuquanđiểm.', 'Khônglấymụctiêutop10/100000USDlàmthànhtựuđạthoặclờihứachắcchắn.'),
    (1511.5, 1515, 'Mờiđểlạiýkiếnvềdựán.',
     '25:12.5đổisangnềnlướiđenvàmascot;25:15mascotbênthẻkênh.',
     'Đổinềnđánh dấuCTA; lờimờibìnhluậnđúngchủđềchứkhônggiaobàitậpngoàiphạmvi.',
     'Mởkhônggiannhậnxétchokhángiảsauphầnlậpluận.', 'Đăngkývàlờichào.', ''),
    (1515, 1524, 'Xưngtên,nhắcđăngký,chàohẹngặplại vàđuôinhận diện.',
     '25:15–25:21.5thẻkênhLóngvớinútlike/subscribe/bell,mascotcửđộng;đuôicònđến25:24theometadata.',
     'Hìnhhànhđộngđăngkýkhớplờikêu gọi; khôngcầntómtoànbộ25phútlần nữa.',
     'DùngmộtCTAđơn giảnđểkhép,saukhitrảlờicâuhỏitiêuđề.', 'Kếtvideo.', 'Chưanghetrựctiếpđểchấmcáchngắtnghỉ/mixâmthanhoutro.')])

D['blocks'] = BLOCKS
D['schema_version'] = 'reference-study-v1'
D['id'] = D['videoId']
D['duration'] = D['durationSeconds']
D['inspection'].update({
    'status': 'complete_sampled_timeline_analysis',
    'method': 'Nghiên cứu nối tiếp: đọc toàn bộ801dòngcaption; lượt trước mở63trang/610frame, giữ nguyên8blockđầu; lượt tiếp đọc lại toàncaption và mở lại toàn bộ42trang từ08:00đếnkết. Tổng hồsơphủ26khoảngliêntiếp0–1524s.',
    'reviewedSheetCount': 63, 'sampledFrameCount': 610,
    'reviewedSheets': [s for b in STUDY for s in b['sheets']],
    'samplingLimit': '5-second cadence plus frame-change candidates from 2 fps extraction. Candidate changes often reflect moving flycam, not edit cuts. No claim to detect every shot or continuously watch/listen.'})
D['structure'] = [
    {'start': 0, 'end': 43, 'role': 'Vịtrígiátrịcaođốilậphiệntrạng, nêustakesvàlờihứagiảithích'},
    {'start': 43, 'end': 51.5, 'role': 'Lưuýtổnghợpnguồnvàgócnhìncánhân,mờiđínhchính'},
    {'start': 51.5, 'end': 300, 'role': 'Nềnlịchsử/địachất→bốnđiểmnghẽn'},
    {'start': 300, 'end': 407, 'role': 'Dựthảo/sốtrước-sau→nghịchlýcầnlờigiải'},
    {'start': 407, 'end': 683, 'role': 'Đôthịnén,quốctế,đanxen,nguồntàichính'},
    {'start': 683, 'end': 864, 'role': 'Nhàđôngcầnđilại→TOD,cơchếkếtnốivàvốn'},
    {'start': 864, 'end': 974, 'role': 'Nhu cầuhằngngàycầnởgần→đôthị15phút'},
    {'start': 974, 'end': 1179.5, 'role': 'Tươnglaicóđiềukiện:đường,hồ,hạtầngxãhội'},
    {'start': 1179.5, 'end': 1366.5, 'role': 'Nhàtôithìsao→táiđịnhcư→cộngđồng→sinhkế'},
    {'start': 1366.5, 'end': 1493.5, 'role': 'Bảnvẽchưatựthànhthực→bađiềukiệnthựcthi'},
    {'start': 1493.5, 'end': 1511.5, 'role': 'Gócnhìnthủđôvàtầmnhìnlớn'},
    {'start': 1511.5, 'end': 1524, 'role': 'Commentquanđiểm+đăngký+chào'}]
D['audience'] = {
    'status': 'inference_from_content_not_channel_analytics',
    'likelyViewers': ['NgườiViệtquantâmđôthị/đờisốngHàNộinhưngkhôngchuyênquyhoạch',
                      'Ngườisốnghoặcđilàm/đihọcquakhuvực,gắnloantoàn,ngập,kẹtxe,nhàở',
                      'Khángiảmuốnhiểudựánvànhữngđánhđổiquyềnlợidân,khôngchỉxemphốicảnh'],
    'observableBasis': 'Xưnghôanh em; hỏiđilàmgiờcaođiểm,đưaconđihọc,nhàtôithìsao; giải thíchhộpgiấy,giảichữTOD; dànhphầnriêngchosinhkế/di dời.',
    'notKnown': 'Khôngcóanalyticsđểkhẳngđịnhtuổi,giới,tỷlệcưdân,CTR/retentionhaythànhphầnngườixemthật.'}
D['angle'] = {
    'observedFraming': 'Lậpluậnủnghộsựcầnthiếttáicấutrúctừkhókhănđờisốngvàquan hệgiữabamôhình; lợííchđượcđặtcạnhcácràngbuộcthựcthi vàquyềnlợidân.',
    'emotionalStakesInference': 'Vịtríhứa hẹnđốilậpchấtlượngsống; mấtthờigian/an toàntạocấp thiết; viễncảnhxanh/tiện íchgợimongmuốn; nỗisợdidờivàmấtsinhkếđượctrảlời; bađiềukiệngiữlờihứacógiớihạn.',
    'commercialRelationship': 'Khôngnhậndiệnđoạnsponsor/CTA thươngmạiriêngtrongtoàncaptionvàmẫuhình. ViệcnêuSunGroup/logokhôngđủkếtluậncóhaykhôngcóquan hệtàitrợ.'}
D['semantic_beats'] = [{**beat, 'blockIndex': b['index'], 'timingPrecision': 'Approximate caption/sample boundary; notframeaccurate'} for b in BLOCKS for beat in b['beats']]
D['caveats'] = [
    'Mọisốliệu/quyhoạch/pháplý/dựbáođượcmôtảnhưlậpluậncủavideonguồn,chưaxácminhđộc lập.',
    'Caption2016khácchữ2026ở12:00;caption442ha/186.896nghìncóthểlỗiASR. Khôngsửathầmlặngrawcaption.',
    'Ẩndụhộpgiấynóimười nhưnghình5hộpđượclượttrướcđánh dấu;khớpnghĩachưakhớpmọicon số.',
    'Phốicảnhtươnglaikhôngphảihìnhhiệntrạnghoặcđãhoànthành; nhiềucảnhchỉminhhọabốicảnh.',
    'Khôngđánhgiáchấtlượnggiọng/nhạc/SFXhaykhẳngđịnhngheliêntục;tríchnguồnhọpcónhãnnhưngchưangheđốichiếutừngphátbiểu.',
    'Khôngtáigiớithiệuphươngánthu hồi/đền bùlàtưvấnchongườidân;cầnnguồnpháplýhiệnhànhchobàiviếtmới.',
    'Mộtcảnhflycamcóthểsinhra nhiềuứngviênthayđổiởbộlấyframe;khôngđếm610frame là610cảnhcắt.']

# Proofread mechanically joined Vietnamese syllables in authored continuation notes.
# Original caption files remain untouched. The word inventory is local source text.
word_inventory = Counter()
for transcript in P.parent.parent.glob('**/transcript.json'):
    for row in json.loads(transcript.read_text(encoding='utf-8')):
        word_inventory.update(w.lower() for w in re.findall(r'[^\W\d_]+', row['text']))
for word in ('ASR CTA TOD MVRDV BRT HTV QL Tokyo Roppongi Hills Shanghai Hồng Kông Moreno '
             'compact city value capture Sun Group icon icons mascot render renders '
             'footage flycam frame frames caption raw callback logo logos mix audio '
             'video metadata transcript card dashboard email template baseline gallery '
             'EDL frame accurate source QR scan top').split():
    word_inventory[word.lower()] += 20
for word in ('mâu thuẫn lũy thẩm mĩ đính phỏng ngắt mượt hãm lạc ốc lệ bản tiểu hô '
             'xưng ưu đuôi vẽ góp lỗi bồi thường xứ nêu quỹ lấp kín công năng '
             'phẫu thuật cơ thể sượng trữ nguyện vọng chỉn chu rà soát tham số '
             'nội ngoại thông số huyền thoại cổ nhuận diện chĩa chóp đỉnh nhịp '
             'nhánh khép nợ cổng đón khổ quét lũy ảnh lòi vết rạn '
             'Public Amenities VTC News Eiffel stakes timeline export vest outfit '
             'outro like subscribe bell caption rawASR legend plan sponsor gear '
             'gây nhiễu nhược trũng diều chiến lược bảng khóa gán tựu huynh xâu map HĐND QĐ UBND').split():
    word_inventory[word.lower()] += 20
word_inventory.update(w.lower() for w in re.findall(r'[^\W\d_]+', (P / 'script-pattern.md').read_text(encoding='utf-8')))


@lru_cache(None)
def split_joined(token):
    if token.lower() in word_inventory or not any(ord(c) > 127 for c in token):
        return token
    n = len(token)
    best = [None] * (n + 1)
    best[n] = (0, [])
    for i in range(n - 1, -1, -1):
        # Unknown character remains visible rather than being silently removed.
        score, tail = best[i + 1]
        candidates = [(score + 25, [token[i]] + tail)]
        for j in range(i + 1, min(n, i + 12) + 1):
            bit = token[i:j]
            if bit.lower() in word_inventory:
                score, tail = best[j]
                # One syllable/token costs1, with longer recognized tokens favored.
                candidates.append((score + 1, [bit] + tail))
        best[i] = min(candidates, key=lambda item: item[0])
    score, bits = best[0]
    if any(bit.lower() not in word_inventory for bit in bits):
        return token
    return ' '.join(bits)


def proofread(value):
    if isinstance(value, dict):
        return {key: proofread(item) for key, item in value.items()}
    if isinstance(value, list):
        return [proofread(item) for item in value]
    if isinstance(value, str):
        if not any(ord(c) > 127 for c in value):
            return value
        for before, after in {
            'm âu': 'mâu', 'lũ y': 'lũy', 'bản g': 'bảng', 'Khó a': 'Khóa',
            'g án': 'gán', 'x âu': 'xâu', 'tự u': 'tựu', 'phụ huy n h': 'phụ huynh',
            'NQ-H Đ N D': 'NQ-HĐND', 'g e a r': 'gear', 'chiếnsượccủa': 'chiến lược của',
            'cảnhbốconchơidiều': 'cảnh bố con chơi diều',
            'dụphẫuthuậtcơthểsốngởlờikhôngbịvẽthànhcảnhgâynhiễu': 'dụ phẫu thuật cơ thể sống ở lời không bị vẽ thành cảnh gây nhiễu',
            'nhượcđiểmvùngtrũng': 'nhược điểm vùng trũng',
            'quanhga': 'quanh ga', 'cù nghệ': 'cùng hệ', 'bố cụcvôcớ': 'bố cục vô cớ',
            'cùnghệ': 'cùng hệ',
            'actualxe': 'xe thực tế', 'm ap': 'bản đồ', 'phục họa': 'phụ họa',
            'hết nhập': 'hết ngập', 'vé xăng': 'tiền xăng', 'tóm ba ba': 'tóm ba',
            'dự án tại thiết': 'dự án tái thiết', 'Valuecapture': 'Value capture',
        }.items():
            value = value.replace(before, after)
        value = value.replace('lợíích', 'lợi ích').replace('Lợíích', 'Lợi ích').replace('antoàn', 'an toàn').replace('stakessátmình', 'stakes sát mình')
        value = re.sub(r'[^\W\d_]+', lambda match: split_joined(match.group()), value)
        value = re.sub(r'(?<=\d)(?=[A-Za-zÀ-ỹ])|(?<=[A-Za-zÀ-ỹ])(?=\d)', ' ', value)
        value = re.sub(r',(?=[^\s\d])', ', ', value)
        value = re.sub(r';(?=\S)', '; ', value)
        value = re.sub(r':(?=[^\s\d/*])', ': ', value)
        value = re.sub(r'%(?=[^\s\d])', '% ', value)
        value = value.replace('→', ' → ')
        value = re.sub(r' {2,}', ' ', value)
        # Keep filenames, IDs and technical terms exactly intact after spacing pass.
        for before, after in [('1 OGwWLvasIk','1OGwWLvasIk'),('analysis. json','analysis.json'),
                              ('2 D','2D'),('3 D','3D'),('1 OGwWLv as Ik','1OGwWLvasIk'),
                              ('360 p','360p'),('QL 1 A','QL1A')]:
            value = value.replace(before, after)
        return value
    return value


D = proofread(D)
BLOCKS = D['blocks']

assert len(BLOCKS) == 26
assert all(b['start'] == i * 60 and b['end'] == min((i + 1) * 60, 1524) for i, b in enumerate(BLOCKS))
for b in BLOCKS:
    assert b['beats'][0]['start'] == b['start'], b['index']
    assert b['beats'][-1]['end'] == b['end'], b['index']
    assert all(a['end'] == z['start'] for a, z in zip(b['beats'], b['beats'][1:])), b['index']
(P / 'analysis.json').write_text(json.dumps(D, ensure_ascii=False, indent=2), encoding='utf-8')


def stamp(seconds):
    return f'{int(seconds)//60:02}:{seconds%60:04.1f}'


lines = [
    '# Học toàn tuyến: Tại sao dự án tái thiết đô thị Vĩnh Hưng lại cần thiết?',
    '', '[Video nguồn — Lóng](https://www.youtube.com/watch?v=1OGwWLvasIk) · 25:24 · 26 khoảng liên tiếp · 63 trang hình / 610 frame chọn mẫu.',
    '', '## Phạm vi kiểm tra thực tế', '',
    'Đã đọc toàn bộ801dòngcaption. Hồ sơ nối tiếp giữ8khối đầu của lượt trước và bổ sung18khối còn lại; lượt trước báo đã mở đủ63trang, lượt tiếp mở lại toàn bộ42trang từ08:00đếnkết. Khung hình theo nhịp5giây cộng ứng viên thayđổi ảnh từluồng2fps. Toàn timeline được đối chiếu, không bỏkhoảng phút nào.',
    '', '**Giới hạn:** đây là phân tích toàn caption + toàn contact sheet đã chọn, không phải xác nhận xem/nghe liên tục25:24. Chưa chấm giọng, nhạc, SFX bằng tai; không đo mọi cut nhỏ. Cảnhflycam di chuyển có thể tạo nhiều mẫu;610frame không phải610cảnh. Các mốc beat là ước lượng, không phải EDL frame-accurate.',
    '', 'Nghiên cứu cáchkể, không xác nhận các phát biểu quyhoạch, pháp lý, tài chính, dự báo hay ngày/số liệu của nguồn. Caption tự động được giữ nguyên để còn đối chiếu lỗi; nhãnnguồn trênhình chưa thay việc kiểm tài liệu gốc.',
    '', '## Góc khai thác và người xem hướng tới', '',
    '**Góc kể quan sát được:** '+D['angle']['observedFraming'],
    '', '**Suy luận đối tượng:** '+D['audience']['observableBasis']+' Từ đó suy luận ngườixem là khán giả phổthông quan tâm đôthị/đờisốngHàNội và quyềnlợi người ở trong khu vực. Không có dữ liệu để khẳng định tuổi, giới, CTR hay retention thật.',
    '', '**Đường cảm xúc — suy luận biên tập:** '+D['angle']['emotionalStakesInference'],
    '', '## Cấu trúc lớn', '',
    '| Mốc | Vai trò |', '|---|---|']
for x in D['structure']:
    lines.append(f"| {stamp(x['start'])}–{stamp(x['end'])} | {x['role']} |")
lines += ['', 'Hook khoảng0–43s; disclaimer có lời nói rõ khoảng43–51,5s; nội dung chính đến khoảng1511,5s; CTA cuối gồm mời ý kiến về dự án rồi đăng ký. Không phát hiện đoạn sponsor/CTA thương mại riêng, nhưng không có căn cứ kết luận về quan hệ tài trợ của kênh.', '', '## Ghi theo từng đoạn', '']
for b in BLOCKS:
    title = b.get('title', b['beats'][0]['scriptFunction'])
    lines += [f"### {stamp(b['start'])}–{stamp(b['end'])} — {title}", '',
              'Trang đã kiểm: '+', '.join(f'[{s}]({s})' for s in b['reviewedSheets'])+'.', '']
    for beat in b['beats']:
        lines += [f"**{stamp(beat['start'])}–{stamp(beat['end'])}: {beat['scriptFunction']}**", '',
                  '- Hình nhìn thấy: '+beat['visibleEvidence'],
                  '- Cách giảng / lời–hình: '+beat.get('visualWordRelationship', beat['teaching']),
                  '- Giữ chú ý (suy luận): '+beat['attentionInference'],
                  '- Chuyển ý: '+beat['transition']]
        if beat.get('limit'):
            lines.append('- Giới hạn: '+beat['limit'])
        lines.append('')
    lines += ['**Bài học dùng lại:** '+b['reusableLesson'], '']
lines += ['## Các lỗi / giới hạn không được học theo', '']
lines.extend('- '+c for c in D['caveats'])
lines += ['', '## Áp dụng vào hướng hiện tại', '',
          'Giữ baseline ảnh/gallery3D cũ và giọng NhậtPhong/âmthanh đã chốt theo yêu cầu người dùng. Học cách đặt vấn đề, nối ba mô hình và chọn tư liệu theo hành động cụ thể; không tự thay toàn giao diện thành mascot2D hoặc bảng/dashboard nhiều chữ. Nguồn là case study để rút logic kể, không phải bộ tài sản được phép sao chép.',
          '', 'Trước video mới, mỗi mệnh đề cần bảng lời→chủ thể/hành động/đồ vật/trạng thái cần thấy→tư liệu có nguồn→hình đó chứng minh đến đâu→bố cục→mốc vào/ra theo take thật. Mục tiêu tiếp theo là hình đúng ý trong giao diện đang giữ, không đơn thuần nhiều hình hơn.']
(P / 'analysis.md').write_text(proofread('\n'.join(lines)).replace(': **', ':** ')+'\n', encoding='utf-8')
print({'blocks': len(BLOCKS), 'beats': len(D['semantic_beats']), 'sheets': 63, 'frames': 610})
