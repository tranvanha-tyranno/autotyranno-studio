"""Original continuous bakery story for the user's complete documentary rewrite.

All money is an illustrative model. Stock is context, never the fictional Hanh.
No standalone disclaimer, on-screen presenter, subtitle or invented branding.
"""


def unit(uid, text, tags, **visual):
    return {'id': uid, 'text': text, 'tags': tags.split(','), **visual}


CONTENT = {
    'title': 'Lạm phát giảm, vì sao ổ bánh mì vẫn đắt?',
    'centralQuestion': 'Vì sao lạm phát hạ mà người mua lẫn tiệm bánh vẫn thấy khó hơn?',
    'thesis': 'Giảm tốc tăng giá không xóa mặt bằng giá đã tăng; phần tiệm giữ lại phụ thuộc tổng chi phí, còn sức mua phụ thuộc cả thu nhập.',
    'chapters': [
        {'id': 'hai-nghin-di-dau', 'title': 'Hai nghìn đồng đã đi đâu?', 'question': 'Khách trả thêm có nghĩa chủ tiệm lời hơn không?',
         'answer': 'Trong mô hình, chi phí tăng nhiều hơn giá bán nên phần còn lại giảm.',
         'mechanism': 'Giá bán tăng 2.000 nhưng chi phí biến đổi tăng 2.500, giữ phân bổ cố định và lượng bán giả định không đổi.',
         'takeaway': 'Khách trả thêm không đồng nghĩa người bán giữ lại thêm.',
         'example': '20.000 - 12.000 - 5.000 = 3.000; 22.000 - 14.500 - 5.000 = 2.500, chưa phải lợi nhuận ròng.',
         'nextQuestion': 'Vì sao tin lạm phát giảm chưa làm giá trở lại?',
         'bridgeReason': 'Hóa đơn giải thích sức ép của tiệm, nhưng chưa giải thích chữ giảm trong bản tin mà khách đang chờ.',
         'units': [
             unit('b01', 'Ổ bánh tăng hai nghìn. Nhưng người bán lại giữ được ít hơn năm trăm đồng. Khách thấy đắt, chủ tiệm cũng thấy hụt. Trong khi đó, bản tin bảo lạm phát đã giảm. Vì sao cả hai vẫn thấy khó hơn?', 'bread,payment', phase='hook', headline='Lạm phát giảm. Sao vẫn khó hơn?'),
             unit('b02', 'Thử theo một ngày ở tiệm bánh giả định của chị Hạnh. Ta đặt các con số đơn giản vào tiệm này để lần theo số tiền vừa tăng. Chìa khóa nằm ở ba thứ thường bị nhìn riêng: bảng giá, hóa đơn đầu vào, và tiền người mua kiếm được.', 'bakery,receipt', phase='content'),
             unit('b03', 'Trước lần đổi bảng, một ổ bán hai mươi nghìn. Nguyên liệu và những khoản thay đổi theo lượng bánh hết mười hai nghìn. Tiền thuê cùng chi phí cố định được chia ra năm nghìn một ổ, ở lượng bán đang giả định. Còn ba nghìn.', 'bread,ingredients', kind='cost_stack', data={'stage':'before','price':20000,'variable':12000,'fixed':5000,'remaining':3000}),
             unit('b04', 'Khoan gọi ba nghìn ấy là tiền bỏ túi. Mô hình còn chưa tính đủ thuế, khấu hao và công của chủ tiệm. Cứ giữ cách tính ấy để so trước với sau, rồi nhìn hóa đơn mới chị Hạnh vừa nhận.', 'receipt,bakery'),
             unit('b05', 'Cùng một ổ bánh, phần chi phí biến đổi giờ thành mười bốn nghìn năm trăm. Nếu giữ giá cũ, khoảng còn lại chỉ còn năm trăm đồng. Chị Hạnh đổi bảng lên hai mươi hai nghìn. Khách trả thêm hai nghìn; nhưng đầu vào đã tăng hai nghìn năm trăm.', 'ingredients,receipt', kind='cost_stack', data={'stage':'after','price':22000,'variable':14500,'fixed':5000,'remaining':2500}),
             unit('b06', 'Kết quả: từ ba nghìn, tiệm chỉ còn hai nghìn năm trăm trên một ổ. Hai nghìn tăng thêm không biến mất. Nó chưa bù hết phần chi phí tăng. Giá bán đi lên mà khoảng dư vẫn co lại. Chỉ nhìn tấm bảng, khách không thể biết điều đó.', 'payment,receipt', kind='cost_stack', data={'stage':'compare','price':22000,'variable':14500,'fixed':5000,'remaining':2500}, emphasis='Trả thêm ≠ giữ lại thêm'),
             unit('b07', 'Đấy là chuyện của tiệm trong ví dụ. Tiệm khác có thể giữ giá, giảm phần dư, hoặc tăng được lãi; muốn kết luận phải có sổ thật. Nhưng người khách vẫn có lý do để hỏi chị Hạnh: nếu lạm phát đang giảm, tại sao bảng giá không quay về hai mươi nghìn?', 'bakery,bread', headline='Nhưng bản tin nói “giảm” mà?'),
         ]},
        {'id': 'giam-cai-gi', 'title': '“Giảm” — nhưng giảm cái gì?', 'question': 'Vì sao giảm lạm phát không đồng nghĩa bánh rẻ lại?',
         'answer': 'Tỷ lệ tăng dương nhỏ hơn vẫn làm giá tăng từ mặt bằng đã cao.',
         'mechanism': 'Cùng lượng/chất lượng, 20.000 tăng10% thành22.000 rồi tăng2% thành22.440. Một món chỉ minh họa, không phải CPI.',
         'takeaway': 'Bản tin nói tốc độ; người mua đang chịu mặt bằng giá.',
         'example': 'Chuỗi 20.000 ->22.000 ->22.440 là phép tính minh họa, không giá hiện hành.',
         'nextQuestion': 'Nếu hóa đơn bột giảm thật thì sao?',
         'bridgeReason': 'Phân biệt tỷ lệ và mức giá trả lời bản tin nhưng không trả lời động lực hạ giá của tiệm.',
         'units': [
             unit('b08', 'Hãy giữ đúng chiếc bánh ấy, cùng lượng nhân và kích cỡ. Từ hai mươi lên hai mươi hai nghìn là tăng mười phần trăm. Nếu kỳ sau chỉ tăng hai phần trăm, bánh không trở lại hai mươi nghìn. Nó thành hai mươi hai nghìn bốn trăm bốn mươi đồng trong phép tính.', 'bread,bakery', kind='price_path', data={'values':[20000,22000,22440],'rates':[10,2]}),
             unit('b09', 'Tỷ lệ đã hạ từ mười xuống hai. Số tiền phải trả vẫn tăng. Đây là chỗ lời nói và kỳ vọng dễ đi lệch nhau: bản tin nói tốc độ tăng chậm lại, còn khách đang chờ giá hạ xuống. Hai việc ấy khác nhau.', 'payment,bread', kind='price_path', data={'values':[20000,22000,22440],'rates':[10,2]}, emphasis='Tăng chậm hơn vẫn là tăng'),
             unit('b10', 'Một ổ bánh không đại diện cho lạm phát cả nước. Chỉ số chung nhìn một rổ nhiều hàng hóa và dịch vụ. Chiếc bánh ở đây chỉ giúp ta thấy phép tính: mức tăng mới có thể nhỏ, nhưng nó cộng lên phần giá đã tăng từ trước.', 'market,bread'),
             unit('b11', 'Vì thế, chị Hạnh không thể nghe một tỷ lệ lạm phát thấp hơn rồi tự suy ra bao bột, tiền thuê và tiền điện của mình đã về giá cũ. Nhưng nếu có một hóa đơn thực sự giảm thì sao? Chẳng hạn, bột mua cho mẻ bánh mới đã rẻ hơn. Lúc ấy khách có được chờ bánh rẻ lại không?', 'flour,receipt', headline='Bột rẻ lại. Bánh có rẻ theo?'),
         ]},
        {'id': 'hoa-don-nao-giam', 'title': 'Một hóa đơn giảm chưa đủ', 'question': 'Khi nào giảm chi phí thật sự có thể dẫn tới giảm giá bán?',
         'answer': 'Phải nhìn tổng chi phí, độ trễ và cạnh tranh, không chỉ một đầu vào; lợi nhuận cũng có thể tăng.',
         'mechanism': 'Bột mua mới khác lô tồn; thuê, lương còn hợp đồng; tổng chi phí giảm và khách có lựa chọn thay thế có thể ép giá bán.',
         'takeaway': 'Không bênh hay kết tội chủ tiệm chỉ từ một tờ hóa đơn.',
         'example': 'Cùng tiệm Hạnh: hóa đơn bột mới giảm nhưng các khoản khác không tự đổi; phản ví dụ tổng chi phí giảm.',
         'nextQuestion': 'Bánh chưa rẻ, tăng lương có đủ để người mua dễ thở hơn không?',
         'bridgeReason': 'Quyết định giá của tiệm chưa cho biết sức mua của khách; phải nối sang khoản thu của chính người mua bánh.',
         'units': [
             unit('b12', 'Chị Hạnh mở kho. Bao bột đang dùng có thể thuộc lô mua trước, giá cao. Hóa đơn mới thấp hơn chưa đổi ngay giá vốn của mẻ bánh hôm nay. Đấy là một độ trễ có thể có, không phải lý do mặc định cho mọi tiệm.', 'flour,storage'),
             unit('b13', 'Rồi chị đặt hóa đơn bột cạnh các khoản khác. Tiền thuê vẫn theo hợp đồng. Lương người phụ bán đã thỏa thuận. Điện, nhân bánh, bao bì có thể đi theo hướng khác. Một dòng giảm chưa có nghĩa tổng chi phí của chiếc bánh đã trở lại như trước.', 'receipt,ingredients'),
             unit('b14', 'Nhưng nói đến đây rồi dừng sẽ là bênh người bán quá dễ. Ta phải hỏi ngược: nếu tổng chi phí đã giảm thật, lượng bán vẫn như cũ, mà chị Hạnh giữ giá, thì sao? Khoảng dư có thể tăng. Không có quy luật nào bảo mọi cửa hàng luôn phải chịu thiệt.', 'payment,bakery', emphasis='Chi phí giảm, khoảng dư có thể tăng'),
             unit('b15', 'Lúc này người khách có vai trò. Nếu bên cạnh có bánh tương đương, rẻ hơn và dễ mua, chị Hạnh phải cân nhắc mất khách. Nếu khách khó chuyển chỗ mua, sức ép ấy có thể yếu hơn. Giá bán còn là kết quả của lựa chọn và cạnh tranh, không chỉ phép cộng trên hóa đơn.', 'shop,market'),
             unit('b16', 'Vậy câu hỏi đúng không phải: bột giảm rồi, sao chị chưa giảm? Mà là: tổng chi phí đã đổi bao nhiêu, và khách có lựa chọn nào? Ta vừa nhìn được hai phía của quầy. Còn một phía nữa: chiếc ví của người mua.', 'receipt,payment', headline='Còn người mua thì sao?'),
         ]},
        {'id': 'luong-mua-bao-nhieu-banh', 'title': 'Lương tăng, mua được bao nhiêu bánh?', 'question': 'Vì sao nhận nhiều tiền hơn mà mua cùng bữa sáng vẫn khó hơn?',
         'answer': 'Sức mua phụ thuộc tỷ lệ thu nhập tăng so với giá của cùng lượng hàng; bread is only a yardstick.',
         'mechanism': 'Thu nhập10triệu->10,5triệu(+5%); bánh20nghìn->22nghìn(+10%); số ổ tương đương500->477,27(-4,55%). Không giả định chi toàn lương cho bánh.',
         'takeaway': 'Tờ lương tăng chưa bảo đảm cùng lượng hàng dễ mua hơn.',
         'example': 'Cùng giá bánh 20.000/22.000 từ chương1, dùng làm thước so thu nhập minh họa, không tính CPI hay giỏ hộ trung bình.',
         'nextQuestion': 'Đọc tin lạm phát giảm thì nên kiểm những gì?',
         'bridgeReason': 'Đã đủ giá, chi phí và thu nhập để trả lời hook và rút một cách đọc cụ thể thay vì thêm giáo trình.',
         'units': [
             unit('b17', 'Quay lại đúng kỳ chiếc bánh tăng từ hai mươi lên hai mươi hai nghìn. Giả sử thu nhập của người phụ bán cũng tăng trong kỳ ấy: từ mười triệu lên mười triệu rưỡi, tức năm phần trăm. Anh nhận nhiều tiền hơn, nhưng giá bữa sáng đã tăng nhanh hơn lương.', 'bakery,payment', kind='purchasing_power', data={'stage':'income','incomeBefore':10000000,'incomeAfter':10500000,'priceBefore':20000,'priceAfter':22000}),
             unit('b18', 'Thử dùng chính chiếc bánh làm thước đo nhỏ. Mười triệu tương đương năm trăm ổ giá cũ. Mười triệu rưỡi chỉ tương đương khoảng bốn trăm bảy mươi bảy ổ giá mới. Không ai cần đem toàn bộ lương đi mua bánh. Phép so chỉ hỏi: thu nhập mỗi kỳ đổi được bao nhiêu chiếc bánh cùng loại?', 'bread,payment', kind='purchasing_power', data={'stage':'quantity','before':500,'after':477.2727,'change':-4.54545}),
             unit('b19', 'Tiền lương tăng, sức mua tính riêng bằng bánh lại giảm khoảng bốn phẩy năm phần trăm. Vẫn chiếc bánh ấy, vẫn lần đổi bảng ấy. Nhìn từ quầy bán, khoảng dư của chị Hạnh co lại. Nhìn từ người làm công, tờ lương tăng mà số bánh mua được cũng ít đi.', 'bread,bakery', kind='purchasing_power', data={'stage':'result','before':500,'after':477.2727,'change':-4.54545}, emphasis='Nhiều tiền hơn, ít bánh hơn'),
             unit('b20', 'Đời sống thật không chỉ có bánh mì. Người phụ bán còn tiền nhà, đi lại và nhiều khoản khác. Muốn biết sức mua cả gia đình, phải nhìn giá của cùng một giỏ chi tiêu với lượng và chất lượng tương đương. Một ổ bánh là cửa vào để hiểu, không phải chiếc máy đo toàn bộ đời sống.', 'market,groceries'),
             unit('b21', 'Nếu những khoản anh mua nhiều tăng nhanh, anh có thể thấy áp lực hơn con số bình quân. Nhà khác chi tiêu khác thì trải nghiệm cũng khác. Vì vậy, cảm giác thiếu tiền không tự chứng minh bản tin sai; còn tỷ lệ lạm phát thấp hơn cũng không bảo đảm chiếc ví nào đã nhẹ gánh.', 'groceries,payment'),
         ]},
        {'id': 'tro-lai-quay-banh', 'title': 'Đặt ba thứ cạnh nhau', 'question': 'Câu trả lời cuối cho nghịch lý mở đầu là gì?',
         'answer': 'Bản tin đo tốc độ giá; tiệm chịu tổng chi phí và cạnh tranh; người mua chịu giá tích lũy tương quan thu nhập.',
         'mechanism': 'Callback đúng các kết quả đã giải, không thêm ví dụ độc lập hay chương chính sách.',
         'takeaway': 'Đọc cùng bảng giá, hóa đơn và khoản thu để hiểu sức ép từng phía.',
         'example': 'Trở lại đúng một tiệm, một lần tăng giá, một người làm công và chiếc bánh xuyên suốt.',
         'units': [
             unit('b22', 'Trở lại buổi sáng ở tiệm Hạnh. Khách trả thêm hai nghìn không có nghĩa chị giữ thêm hai nghìn. Tin lạm phát giảm không có nghĩa giá trở lại mốc cũ. Và lương tăng không tự bảo đảm mua được nhiều hơn. Ba điều ấy có thể cùng đúng, chẳng cần mâu thuẫn nào cả.', 'bread,bakery', emphasis='Giá bán · chi phí · sức mua'),
             unit('b23', 'Lần tới nghe lạm phát hạ, hãy hỏi: đang tăng chậm hơn hay giảm giá thật? So với mốc nào? Và thu nhập của mình có theo kịp những khoản mình thực sự mua không? Bắt đầu từ một bữa sáng quen, nhưng so cùng lượng, cùng chất lượng. Đừng chỉ nhìn con số to nhất trên bản tin.', 'bread,receipt'),
             unit('b24', 'Ở chỗ bạn, món ăn sáng nào tăng giá rõ nhất, và bạn đang so với năm nào? Hãy để lại một ví dụ cụ thể trong bình luận. Nếu muốn xem thêm những câu chuyện kinh tế được bóc từ đời sống như thế này, hãy đăng ký kênh và bật chuông.', 'bread,shop', phase='cta', headline='Bữa sáng của bạn đã đổi thế nào?'),
         ]},
    ],
}
