"""Rebuild the library inventory and this session's explicitly scoped caption notes.

This is an evidence index, not automatic semantic review or an AV listening claim.
Editorial notes below were written after reading the stated caption intervals.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

import cv2
import imageio_ffmpeg

WORKSPACE = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def rel(path):
    return path.relative_to(WORKSPACE).as_posix()


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def ch(start, end, title, question, claim, example, mechanism, transition, payoff, emphasis, kind='argument'):
    return dict(start=start, end=end, title=title, question=question, claim=claim,
                evidence_example=example, mechanism=mechanism, transition=transition,
                payoff=payoff, emphasis=emphasis, kind=kind,
                confidence='caption_semantics; boundary approximate; not measured cut or vocal stress')


DEEP = {
 '29B8-FtuC6U': {
  'spine': 'Tại sao năng lực sản xuất lớn vẫn không tạo ra sức mua tương xứng, và thay đổi phân bổ nguồn lực có thể giải quyết nút thắt nào?',
  'chapters': [
   ch(0.56,84.4,'Bếp rất mạnh, sảnh ăn vắng khách','Có vốn và công nghệ rồi thì thiếu gì?',
      'Người kể trả lời sớm: thiếu cầu đủ hấp thụ công suất.',
      '15,92–48,16: nhà hàng đầy đầu bếp và món ăn nhưng chỉ vài khách; đây là ẩn dụ, không phải hồ sơ doanh nghiệp.',
      'Đặt hai đại lượng đối lập: khả năng làm ra hàng và khả năng mua hàng.',
      '76,52–82,48 quay lại câu hỏi sống bằng gì khi làm rẻ mà không có người mua.',
      'Người xem biết câu hỏi chính trước khi bước vào giải thích.',
      'Nhấn tương phản công suất/cầu; tránh tiếp tục thêm danh sách máy móc.'),
   ch(84.4,96.28,'Nhận diện kênh','Đây là chương giải thích không?', 'Đây là bumper/nhận diện.',
      '84,4 lời chào kênh; nhạc trong caption.', 'Ngắt mạch để nhận diện.',
      'Đi vào quảng bá ở 96,28.', 'Không có luận cứ mới cho câu hỏi kinh tế.', 'Tách khỏi dàn ý học thuật.', 'branding'),
   ch(96.28,126.85,'Quảng bá hệ sinh thái riêng','Người kể đang bán gì?', 'Quảng bá sách/audio/công cụ riêng.',
      'Lời mời truy cập dịch vụ và hứa lợi ích phát triển bản thân.', 'Chuyển từ chủ đề kinh tế sang chuyển đổi bán hàng.',
      '126,85 trở lại tiêu đề dọn cỗ trước/tìm khách sau.', 'Không phải miễn trừ trách nhiệm.',
      'Không học độ dài quảng bá này thành độ dài hook.', 'promotion'),
   ch(126.85,284.33,'Vì sao vẫn tiếp tục làm hàng dư thừa?','Nếu bán lỗ, vì sao không đóng nhà máy?',
      'Người kể liên kết ưu đãi sản xuất với mở công suất và động lực giữ việc/GDP/nợ ngân hàng.',
      '144,33–184,33 chủ xưởng nhận ưu đãi; 211,21–253,61 kho xe/pin/thép và khái niệm xác sống có năng suất.',
      'Vốn rẻ → mở rộng trước khi có khách; chi phí đóng cửa đẩy động lực duy trì sản xuất.',
      '254,77 hỏi tại sao không tắt máy; 284,33 chuyển sang vì sao dân không mở ví.',
      'Trả lời được nghịch lý công suất hiện đại mà lợi nhuận yếu trong logic người kể.',
      'Nhấn 2 bước nhân quả riêng; số 4,4%/800 tỷ là lời nguồn chưa được kiểm lại.'),
   ch(284.33,445.74,'Vì sao người dân giữ tiền?','Tại sao hàng rẻ mà người mua vẫn dè dặt?',
      'Người kể giải thích tiết kiệm phòng ngừa bằng rủi ro y tế/hưu trí và mất của cải nhà ở.',
      '328,33 đặt người xem vào gia đình; 337,09 viện phí/học hành/hưu trí; 400,81 nhà là két tiết kiệm.',
      'Bất an tương lai và tài sản giảm → hoãn xe/du lịch/ăn nhà hàng.',
      '445,74 chuyển từ gia đình điển hình sang nhóm lao động di cư cụ thể.',
      'Đổi nhãn tiết kiệm thành một quyết định có nguyên nhân, thay vì chỉ quy tính cách.',
      'Mỗi rủi ro phải gắn một khoản chi bị hoãn; không dùng cảnh tiền chung chung.'),
   ch(445.74,548.38,'Một nhóm người cụ thể: lao động di cư','Cùng làm ở đô thị, vì sao vẫn không tiêu như cư dân đô thị?',
      'Người kể đặt quyền tiếp cận phúc lợi/hộ khẩu làm nút thắt.',
      '488,9–508,3: trường học, nhà ở và thanh toán y tế; 519,66–527,7 gửi lương về quê.',
      'Quyền lợi không ổn định → phòng ngừa nhiều hơn → tiêu dùng hiện tại ít.',
      '548,38 mở sang ai nhận được thu nhập của nền kinh tế.',
      'Cụ thể hóa một cơ chế thể chế bằng hành vi có thể hình dung.',
      'Chỉ rõ chủ thể, quyền bị hạn chế và hành vi; 300 triệu/+30% chưa đối chiếu nguồn.'),
   ch(548.38,621.14,'Ai nhận phần bánh thu nhập?','Ngoài nỗi sợ, người dân có bao nhiêu phần thu nhập?',
      'Người kể chuyển từ hành vi giữ ví sang phân bổ thu nhập/lợi nhuận và thuế.',
      '556,22–579,74 dùng 100 ổ bánh mì để diễn giải tỷ trọng.',
      'Nguồn lực ở doanh nghiệp/chính quyền tái đầu tư → chưa chảy tương ứng về hộ gia đình.',
      '621,14 hỏi giấc mộng bán ra ngoài đã vỡ ra sao.',
      'Bổ sung tầng phân phối, không lặp lại tầng tâm lý trước.',
      'Ẩn dụ không thay định nghĩa thống kê: tỷ trọng thu nhập và tiêu dùng cần tách khi viết mới.'),
   ch(621.14,709.1,'Có thể bán hàng dư ra nước ngoài mãi không?','Tại sao không chỉ xuất khẩu nhiều hơn?',
      'Người kể dùng rào cản thương mại để giới hạn lối thoát xuất khẩu.',
      '651,66–679,26 liệt kê Mỹ/EU/các thị trường khác và phản ứng thương mại.',
      'Sản xuất dư → xuất khẩu → đối tác bảo vệ ngành nội địa → lối thoát bị thu hẹp.',
      '705,5 kết lời giải phải tìm trong nước; 709,1 chuyển đề xuất.',
      'Bịt một phản biện tự nhiên trước khi nêu giải pháp.',
      'Nhấn giới hạn của phương án thay thế; mức thuế/niên đại phải xác minh riêng.'),
   ch(709.1,792.66,'Đổi dòng vốn: từ công suất sang an sinh','Can thiệp nào nhắm đúng các nút thắt vừa nêu?',
      'Người kể đề xuất phúc lợi, cổ tức/an sinh và quyền cư trú.',
      '736,66 bệnh viện/trường học; 761,78 doanh nghiệp; 776,62 hộ khẩu.',
      'Mỗi giải pháp trả lại một nguyên nhân đã dựng, tạo cấu trúc đối xứng.',
      '792,66 hỏi nếu có lời giải vì sao chưa làm.',
      'Giải pháp không xuất hiện từ khoảng trống; được gắn với từng vấn đề đã giải thích.',
      'Tránh học lời hứa giải phóng 2–3 đồng như hệ số chắc chắn.'),
   ch(792.66,883.34,'Vì sao lời giải khó, và quay về chiếc ví','Có giải pháp rồi thì trở ngại ở đâu?',
      'Người kể đặt xung đột tư duy/lợi ích làm giới hạn, rồi chốt bằng cảm giác an toàn của gia đình.',
      '856,94–874,42 người mẹ/công nhân/người già trở lại với nhu cầu cụ thể.',
      'Callback từ máy móc đầu phim sang người mua cuối phim, mở thêm tầng niềm tin.',
      'Hết lời rồi còn đuôi hình/end screen trong media.',
      'Câu trả lời cuối phát triển đáp án đầu: cầu không chỉ là số người, còn là khả năng và an tâm chi tiêu.',
      'Giữ một kết luận chính; không biến câu chốt cảm xúc thành bằng chứng thực nghiệm.'),
  ],
  'observations': [
   'Đọc toàn bộ caption 0,56–883,34; không xem/nghe liên tục 893 giây.',
   'Đã mở contact-sheet.jpg: 20s lời đang nói bếp/robot, hình chọn mẫu là người ở phố, không xác nhận sự khớp đối tượng. 382,71s có bảng budget trong khi lời đang nói trợ cấp; ảnh không chứng minh số thống kê.',
   'Giữ tuyến cung→cầu→nhóm người→phân phối→xuất khẩu→giải pháp→cản trở. Không coi mọi con số và khái quát mạnh của người kể là nguồn kinh tế đã được xác minh.'
  ],
  'rules': [
   ['15.92–82.48','Cho người xem nhìn thấy mâu thuẫn bằng một tình huống có hai trạng thái đối lập trước khi giải thích thuật ngữ.'],
   ['254.77–286.81','Chuyển chương bằng hệ quả/câu hỏi mà câu trả lời trước vừa tạo ra.'],
   ['709.10–792.66','Mỗi giải pháp phải trỏ ngược về một nguyên nhân đã chứng minh trong kịch bản.'],
  ]
 },
 '5zqAMK2qsfM': {
  'spine': 'Vì sao học và lưu nhiều mà vẫn không tiến bộ, và làm một sản phẩm nhỏ cho người khác thay đổi điều gì?',
  'chapters': [
   ch(0,81.32,'Rất nhiều đầu vào, không có đầu ra','Vì sao mình luôn học nhưng kế hoạch không thành việc?',
      'Người kể gom các hành vi lưu bài/mua sách/xin lời khuyên rồi đối lập với việc không tạo sản phẩm.',
      '0–46,72 điện thoại, sách còn nilông, cà phê xin lời khuyên, sổ kế hoạch không được làm.',
      'Tình huống nhận diện bản thân → mâu thuẫn đầu vào/đầu ra → lời hứa phá vòng lặp.',
      '81,32 nhận diện kênh.', 'Một vấn đề duy nhất xuyên hook, thay vì ghép nhiều lời khuyên rời.',
      'Nhấn hành vi quan sát được trước nhãn lười/giỏi; không sao chép sự quy kết tâm lý.'),
   ch(81.32,124.65,'Nhận diện và quảng bá','Đây có phải phần giải thích?', 'Đây là bumper rồi quảng bá sách/hệ sinh thái.',
      '81,32 chào kênh; 92,8–124,65 lời mời mua/truy cập.',
      'Dừng câu chuyện để nhận diện và bán dịch vụ.', '124,65 gọi tên chương đầu.',
      'Không phải miễn trừ; không có luận cứ mới cho luận đề.', 'Tách nhãn promotion khỏi chương biên tập.', 'promotion'),
   ch(124.65,226.21,'Vì sao nạp thông tin dễ gây cảm giác tiến bộ?','Phần thưởng của lưu bài khác gì phần thưởng của làm việc?',
      'Người kể diễn giải tiêu thụ như một phần thưởng dễ, có thể thay cho hành động khó.',
      '167,17 mua sách không sở hữu tri thức; 181,09–204,41 ví việc nạp với ti giả.',
      'Phần thưởng dễ → né trang giấy trắng/phán xét → chuẩn bị kéo dài.',
      '226,21 chuyển sang thông tin lưu lại trong trí nhớ thế nào.',
      'Nêu một cơ chế cho mâu thuẫn hook.',
      'Các phát biểu vùng não/dopamine là lời nguồn chưa được kiểm khoa học; chỉ học chức năng giải thích.'),
   ch(226.21,338.37,'Từ nhớ thụ động sang tái cấu trúc','Viết lại/ứng dụng khác đọc thêm như thế nào?',
      'Người kể đối chiếu quên lãng với tự tóm tắt, giải thích và ứng dụng.',
      '273,09–282,41 bị hỏi cuốn sách nói gì thì không nói ra; 307,61–335,81 viết/giải thích buộc đối chiếu.',
      'Đầu ra buộc truy hồi và tổ chức ý; người kể dùng đó làm cầu sang định nghĩa xuất bản.',
      '338,37 hỏi xuất bản trong đời thường là gì.',
      'Khái niệm cần một hoạt động cụ thể, không dừng khẩu hiệu học chủ động.',
      'Con số quên 75% trong 48–72h chưa được kiểm; không đưa vào kịch bản như hằng số.'),
   ch(338.37,479.3,'Xuất bản nhỏ trông ra sao?','Có phải phải viết sách hay có triệu người theo dõi?',
      'Người kể hạ ngưỡng hành động: một đầu ra nhỏ mà người khác dùng được.',
      '386,54 bài cảm nhận; 407,25 bảng chi tiêu; 420,65 công thức nấu ăn; 448,18 quy trình cho đồng nghiệp.',
      'Định nghĩa trừu tượng → nhiều nghề/hành vi → nhận ra việc có thể làm ngay.',
      '479,3 chuyển sang tác động lên tư duy.',
      'Người xem có tiêu chuẩn nhận biết đầu ra, không chỉ được khuyến khích.',
      'Mỗi ví dụ cần thêm một tình huống khác; có thể cắt bớt nếu nhiều ví dụ không tăng hiểu biết.'),
   ch(479.3,598.14,'Lợi ích thứ nhất: tư duy rõ hơn','Tại sao phải viết ra mới thấy lỗ hổng?',
      'Người kể dùng việc biên tập để kiểm nguyên nhân, bằng chứng và định kiến.',
      '526,5–536,38 các câu hỏi nguyên nhân/hiện tượng/bằng chứng.',
      'Đóng gói lời → buộc chọn quan hệ logic → lộ chỗ hiểu hời hợt.',
      '598,14 báo rõ chuyển sang giao tiếp/EQ.',
      'Mỗi lợi ích có cơ chế riêng, không chỉ đọc tên lợi ích.',
      'Chốt ở thay đổi trong cách nghĩ; lời hứa quyết định luôn chuẩn xác là cường điệu cần loại.'),
   ch(598.14,717.1,'Lợi ích thứ hai: nghĩ từ phía người nhận','Làm sao truyền đạt để người khác hiểu?',
      'Người kể giải thích luyện xuất bản qua câu hỏi ai đọc, vướng gì, hiểu từ ngữ này không.',
      '648,14–662,66 câu hỏi về độc giả và hình ảnh đời thường.',
      'Có người nhận cụ thể → sửa từ/cấu trúc → tăng cơ hội hiểu và phản hồi.',
      '717,1 gọi tên vốn sống và quan hệ.',
      'Tiến từ tổ chức suy nghĩ cá nhân sang giao tiếp.',
      'Nhấn một người nhận/một điều họ cần; không khẳng định việc đăng bài tự động tăng EQ.'),
   ch(717.1,878.98,'Lợi ích thứ ba: quan sát và quan hệ','Khi cần chia sẻ, mình chú ý cuộc sống khác thế nào?',
      'Người kể phát triển hai hệ quả: quan sát kỹ hơn và thu hút người cùng mối quan tâm.',
      '747,34–769,78 tình huống đời thường thành chất liệu; 814,42–866,22 chia sẻ chuyên môn gợi kết nối.',
      'Mục tiêu tạo đầu ra → tìm chất liệu; đầu ra công khai → người khác có cơ sở tương tác.',
      '878,98 chuyển từ quan hệ sang đòn bẩy nghề nghiệp.',
      'Tăng quy mô lợi ích, nhưng phần này dễ dài và trùng hứa hẹn.',
      'Không sao chép khẳng định người tiêu thụ chỉ hút bạn tiêu cực hoặc xuất bản chắc chắn vào vòng tinh hoa.'),
   ch(878.98,1021.22,'Lợi ích thứ tư: đầu ra có thể được tìm lại','Tại sao một bài làm rồi vẫn có thể tạo cơ hội?',
      'Người kể đối chiếu tiêu thụ một lần với tài liệu có thể dùng lại/tìm thấy.',
      '965,34–986,86 kịch bản bài viết hôm nay được độc giả/đối tác tìm sau này.',
      'Sản phẩm lưu được → nhiều lượt tiếp cận → khả năng người cần giải pháp nhận ra năng lực.',
      '1021,22 chuyển sang tự tin từ kiểm chứng thực tế.',
      'Nêu giá trị khả dụng của đầu ra.',
      'Kịch bản cơ hội là minh họa, không phải kết quả tất yếu hoặc lãi kép không giới hạn.'),
   ch(1021.22,1143.5,'Lợi ích thứ năm: tự tin từ phản hồi','Nếu sản phẩm đầu dở thì sao?',
      'Người kể dẫn chuỗi làm vụng→nhận phản hồi→sửa→giúp được người thật.',
      '1067,98–1108,58 bài đầu không ai thích rồi một người cảm ơn hoặc mua giải pháp.',
      'Hành động tạo dữ kiện năng lực → sửa theo phản hồi → tự tin có căn cứ hơn.',
      '1143,5 gọi hành động ngay hôm nay.',
      'Giải nỗi sợ đã nêu ở chương đầu, tạo callback.',
      'Giữ phản hồi cụ thể; bớt hình dung thành công dài và lời hứa bất khả lay chuyển.'),
   ch(1143.5,1278.51,'Chọn một việc để xuất bản','Sau khi xem, cần làm việc nhỏ nào?',
      'Người kể quay lại lưu bài/mua sách và yêu cầu biến một kinh nghiệm thành đầu ra.',
      '1198,66–1219,38 bài học nuôi con, bảng tính, chia sẻ trải nghiệm; 1267,94 hỏi lĩnh vực sẽ bắt đầu.',
      'Callback hành vi cũ → thay thế bằng thao tác → câu hỏi comment đúng nội dung.',
      'Hết lời, media còn end screen.',
      'CTA phát sinh từ luận đề, không chỉ xin đăng ký.',
      'Nên rút đoạn nhắc lại/tiên đoán tiền tài; CTA chọn một sản phẩm nhỏ và một người nhận.'),
  ],
  'observations': [
   'Đã đọc toàn caption; mốc kết tính từ caption cuối, không phải thời gian lời được forced align.',
   'Đã mở contact sheet toàn timeline: mic/waveform/player lặp; tại 184,14s có mẹ/con ngoài trời, chưa thấy ti giả như ẩn dụ đang đọc. Không nhận mẫu này làm chuẩn khớp hình.',
   'Lợi ích nhiều và đánh dấu bằng câu tiêu đề rõ, nhưng 717–1143s nối quan hệ, tài sản số, tự tin dễ thành liệt kê lời hứa. Bản gốc mới nên chọn ít tầng có bằng chứng thay vì sao chép toàn độ dài.'
  ],
  'rules': [
   ['338.37–479.30','Đặt định nghĩa trừu tượng vào đầu ra nhỏ có người nhận và có thể quan sát.'],
   ['648.14–662.66','Trước khi viết chương, xác định người nghe là ai, họ cần giải được gì, từ nào họ chưa hiểu.'],
   ['1067.98–1143.50','Phản hồi của người thật là bước phát triển câu chuyện; lời tự khen và test kỹ thuật không thay bước này.'],
   ['1267.94–1278.51','Hỏi khán giả một lựa chọn có thể làm ngay từ nội dung vừa giải thích.'],
  ]
 },
 '5uTC396kCs4': {
  'spine': 'Người kể phân loại năm kiểu dịch chuyển vốn để giải thích cuộc đuổi bắt giữa rào cản, động lực và phương thức; chỉ học cấu trúc, không biến thành hướng dẫn lách luật.',
  'chapters': [
   ch(0.4,94.32,'Cùng con số, hai nhu cầu','Vì sao một hạn mức nhỏ lại tạo câu chuyện lớn?',
      'Người kể đặt nhu cầu thông thường cạnh khối tài sản lớn và hứa năm nhóm cơ chế.',
      '0,4–36,96 cùng con số nhìn từ gia đình và siêu giàu; 38,04–50,08 ẩn dụ nước/đập.',
      'Một quy mô không khớp nhu cầu → câu hỏi tiền đi đường nào.',
      '83,96–93,32 nêu lộ trình từ sơ khai đến phức tạp.',
      'Người xem biết phạm vi và thứ tự chương.',
      'Nhấn xung đột về quy mô; hạn mức/pháp luật trong lời nguồn chưa được kiểm.'),
   ch(94.32,137.53,'Nhận diện và quảng bá','Đâu là nội dung chính?', 'Bumper rồi quảng bá hệ sinh thái.',
      '94,32 chào; 106,08 quảng bá tới 135,89.', 'Ngắt mạch nhận diện/bán hàng.',
      '137,53 mở phần thứ nhất.', 'Không có disclaimer pháp lý đầu.', 'Ghi rõ đây là promotion.', 'promotion'),
   ch(137.53,327.09,'Phần một: giới hạn vật lý','Vì sao phương án sơ khai không mở rộng được?',
      'Người kể cấu trúc mỗi nhóm theo cơ chế→tình huống→trở ngại.',
      '230,17 đưa vụ bắt giữ; 273,89 trở lại khối lượng và rủi ro phát hiện.',
      'Nhu cầu giá trị cao gặp giới hạn vận chuyển và thực thi.',
      '340,69 sang phương án chuyển từ vật lý sang hệ thống.',
      'Kết mỗi nhóm bằng hạn chế làm xuất hiện nhu cầu nhóm kế tiếp.',
      'Trong bản mới chỉ cần phân loại/rủi ro, không tái hiện các bước thực hiện sai phạm.'),
   ch(327.09,340.69,'Thông báo nguồn đăng','Có thêm luận cứ không?', 'Thông báo chống reup.',
      '327,09 tên đơn vị/kênh chính chủ.', 'Ngắt nội dung để bảo vệ nguồn đăng.',
      '340,69 tiếp tục phần hai.', 'Không phải phần giải thích cơ chế hay disclaimer đầu.', 'Tách khỏi tuyến chương.', 'ownership_notice'),
   ch(340.69,524.22,'Phần hai: gom quy mô và dấu vết','Đổi từ vật lý sang hệ thống khắc phục được gì, lộ ra gì?',
      'Người kể cho nhóm hai cùng cấu trúc: quy mô→vụ việc→phát hiện→giới hạn.',
      '421,1–501,58 câu chuyện vụ án được người kể dùng làm minh họa; 503,14–522,58 trở về giám sát.',
      'Thay phương án trước bằng mạng nhiều bên nhưng tạo dấu vết liên kết.',
      '524,22 chuyển từ cấp cá nhân lên cấp doanh nghiệp.',
      'Phần hai không chỉ đổi tên; đổi đơn vị hành động và dạng trở ngại.',
      'Dùng một bảng so sánh cấp độ/rủi ro, không phát hành cách né giám sát.'),
   ch(524.22,712.78,'Phần ba: giao dịch và chứng từ','Tại sao quy mô doanh nghiệp làm câu chuyện phức tạp hơn?',
      'Người kể đối lập tài khoản vốn/thương mại và dùng chứng từ làm lớp diễn giải.',
      '630,5–686,22 đưa Thanh Đảo như ví dụ; đó là lời nguồn, chưa đối chiếu vụ án và tính tương đồng cơ chế.',
      'Hình thức giao dịch được dùng để giải thích sự khó thẩm định.',
      '739,5 chuyển sang mạng lưới trung gian/đặc khu.',
      'Tăng độ phức tạp theo tiêu chí đã hứa ở hook.',
      'Không sao chép khẳng định an toàn pháp lý/hợp pháp hoàn hảo của nguồn; giấy tờ không chứng minh hợp pháp.'),
   ch(712.78,739.5,'Thông báo chống mạo danh','Vì sao mạch giải thích dừng?', 'Thông báo về reup/mạo danh/quảng cáo ngoài kênh.',
      '714–737,5 cảnh giác nội dung kênh khác.', 'Bảo vệ nhận diện, không thêm mắt xích nhân quả.',
      '739,5 gọi rõ phần bốn.', 'Không nhầm thành ví dụ nội dung.', 'Đánh dấu ownership_notice.', 'ownership_notice'),
   ch(739.5,895.3,'Phần bốn: mạng trung gian và phản ứng thực thi','Một cơ chế từng tồn tại có thể bị đổi luật/thực thi ra sao?',
      'Người kể đóng phần bằng phản ứng quản lý làm mô hình cũ bị thu hẹp.',
      '849,5–892,62 chuyển từ mô tả mô hình sang bắt giữ/án và siết quản lý được người kể viện dẫn.',
      'Đổi môi trường thực thi → thay tính khả dụng của cách cũ.',
      '895,3 chuyển từ hệ thống vật lý sang kỹ thuật số.',
      'Mỗi chương có thay đổi điều kiện, tránh mô tả một cơ chế tĩnh từ đầu đến cuối.',
      'Giữ bài học về điều kiện/giới hạn; không diễn các thao tác rửa tiền.'),
   ch(895.3,1091.22,'Phần năm: số hóa không xóa rủi ro','Ít rào cản vật lý hơn có đồng nghĩa hết rủi ro?',
      'Người kể chuyển tới phương thức số rồi nêu rủi ro đối tác, theo dấu và phong tỏa.',
      '1054,38–1089,26 là đoạn giới hạn/rủi ro thay vì chỉ nói sức mạnh công nghệ.',
      'Thay dạng phương tiện tạo rủi ro khác, không xóa giám sát hoặc nghĩa vụ pháp lý.',
      '1091,22 gọi tên bức tranh toàn cảnh.',
      'Chương cuối vẫn có giới hạn, không chỉ cao trào công nghệ.',
      'Lược bỏ cách làm cụ thể; các khẳng định loại bỏ hoàn toàn kiểm soát/ngưỡng vô hạn không nên học.'),
   ch(1091.22,1203.3,'So sánh lại năm nhóm','Năm chương vừa nghe khác nhau ở tiêu chí nào?',
      'Người kể tổng kết theo quy mô, độ phức tạp, chi phí và mức giám sát.',
      '1095,18–1201,46 lần lượt gọi lại từng nhóm với cùng bộ trục.',
      'Từ năm câu chuyện thành một mô hình so sánh chung.',
      '1203,3 hỏi tại sao người sở hữu tài sản chấp nhận chi phí/rủi ro.',
      'Payoff không phải chỉ nhắc lại tên phần; bổ sung bản đồ quan hệ.',
      'Dùng tiêu chí lặp nhất quán; số chi phí/quy mô trong nguồn không được coi là bảng hướng dẫn.'),
   ch(1203.3,1303.43,'Từ các nhóm trở lại động lực','Vì sao cuộc đuổi bắt tiếp tục?',
      'Người kể khép bằng động lực phòng vệ/bất an và ẩn dụ dòng nước ban đầu.',
      '1244,66–1287,66 liên kết rào cản, động lực và phí; 1297,46–1303,43 callback dòng tiền.',
      'Từng phương thức riêng → động lực hệ thống → trở về lời hứa hook.',
      'Sau lời cuối là đuôi media/đen; không có lời CTA đăng ký trong caption cuối.',
      'Một hình tượng quay lại nhưng đã mang cơ chế mới.',
      'Callback phải thêm kiến thức; không khẳng định dòng tiền luôn thoát trong mọi điều kiện.'),
  ],
  'observations': [
   'Đã đọc toàn caption; chưa kiểm chứng các vụ việc, điều luật, số liệu hay tính đúng của cơ chế tài chính được người kể nêu.',
   'Đã mở contact sheet toàn timeline; mic/waveform phủ lặp. 1319s đen, không mặc định có end screen/CTA giống video khác.',
   'Đây là nghiên cứu cấu trúc taxonomy và progression, không cung cấp hoặc phê chuẩn thao tác né luật. Nhãn thủ thuật không phải cơ sở dùng lại nội dung chỉ dẫn.'
  ],
  'rules': [
   ['83.96–93.32','Hứa lộ trình có tiêu chí: từ cách đơn giản tới cấu trúc phức tạp.'],
   ['273.89–340.69; 503.14–524.22','Kết chương bằng giới hạn mà chương kế tiếp phải giải thích.'],
   ['1091.22–1203.30','Tổng kết nhiều chương bằng cùng các trục so sánh để tạo hiểu biết mới.'],
   ['1297.46–1303.43','Callback quay về hình tượng đầu với cơ chế đã được dựng, không chỉ lặp lại khẩu hiệu.'],
  ]
 },
 'JlfAd_OaFek': {
  'spine': 'AI giúp hay làm phụ thuộc: khả năng của công cụ, thay đổi nhiệm vụ, năng suất và điều kiện sử dụng; cuối video chuyển rõ sang phần cứng tài trợ.',
  'chapters': [
   ch(0,34.52,'Tôi dùng AI rồi sẽ còn gì để đi làm?','Dùng nhiều có làm mình mất năng lực không?',
      'Người kể mở từ quán ăn/menu/học tập rồi đặt nỗi lo gần nhóm người trẻ.',
      '12,4–20,84 tự hỏi chưa kịp đi làm đã thất nghiệp.', 'Tình huống cá nhân → câu hỏi người xem có liên quan.',
      '34,52 lưu ý phạm vi.', 'Lời hứa về cách dùng, không chỉ tổng quan công nghệ.', 'Chốt một mâu thuẫn cụ thể.'),
   ch(34.52,47.8,'Lưu ý và công bố tài trợ','Độ chắc của thông tin và tài trợ là gì?',
      'Nguồn tổng hợp/nhận định cá nhân, mời đính chính; công bố ASUS.',
      '34,52–43,68; 43,68–45,36 tài trợ.', 'Tách phạm vi và tài trợ khỏi thân giải thích.',
      '47,8 bước vào lao động Gen Z.', 'Disclaimer có thật trong lời nguồn; không suy cho kênh khác.', 'Một phần ngắn có chức năng rõ.', 'disclaimer_sponsor'),
   ch(47.8,136.33,'Vừa sợ AI vừa dùng AI','Nỗi lo việc làm xuất phát từ hoàn cảnh nào?',
      'Người kể đặt khó khăn tài chính và mức sử dụng vào thế đối lập.',
      '98,52 nêu khảo sát lo thay thế; 121,33–134,29 nêu mức dùng và nghịch lý.',
      'Nhu cầu việc làm ổn định + công cụ được dùng thường xuyên → động cơ tìm hiểu.',
      '136,33 hỏi AI thực sự làm được gì.', 'Đưa người xem vào thế khó trước khi định nghĩa.', 'Số khảo sát cần kiểm nguồn, không dùng như facts đã xác nhận.'),
   ch(136.33,307.09,'AI làm được gì, người giao việc làm gì?','Phân biệt nhận diện/tạo sinh/agent để làm gì?',
      'Người kể tăng mức tự chủ từng bậc rồi dừng ở xác định mục tiêu/đánh giá kết quả.',
      '262,09–280,41 trò rắn săn mồi cần mô tả luật và kết quả.',
      'Khả năng tăng không xóa nhu cầu định nghĩa sản phẩm.', '307,09 quay lại câu hỏi thất nghiệp.',
      'Phần định nghĩa phục vụ câu hỏi việc làm, không mở rộng vô tận lịch sử AI.',
      'Ví dụ phải có kết quả đúng/sai thấy được; không nói agent luôn tự hoàn thành.'),
   ch(307.09,516.14,'Thay việc hay thay một phần nhiệm vụ?','Tự động hóa một phần có đồng nghĩa mất nghề?',
      'Người kể phân biệt đổi nhiệm vụ và xóa công việc, cần kỹ năng chuyển đổi/kiểm lỗi.',
      '394,54–418,33 báo cáo cần người kiểm; 447,25–466,3 xe đua/code lỗi; 474,57–514,14 thợ ống nước.',
      'Công cụ xử lý được thao tác nhưng chẩn đoán/tiêu chuẩn đầu ra vẫn cần chuyên môn.',
      '516,14 chuyển sang vì sao doanh nghiệp đầu tư.', 'Bác một suy luận quá nhanh từ khả năng công cụ tới mất nghề.',
      'Các dự báo WEF đa yếu tố không phải AI gây số mất việc ấy; caption ghi nhầm năm có thể xảy ra.'),
   ch(516.14,664.38,'Năng suất tăng ở đâu, có giới hạn gì?','Giảm thời gian công việc cụ thể có lợi ích nào?',
      'Người kể lần lượt lập trình, viết, chăm sóc khách hàng, rồi tổng hợp tác động.',
      '556,02–560,42 nhiều code không đồng nghĩa sản phẩm tốt; 629,82–636,46 người mới không tự thành chuyên gia.',
      'Tác vụ cụ thể → phần tiết kiệm → điều kiện kiểm tra → kết quả tổng.',
      '664,38 thông báo phần rủi ro.', 'Tăng quy mô từ cá nhân sang doanh nghiệp rồi mô hình kinh tế.',
      'Không cộng trộn % nghiên cứu khác tác vụ/đối tượng thành một mức năng suất chung.'),
   ch(664.38,834.74,'Ba điều kiện của Cloud AI','Tính tiện có đổi lấy gì?',
      'Người kể đặt ba nhãn rõ: dữ liệu, chi phí, kết nối/độ trễ.',
      '704,26 tài liệu công ty; 751,98 token ở quy mô doanh nghiệp; 808,9 dịch hội thoại.',
      'Mỗi nhãn có tình huống làm rõ tác hại khác nhau.', '834,74 chuyển giải pháp phần cứng local.',
      'Người xem biết đang ở mục nào và vì sao ví dụ thuộc mục đó.', 'Đây là bài học phân đoạn mạnh nhất: 3 nhánh ít giao thoa.'),
   ch(834.74,1052.02,'Cầu nối tới sản phẩm tài trợ','Từ vấn đề tới lời chào hàng chuyển ở đâu?',
      'Giới thiệu local AI/NPU rồi chuyển hệ sản phẩm ASUS và nơi mua.',
      '935,54 gọi ASUS; 1031,34 đại lý và danh mục mua.',
      'Ba rủi ro trước được dùng làm nhu cầu cho giải pháp tài trợ.',
      '1052,02 quay lại lời kết chung về AI.', 'Có cấu trúc problem→product, nhưng đây là phần thương mại.',
      'Không học lời tuyệt đối giải quyết toàn bộ/bảo mật tuyệt đối như kết luận kỹ thuật.', 'sponsor_integration'),
   ch(1052.02,1075.7,'Khép lại và CTA','Nên giữ thái độ/hành vi gì?',
      'Người kể quay về học dùng công cụ rồi xin đăng ký.',
      '1063,86–1072,14 học tận dụng công cụ và đăng ký.', 'Callback nỗi lo ban đầu.',
      'Chào kết.', 'Lời cuối hơi tuyệt đối so với các giới hạn thân bài; bản mới phải giữ điều kiện.',
      'Không kết rằng AI không bao giờ thay việc sau khi thân bài đã nêu việc có thể biến mất.'),
  ],
  'observations': ['Đã đọc toàn transcript; không mở thêm sheet hay nghe AV trong lượt này.',
    'Đây là Lóng, không phải THE HIDDEN SELF. Không gán lẫn kết luận giữa kênh.',
    'Mục 834,74–1052,02 là giải pháp dẫn sang tài trợ, không phải bằng chứng độc lập. Các số khảo sát/benchmark cần nguồn gốc và phạm vi trước khi dùng mới.'],
  'rules': [['697.14–702.54','Nói trước có ba vấn đề, rồi mỗi nhánh chỉ giải thích một vấn đề với một tình huống.'],
    ['394.54–418.33','Chèn phân biệt khái niệm đúng ngay chỗ người xem dễ suy luận quá mức.'],
    ['834.74–1052.02','Gắn nhãn tài trợ riêng để không học câu bán hàng như bằng chứng khách quan.']]
 },
 'podWgLH4b3M': {
  'spine': 'Một chiếc áo cực rẻ cần những điều kiện nào; khi các điều kiện đổi, mô hình và quan hệ với khách phải đổi ra sao?',
  'chapters': [
   ch(0.2,61.7,'Chiếc áo rẻ, con đường không còn rẻ','Công thức từng thắng bị chặn ở đâu?',
      'Người kể mở từ giá áo/mua theo trend, rồi đặt nghịch lý chi phí/luật chơi đổi.',
      '11,4–33,3 váy vài đô/content dùng một lần; 34,9–59,3 luật/chậm tăng trưởng/câu hỏi tương lai.',
      'Vật thể và hành vi gần gũi → câu hỏi về hệ thống phía sau.', '61,7 lưu ý phạm vi.',
      'Hứa giải thích điều kiện giá rẻ và tương lai mô hình.', 'Một vật thể làm trục; không kể lịch sử công ty vô mục đích.'),
   ch(61.7,68.6,'Lưu ý phạm vi','Thông tin có phải tuyệt đối chính xác?',
      'Tổng hợp nhiều nguồn và kinh nghiệm cá nhân, mời đính chính.', '61,7–68,6 lời lưu ý riêng.',
      'Đặt độ chắc thông tin.', '68,6 vào cơ chế.', 'Disclaimer ngắn có ranh giới.', 'Không đưa quảng cáo vào đây.', 'disclaimer'),
   ch(68.6,173.09,'Công thức thử ít rồi đo phản ứng','Khác biệt vận hành nào tạo lợi thế?',
      'Người kể đối chiếu sản xuất dự báo theo mùa với thử ít/đo phản ứng/làm thêm mẫu thắng.',
      '96,5–116,6 đối chiếu trực tiếp hai cách làm; 139,29–145,29 liên tưởng TikTok.',
      'Phản hồi nhanh và lô thử nhỏ → lựa chọn mẫu rồi mở quy mô.',
      '173,09 hỏi áo làm ở Trung Quốc bay nửa vòng vẫn rẻ nhờ đâu.',
      'Giải thích được một động cơ, rồi mở nút thắt logistics/chính sách.',
      'Caption số mẫu/doanh thu có dấu hiệu sai bậc; không nhập lại làm facts.'),
   ch(173.09,313.49,'Điều kiện giá rẻ thay đổi tại Mỹ','Chi phí ngoài xưởng thay đổi tác động ra sao?',
      'Người kể dùng ưu đãi kiện nhỏ/thuế thay đổi để nối tới giá và kết quả kinh doanh.',
      '257,79–275,39 giỏ hàng và khác biệt nhóm hàng; 294,09–311,09 kết quả công ty được viện dẫn.',
      'Điều kiện giao hàng/thuế → giá tới khách → phản ứng mua → tăng trưởng/lợi nhuận.',
      '313,49 móc dòng tiền sang sponsor.', 'Thấy chuỗi nhân quả qua nhiều tầng, không chỉ đọc con số.',
      'Mốc luật và báo cáo công ty cần kiểm nguồn primary; ở đây mới phân tích lời người kể.'),
   ch(313.49,389,'Quảng bá Odoo','Mạch nội dung ngừng ở đâu?',
      'Lời mời sự kiện/phần mềm doanh nghiệp.', 'Tên sự kiện, ngày/địa điểm, link đăng ký.',
      'Móc từ lỗ/dòng tiền sang giải pháp sponsor.', '389 gọi rõ quay lại Shein.',
      'Một đoạn thương mại riêng dài khoảng 75,5s.', 'Không đưa sponsor vào phân tích nguyên nhân Shein.', 'promotion'),
   ch(389,577.3,'Châu Âu: không chỉ tăng một loại phí','Cùng mô hình gặp thêm loại rào cản nào?',
      'Người kể phân biệt phản ứng xã hội, tuân thủ/an toàn, phí và luật nhắm siêu nhanh.',
      '471,89–491,3 phép tính phí với món rẻ làm rõ mức tương đối.',
      'Phí cố định nhỏ / giá món nhỏ = tỷ lệ lớn; điều kiện lợi thế cực rẻ bị mài mòn.',
      '577,3 chuyển từ bán hàng sang IPO.', 'Mở thêm một tầng luật/uy tín, không lặp lại Mỹ bằng địa danh khác.',
      'Trong lời có nhiều năm ASR 2015/2016/2018 bất thường, bắt buộc kiểm riêng trước dùng.'),
   ch(577.3,695.7,'Định giá và kết quả kinh doanh','Kỳ vọng nhà đầu tư phản ứng với mô hình đổi ra sao?',
      'Người kể chuyển từ chi phí mua hàng sang định giá/tăng trưởng/biên lợi nhuận.',
      '610,6–629,82 đối chiếu kỳ vọng định giá/diễn biến; 648,9–686,2 phân rã vùng và lợi nhuận.',
      'Triển vọng bị hỏi lại → thị trường đánh giá; doanh thu không tự đảm bảo lợi nhuận.',
      '695,7 hỏi còn đường nào hồi phục.', 'Tạo stakes mới cho câu hỏi sống ra sao của hook.',
      'Các sự kiện IPO/định giá trong nguồn chưa được xác minh, không được coi là dữ kiện.'),
   ch(695.7,818.1,'Đối thủ và lựa chọn khách hàng','Nếu tăng giá, vì sao khách có thể rời đi?',
      'Người kể mở rộng so sánh Temu, hãng truyền thống, đồ cũ để giải thích mất khoảng cách giá.',
      '775,1–781,4 chất lượng bình thường nhưng rẻ; 808,3–818,1 áo cộng phí so với đồ cũ.',
      'Khoảng cách tổng chi phí thu hẹp → lý do chọn app yếu hơn.',
      '818,1 hỏi Shein xoay sở kiểu gì.', 'Biến cạnh tranh thành lựa chọn thật của người mua.',
      'So sánh phải cùng chất lượng/điều kiện, không gom ngẫu nhiên số liệu đối thủ.'),
   ch(818.1,887.7,'Ba đường thích nghi','Thay mô hình bằng những đòn bẩy nào?',
      'Người kể chia ba đường: giá trị đơn cao, bán năng lực chuỗi cung ứng, đổi nơi sản xuất/tiêu thụ.',
      '820,8 nâng phân khúc; 843,7 bán hệ thống; 858,5 đổi chiến trường.',
      'Mỗi đường thay một biến khác của mô hình đã dựng.',
      '887,7 người kể chuyển rõ sang quan điểm trung tâm.', 'Có phương án cùng đánh đổi; không chỉ kết công ty chết.',
      'Chỉ giữ số liệu khi có nguồn; rút giới thiệu để dành thời lượng cho tradeoff.'),
   ch(887.7,977.4,'Payoff: khách yêu món hời hay yêu thương hiệu?','Vấn đề sâu hơn thuế là gì?',
      'Người kể đưa luận điểm riêng: hành vi săn rẻ từng nuôi tăng trưởng cũng làm thiếu trung thành.',
      '907,5–924,6 phân biệt yêu hãng với yêu món hời; 958,1–975,5 điều kiện siêu rẻ mất nhưng kỳ vọng còn.',
      'Mô hình thắng → đào tạo kỳ vọng của khách → kỳ vọng trở thành rào cản chuyển mô hình.',
      '977,4 hỏi trải nghiệm người xem.', 'Trả hook bằng một ý mới, không chỉ bảng tóm tắt thuế/giá.',
      'Đặt luận điểm đáng nhớ ở payoff; vẫn ghi đó là diễn giải, không chứng minh mọi khách đều thế.'),
   ch(977.4,987.4,'CTA gắn trải nghiệm','Khán giả có thể tham gia bằng điều gì?',
      'Hỏi đã mua/chọn đồ thế nào rồi mời đăng ký.', '977,4–987,4 câu hỏi và lời chào.',
      'Nội dung về hành vi khách → hỏi hành vi thật của khán giả.', 'Kết.',
      'CTA cùng chủ đề, không mời bình luận vô nghĩa.', 'Một câu hỏi cụ thể; không xin hàng loạt thao tác.'),
  ],
  'observations': ['Đã đọc toàn transcript, chưa xem/nghe liên tục hay kiểm nguồn nội dung.',
     'Đây là Lóng. Chia chương trên do agent suy luận theo lời, metadata không có chapters chính thức.',
     'Caption có các mốc năm và quy mô số nghi ngờ sai; ngoài ASR còn có thể có vấn đề nguồn. Không dùng để xác nhận kinh doanh/pháp luật hiện hành.',
     'Payoff 887,7–977,4 phát triển một ý riêng về kỳ vọng giá, có giá trị biên tập hơn việc chồng thêm số liệu.'],
  'rules': [['96.50–173.09','Giải thích lợi thế bằng đối chiếu hai quy trình, rồi hỏi điều kiện nào còn thiếu.'],
     ['173.09–313.49','Chuỗi chi phí→giá tới khách→phản ứng mua→kết quả kinh doanh phải có đủ mắt xích.'],
     ['887.70–977.40','Payoff thêm một kết luận của tác giả về cơ chế đã kể; không chỉ nhắc lại các chương.']]
 },
}

# Additional videos: explicit sampled-caption scope, not full-script review.
MINI = {
 '5_7IDQEU5OI': ['economic_podcast', '0,44–53,48: niềm tin chăm chỉ/công bằng bị đặt câu hỏi; 636,94–674,5: các mắt xích sang tay rủi ro; 1222,7–1261,87: trở lại sự cả tin vào luật chơi.', 'Học cách đưa một chuỗi trung gian và động cơ riêng vào giải thích hệ thống; không học quy kết toàn hệ thống là âm mưu khi thiếu bằng chứng.'],
 '96eyTrbH-ak': ['economic_podcast','0,56–54,36: từ tăng trưởng nhanh sang chững lại; 493,44–530: ví dụ khu vực được người kể dùng cho mô hình cũ; 932,16–968,36: kết bằng đổi công cụ/mô hình.', 'Câu hỏi vì sao từ thành công đến mắc kẹt tạo trục. Tránh đồng nhất các nước/đơn nguyên nhân khi chỉ có ví dụ khái quát.'],
 '9I2suK0eob4': ['financial_commentary','0–54,64: đặt 2027 như câu hỏi và bắt đầu nói chưa đủ cơ sở khẳng định; 941,04–974,64: ví dụ giả định nợ và khoản tiền phải bù; 1827,84–1848,43: hỏi cách xử lý rủi ro rồi xin comment đã xem cuối.', 'Một số thiếu hụt tiền thật trong ví dụ có sức nặng hơn nhiều tính từ. Học nhãn giả định; bỏ CTA comment đã xem cuối vì không thêm giá trị.'],
 'bm5q0e4MXhg': ['policy_news_commentary','4,96–54,56: tăng trưởng và chợ/đóng cửa tương phản; 1196,14–1233,38: giải thích bảng giá và nghĩa vụ; 2364,92–2389,12: lưu ý tham khảo/cuối video.', 'Có chapters metadata nhưng headline đất và opening tăng trưởng không trùng trọng tâm: cần kiểm lời hứa của title với chương đầu. Không chấp nhận số liệu/chính sách từ video này như nguồn pháp lý.'],
 'BOD_6bf_6pM': ['financial_commentary','0,32–54,52: chuỗi mốc cách 18 năm gợi quy luật; 977,96–1016,32: nối bất động sản thương mại với lãi vay/trái phiếu; 1901,2–1952,84: chuẩn bị tiền mặt/kiến thức và CTA.', 'Học việc nêu mốc so sánh; không học cách biến vài mốc lịch sử chọn lọc thành tiên đoán chắc chắn hay lời hứa triệu phú.'],
 'ERI4I4V4sBs': ['financial_commentary','0–54,28: tiền mặt mất sức mua nhưng tài sản cũng giảm; 915,14–953,22: nối luân chuyển tín dụng sang nợ nhóm hai; 1775,23–1824,55: giữ khả năng lựa chọn, hỏi mua hay giữ thanh khoản.', 'Mâu thuẫn hai phía và giới hạn mỗi tài sản tạo luận đề có điều kiện; tách rõ kịch bản với dự báo, không suy mọi tài sản sẽ sụp đổ từ title.'],
 'ggxRI_1u0_4': ['life_behavior_podcast','0,4–54,64: đồ không dùng trong phòng; 641,24–676,32: phân biệt chặn đầu vào/bỏ đồ/rời lệ thuộc; 1225,96–1266,48: trở về sống vừa đủ.', 'Mở bằng đồ vật khán giả nhìn được và định nghĩa ba hành động khác nhau; không lấy thống kê tủ đồ mơ hồ làm chứng cứ.'],
 'Glw9YcOMw2s': ['economic_podcast','0–54,96: quy mô nợ, đảo vai con nợ/chủ nợ và khẳng định tuyệt đối; 587,6–625,44: chuyển từ lạm phát sang AI/tăng trưởng; 1119,24–1157,56: chuyển giao trật tự và lời kết.', 'Một luận đề cần các cơ chế riêng; không học chữ tuyệt đối không vỡ nợ hoặc quy kết người khác chắc chắn trả hộ khi chưa có nguồn và điều kiện.'],
 'L0uNZyvCAxE': ['policy_finance_commentary','5–54: niềm tin vàng an toàn và vay ưu đãi bị đặt lại; 1101,16–1138,96: số tiền lỗ được quy ra học phí/sinh hoạt; 2176,32–2198,16: disclaimer cuối.', 'Quy đổi mức thiệt hại sang hệ quả đời sống giúp hiểu độ lớn, nhưng không trộn hai chủ đề nếu không có một cơ chế chung được nêu rõ.'],
 'NCl_PG00oa4': ['economic_podcast','0,32–53,64: siêu thị đầy hàng ít khách, hứa bỏ thuật ngữ khó; 690,62–726,22: giải thích khóa tín dụng qua doanh nghiệp địa ốc; 1323,31–1364,27: công nghệ cao và câu hỏi bình luận.', 'Tình huống cụ thể dẫn tới hệ thống; cần tránh ví dụ y khoa/ống thở thay cho bằng chứng chuỗi nợ và bỏ qua nhiều yếu tố khác.'],
 'njD0SI3TNxg': ['policy_finance_commentary','4,96–53,84: giá giảm mà không người mua cạnh tiền gửi lớn; 1090,84–1127,72: phép tính thu nhập/tiết kiệm và giá nhà; 2154,36–2177,08: lưu ý tham khảo.', 'Đặt câu hỏi trung tâm bằng hai đại lượng trái chiều; phép tính phải giữ nhất quán đã trừ sinh hoạt hay chưa, tránh nói không ăn không uống sau khi dùng tiền tiết kiệm.'],
 'UA7yZNRmZYY': ['life_psychology_podcast','0,32–54,28: hai người bước vào phòng khác nhau; 365,13–402,57: đổi thước đo kết quả sang hành vi; 693,94–711,74: mở ghi chú và ghi bằng chứng hành động.', 'CTA là một thao tác cụ thể hợp với luận đề; lời dẫn cần tránh coi mọi tự ti chỉ do một chuỗi ngộ nhận.'],
 'v74IRBimBk0': ['policy_news_commentary','5,12–54,32: năm nhóm đề xuất và tác động tới mảnh đất gia đình; 1176,52–1215,48: chương đang đổi từ quy định sang cơ chế vốn vĩ mô; 2322,04–2351,12: nói rõ dự thảo chưa chốt.', 'Học tên chương và chia nhóm người chịu tác động; không để chữ luật mới làm khán giả hiểu đề xuất đã thành quy định, không thay xác minh cơ quan gốc bằng caption.'],
 'X2Uadb-AKTw': ['financial_commentary','0,04–53,36: ẩn dụ đập nước gắn một lượng tiền; 887,56–919,04: ví dụ sức mua bị bào mòn và gợi phân bổ; 1723,8–1761,24: xin comment đã xem cuối và chào.', 'Ẩn dụ tạo hình dung nhưng dễ dẫn tới khẳng định mọi dòng tiền gây lạm phát/giá tài sản cùng tăng; học cấu trúc câu hỏi, không lấy lời kêu gọi đầu tư làm bằng chứng.'],
}


def read_catalogs():
    rows = {}
    for stamp, cat in [('2026-11-11','catalog-complete.json'),('2026-11-12-two-directions','catalog.json')]:
        root = WORKSPACE/'docs/video-references'/stamp
        for item in json.loads((root/cat).read_text(encoding='utf-8')):
            rows[item['id']] = {'metadata': item, 'folders': [root/item['id']], 'catalog': root/cat}
    root = WORKSPACE/'docs/video-references/2026-11-13-user-samples'
    for metadata in sorted(root.glob('*/metadata.json')):
        item = json.loads(metadata.read_text(encoding='utf-8'))
        if item['id'] in rows:
            rows[item['id']]['folders'].append(metadata.parent)
        else:
            rows[item['id']] = {'metadata': item, 'folders': [metadata.parent], 'catalog': metadata}
    return rows


def main():
    OUT.mkdir(exist_ok=True)
    inventory=[]
    for vid, record in read_catalogs().items():
        m=record['metadata']; folder=record['folders'][-1]
        media = next((folder/name for name in ['reference-av.mp4','reference.mp4'] if (folder/name).exists()), None)
        transcript = folder/'transcript.json'
        captions = json.loads(transcript.read_text(encoding='utf-8')) if transcript.exists() else []
        duration=float(m['duration'])
        cap_end=max((r['start']+r.get('duration',r.get('end',r['start'])-r['start']) for r in captions),default=0)
        intervals=[]
        if captions:
            for r in captions:
                a=float(r['start']); b=a+float(r.get('duration',0))
                if intervals and a<=intervals[-1][1]: intervals[-1][1]=max(intervals[-1][1],b)
                else: intervals.append([a,b])
        probe={}
        if media:
            cap=cv2.VideoCapture(str(media)); fps=cap.get(cv2.CAP_PROP_FPS); count=cap.get(cv2.CAP_PROP_FRAME_COUNT); cap.release()
            proc=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-i',str(media)],capture_output=True,text=True,encoding='utf-8',errors='replace')
            probe={'video_duration_from_frame_metadata':round(count/fps,3) if fps else None,
                   'video_frames_metadata':int(count),'fps_metadata':fps,
                   'has_audio_stream':bool(re.search(r'Stream .*Audio:',proc.stderr)),
                   'method':'container/stream metadata only; no fresh full decode or AV viewing'}
        source={'id':vid,'url':m.get('url',f'https://www.youtube.com/watch?v={vid}'),
                'title':m.get('title'),'channel':m.get('channel'),
                'declared_duration':duration, 'metadata_source':rel(record['catalog']),
                'metadata_source_sha256':sha(record['catalog']),
                'transcript_path':rel(transcript) if transcript.exists() else None,
                'transcript_sha256':sha(transcript) if transcript.exists() else None,
                'media_path':rel(media) if media else None,
                'media_sha256':sha(media) if media else None}
        rec={'source':source,'alternate_local_folders':[rel(f) for f in record['folders']],
             'local_media':{'present':media is not None,'scope':'full-duration local file' if media and probe.get('video_duration_from_frame_metadata',0)>=duration-2 else 'needs_check',**probe},
             'captions':{'segments':len(captions),'start':min((r['start'] for r in captions),default=0),'end':cap_end,
                         'timed_interval_union_seconds':round(sum(b-a for a,b in intervals),3),
                         'scope':'full-timeline caption file; no assumption that every spoken word is correct or present',
                         'rolling_overlap_note':'YouTube rows overlap; sum of durations is not speech duration.'},
             'official_chapters':m.get('chapters'), 'chapter_interpretation':'metadata chapters separate from agent-inferred content chapters',
             'fresh_download':False,'download_note':'Full local media already exists; no redundant download made.',
             'continuous_av_review':False,'audio_listening':False}
        if vid in DEEP:
            notes=DEEP[vid]
            study={'schema':'reference-content-analysis/1','source':source,
                   'coverage':{'method':'full_caption_read', 'reviewed_start':rec['captions']['start'],
                      'reviewed_end':cap_end,'caption_full_read':True,'continuous_av_review':False,
                      'audio_listening':False,'visual_method':'existing sparse contact sheet inspected' if vid in ['29B8-FtuC6U','5zqAMK2qsfM','5uTC396kCs4'] else 'no new visual review'},
                   'chapter_source':'agent-inferred semantic sections from caption; not official chapters or frame-accurate cuts',
                   'central_question':notes['spine'],'chapters':notes['chapters'],
                   'observations':notes['observations'],
                   'transferable_rules':[{'reference_interval':a,'rule':b,'status':'editorial observation; not user-approved production lesson'} for a,b in notes['rules']],
                   'factual_validation':'not performed; all claims/examples describe what source narrator says, not verified facts'}
            write(OUT/'analyses'/f'{vid}.json',study)
            lines=[f"# {source['title']}",'',f"Nguồn: [{source['channel']}]({source['url']}) · ID `{vid}`",'',
                   f"Trục câu hỏi: {notes['spine']}",'',
                   f"Phạm vi: đọc toàn caption {rec['captions']['start']:.2f}–{cap_end:.2f}s. Phân chương do agent suy luận, không phải chapters chính thức hoặc cut chính xác. Chưa xem/nghe liên tục. Các số liệu/sự kiện là lời người kể chưa xác minh.",'']
            for c in notes['chapters']:
                lines += [f"## {c['start']:.2f}–{c['end']:.2f}s · {c['title']}",'',
                  f"**Câu hỏi:** {c['question']}",f"\n**Ý chính:** {c['claim']}",f"\n**Ví dụ/lời nguồn:** {c['evidence_example']}",
                  f"\n**Cơ chế:** {c['mechanism']}",f"\n**Cách chuyển:** {c['transition']}",
                  f"\n**Điều nhận được:** {c['payoff']}",f"\n**Điểm cần nhấn / giới hạn:** {c['emphasis']}",'']
            lines+=['## Quan sát và phần không nên học','']+[f'- {x}' for x in notes['observations']]+['','## Quy tắc có thể dùng lại','']+[f'- {a}s: {b}' for a,b in notes['rules']]
            (OUT/'analyses'/f'{vid}.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
            rec['session_review']={'method':'full_caption_read','analysis_path':rel(OUT/'analyses'/f'{vid}.json'),
                                   'caption_full_read':True,'continuous_av_review':False}
        elif vid in MINI:
            genre, note, rule=MINI[vid]
            rec['session_review']={'method':'sampled_caption_read','caption_full_read':False,
               'intervals':[[0,55],[duration/2,duration/2+40],[duration-55,duration]],
               'genre':genre,'observations':note,'transferable_rule':rule,
               'scope_limit':'Only these caption windows read this session; intervening content not deeply analyzed; no AV listening.'}
            rec['caption_evidence']=[{'start':r['start'],'duration':r['duration'],'text':r['text']} for r in captions
                if any(a<=r['start']<b for a,b in rec['session_review']['intervals'])]
        else:
            rec['session_review']={'method':'inventory_only_in_this_worker','caption_full_read':False,
                                  'note':'Four user-supplied Lóng videos assigned to sibling analysis workers; root must verify their reports separately.'}
        inventory.append(rec)
    report={'schema':'reference-library-review/1','date':'2026-11-14','scope':'Existing downloaded YouTube reference library, 11/11 + 12/11 + four user samples 13/11, deduplicated by video ID.',
      'unique_videos':len(inventory),'channels':sorted({r['source']['channel'] for r in inventory}),
      'full_caption_reads_this_worker':list(DEEP), 'sampled_caption_reads_this_worker':list(MINI),
      'new_downloads':0,'continuous_av_review':False,'audio_listening':False,
      'fresh_inventory_method':'File existence/hash, OpenCV frame-count/fps metadata and FFmpeg stream header; no new full decode.',
      'global_limits':['Full local media does not mean it was watched or listened to.',
        'Source narrator claims remain unverified. This report studies content structure, not financial/legal accuracy.',
        'No audience-retention data is available; cannot prove which storytelling feature caused retention.',
        'Rows and chapters do not prove the source video is good or that a future production is approved.'],
      'videos':inventory}
    write(OUT/'library-review.json',report)
    lines=['# Thư viện tham khảo và phạm vi đọc lại — 14/11/2026','',
       f"Đã kiểm kê **{len(inventory)} ID riêng biệt** thuộc {len(report['channels'])} kênh; các bản trùng ID được giữ ở alternate_local_folders. Tất cả đã có file media toàn thời lượng, nên không tải trùng. Kiểm lần này là metadata stream + hash, không phải giải mã lại hay xem/nghe toàn bộ.",'',
       'Đọc toàn caption 5 video trong worker này (3 THE HIDDEN SELF, 2 Lóng). Với 14 video cũ còn lại chỉ đọc cửa sổ đầu 0–55s, giữa 40s và cuối 55s. Bốn mẫu Lóng người dùng gửi ngày 13/11 được phân công phân tích riêng. Không tự cộng phạm vi của worker khác khi chưa nhận và đối chiếu báo cáo.','',
       '**Chỉnh danh tính:** JlfAd_OaFek (AI) và podWgLH4b3M (Shein) là **Lóng**, không phải THE HIDDEN SELF. Nguồn metadata nằm ngay trong JSON.','',
       '| ID | Kênh | Thời lượng metadata | Phạm vi đọc lần này |','|---|---|---:|---|']
    for r in inventory:
        s=r['source']; mode=r['session_review']['method']
        label={'full_caption_read':'Toàn caption, có phân chương','sampled_caption_read':'Caption đầu/giữa/cuối','inventory_only_in_this_worker':'Kiểm kê; phân công worker khác'}[mode]
        lines.append(f"| [{s['id']}]({s['url']}) | {s['channel']} | {s['declared_duration']:.0f}s | {label} |")
    lines+=['','## Phân tích sâu có thể kiểm lại','']
    for vid in DEEP:
        src=next(r['source'] for r in inventory if r['source']['id']==vid)
        lines.append(f"- [{src['title']}](analyses/{vid}.md): {DEEP[vid]['spine']}")
    lines+=['','## Các cửa sổ caption của 14 nguồn còn lại','',
      'Đây là đối chiếu chọn đoạn, không phải kết luận về toàn bộ kịch bản. Timestamps và câu gốc đầy đủ nằm trong caption_evidence của library-review.json. Không sao chép các dự báo tài chính/quy định pháp luật của nguồn làm sự thật.','']
    for vid,(genre,note,rule) in MINI.items():
        src=next(r['source'] for r in inventory if r['source']['id']==vid)
        lines += [f"### {src['channel']} · {vid} · {genre}",'',note,'',f"**Dùng lại / loại bỏ:** {rule}",'']
    lines+=['## Khác biệt cần giữ giữa các nhóm','',
      '- **Lóng:** trường hợp/đối tượng cụ thể → cách vận hành → điều kiện đổi → phương án → quan điểm kết. Lời dẫn thân mật không thay cho luận cứ. Phần tài trợ cần gắn nhãn riêng.',
      '- **THE HIDDEN SELF:** mâu thuẫn/ẩn dụ → các tầng cơ chế hay các nhóm phân loại → quay về câu hỏi đầu. Có thể học tổ chức luận điểm, nhưng tránh độ tuyệt đối, lời hứa kết quả và ẩn dụ dài; không lấy mic/waveform lặp làm default.',
      '- **Giao Lộ Chính Sách:** chia quyền lợi/đề xuất/nhóm đối tượng và việc cần kiểm tra. Có chapters chính thức, nhưng tiêu đề chương không tự bảo đảm trọng tâm; phân biệt dự thảo với luật có hiệu lực và kiểm nguồn cơ quan gốc khi làm chủ đề thật.',
      '- **Bí mật kinh doanh:** xung đột cơ hội/rủi ro và ví dụ dòng tiền làm stakes dễ hiểu. Tránh sao chép giật tít tận thế, lịch chu kỳ như tiên tri, CTA bình luận đã xem cuối hoặc lời phân bổ tài sản không có điều kiện.','',
      '## Điều thay đổi trong cách viết mới','',
      '1. Một video có một câu hỏi chính và một câu trả lời của tác giả. Chỉ thêm phần mới nếu nó giải một mắt xích còn thiếu.',
      '2. Mỗi phần ghi rõ câu hỏi → một luận điểm → ví dụ/bằng chứng → vì sao dẫn tới kết quả → giới hạn → câu chốt → lý do chuyển phần.',
      '3. Đọc riêng các câu chốt theo thứ tự: chúng phải tạo được một lập luận hoàn chỉnh. Nếu đổi chỗ tùy ý vẫn như nhau, cần xem lại quan hệ giữa các phần.',
      '4. Lập chỗ nhấn nghĩa trước chỗ nhấn âm/hình: đối chiếu gì, con số nào đổi kết luận, điều gì người xem cần nhớ. Chưa nghe mẫu thì không khẳng định đã học nhấn giọng của người kể.',
      '5. Kết trả lời lời hứa đầu và thêm một kết luận rút ra từ các phần; CTA là một hành động cụ thể hợp chủ đề.','',
      'Không có dữ liệu retention, không kiểm chứng mọi claim của kênh, không xác nhận đã xem/nghe liên tục. Hồ sơ này là nghiên cứu biên tập có giới hạn; chưa phải duyệt video mới của người dùng.']
    (OUT/'LIBRARY_REVIEW.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'unique_videos':len(inventory),'full_caption_reads_this_worker':len(DEEP),'sampled_caption_reads_this_worker':len(MINI),
       'full_media':sum(x['local_media']['scope']=='full-duration local file' for x in inventory),
       'audio_streams':sum(x['local_media'].get('has_audio_stream',False) for x in inventory),'output':rel(OUT/'library-review.json')},ensure_ascii=False))


if __name__=='__main__': main()
