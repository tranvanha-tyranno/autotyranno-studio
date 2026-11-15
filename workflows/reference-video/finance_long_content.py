"""Original narration; all people, prices and amounts are fictional teaching examples."""

CONTENT = {'title': 'Lương tăng mà vẫn hết tiền: sửa dòng tiền trong 30 ngày',
 'chapters': [{'id': 'nghich-ly',
               'title': 'Tiền tăng, khoản dư đứng yên',
               'beats': [{'id': 'b01',
                          'kind': 'hook',
                          'headline': 'Tăng 2 triệu. Dư vẫn 2 triệu.',
                          'text': 'Lương tăng hai triệu. Cuối tháng, tiền dư vẫn hai triệu. Minh nhìn ví, rồi '
                                  'nhìn thông báo tăng lương: tiền vừa vào đã biết đường trốn? Đặt hai tháng cạnh '
                                  'nhau, xem từng đồng đã nhận công việc gì.',
                          'cue': 'tiền dư vẫn hai triệu',
                          'data': {'raise': 2000000, 'surplus': 2000000}},
                         {'id': 'b02',
                          'kind': 'disclaimer',
                          'headline': 'MIỄN TRỪ TRÁCH NHIỆM',
                          'text': 'Minh, Lan và toàn bộ số tiền là ví dụ giả định. Video giúp hiểu cách lập kế '
                                  'hoạch chi tiêu, không phải tư vấn tài chính cá nhân. Hãy điều chỉnh theo hoàn '
                                  'cảnh thực tế.',
                          'cue': 'ví dụ giả định',
                          'data': {'illustrative': True}},
                         {'id': 'b03',
                          'kind': 'audit',
                          'headline': 'Đừng tìm một món đồ thật lớn',
                          'text': 'Minh quả quyết không mua điện thoại, cũng chẳng đi du lịch. Lan mở lịch sử chi '
                                  'tiêu, kéo những tờ hóa đơn nhỏ ra bàn. Từng khoản khó giải thích cả tháng, '
                                  'nhưng cộng lại thì khác.',
                          'cue': 'những tờ hóa đơn nhỏ',
                          'data': {'action': 'spread_receipts'}},
                         {'id': 'b04',
                          'kind': 'choice',
                          'headline': 'Tăng lương để sống tốt hơn',
                          'text': 'Tăng lương rồi sống thoải mái hơn không có gì sai. Nhưng Minh muốn có khoảng '
                                  'thở lúc xe hỏng, trong khi phần tăng thu nhập chưa từng được dành cho việc đó. '
                                  'Mọi khoản tăng đã trở thành thói quen.',
                          'cue': 'lúc xe hỏng',
                          'data': {'action': 'repair_vs_treat'}},
                         {'id': 'b05',
                          'kind': 'review',
                          'headline': 'Một câu hỏi cho cả video',
                          'text': 'Sửa thế nào để không biến cuộc sống thành cuộc thi chịu khổ? Đi từ hai chiếc '
                                  'phong bì tới một tháng hóa đơn, rồi làm kế hoạch ba mươi ngày. Nhìn rõ lựa '
                                  'chọn, trước khi quyết định giữ hay đổi.',
                          'cue': 'hai chiếc phong bì',
                          'data': {'days': 30}}]},
              {'id': 'hai-ngan-sach',
               'title': 'Hai tháng đặt cạnh nhau',
               'beats': [{'id': 'b06',
                          'kind': 'budget_before',
                          'headline': '12 − 10 = 2 triệu',
                          'text': 'Tháng đầu, Minh có thu nhập mười hai triệu, tổng chi mười triệu. Lấy mười hai '
                                  'trừ mười, còn hai triệu. Ta gọi đây là khoản dư của phép so sánh, chưa mặc '
                                  'định toàn bộ đều có thể đem tiêu.',
                          'cue': 'Lấy mười hai trừ mười',
                          'data': {'income': 12000000, 'expenses': 10000000, 'surplus': 2000000}},
                         {'id': 'b07',
                          'kind': 'budget_after',
                          'headline': '14 − 12 = 2 triệu',
                          'text': 'Tháng mới, lương mười bốn triệu, tổng chi mười hai triệu. Lấy mười bốn trừ '
                                  'mười hai, vẫn còn hai triệu. Hai chiếc phong bì đều phình ra, riêng phần dư ở '
                                  'giữa vẫn nguyên kích thước.',
                          'cue': 'Lấy mười bốn trừ mười hai',
                          'data': {'income': 14000000, 'expenses': 12000000, 'surplus': 2000000}},
                         {'id': 'b08',
                          'kind': 'budget_after',
                          'headline': 'Phần tăng đã có nơi để đi',
                          'text': 'Không có tiền bí ẩn biến mất. Phần tăng lương đã chuyển sang phần chi thêm. '
                                  'Nhìn con số lương, Minh thấy mình khá hơn. Nhìn cả hai phía phép trừ, cậu hiểu '
                                  'vì sao cuối tháng vẫn như cũ.',
                          'cue': 'chuyển sang phần chi thêm',
                          'data': {'raise': 2000000, 'extraExpense': 2000000}},
                         {'id': 'b09',
                          'kind': 'essentials',
                          'headline': 'Chi tăng có nhiều nguyên nhân',
                          'text': 'Nhưng đừng vội dán nhãn hoang phí. Tiền nhà có thể tăng, người thân cần hỗ '
                                  'trợ, công việc mới tốn thêm đi lại. Những việc đó khác với mua thêm vì thấy '
                                  'tài khoản nhiều tiền. Cách sửa phụ thuộc nguyên nhân thật.',
                          'cue': 'Tiền nhà có thể tăng',
                          'data': {'categories': ['nhà ở', 'gia đình', 'đi lại']}},
                         {'id': 'b10',
                          'kind': 'audit',
                          'headline': 'Gắn nhãn trước khi cắt giảm',
                          'text': 'Lan đặt hai nhãn: cần thiết và có thể lựa chọn. Minh kéo từng hóa đơn vào chỗ '
                                  'phù hợp, để nhóm chưa rõ kiểm sau. Họ phân biệt phần buộc phải gánh với phần '
                                  'có thể thương lượng.',
                          'cue': 'kéo từng hóa đơn',
                          'data': {'action': 'sort_receipts'}}]},
              {'id': 'khoan-nho',
               'title': 'Khoản nhỏ gặp lịch tháng',
               'beats': [{'id': 'b11',
                          'kind': 'daily',
                          'headline': '60.000 nhìn rất nhỏ',
                          'text': 'Trong ví dụ này, Minh chi thêm sáu mươi nghìn mỗi ngày so với trước. Đó là '
                                  'tổng phần nâng cấp nhỏ, không phải giá một món cụ thể. Tờ hóa đơn mỏng đến mức '
                                  'cậu gần như không coi nó là quyết định.',
                          'cue': 'chi thêm sáu mươi nghìn',
                          'data': {'daily': 60000, 'days': 30, 'total': 1800000}},
                         {'id': 'b12',
                          'kind': 'daily',
                          'headline': '60.000 × 30 = 1,8 triệu',
                          'text': 'Lan đưa hóa đơn qua ba mươi ô lịch. Sáu mươi nghìn nhân ba mươi bằng một triệu '
                                  'tám. Phép tính không kết tội ly nước nào. Nó đổi góc nhìn: lựa chọn lặp lại '
                                  'cần được đánh giá bằng tổng tháng.',
                          'cue': 'qua ba mươi ô lịch',
                          'data': {'daily': 60000, 'days': 30, 'total': 1800000}},
                         {'id': 'b13',
                          'kind': 'dinner',
                          'headline': 'Thêm 200.000: vừa đủ 2 triệu',
                          'text': 'Thêm một bữa ăn hai trăm nghìn ngoài mức chi cũ. Một triệu tám cộng hai trăm '
                                  'nghìn, vừa hết hai triệu tăng lương. Minh im một nhịp. Không có món đồ khổng '
                                  'lồ, nhưng chuỗi quyết định đứng cạnh nhau đã đủ lớn.',
                          'cue': 'Một triệu tám cộng hai trăm nghìn',
                          'data': {'dailyTotal': 1800000, 'dinner': 200000, 'total': 2000000}},
                         {'id': 'b14',
                          'kind': 'choice',
                          'headline': 'Giữ niềm vui, đổi tần suất',
                          'text': 'Minh có thể giữ khoản đáng tiền, hoặc đổi tần suất và mức nâng cấp. Một bữa '
                                  'gặp bạn có thể quan trọng hơn nhiều lần đặt thêm vì tiện. Không cần cắt đều '
                                  'mọi thứ.',
                          'cue': 'đổi tần suất',
                          'data': {'action': 'keep_or_reduce'}},
                         {'id': 'b15',
                          'kind': 'daily',
                          'headline': 'Giảm 20.000/ngày → 600.000',
                          'text': 'Thử bớt hai mươi nghìn mỗi ngày. Hai mươi nghìn nhân ba mươi bằng sáu trăm '
                                  'nghìn. Khoản khác giữ nguyên thì tổng chi còn mười một triệu tư, dư hai triệu '
                                  'sáu. Đây là kịch bản, không phải mức tiết kiệm bắt buộc.',
                          'cue': 'Hai mươi nghìn nhân ba mươi',
                          'data': {'dailyBefore': 60000,
                                   'dailyAfter': 40000,
                                   'days': 30,
                                   'saved': 600000,
                                   'expenses': 11400000,
                                   'surplus': 2600000}}]},
              {'id': 'kiem-tra',
               'title': 'Tìm dấu vết trên hóa đơn',
               'beats': [{'id': 'b16',
                          'kind': 'audit',
                          'headline': 'Đọc giao dịch, đừng đoán',
                          'text': 'Mở lịch sử giao dịch và ghi thêm tiền mặt dễ quên. Mỗi dòng cần ngày, khoản '
                                  'chi, số tiền và ghi chú ngắn. Minh dùng dữ liệu đang có, không chờ tìm ứng '
                                  'dụng hoàn hảo.',
                          'cue': 'ngày, khoản chi, số tiền',
                          'data': {'fields': ['ngày', 'khoản chi', 'số tiền', 'ghi chú']}},
                         {'id': 'b17',
                          'kind': 'audit',
                          'headline': 'Chuyển tiền chưa chắc là chi',
                          'text': 'Chuyển tiền giữa hai tài khoản của mình chưa phải chi mua hàng. Rút tiền mặt '
                                  'cũng chưa cho biết đã mua gì. Vừa tính lần rút, vừa tính lần dùng tiền mặt, '
                                  'một khoản có thể bị đếm hai lần.',
                          'cue': 'đếm hai lần',
                          'data': {'action': 'remove_duplicate_transfer'}},
                         {'id': 'b18',
                          'kind': 'review',
                          'headline': 'Khoản hoàn trả đứng riêng',
                          'text': 'Khoản bạn trả lại tiền ăn chung không tự thành thu nhập mới. Lan ghép khoản '
                                  'trả trước với khoản được hoàn lại. Hai dòng đứng cạnh nhau giúp Minh thấy phần '
                                  'nào thực sự thuộc chi tiêu của cậu.',
                          'cue': 'ghép khoản trả trước',
                          'data': {'action': 'match_reimbursement'}},
                         {'id': 'b19',
                          'kind': 'audit',
                          'headline': 'Khoản nào thực sự đáng tiền?',
                          'text': 'Minh đánh dấu: cần giữ, chưa chắc, và muốn đổi. Khoản nhỏ dùng mỗi ngày có thể '
                                  'hữu ích; món lớn mua rẻ lại nằm im. Họ đánh giá công dụng cùng tần suất, không '
                                  'chỉ nhìn giá.',
                          'cue': 'cần giữ, chưa chắc, và muốn đổi',
                          'data': {'labels': ['giữ', 'kiểm lại', 'đổi']}},
                         {'id': 'b20',
                          'kind': 'choice',
                          'headline': 'Chọn một thay đổi trước',
                          'text': 'Minh chọn một khoản để thử trong tuần tới: bớt một lần đặt thêm, hoặc kiểm '
                                  'dịch vụ đang trả tiền. Lời hứa sẽ tiết kiệm hơn khó đo. Một việc cụ thể có mốc '
                                  'kiểm lại thì dễ theo dõi.',
                          'cue': 'chọn một khoản',
                          'data': {'action': 'select_one_receipt'}}]},
              {'id': 'phi-lap-lai',
               'title': 'Khoản lặp lại và khoản theo năm',
               'beats': [{'id': 'b21',
                          'kind': 'recurring',
                          'headline': 'Tự trừ không có nghĩa tự cần',
                          'text': 'Dịch vụ tự trừ tiền, dù Minh chẳng nhớ lần cuối sử dụng. Lan đặt biểu tượng '
                                  'gia hạn lên lịch: tháng tới mình có chủ động mua lại không? Quyết định cũ vẫn '
                                  'chạy mà ít được xem lại.',
                          'cue': 'biểu tượng gia hạn lên lịch',
                          'data': {'action': 'inspect_subscription'}},
                         {'id': 'b22',
                          'kind': 'recurring',
                          'headline': '120.000 × 12 = 1,44 triệu',
                          'text': 'Dịch vụ giả định giá một trăm hai mươi nghìn mỗi tháng. Nhân mười hai tháng là '
                                  'một triệu bốn trăm bốn mươi nghìn. Nếu không cần, kiểm điều kiện hủy. Đừng coi '
                                  'tổng năm là tiền tiết kiệm ngay, khi khoản đã trả không được hoàn.',
                          'cue': 'Nhân mười hai tháng',
                          'data': {'monthly': 120000, 'months': 12, 'annual': 1440000}},
                         {'id': 'b23',
                          'kind': 'annual',
                          'headline': 'Không hằng tháng vẫn phải trả',
                          'text': 'Có khoản ít xuất hiện nên bị quên: bảo dưỡng, thay đồ dùng, nghĩa vụ định kỳ. '
                                  'Chưa tới hạn không nghĩa là bất ngờ. Minh đưa việc dự kiến lên một lịch riêng, '
                                  'tách khỏi sự cố chưa biết.',
                          'cue': 'lên một lịch riêng',
                          'data': {'action': 'annual_calendar'}},
                         {'id': 'b24',
                          'kind': 'annual',
                          'headline': '1,2 triệu/năm → 100.000/tháng',
                          'text': 'Khoản dự kiến một triệu hai cho cả năm tương đương một trăm nghìn mỗi tháng. '
                                  'Đây là ví dụ độc lập. Nhưng nếu hạn đã gần, chưa để dành gì, không thể chia '
                                  'mười hai rồi coi như chuẩn bị đủ.',
                          'cue': 'một trăm nghìn mỗi tháng',
                          'data': {'annual': 1200000, 'months': 12, 'monthly': 100000}},
                         {'id': 'b25',
                          'kind': 'buffer',
                          'headline': 'Tiền đã có việc thì chưa rảnh',
                          'text': 'Tiền nằm trong tài khoản có thể đã có việc cho tháng sau. Minh tách khoản dự '
                                  'trù vào phong bì có nhãn. Chuyển chỗ không làm cậu giàu thêm; nó giúp tránh '
                                  'tiêu nhầm tiền đã có nhiệm vụ.',
                          'cue': 'phong bì có nhãn',
                          'data': {'action': 'reserve_envelope'}}]},
              {'id': 'lich-dong-tien',
               'title': 'Đúng tổng nhưng lệch ngày',
               'beats': [{'id': 'b26',
                          'kind': 'calendar',
                          'headline': 'Dòng tiền có cả ngày đến hạn',
                          'text': 'Cả tháng vẫn dư nhưng giữa tháng thiếu. Ví dụ mới: tiền nhà đến hạn trước ngày '
                                  'lương về. Lan trải lịch, đặt tiền đúng ngày nhận, hóa đơn đúng ngày trả. Tổng '
                                  'tháng không tự dời được hạn.',
                          'cue': 'tiền nhà đến hạn trước ngày lương',
                          'data': {'action': 'place_income_and_due_dates'}},
                         {'id': 'b27',
                          'kind': 'calendar',
                          'headline': 'Trống tiền trước ngày nhận lương',
                          'text': 'Minh đi qua từng ngày, mang số dư hôm trước sang hôm sau. Khi hóa đơn xuất '
                                  'hiện trước tiền vào, đường tiền chạm đáy. Đây là vấn đề thời điểm. Muốn hiểu '
                                  'chỗ thiếu, phải xem diễn biến trên lịch.',
                          'cue': 'hóa đơn xuất hiện trước tiền vào',
                          'data': {'action': 'walk_calendar_balance'}},
                         {'id': 'b28',
                          'kind': 'buffer',
                          'headline': 'Tạo khoảng đệm khi có thể',
                          'text': 'Một hướng là khoảng đệm tiền mặt phù hợp, để nghĩa vụ gần tới bớt phụ thuộc '
                                  'lần tiền vào kế tiếp. Nếu chưa tạo được, nhận diện ngày dễ thiếu, xem có thể '
                                  'thương lượng lịch trả không.',
                          'cue': 'khoảng đệm tiền mặt',
                          'data': {'action': 'bridge_due_date_gap'}},
                         {'id': 'b29',
                          'kind': 'automate',
                          'headline': 'Báo trước khi đến hạn',
                          'text': 'Minh đặt nhắc việc trước hạn trả và gia hạn dịch vụ. Thông báo không tạo ra '
                                  'tiền, nhưng cho thời gian kiểm. Dùng chuyển tự động thì cần đủ số dư và hiểu '
                                  'điều kiện. Chiếc nút vẫn cần kế hoạch phía sau.',
                          'cue': 'đặt nhắc việc',
                          'data': {'action': 'schedule_reminder'}},
                         {'id': 'b30',
                          'kind': 'review',
                          'headline': 'Hai câu hỏi, hai phép kiểm',
                          'text': 'Lan viết hai câu hỏi cạnh nhau: cả tháng có đủ không? Tới ngày trả, có sẵn '
                                  'tiền không? Câu đầu kiểm cân đối, câu sau kiểm lịch dòng tiền. Tách chúng ra, '
                                  'Minh mới chọn cách sửa đúng chỗ.',
                          'cue': 'hai câu hỏi cạnh nhau',
                          'data': {'action': 'monthly_vs_timing'}}]},
              {'id': 'thiet-yeu',
               'title': 'Đừng cắt vào điều cần giữ',
               'beats': [{'id': 'b31',
                          'kind': 'essentials',
                          'headline': 'Phần thiết yếu cần được giữ',
                          'text': 'Nhà ở, ăn uống, đi lại, trách nhiệm gia đình có thể chiếm gần hết thu nhập. '
                                  'Trước khi tự trách, hãy nhìn phần chi buộc phải giữ. Bớt món nhỏ không giải '
                                  'quyết mọi trường hợp.',
                          'cue': 'phần chi buộc phải giữ',
                          'data': {'action': 'protect_essentials'}},
                         {'id': 'b32',
                          'kind': 'essentials',
                          'headline': 'Sức khỏe không phải khoản thừa',
                          'text': 'Ngân sách phải có chỗ cho sức khỏe và nghĩa vụ đã cam kết. Lan kéo hóa đơn '
                                  'quan trọng ra khỏi chiếc kéo. Cắt khoản cần thiết chỉ để số tiết kiệm đẹp có '
                                  'thể khiến vấn đề quay lại lớn hơn.',
                          'cue': 'ra khỏi chiếc kéo',
                          'data': {'action': 'stop_cutting_essentials'}},
                         {'id': 'b33',
                          'kind': 'choice',
                          'headline': 'Không đủ dư: đổi bài toán',
                          'text': 'Nếu phần thiết yếu đã vượt thu nhập, bài toán không chỉ là kỷ luật. Có thể '
                                  'phải xem phương án nhà ở, công việc hoặc sắp xếp nghĩa vụ. Mỗi lựa chọn có '
                                  'điều kiện; video không quyết định thay bạn.',
                          'cue': 'phần thiết yếu đã vượt thu nhập',
                          'data': {'action': 'income_expense_gap'}},
                         {'id': 'b34',
                          'kind': 'budget_after',
                          'headline': 'Đổi giả định, tính lại kết quả',
                          'text': 'Dư hai triệu sáu chỉ đúng nếu chi khác không đổi. Nhà tăng giá thì kết quả '
                                  'phải tính lại. Đừng ép đời sống khớp phép tính đẹp. Ngân sách là bản nháp cần '
                                  'cập nhật, không phải lời hứa.',
                          'cue': 'kết quả phải tính lại',
                          'data': {'baselineIncome': 14000000,
                                   'baselineExpense': 11400000,
                                   'baselineSurplus': 2600000,
                                   'conditional': True}},
                         {'id': 'b35',
                          'kind': 'review',
                          'headline': 'So với mình của tháng trước',
                          'text': 'Đừng lấy mức dư người khác chấm điểm mình. Minh so với dữ liệu của chính cậu: '
                                  'khoản nào rõ hơn, lần quên nào giảm, có bớt thiếu trước hạn không? Tiến bộ có '
                                  'thể bắt đầu bằng lịch thanh toán rõ ràng.',
                          'cue': 'dữ liệu của chính cậu',
                          'data': {'action': 'own_progress'}}]},
              {'id': 'giao-viec-cho-tien',
               'title': 'Giao việc trước cho khoản dư',
               'beats': [{'id': 'b36',
                          'kind': 'buffer',
                          'headline': 'Khoản dư cần một mục đích',
                          'text': 'Biết nghĩa vụ và khoản dự trù rồi, Minh mới chọn phần dành cho khoảng đệm. Mục '
                                  'đích rõ giúp cậu hiểu vì sao giữ tiền hôm nay: để xử lý một việc cần thiết mà '
                                  'ít phải đảo lộn cả tháng.',
                          'cue': 'dành cho khoảng đệm',
                          'data': {'action': 'assign_buffer_goal'}},
                         {'id': 'b37',
                          'kind': 'buffer',
                          'headline': 'Bắt đầu ở mức có thể giữ',
                          'text': 'Minh bắt đầu bằng ba trăm nghìn. Không phải chuẩn chung: quá sức thì điều '
                                  'chỉnh, thuận lợi hơn có thể chọn khác. Cần kiểm khoản dành ra có làm thiếu '
                                  'tiền cho nghĩa vụ gần tới không.',
                          'cue': 'ba trăm nghìn',
                          'data': {'amount': 300000, 'illustrative': True}},
                         {'id': 'b38',
                          'kind': 'automate',
                          'headline': 'Chuyển sau khi đã tính nghĩa vụ',
                          'text': 'Minh lên lịch chuyển sau ngày thu nhập về, cùng số tiền đã cân nhắc với hóa '
                                  'đơn. Cậu kiểm lần đầu. Tự động phù hợp giúp bớt phải nhớ; nếu lịch lương hoặc '
                                  'nghĩa vụ đổi, lịch chuyển cũng cần xem lại.',
                          'cue': 'sau ngày thu nhập về',
                          'data': {'action': 'transfer_after_payday', 'amount': 300000}},
                         {'id': 'b39',
                          'kind': 'choice',
                          'headline': 'Dùng đúng mục đích rồi bù lại',
                          'text': 'Lúc xe cần sửa, Minh dùng phần đã chuẩn bị. Phong bì mỏng đi không nghĩa là '
                                  'thất bại: nó đang làm việc được giao. Sau đó, xem khả năng bổ sung từng bước, '
                                  'thay vì bỏ quên nghĩa vụ.',
                          'cue': 'xe cần sửa',
                          'data': {'action': 'use_and_replenish_buffer'}},
                         {'id': 'b40',
                          'kind': 'review',
                          'headline': 'Đếm khả năng xử lý, không chỉ tiền',
                          'text': 'Chuyển tiền giữa hai túi không tự tạo lợi nhuận. Giá trị là nhận diện tiền có '
                                  'nhiệm vụ và tránh tiêu nhầm. Nhìn chiếc ví đầu video, Minh chưa thành người '
                                  'giàu, nhưng hiểu đồng nào đang được dành cho việc gì.',
                          'cue': 'không tự tạo lợi nhuận',
                          'data': {'action': 'same_total_different_jobs'}}]},
              {'id': 'mua-co-chu-dich',
               'title': 'Trước khi bấm thanh toán',
               'beats': [{'id': 'b41',
                          'kind': 'choice',
                          'headline': 'Đừng chỉ nhìn giá trên nhãn',
                          'text': 'Trước khi mua, Minh đừng chỉ nhìn giá trên nhãn. Lan kéo thêm những mảnh còn '
                                  'thiếu: phụ kiện cần mua, phí giao nếu có, chi phí sử dụng dự kiến. Tổng tiền '
                                  'phải bỏ ra giúp so lựa chọn công bằng hơn.',
                          'cue': 'những mảnh còn thiếu',
                          'data': {'action': 'total_purchase_cost'}},
                         {'id': 'b42',
                          'kind': 'choice',
                          'headline': 'Giảm giá vẫn là chi tiền',
                          'text': 'Giảm giá vẫn là chi tiền nếu mua. Khoảng chênh trên nhãn không tự thành tiền '
                                  'dư thật. Minh đặt món đồ xuống: không thấy khuyến mại, mình có cần không? Nếu '
                                  'có, so tổng chi phí và điều kiện. Nếu không, có thể chờ.',
                          'cue': 'đặt món đồ xuống',
                          'data': {'action': 'discount_vs_need'}},
                         {'id': 'b43',
                          'kind': 'calendar',
                          'headline': 'Chia nhỏ khoản trả, tổng vẫn còn',
                          'text': 'Chia nhiều lần trả không làm tổng giá nhỏ đi. Kiểm tổng tiền, phí nếu có, ngày '
                                  'đến hạn. Minh xếp các lần thanh toán lên lịch, cạnh nghĩa vụ cũ. Số nhỏ hôm '
                                  'nay đi cùng lời hẹn phía sau.',
                          'cue': 'xếp các lần thanh toán lên lịch',
                          'data': {'action': 'installments_on_calendar'}},
                         {'id': 'b44',
                          'kind': 'choice',
                          'headline': 'Cho lựa chọn thêm một nhịp',
                          'text': 'Món chưa cần ngay, Minh thử lưu lại rồi xem sau. Khoảng dừng cho cậu cơ hội '
                                  'đối chiếu kế hoạch, không bảo đảm luôn chọn đúng. Nếu vẫn cần và đủ khả năng, '
                                  'quyết định mua có thể rất hợp lý.',
                          'cue': 'lưu lại rồi xem sau',
                          'data': {'action': 'pause_purchase'}},
                         {'id': 'b45',
                          'kind': 'review',
                          'headline': 'Mua ít hơn chưa chắc mua tốt hơn',
                          'text': 'Mua ít hơn chưa chắc tốt hơn. Đồ dùng lâu, giải quyết nhu cầu thật có thể đáng '
                                  'tiền hơn món ngẫu hứng. Minh giữ một lựa chọn cần thiết, bỏ món không còn '
                                  'muốn. Cậu đang chọn ưu tiên.',
                          'cue': 'giữ một lựa chọn cần thiết',
                          'data': {'action': 'useful_vs_unused'}}]},
              {'id': 'ba-muoi-ngay',
               'title': 'Kế hoạch 30 ngày',
               'beats': [{'id': 'b46',
                          'kind': 'audit',
                          'headline': 'Tuần 1: nhìn rõ dòng tiền',
                          'text': 'Làm kế hoạch ba mươi ngày. Tuần đầu, ghi chi tiêu và hạn trả, sửa dòng đếm hai '
                                  'lần. Chưa đổi tất cả. Cần bức tranh đủ thật để tuần sau không phải quyết định '
                                  'bằng cảm giác.',
                          'cue': 'Tuần đầu',
                          'data': {'week': 1, 'action': 'observe'}},
                         {'id': 'b47',
                          'kind': 'recurring',
                          'headline': 'Tuần 2: sửa một khoản lặp lại',
                          'text': 'Tuần hai, kiểm một khoản lặp lại: còn cần không, tổng tháng bao nhiêu? Nếu '
                                  'đổi, ghi rõ cách đổi và mốc kiểm. Minh thử mức chi thêm thấp hơn, giữ bữa gặp '
                                  'bạn. Một lựa chọn cụ thể thay cho danh sách cấm đoán dài.',
                          'cue': 'Tuần hai',
                          'data': {'week': 2, 'action': 'one_change'}},
                         {'id': 'b48',
                          'kind': 'automate',
                          'headline': 'Tuần 3: giao việc cho tiền',
                          'text': 'Tuần ba, đặt nhắc việc và tách khoản dự trù phù hợp. Dùng chuyển tự động thì '
                                  'kiểm số dư cùng ngày lương thực tế. Bắt đầu bằng mức có thể giữ. Chuyển giữa '
                                  'hai túi của mình không thành khoản chi mới.',
                          'cue': 'Tuần ba',
                          'data': {'week': 3, 'action': 'assign_and_schedule'}},
                         {'id': 'b49',
                          'kind': 'review',
                          'headline': 'Tuần 4: kiểm lại giả định',
                          'text': 'Tuần bốn, so thực tế với kế hoạch: thu, chi, dự trù, ngày thiếu tiền. Chênh '
                                  'thì tìm nguyên nhân, sửa giả định. Tuần bận hay hóa đơn mới là dữ liệu điều '
                                  'chỉnh, không phải lý do xé sổ.',
                          'cue': 'Tuần bốn',
                          'data': {'week': 4, 'action': 'compare_and_adjust'}},
                         {'id': 'b50',
                          'kind': 'cta',
                          'headline': 'Chọn một khoản. Cộng đủ tháng.',
                          'text': 'Lương tăng mà dư đứng yên vì chi tăng cùng nhịp. Hôm nay, chọn một khoản, cộng '
                                  'đủ cả tháng, rồi quyết định giữ hay đổi. Ghi ngày kiểm lại. Từng đồng có việc '
                                  'rõ giúp bạn chọn cuộc sống mình muốn hơn.',
                          'cue': 'chọn một khoản, cộng đủ cả tháng',
                          'data': {'days': 30, 'action': 'select_total_decide_review'}}]}]}
