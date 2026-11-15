"""Human-authored, proofread reference analysis. Preserve raw acquisition files."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
data = json.loads((root / 'analysis.json').read_text(encoding='utf-8'))
study = json.loads((root / 'study-blocks.json').read_text(encoding='utf-8'))
notes = []


def note(title, script, visual, relation, retention, lesson, caveat):
    notes.append((title, script, visual, relation, retention, lesson, caveat))


note('Hook: ba câu hỏi, disclaimer ngắn và định nghĩa bằng hành vi',
     '00:00–00:13 liên hệ Labubu, đồ hype và các video trước; có lời đùa về người trong cộng đồng. 00:13–00:29 đặt nghịch lý vật liệu rẻ nhưng giao dịch đắt. 00:29–00:39 hứa giải thích giá trị, sức hút và độ bền. 00:39.48–00:46.92 nói rõ tổng hợp nhiều nguồn và mời đính chính. Từ khoảng 00:47 bắt đầu định nghĩa TCG.',
     '00:02.5 có hai thumbnail cũ; 00:08.5–00:13 là nhóm người trong cửa hàng thẻ. 00:15–00:39.5 có cận thẻ, tủ trưng bày và hội chợ. 00:40/00:45 chuyển sang mascot ghi chép/laptop trên nền tím. 00:51.5 hiện tên TRADING CARD GAME và bản dịch trên tư liệu thẻ.',
     'Thẻ và thao tác cầm/xem có ngay khi giới thiệu vật phẩm. Disclaimer có không gian hình riêng; phần định nghĩa chỉ thêm thuật ngữ ngắn.',
     'Nghịch lý tạo khoảng trống cần giải thích; ba lời hứa mở ba tuyến sẽ được gọi lại. Đây là suy luận cấu trúc, không phải retention đã đo.',
     'Hook cần mâu thuẫn cụ thể và lời hứa có thể trả được; định nghĩa bằng điều người ta làm với vật đó.',
     'Giá và tên riêng trong caption chưa được kiểm chứng. Không biến lời đùa thành cáo buộc; không lấy thumbnail hoặc mascot làm tài sản cho video mới.')

note('Định nghĩa → cơ chế tạo giá trị → cửa ngõ thương mại',
     '01:00–01:08 giải thích mở gói, xếp bộ, đấu bài. 01:08–01:28 tách chi phí vật liệu khỏi giá trị cộng đồng công nhận; nhà phát hành tạo luật, truyện, nhân vật và độ hiếm. 01:28–01:42 mở rộng thành ngành sản xuất, kiểm định, mua bán và đầu tư. 01:42–02:00 đặt giả định mở shop, đơn tăng khiến quản lý phức tạp.',
     '01:00–01:05 có người lựa thẻ; 01:08–01:15 mặt sau Pokémon và hai nhân vật đồng ý. 01:16.5–01:25 thêm tòa nhà cùng icon luật/truyện/nhân vật/độ hiếm. 01:30–01:41.5 trở lại hội chợ. 01:43–01:55 là cửa hàng minh họa, nhân vật sau quầy chuyển sang ôm đầu.',
     'Công ty được biểu tượng hóa khi lời nói chuyển sang quyền thiết kế hệ thống. Quầy minh họa là tình huống giả định cho cầu nối tài trợ, không phải bằng chứng về một shop thật.',
     'Tuyến ý tăng cấp có lý do: trò chơi → ngành kinh doanh → bài toán vận hành.',
     'Định nghĩa xong phải chỉ ra ai tạo quy tắc và giá trị. Cầu nối sponsor cần xuất phát từ một vấn đề liên quan đến chủ đề.',
     'Icon không chứng minh tài liệu thật. Không suy ra phần mềm dựng từ các layer phẳng.')

note('Sponsor: vấn đề → demo thao tác → lợi ích → CTA → quay lại bài',
     '02:00–02:29 giới thiệu Odoo và kết nối TikTok Shop, chuyển đơn và cập nhật tồn. 02:29–02:36 chốt lợi ích giảm sao chép thủ công. 02:36.56–02:41.32 mời dùng thử, báo quay lại thẻ bài. 02:41–02:53 mở ba động lực tâm lý, tài sản, tuổi thơ; cuối phút bắt đầu cảm giác mở gói.',
     '02:00 có logo và nhãn tài trợ. 02:05 là trang đơn/quotation, 02:10 trang shop đồng bộ, 02:20 bảng inventory; 02:23.5–02:25 có TikTok Seller Center. 02:30–02:35 người thao tác trên máy bán hàng; 02:37/02:40 thẻ chữ và logo. 02:42 trở về tủ thẻ; 02:53–02:55 nhân vật cầm hộp trong phòng.',
     'Lời nói về đơn/tồn đi với UI thật, cụ thể hơn logo đứng yên. Hình thẻ xuất hiện lại khi quay về nội dung chính.',
     'Nhãn tài trợ và câu quay lại giúp nhận biết nhánh thương mại. CTA giữa bài khác chức năng CTA đăng ký cuối video.',
     'Chỉ dùng UI khi chính câu nói bàn về thao tác trên UI; không kéo dashboard sang mọi đoạn giải thích.',
     'UI mẫu chưa chứng minh tất cả claim quảng cáo. Không tái dùng ưu đãi hoặc link của tài trợ; tài trợ không đồng nghĩa disclaimer nguồn.')

note('Tâm lý mở gói, hiệu ứng sở hữu và địa vị',
     '03:00–03:08 nói cảm xúc khi mở được thẻ hiếm. 03:08–03:22 viện dẫn tâm lý sưu tầm, đồ khó kiếm và hiệu ứng sở hữu. 03:22–03:46 dùng ví dụ thẻ cầu thủ trong bim bim để nói địa vị. 03:46–04:00 mở động cơ mua như tài sản, gắn với áp lực nhà ở và lương.',
     '03:00–03:05 nhân vật cầm hộp rồi thẻ, biểu cảm thay đổi. 03:08–03:10 là bàn giấy có biểu đồ; sau đó trở lại người cầm và chọn thẻ. 03:33–03:45 nhân vật cầm gói Poca rồi thẻ cầu thủ, hai người khác giơ ngón cái. 03:50 có hai nhân vật; 03:55 thêm ngôi nhà.',
     'Ví dụ Poca được diễn thành quan hệ dễ nhìn: có món đồ → được chú ý. Bàn biểu đồ chỉ gợi bối cảnh nghiên cứu, chưa hiển thị một nghiên cứu cụ thể.',
     'Ký ức quen thuộc của người Việt làm cầu nối cho khái niệm trừu tượng. Câu hỏi về tài sản mở tuyến mới.',
     'Mỗi cơ chế trừu tượng cần một tình huống gần gũi có hành động và phản ứng nhìn thấy được.',
     'Không coi câu dopamine hoặc động cơ thế hệ là kết luận khoa học đã kiểm chứng. Không gán mọi người mua bài vào động cơ khoe của.')

note('Tài sản nhỏ hơn, giai thoại lợi nhuận và caveat ngay tại chỗ',
     '04:00–04:12 nói tài sản lớn khó tiếp cận. 04:12–04:31 chuyển sang đồ sưu tập, giao dịch mạng và theo dõi giá. 04:31–04:41 kể người quen giữ hộp sealed rồi bán lời. 04:41–04:57 ngắt đà hào hứng: không mua theo giai thoại, có rủi ro và khó thanh khoản. Cuối phút mở tuổi thơ.',
     '04:00–04:10 mascot trước nền ngôi nhà bị làm mờ. 04:15–04:26.5 có hội chợ và thẻ gắn giá. 04:30 là điện thoại với đồ thị; 04:31.5–04:35 nhân vật cầm hộp Pokémon trong phòng. 04:38–04:55 mascot nói trước nền phòng mờ.',
     'Tem giá/đồ thị phục vụ ý mua bán. Hộp chỉ thể hiện trạng thái giữ kín, không chứng minh lợi nhuận trong giai thoại.',
     'Giai thoại tạo gần gũi; caveat ngay sau đó giữ lời kể khỏi thành lời mời mua. Nền thưa giúp tập trung vào lời dẫn.',
     'Câu chuyện lời cao phải có điều kiện và rủi ro ngay cạnh; không đẩy hết giới hạn xuống cuối bài.',
     'Chưa xác minh giai thoại hoặc tính chống lạm phát. Phần này phân tích cách kể, không hướng dẫn đầu tư.')

note('Hoài niệm phân nhóm người mua; chuyển sang đầu cơ',
     '05:00–05:18 nói người từng chơi lúc nhỏ nay có thu nhập để mua lại ký ức; Goku là ví dụ sở thích. 05:18–05:32 gom ba nhóm: chơi, sưu tầm, kiếm tiền. 05:32–06:00 phân biệt đầu tư và đầu cơ ngắn hạn, yếu tố thích rủi ro, rồi gom thành thị trường lớn.',
     '05:00–05:10 có giao dịch và tủ thẻ cũ. 05:11.5–05:18 là mô hình Goku trong phòng với mascot. 05:30 trao đổi thẻ; 05:35 tay cầm ba lá. 05:36.5 là quầy CGC; 05:40–05:55 có chụp thẻ, giấy nhận và thao tác tại quầy PSA.',
     'Goku khớp ví dụ vừa được nhắc. Giao nhận và chấm điểm cho thấy hệ sinh thái vượt khỏi việc mở pack.',
     'Ba động cơ tạo tầng bậc, không quy giá vào một lý do. Câu gom ý chuẩn bị đổi từ cá nhân sang ngành.',
     'Phân nhóm bằng mục đích sử dụng; với mỗi nhóm cần hành vi phù hợp, không chỉ đổi nền.',
     'Người trong tư liệu giao dịch không mặc nhiên là nhà đầu cơ. Không xác nhận ảnh mô hình thuộc sở hữu người kể.')

note('Quy mô ngành và bất đồng cách đo',
     '06:00–06:15 nói các tổ chức đưa số khác nhau. 06:15–06:29 giải thích khác biệt phạm vi: thẻ thật, số, doanh số phát hành hoặc mua bán lại. 06:29–07:00 đối chiếu ba bộ ước tính và dự báo, thay vì chốt một số duy nhất.',
     '06:04–06:10 có laptop, biểu đồ và tiền. 06:15–06:28.5 là thẻ và người cầm slab. 06:30 hiện Dataintelo; 06:35 thêm Mordor Intelligence; 06:40 thêm Custom Market Insights. Số cơ sở màu trắng, số dự báo màu vàng và tỷ lệ xanh bổ sung ở 06:50–06:55.',
     'Sự khác biệt dữ liệu trở thành đối tượng so sánh. Bố cục ổn định để tích lũy thông tin; logo không thay báo cáo gốc.',
     'Trước khi khoe quy mô, nguồn giải thích vì sao các số lệch nhau. Nhịp chậm hơn montage để đọc.',
     'Dữ liệu cần phạm vi trước số. Phải hiện năm cơ sở và năm đích, nhất là khi các dự báo khác chân trời.',
     'Chưa xác minh báo cáo, số liệu hoặc phương pháp gộp. Stock tài chính không phải chứng cứ; dự báo không phải kết quả đã xảy ra.')

note('Ước tính thấp hơn, thẻ vật lý/số và cảm giác sở hữu',
     '07:00–07:24 đưa hai ước tính thấp hơn rồi chỉ gom hướng dự báo. 07:24–07:43 hỏi tiền mua gì: thẻ vật lý và số. 07:43–07:53 dùng ví dụ đĩa game/PS5 giải thích nhu cầu cầm nắm, trưng bày. Cuối phút mở nhóm người mua.',
     '07:02–07:25 là hai cột TechSci Research/Business Research Insights. 07:29–07:35 cặp icon thẻ và điện thoại cùng tỷ lệ. 07:40–07:50 quay về phòng/nhân vật, có bong bóng suy nghĩ. 07:53–07:55 bắt đầu nền giấy trắng chia cột.',
     'Không chỉ giữ nguồn có số cao nhất. Cặp vật thể thật/số khớp lời; căn phòng đưa bài trở lại trải nghiệm sau chuỗi logo.',
     'Câu hỏi mới đổi từ tổng lượng sang cấu trúc. Giữ bảng lâu để đọc có thể là lựa chọn có ích.',
     'Sau số tổng có thể lần lượt hỏi mua gì, ai chi, ở đâu, ai kiểm soát; không dồn mọi phân chia lên một màn hình.',
     'Caption có cụm dự báo khó hiểu “10 chục tỷ”; hình 07:10 hiện 12,86 tỷ. Giữ raw ASR và kiểm nguồn/audio trước tái dùng, không sửa âm thầm.')

note('Ai mua, mua để làm gì, thị trường ở đâu và ai giữ IP',
     '08:00–08:15 đối chiếu người trưởng thành cất giữ/chấm điểm với người trẻ chơi/cộng đồng/đấu giải. 08:15–08:47 chuyển sang các vùng thị trường. 08:47–09:00 đưa quyền lực về một số công ty nắm IP.',
     '08:00–08:10 hai nhân vật, bullet từng cột thêm dần. 08:15–08:25 là địa cầu/nhãn châu Á–Thái Bình Dương; 08:35–08:40 thêm Bắc Mỹ; 08:45 thêm châu Âu. 08:50–08:55 là tòa nhà biểu tượng và logo The Pokémon Company.',
     'Mục đích của hai nhóm nằm đúng hai cột. Địa cầu phân biệt phạm vi; tòa nhà đổi cấp từ vùng thị trường sang công ty.',
     'Các câu hỏi nối theo chuỗi giá trị giúp dữ liệu không rời rạc. Người xem có thời gian đọc trước khi thêm ý.',
     'Dùng một hình thức cho một quan hệ; chỉ đổi layout khi câu hỏi đổi loại.',
     'Tỷ lệ người mua trong nội dung không phải nhân khẩu học khán giả. Không suy công cụ 3D từ hình địa cầu đã render.')

note('Nhà phát hành, IP và callback nghịch lý khan hiếm',
     '09:00–09:13 dùng Pokémon làm ví dụ sản lượng/doanh thu/thị phần. 09:13–09:39 nói Bandai và liên kết giải trí–thẻ. 09:39–09:51 nhắc đã biết ai mua/bán, nhưng vì sao in hàng tỷ vẫn có lá cực hiếm? 09:51–10:00 bắt đầu phân tầng độ hiếm.',
     '09:00–09:10 có logo Pokémon và bullet. 09:15–09:30 có Bandai, One Piece, Dragon Ball và số. 09:34–09:35 poster Netflix cạnh thẻ nhân vật. 09:40–09:45 album/máy in; 09:48–09:53 là thẻ/album; 09:55–09:58.5 có dây chuyền.',
     'Nhân vật phim gắn trực tiếp thẻ tương ứng. Tới câu in hàng tỷ, hình đổi sang máy và album. Máy chưa rõ nguồn chỉ là minh họa sản xuất.',
     'Đây là callback rõ tới hook sau nhánh số liệu dài: gói điều đã biết rồi mở điều còn thiếu.',
     'Bài dài cần điểm kiểm: đã trả câu nào, còn câu nào. Mỗi chỉ số phải giữ đúng phạm vi.',
     'Lời phân biệt mảng hàng hóa One Piece với riêng TCG; logo CARD GAME cạnh số rộng hơn có thể làm người xem hiểu sai. Không dùng ảnh này để nhập các phạm vi thành một.')

note('Độ hiếm, thị trường bán lại và bước sang card grading',
     '10:00–10:12 đối chiếu thẻ thường/đặc biệt và tỷ lệ mở. 10:12–10:27 giải thích cung cầu. 10:27–10:47 nói hiếm chưa đủ, giới thiệu grading và công ty kiểm định. 10:47–11:00 mở bốn tiêu chí.',
     '10:00–10:10 có máy, thẻ ánh kim và máy in DLICAN. 10:12.5 là eBay, 10:15 TCGplayer, 10:18.5–10:20 Goldin; 10:23.5–10:30 thêm listing. 10:33.5 hiện CARD GRADING; 10:35–10:43 có kính lúp, màn phóng đại và người thao tác. 10:50–10:55 một lá thẻ với callout góc/cạnh.',
     'Listing cho thấy hoạt động thị trường, chưa chứng minh giá chốt. Kính lúp và callout cùng vật đang được giải thích.',
     'Câu “hiếm chưa đủ” mở tầng mới: tình trạng và chứng nhận làm cùng một lá khác giá.',
     'Quy trình phải có đối tượng, thao tác, đầu ra; không chỉ ảnh thị trường. Phân biệt giá rao, giá đấu và giao dịch hoàn tất.',
     'Không xác nhận máy DLICAN là dây chuyền nhà phát hành đang kể. Các quy trình kiểm định cần kiểm riêng theo từng công ty.')

note('Bốn điểm kiểm tra → slab/nhãn → chênh lệch giá',
     '11:00–11:07 hoàn tất góc/cạnh/bề mặt/căn giữa. 11:07–11:28 giải thích điểm và hộp có nhãn; chưa bóc không chắc điểm hoàn hảo. 11:28–11:41 nguồn nêu một số lợi nhuận. 11:41–11:50 liên hệ trò TCG Simulator; cuối phút hỏi lá vừa hiếm vừa điểm cao đắt thế nào.',
     '11:00–11:05 bốn mũi tên quanh Charizard, đọc được tại native 0665.png. 11:10 là slab; 11:15 chỉ vùng nhãn; 11:35–11:40 thêm 18,3%. 11:45–11:48 có gameplay với điểm/giá. 11:49–11:51.5 có kiểm tra dưới đèn và đặt hộp vào máy.',
     'Giữ một lá làm neo để tiêu chí bám đúng vùng. Hình chỉ định vị, chưa cho thấy một vết xước hay độ lệch thật.',
     'Gameplay tạo nhịp nghỉ rồi câu hỏi giá kỷ lục nâng tò mò. Không nhầm sức hấp dẫn với lời mời đầu cơ.',
     'Nói lỗi thì cần ảnh lỗi thật; nói điểm thì cần đúng nhãn. Ghi gameplay là game, không là giao dịch thật.',
     '18,3% là claim quá khứ chưa xác minh tập mẫu, không là lời hứa. Hộp/chứng nhận không được mô tả như bảo đảm tuyệt đối.')

note('Mini-case: nguồn gốc → độ hiếm/điểm → người mua/giá',
     '12:00–12:27 kể Pikachu Illustrator, xuất xứ giải thưởng và giao dịch nổi tiếng. 12:27–12:46 kể The One Ring, bản độc nhất/người mở/người mua. 12:46–12:53 nói dùng lá đại diện để giữ lá thật. Cuối phút mở Black Lotus.',
     '12:00 cận Illustrator; 12:04–12:10 tạp chí Nhật; 12:15–12:20 slab PSA 10 cạnh Logan Paul/cert và giá; 12:25 là PSA 9. 12:30–12:35 có The Lord of the Rings/sự kiện/thẻ; 12:38–12:45 ảnh người và slab kèm giá. 12:50 bàn Magic; 12:53.5–12:55 Black Lotus.',
     'Giá gắn đúng vật và mức điểm; tạp chí giúp kể nguồn gốc. Ảnh liên quan chưa tự chứng minh điều khoản giao dịch.',
     'Các câu chuyện là phần trả thưởng cho hook, có lý do khan hiếm chứ không chỉ con số lớn.',
     'Ví dụ giá cao cần tên, phiên bản, điểm, thời điểm, loại giao dịch và nguồn; không thay bằng vật gần giống.',
     'Tên/niên đại ASR có thể sai. Giá kỷ lục không phải định giá hiện hành hoặc kết quả đại diện của người sưu tập.')

note('Tiền lớn dẫn sang rủi ro giả mạo thẻ, nhãn và hộp',
     '13:00–13:10 khép Black Lotus bằng giá nguồn nêu. 13:10–13:19 hứa ba vấn đề rủi ro. 13:19–13:29 mở thẻ/hộp/chứng nhận giả. 13:29–13:49 giải thích vì sao chỉ tra mã chưa đủ; cuối phút mở dấu hiệu kiểm tra.',
     '13:02.5–13:09.5 có ảnh kỷ lục CGC Pristine 10. 13:20–13:25 là slab. 13:30 cặp REAL/FAKE; 13:32.5–13:40 nhãn phóng đại/vòng đỏ. 13:41.5–13:45 ghép thẻ Pokémon với màn ví dụ nhãn LeBron. 13:46.5–13:50 là mép hộp và mũi tên; 13:55 callout UV.',
     'Chi tiết được phóng đúng vùng cần nhìn. Hình xác minh ở 13:45 là các đối tượng khác nhau, không phải ca khớp duy nhất.',
     'Sau giá cao, mặt trái phát triển từ chính cơ chế chứng nhận và giá; không phải cảnh tiêu cực ngẫu nhiên.',
     'So sánh phải đủ gần, đủ lớn, cùng đối tượng. Hình ghép khác nguồn phải được trình bày như minh họa.',
     'Không gán người trong footage hội chợ là kẻ lừa đảo. Các dấu hiệu xác thực chưa được nghiên cứu này chứng nhận đủ cho mọi đời hộp.')

note('Cách nhìn hộp, box break và FOMO',
     '14:00–14:13 tiếp tục UV, đường hàn và hologram theo nguồn. 14:13–14:37 định nghĩa box break bằng cơ chế trả tiền/chờ kết quả. 14:37–14:45 nhắc tranh chấp theo lời nguồn. 14:45–15:00 nói FOMO và lặp mua quá mức.',
     '14:00–14:10 một slab ở nền lưới, các nhãn kiểm tra thêm dần. 14:15–14:20 hộp và chữ BOX BREAKS. 14:25 người xem điện thoại; 14:30 màn livestream/listing slot; 14:35 mở gói ở bàn. 14:40 logo Whatnot/Fanatics Live trên nền giấy/búa; 14:50–14:55 màn điện thoại và nhân vật.',
     'Livestream/slot khớp mô hình lựa chọn đang kể. UV mới là callout chữ trên ảnh, chưa thấy thao tác chiếu và phản ứng vật liệu. Búa là ký hiệu pháp lý, không là hồ sơ vụ kiện.',
     'Từ giả vật phẩm chuyển sang rủi ro cách bán, vẫn giữ cùng hệ thống. Nhân vật trở lại khi lời nói về tâm lý.',
     'Phép thử vật lý cần thao tác và kết quả thật. Claim pháp lý phải giữ trạng thái và nguồn, không dùng biểu tượng để tăng vẻ chắc chắn.',
     'Không xác nhận vụ kiện, phân loại cờ bạc hoặc hiệu lực các dấu hiệu xác thực. Đây không phải tư vấn kiểm định hay pháp lý.')

note('Ôm hàng và callback chu kỳ thẻ thể thao',
     '15:00–15:06 khép FOMO. 15:06–15:27 nói gom hàng/bot và giá bán lại khiến người muốn chơi khó mua. 15:27–15:39 hỏi vòng mua đắt rồi bán đắt hơn còn bền không. 15:39–16:00 kể Junk Wax để giải thích cung vượt cầu.',
     '15:05–15:10 hàng hộp; 15:15 danh sách sản phẩm/giao dịch; 15:20 kệ trống; 15:21.5–15:25 trang giá/đồ thị tiếng Nhật. 15:30–15:36.5 tư liệu trẻ em chơi/đổi thẻ. 15:40–15:50 album bóng chày; 15:53 hiện JUNK WAX; 15:55 hộp Topps và thẻ.',
     'Hình đổi đúng loại thẻ khi chuyển lịch sử thể thao. Kệ trống cho thấy trạng thái thiếu hàng, chưa chứng minh do bot/gom hàng.',
     'Câu hỏi độ bền xuất hiện sau rủi ro giá; callback trả lời lời hứa thứ ba thay vì mở đề mới ở cuối.',
     'So sánh chu kỳ bằng cơ chế giống/khác. Kệ trống và chart cần nguồn/ngày nếu dùng như bằng chứng.',
     'Chưa kiểm chứng lịch sử Junk Wax hay nguyên nhân mọi biến động giá. Listing chỉ là ảnh chụp được nguồn sử dụng.')

note('Phản biện hai nấc: khan hiếm chưa đủ, còn nhu cầu sử dụng',
     '16:00–16:23 so TCG với thẻ thể thao qua kiểm soát in và grading. 16:23–16:37 tự phản biện: thời trang hype cũng giới hạn nhưng có thể mất giá. 16:37–17:00 đưa khác biệt là người chơi thật, luật, giải đấu và cộng đồng.',
     '16:03–16:08.5 dây chuyền đóng gói; 16:10–16:13.5 thẻ ánh kim; 16:19 tay cầm thẻ. 16:28–16:30 hàng người trước Supreme. 16:34–16:35 listing áo/đường đỏ giảm. 16:38–16:40 người chơi Magic; 16:45–16:50 bàn thi đấu có số; 16:55 xếp thẻ vào album.',
     'Phản ví dụ thời trang có đúng vật thể. Khi nói nhu cầu chơi, quay về hành động chơi và giải đấu, không cần icon trang trí.',
     'Đưa lý do → thừa nhận phản ví dụ tốt → bổ sung cơ chế phân biệt. Lập luận tiến triển thay vì lặp lớn hơn.',
     'Giữ phản biện mạnh trong kịch bản rồi giải quyết bằng quan hệ nhìn thấy. Không mặc định mọi vật giới hạn đều bền giá.',
     'Nguồn suy luận độ bền ngành, không chứng minh giá từng lá an toàn. Không xác nhận danh tính mọi người hoặc tên giải từ mẫu hình.')

note('Kết luận có điều kiện, giữ rủi ro giá rồi CTA ngắn',
     '17:00–17:11 nói IP/ký ức lâu năm tạo sức bền khác trend ngắn. 17:11–17:24 giữ giới hạn: nhu cầu bền không đồng nghĩa giá luôn giữ; có thể bán tháo lấy tiền mặt. 17:24.76 mời bình luận; 17:26.32 xưng tên; 17:27.64–17:29.92 mời đăng ký/chào, đệm hình đến 17:32.',
     '17:00 người sắp thẻ; 17:01.5–17:07 cảnh Pokémon animation. 17:10 hội chợ; 17:12.5–17:16.5 lựa thẻ trong hộp; 17:20–17:24 giao dịch. 17:25 chuyển nền lưới; 17:30 mascot và UI đăng ký Lóng, rõ ở native 1050.png.',
     'Nhân vật truyện khớp hoài niệm; giao dịch trở lại khi cảnh báo giá. CTA có UI hành động tương ứng.',
     'Trả lời đủ lời hứa và chừa giới hạn để thảo luận. CTA đến sau kết luận, không cắt câu chốt.',
     'Phân biệt giá trị sử dụng với biến động giá; kết bằng luận điểm chứ không chỉ số tiền kỷ lục. Giữ nguyên câu nói cuối.',
     'Không biến kết luận nguồn thành bảo đảm ngành không thể sụp đổ hay đầu tư an toàn. Chưa nghe để chấm giọng, nhạc, SFX hoặc cảm xúc của mix.')

labels = [('script_function','Lời và chức năng'),('visible_evidence','Hình quan sát được'),
          ('visual_word_relationship','Quan hệ lời–hình'),('retention_inference','Giữ chú ý — suy luận'),
          ('reusable_lesson','Bài học dùng lại'),('limits_or_corrections','Giới hạn/điểm cần sửa')]
blocks = []
for ix, values in enumerate(notes):
    block = {'index':ix,'start':study[ix]['start'],'end':study[ix]['end'],'title':values[0],
             'sheets':study[ix]['sheets'],'frame_times':[x['time'] for x in study[ix]['frames']]}
    block.update({key:value for (key,_),value in zip(labels,values[1:])})
    block['notes_markdown'] = '\n\n'.join('**'+label+':** '+block[key] for key,label in labels)
    blocks.append(block)

beat_meanings = [
 'Liên hệ các trào lưu và video trước với cộng đồng quen thuộc',
 'Đặt nghịch lý bìa rẻ nhưng giao dịch đắt',
 'Hứa giải thích giá trị, sức hút và độ bền',
 'Tổng hợp nhiều nguồn, mời sửa sai',
 'Định nghĩa TCG qua mua, mở, xếp bộ và đấu',
 'Vật liệu khác giá trị cộng đồng; nhà phát hành tạo hệ thống',
 'Từ trò chơi sang ngành kinh doanh',
 'Giả định mở shop và quản lý đơn, tồn kho',
 'Demo Odoo/TikTok Shop theo lời quảng bá',
 'Nhiều gian hàng và giảm sao chép thủ công',
 'CTA dùng thử, báo quay lại nội dung',
 'Mở bản đồ tâm lý, tài sản và ký ức',
 'Chờ đợi, mở gói và cảm xúc có thẻ hiếm',
 'Đồ khó kiếm và hiệu ứng sở hữu',
 'Địa vị cộng đồng và ví dụ thẻ trong Poca',
 'Áp lực nhà ở và tài sản nhỏ hơn',
 'Thương hiệu quen, giao dịch và theo dõi giá',
 'Giai thoại hộp sealed bán lời',
 'Không mua theo giai thoại; rủi ro thanh khoản',
 'Tuổi thơ, thu nhập hiện tại và sản phẩm hoài niệm',
 'Ba mục đích: chơi, sưu tầm, kiếm tiền',
 'Đầu cơ ngắn hạn và động cơ thích rủi ro',
 'Quy mô lớn nhưng dự báo khác nhau',
 'Phạm vi thẻ thật, số và mua bán lại khác nhau',
 'Ba bộ ước tính và dự báo cao hơn',
 'Hai nguồn ước tính thấp hơn',
 'Gom xu hướng rồi hỏi tiền mua gì',
 'Thẻ giấy, số và ví dụ sở hữu đĩa game',
 'Người lớn và người trẻ dùng thẻ khác nhau',
 'Các vùng châu Á–Thái Bình Dương, Bắc Mỹ, châu Âu',
 'Pokémon và quyền kiểm soát IP, sản lượng',
 'Bandai và liên kết IP giải trí với thẻ',
 'Callback: đã biết ai mua/bán, vì sao vẫn có thẻ hiếm?',
 'Phân tầng thẻ thường, đặc biệt và tỷ lệ mở',
 'Cung cầu trên thị trường bán lại',
 'Hiếm chưa đủ: tình trạng và chứng nhận',
 'Bốn tiêu chí góc, cạnh, bề mặt, căn giữa',
 'Điểm và hộp có nhãn',
 'Chênh lệch giá và claim lợi nhuận của nguồn',
 'Liên hệ game, điểm thấp và cao',
 'Hiếm cùng điểm cao có thể đắt thế nào?',
 'Pikachu: xuất xứ giải thưởng, điểm và giao dịch',
 'The One Ring: bản độc nhất và người mua',
 'Lá đại diện để chơi, giữ lá thật',
 'Black Lotus: lịch sử, ngừng in, điểm và giá',
 'Tiền lớn dẫn sang ba vấn đề rủi ro',
 'Giả mạo hoặc can thiệp thẻ, nhãn và hộp',
 'Nguồn nêu UV, viền hộp và hologram',
 'Box break: trả tiền chờ kết quả ngẫu nhiên',
 'Nhắc tranh chấp theo nguồn, chưa xác minh',
 'FOMO, lặp mua và chi tiêu quá mức',
 'Gom hàng, giá bán lại và người muốn chơi',
 'Callback câu hỏi độ bền so với trào lưu trước',
 'Junk Wax: thẻ thể thao và cung vượt cầu',
 'Kiểm soát in và tầng khan hiếm do grading',
 'Phản ví dụ thời trang giới hạn vẫn mất giá',
 'Nhu cầu chơi, luật và giải đấu',
 'IP và ký ức lâu năm tạo sức bền',
 'Sức bền ngành không bảo đảm giá thẻ',
 'Bình luận, đăng ký và lời chào']
assert len(beat_meanings) == len(data['semantic_beats']) == 60
for beat, meaning in zip(data['semantic_beats'],beat_meanings):
    beat['meaning'] = meaning

data['blocks'] = blocks
data['method'] = {
    'complete_caption_read':True,'caption_rows':595,
    'reviewed_sheets':sum((x['sheets'] for x in study),[]),'selected_frame_count':408,
    'native_detail_frames':[str(p.relative_to(root)).replace('\\','/') for p in sorted((root/'inspection').glob('*.png'))],
    'continuous_av_playback':False,'auditory_evaluation':False,
    'coverage':'18 khoảng thời gian liên tiếp đến 1052 giây; đã mở lại đủ 43 trang và 8 khung native trong lượt tiếp tục.',
    'boundary_precision':'Mốc ý xấp xỉ từ caption ASR và hình chọn mẫu, không phải EDL chính xác theo frame.',
    'limits':'Lấy mẫu hình không chứng minh đã xem/nghe liên tục, mọi cut nhanh, nguồn/quyền ảnh hoặc chất lượng giọng/nhạc/SFX. Decode chỉ là kiểm tra kỹ thuật.'}
data['angle'] = 'Nghịch lý vật liệu rẻ/giá đắt → động lực mua → hệ sinh thái thị trường → khan hiếm và grading → kỷ lục → mặt trái → so sánh chu kỳ và kết luận có điều kiện.'
data['audience_inference'] = {
    'status':'inference_not_analytics',
    'primary':'Người Việt tò mò về văn hóa tiêu dùng/giải trí và muốn hiểu giá trị xã hội, chưa cần biết luật TCG.',
    'secondary':'Người biết Pokémon, One Piece hoặc sưu tầm; họ có thêm chi tiết grading, giao dịch, rủi ro và chu kỳ.',
    'grounds':['Định nghĩa TCG từ 47–68 giây.','Cầu nối Poca, PS5 và Goku.','Phân biệt mục đích chơi, sưu tầm, đầu tư và giữ caveat rủi ro.'],
    'not_established':'Không có analytics về tuổi, giới, thu nhập, CTR, retention hoặc ý định tác giả. Nhóm được bàn đến trong nội dung không đồng nghĩa nhóm khán giả đã đo.'}
data['reusable_principles'] = [
    'Lời hứa ở hook được gọi lại và trả lời trong thân bài, phần kết.',
    'Tư liệu thật đúng vật và hành động; sơ đồ khi cần quan hệ trừu tượng.',
    'Phạm vi dữ liệu đi trước số; giữ năm, đơn vị và loại giao dịch.',
    'Một đối tượng làm neo khi thêm callout; cho đủ thời gian đọc.',
    'Caveat ngay cạnh giai thoại lợi nhuận; độ bền ngành không bảo đảm giá.',
    'Đưa phản ví dụ tốt rồi giải thích khác biệt về nhu cầu sử dụng.',
    'Không sao chép mascot, câu văn, ảnh, thumbnail hoặc âm thanh của kênh.']
data['production_scope'] = 'Nghiên cứu và lưu bài học; giữ giao diện ảnh/gallery 3D cũ, giọng Nhật Phong và hướng âm thanh đã duyệt. Không tạo video mới trong nhiệm vụ này.'

intro = '''# Phân tích toàn timeline — Vì sao 1 thẻ bài TCG lại đắt giá đến thế?

Nguồn: [Lóng — gNznfzAUiLw](https://www.youtube.com/watch?v=gNznfzAUiLw), thời lượng **17:32**. Đây là nghiên cứu cách kể, kịch bản và chọn hình, không xác nhận claim khoa học, tài chính, pháp lý hoặc quảng cáo trong nguồn.

## Phạm vi đã kiểm tra

Đã đọc đủ **595 dòng caption**, đối chiếu đủ **43 trang / 408 khung hình chọn mẫu** và **8 khung native 640×360**, phủ **18 khoảng liên tiếp** từ đầu đến hết. Trong lượt tiếp tục đã tự mở lại toàn bộ các trang này. Bản tải có video và audio; receipt ghi full decode A/V không báo lỗi.

Đây là phân tích toàn timeline qua transcript và hình chọn mẫu, **không phải xác nhận xem/nghe liên tục**. Không đủ để chấm giọng, nhạc, SFX hoặc mọi cut dưới nửa giây. Mốc ý là xấp xỉ từ ASR; raw caption được giữ nguyên, lỗi chỉ được ghi nhận riêng. Decode thành công không chứng minh thẩm mỹ hoặc độ đúng của nội dung.

## Góc khai thác và người xem hướng tới

Góc kể: chi phí vật liệu không giải thích được giá trị xã hội; muốn hiểu giá phải lần theo người mua, quyền kiểm soát IP, độ hiếm, chứng nhận và nhu cầu sử dụng. Nguồn đặt câu hỏi văn hóa/kinh tế, không chỉ trình bày một danh sách lá đắt tiền.

Người xem chính được **suy luận** là người Việt tò mò chuyện tiêu dùng/giải trí, chưa cần hiểu TCG. Người đã biết Pokémon/One Piece hoặc sưu tầm nhận thêm lớp grading, ví dụ giao dịch và rủi ro. Căn cứ là phần định nghĩa từ đầu và các cầu nối Poca, PS5, Goku. Không có analytics để kết luận tuổi, giới, thu nhập hoặc retention. Không lấy nhóm Gen Z được nói trong bài làm nhân khẩu học khán giả đã đo.

Đường cảm xúc được diễn giải: ngạc nhiên → nhận ra ký ức/hành vi quen → hiểu cơ chế → thấy mặt trái → cân nhắc kết luận. Đây không phải xác nhận ý định tác giả.

## Bản đồ kịch bản

- **00:00–00:39:** hook nghịch lý và ba lời hứa.
- **00:39–00:47:** disclaimer tổng hợp nguồn, mời đính chính.
- **00:47–01:42:** định nghĩa và hệ sinh thái kinh doanh.
- **01:42–02:41:** nhánh sponsor Odoo: vấn đề, demo, lợi ích, CTA, quay lại bài.
- **02:41–05:59:** tâm lý, sở hữu/địa vị, tài sản/rủi ro, hoài niệm, đầu cơ.
- **05:59–09:40:** quy mô/phạm vi đo, tiền mua gì, ai mua, ở đâu, ai giữ IP.
- **09:40–11:50:** callback nghịch lý, khan hiếm và grading.
- **11:50–13:10:** mini-case các lá nổi bật, nguồn gốc/điểm/giá.
- **13:10–15:28:** hàng giả, box break/FOMO và ôm hàng.
- **15:28–17:24:** trả lời về độ bền bằng so sánh và phản biện, giữ rủi ro giá.
- **17:24–17:32:** bình luận, đăng ký và chào.

Tài trợ là nhánh tùy chọn. Disclaimer, caveat rủi ro, tài trợ và CTA có chức năng khác nhau; không ép chúng thành một bước duy nhất.
'''

def stamp(t):
    return f'{int(t)//60:02}:{int(t)%60:02}'

sections=[]
for b in blocks:
    sections.append(f"## {stamp(b['start'])}–{stamp(b['end'])} — {b['title']}\n\n"+
                    b['notes_markdown']+'\n\n**Trang hình:** '+
                    ', '.join('['+Path(s).name+']('+s+')' for s in b['sheets']))
outro = '''
## Các điểm cần cải thiện khi áp dụng

1. Tư liệu đúng chủ thể và hành động quan trọng hơn nhiều ảnh. Cảnh hội chợ không chứng minh người trong hình đang đầu cơ; máy in chưa rõ nguồn không chứng minh nhà phát hành cụ thể.
2. Callout trên một lá thẻ chỉ định vị tiêu chí. Khi nói xước/lệch hoặc một phép thử, cần chính ảnh lỗi hoặc thao tác và kết quả nhìn thấy được.
3. Dữ liệu phải hiện năm, đơn vị và phạm vi. Không trộn toàn bộ mảng hàng hóa IP với riêng TCG, hoặc giá rao với giá chốt.
4. Giữ bảng đủ lâu để đọc. Không rút bài học thành phải đổi ảnh mỗi hai giây hoặc biến cả video thành dashboard.
5. Kiểm ASR với tên riêng, đơn vị và lời đùa. Không cắt caveat để chỉ lấy giai thoại lời cao.
6. Giữ cả hai vế khi kết luận: nhu cầu chơi có thể tạo sức bền, giá thị trường vẫn có thể giảm. Không chuyển thành bảo đảm đầu tư.

## Phần chưa được xác lập

Không có bằng chứng về công cụ dựng, thư viện 3D, nguồn/quyền sử dụng của mọi ảnh, CTR/retention, nhân khẩu học hoặc ý định cá nhân của tác giả. Không chấm giọng/nhạc/SFX khi chưa nghe. Địa cầu hoặc layer trong hình không chứng minh một kỹ thuật render cụ thể.

Không sao chép mascot, câu văn, tư liệu hoặc âm thanh của kênh làm tài sản đầu ra. Giao diện ảnh/gallery 3D cũ, giọng Nhật Phong và hướng âm thanh đã duyệt vẫn là ràng buộc riêng của dự án. Hồ sơ này học mạch ý và chọn hình, không cho phép tự đổi UI hoặc tạo video mới.
'''
(root/'analysis.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'analysis.md').write_text(intro+'\n\n'+'\n\n'.join(sections)+outro,encoding='utf-8')

pattern = '''# Cách viết rút ra từ video TCG của Lóng

Tham chiếu: [gNznfzAUiLw](https://www.youtube.com/watch?v=gNznfzAUiLw). Đọc `analysis.md` để xem bằng chứng theo toàn timeline và giới hạn kiểm tra. Đây là diễn giải phương pháp, không phải bản script để chép, không phải xác nhận ý định tác giả hay đào tạo trọng số mô hình.

## Góc tiếp cận người xem

Mở bằng thứ có vẻ vô lý: vật liệu rẻ nhưng giá trị trao đổi lớn. Dẫn tò mò bằng những câu hỏi cụ thể: ai muốn nó, họ trả tiền cho điều gì, ai tạo quy tắc, điều gì khiến giá trị còn tồn tại? Cảm xúc đi từ ngạc nhiên đến hiểu cơ chế rồi cân nhắc mặt trái. Hiệu quả thực tế chưa được đo.

Hai cửa vào cùng bài: người ngoài cộng đồng cần định nghĩa dễ; người trong cộng đồng cần chi tiết đúng vật, đúng thao tác và ví dụ sâu. Không mặc định nhắc Gen Z là đã xác định được khán giả thật của kênh.

## Khung cho một chủ đề nguyên bản

1. **Mâu thuẫn nhìn thấy được:** một vật/tình huống tưởng chỉ có giá trị thông thường nhưng lại có hệ quả bất ngờ có nguồn. Đưa đúng vật lên hình trước khi giải thích dài.
2. **Lời hứa rõ:** chọn các câu hỏi đáng trả lời về giá trị, sức hút hoặc độ bền. Không cần đúng ba câu cho mọi chủ đề; đã hứa thì phải trả đủ.
3. **Disclaimer ngắn:** nêu phạm vi nguồn và giới hạn thực sự, mời đính chính nếu cần. Không biến nó thành đoạn mở dài lặp lại.
4. **Định nghĩa bằng động từ:** người ta mua, mở, dùng, trao đổi thế nào? Ai tạo quy tắc? Phải hiểu cách sử dụng trước khi giải thích giá.
5. **Động cơ người mua:** từ cảm giác, sở hữu/địa vị đến tài sản và ký ức. Mỗi cơ chế cần một tình huống đời sống khớp hình; không gán tất cả người mua cùng động cơ.
6. **Đổi cấp độ sang hệ sinh thái:** tiền mua gì, ai chi, ở đâu, ai phát hành hoặc kiểm soát? Định nghĩa phạm vi trước số liệu; giữ các ước tính khác nhau khi chúng đo khác nhau.
7. **Callback câu hỏi còn thiếu:** gói điều đã biết trong một câu rồi mở nghịch lý chưa giải được. Đây là bước đi sâu, không phải lặp hook trống.
8. **Giải thích quy trình bằng vật thể:** bộ phận → thứ được kiểm → thao tác → đầu ra → hệ quả. Callout phải bám đúng vùng đang nói.
9. **Mini-case có lý do:** nguồn gốc → đặc tính khác biệt → phiên bản/chứng nhận → hệ quả. Không chỉ tên và con số lớn.
10. **Mặt trái phát triển từ cơ chế:** chứng nhận có giá trị thì có nguy cơ giả mạo; ngẫu nhiên có sức hút thì có FOMO; giá tăng có thể dẫn đầu cơ. Không chèn cảnh báo rời rạc.
11. **Phản biện hai nấc:** đưa lý do → nêu phản ví dụ tốt → giải thích cơ chế phân biệt. Đừng chọn một ví dụ dễ đánh rồi tuyên bố thắng.
12. **Trả lời có điều kiện, sau đó CTA:** sức bền không đồng nghĩa bảo đảm giá. Chốt đúng lời hứa, rồi mời một hành động cụ thể. Sponsor là nhánh riêng nếu cần, có cầu nối, demo, CTA thương mại và câu quay lại bài.

## Chọn hình và nhịp dựng

| Mệnh đề lời nói | Hình cần chuẩn bị | Điều phải kiểm |
|---|---|---|
| Vật và thao tác | Ảnh/footage đúng vật, cầm/mở/dùng/trao đổi | Chính hành động đó có trong pixel, không chỉ cùng chủ đề |
| Cơ chế trừu tượng | Tình huống 2D hoặc sơ đồ ngắn | Thêm từng quan hệ; không giả thành chứng cứ về người thật |
| So sánh dữ liệu | Layout ổn định, nguồn/năm/phạm vi/đơn vị | Đủ thời gian đọc, không trộn các loại chỉ số |
| Bộ phận/lỗi/phép thử | Cận vật, so sánh hoặc thao tác thật | Mũi tên đúng vùng; nói xước phải thấy xước |
| Case cụ thể | Đúng vật/phiên bản/người/sự kiện | Phân biệt tư liệu và minh họa, giá rao và giá chốt |
| Phản biện/caveat | Bố cục thưa, một kết luận chính | Giữ câu giới hạn nguyên vẹn, không che bằng hiệu ứng |

Không áp quy tắc đổi hình mỗi hai giây. Montage có thể nhanh; so sánh hoặc quy trình cần giữ một điểm neo đủ lâu. Đổi layout khi câu hỏi đổi loại. Canh theo take thật đã chốt và kiểm render; không suy cut chính xác từ ASR.

## Áp dụng cho dự án hiện tại

Giữ giao diện ảnh/gallery 3D cũ. Học mạch ý và quan hệ lời–hình, không tự thay bằng mascot/flat 2D hoặc bảng email/dashboard. Chỉ dùng 3D để tổ chức không gian hay quan hệ có ích; nó không thay tư liệu. Giữ giọng Nhật Phong và hướng âm thanh đã duyệt; hồ sơ chưa nghe âm thanh không đủ để phê duyệt giọng/mix khác.

Trước video mới, lập bảng: mệnh đề → điều cần thấy → tư liệu → nguồn/quyền sử dụng → phạm vi chứng minh được → layout → điểm vào/ra theo lời thật. Thiếu hình thì tìm thêm hoặc sửa câu; không lấp bằng ảnh bất kỳ và hiệu ứng. Lưu cả điểm chưa tốt của mẫu: sai phạm vi chỉ số, stock thay nghiên cứu, callout phép thử không có thao tác thật và hình ghép chứng nhận khác đối tượng.
'''
(root/'script-pattern.md').write_text(pattern,encoding='utf-8')
assert len(blocks)==18
assert all(a['end']==b['start'] for a,b in zip(data['semantic_beats'],data['semantic_beats'][1:]))
assert blocks[0]['start']==0 and blocks[-1]['end']==1052
print({'blocks':18,'semantic_beats':60,'sheets':43,'frames':408})
