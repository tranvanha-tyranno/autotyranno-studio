"""Original China economy narrative, dated observed data versus mechanisms/forecasts."""
import json
from pathlib import Path
r=Path(__file__).resolve().parent;chapters=[]
def chapter(cid,title):
 c={'id':cid,'title':title,'beats':[]};chapters.append(c);return c
def beat(c,bid,text,layout,headline,design=None):
 c['beats'].append({'id':bid,'text':text,'phase':'content','layout':layout,'headline':headline,'design':design or {}})
c=chapter('opening','Một nền kinh tế, nhiều nhịp chuyển động')
beat(c,'o01','Một bên là cảng biển, dây chuyền và những đoàn tàu chở hàng. Một bên là người mua nhà và các gia đình vẫn cân nhắc từng khoản chi. Hai cảnh ấy có thể cùng đúng về Trung Quốc.','c-map','Một nền kinh tế. Nhiều nhịp chuyển động.')
beat(c,'o02','Vì sao một nền kinh tế sản xuất rất mạnh vẫn phải lo kích thích nhu cầu? Muốn hiểu, cần tách cỗ máy làm ra hàng hóa khỏi vòng tuần hoàn đưa thu nhập trở lại thị trường.','c-flow','Sản xuất mạnh. Sức mua ở đâu?')
beat(c,'o03','Video này nhìn vào các động cơ tăng trưởng, bất động sản, tiêu dùng và già hóa. Số liệu được chốt theo các công bố đã kiểm tra đến ngày mười ba tháng mười một, năm hai nghìn không trăm hai mươi sáu.','c-compare','Bốn câu hỏi để đọc Trung Quốc')
beat(c,'o04','Đây là phân tích giáo dục, không phải khuyến nghị đầu tư. Biểu đồ số liệu có kỳ đo và nguồn riêng; mô phỏng chỉ giải thích cơ chế, không phải dự báo hay bản sao hoạt động của doanh nghiệp cụ thể.','c-question','Miễn trừ trách nhiệm')
for b in c['beats']:b['phase']='disclaimer' if b['id']=='o04' else 'hook'
c=chapter('factory','Cỗ máy sản xuất và những kết nối')
beat(c,'f01','Trước hết, Trung Quốc không phải một nhà máy duy nhất. Trên bản đồ là các thành phố, vùng công nghiệp, cảng và thị trường lao động kết nối với nhau. Khoảng cách và hạ tầng góp phần quyết định cách hàng hóa di chuyển.','c-map','Những cụm kinh tế kết nối nhau')
beat(c,'f02','Hãy lấy một dây chuyền minh họa. Nhà cung cấp đưa linh kiện tới, công nhân và thiết bị lắp ráp, rồi sản phẩm được kiểm tra trước khi xuất xưởng. Giá trị nằm trong cả chuỗi phối hợp ấy.','c-sim','Linh kiện → Lắp ráp → Kiểm tra')
beat(c,'f03','Khi nhiều nhà cung cấp, kỹ năng và dịch vụ ở gần nhau, việc tìm đầu vào hay xử lý trục trặc có thể thuận tiện hơn. Đó là một lợi thế của cụm sản xuất, không chỉ là câu chuyện tiền công thấp.','c-flow','Lợi thế của một hệ sinh thái')
beat(c,'f04','Nhưng năng lực làm ra sản phẩm chưa tự bảo đảm mọi nhà máy có lợi nhuận. Còn cần đơn hàng, mức giá đủ bù chi phí, chất lượng, công suất sử dụng và khả năng thu hồi tiền.','c-sim','Công suất khác với đơn hàng')
beat(c,'f05','Theo bảng hạch toán sơ bộ của cơ quan thống kê Trung Quốc, giá trị tăng thêm ngành chế tạo trong chín tháng đầu năm hai nghìn không trăm hai mươi sáu tăng năm phẩy sáu phần trăm so với cùng kỳ, theo giá so sánh.','c-chart','Chế tạo: +5,6% cùng kỳ')
beat(c,'f06','Trong cùng bảng và cùng kỳ, xây dựng giảm bốn phẩy một phần trăm, còn khu vực dịch vụ tăng năm phẩy hai phần trăm. Các bộ phận có thể đi khác nhịp, dù đều nằm trong một nền kinh tế.','c-chart','Ba bộ phận, ba nhịp tăng trưởng')
beat(c,'f07','Điều này giúp tránh hai kết luận cực đoan: thấy một ngành tốt rồi cho rằng mọi gia đình đều khá lên, hoặc thấy một ngành khó khăn rồi cho rằng toàn bộ năng lực sản xuất đã biến mất.','c-compare','Một ngành không đại diện tất cả')
beat(c,'f08','Câu hỏi khó hơn là động cơ nào đang kéo, động cơ nào đang ghìm, và sức kéo có chuyển thành thu nhập cùng nhu cầu bền vững hay không. Để thấy phần ghìm, hãy nhìn sang bất động sản.','c-flow','Từ sản lượng đến thu nhập')
c=chapter('property','Vì sao nhà ở tác động vượt khỏi công trường')
beat(c,'r01','Một dự án nhà ở có nhiều bên tham gia: người mua, chủ đầu tư, nhà thầu, ngân hàng và chính quyền địa phương. Vì vậy, khó khăn ở dự án có thể truyền tới những bảng cân đối khác nhau.','c-flow','Nhà ở nối nhiều bảng cân đối')
beat(c,'r02','Trong mô phỏng này, một hộ gia đình mua nhà và một doanh nghiệp triển khai dự án. Khi tiền thu chậm lại, doanh nghiệp phải xem lại lịch thanh toán cho nhà thầu và khả năng hoàn thành công trình.','c-sim','Một dòng tiền chậm, nhiều bên chờ')
beat(c,'r03','Nếu công trình chậm, người mua có thể lo về việc nhận nhà. Nếu doanh nghiệp giảm đầu tư, nhu cầu vật liệu và việc làm liên quan cũng chịu ảnh hưởng. Đây là các kênh truyền dẫn, không phải một tỷ lệ cố định cho mọi dự án.','c-flow','Tiền thu → Hoàn thiện → Niềm tin')
beat(c,'r04','Số liệu chính thức cho biết đầu tư phát triển bất động sản trong chín tháng đầu năm hai nghìn không trăm hai mươi sáu giảm hai mươi phẩy sáu phần trăm so với cùng kỳ. Đây là chỉ tiêu đầu tư, không phải mức giảm của giá mọi căn nhà.','c-chart','Đầu tư bất động sản: −20,6%')
beat(c,'r05','Một gia đình cũng có thể thay đổi hành vi khi giá trị tài sản hoặc triển vọng thu nhập khiến họ bất an. Họ có thể hoãn một món mua lớn hay muốn giữ dự phòng nhiều hơn, ngay cả khi vẫn đang có việc.','c-sim','Tài sản, thu nhập và quyết định chi')
beat(c,'r06','World Bank và IMF đều xem điều chỉnh bất động sản là một phần quan trọng của bài toán tái cân bằng. Nhưng giải quyết dự án dở dang, tổn thất và nghĩa vụ tài chính không đơn giản như bật lại một công tắc xây dựng.','c-flow','Sửa dự án khác với xây thêm')
beat(c,'r07','Xây thêm có thể tạo hoạt động trước mắt, nhưng nếu nhu cầu hoặc hiệu quả không phù hợp thì rủi ro vẫn ở đó. Điều cần phân biệt là hoàn thành nghĩa vụ cũ với mở rộng những cam kết mới.','c-compare','Hoàn thành nghĩa vụ / Mở rộng cam kết')
c=chapter('households','Dòng thu nhập quay về sức mua như thế nào?')
beat(c,'h01','Bây giờ chuyển từ công trường sang hộ gia đình. Một vòng tuần hoàn đơn giản là doanh nghiệp trả thu nhập, người dân chi tiêu, doanh nghiệp có doanh thu rồi tiếp tục tuyển dụng và đầu tư.','c-flow','Thu nhập → Chi tiêu → Doanh thu')
beat(c,'h02','Vòng ấy không chạy chỉ nhờ lời kêu gọi mua sắm. Quyết định chi còn phụ thuộc thu nhập kỳ vọng, độ ổn định công việc, nghĩa vụ nợ và nhu cầu dự phòng cho những việc quan trọng của gia đình.','c-sim','Chi tiêu đi cùng mức độ an tâm')
beat(c,'h03','Để nhìn rõ cơ chế, tạm chia một khoản thu nhập minh họa thành tiêu dùng, trả nghĩa vụ và dự phòng. Các khối chuyển động chỉ thể hiện lựa chọn; chúng không phải cơ cấu tiết kiệm thực tế của Trung Quốc.','c-sim','Ba cách sử dụng thu nhập — minh họa')
beat(c,'h04','Theo khảo sát hộ gia đình, chi tiêu tiêu dùng bình quân đầu người trong chín tháng đầu năm hai nghìn không trăm hai mươi sáu tăng ba phẩy sáu phần trăm theo giá hiện hành, và hai phẩy bảy phần trăm sau điều chỉnh giá.','c-chart','Cùng chỉ tiêu: danh nghĩa / thực')
beat(c,'h05','Hai con số khác nhau vì một bên chưa loại tác động của giá. Và chỉ tiêu bình quân này không có nghĩa mỗi gia đình tăng chi đúng từng ấy. Bình quân có thể che những khác biệt rất lớn.','c-compare','Bình quân không phải mọi gia đình')
beat(c,'h06','Cũng đừng dùng doanh số bán lẻ hàng hóa thay cho toàn bộ tiêu dùng trong GDP. Phạm vi dịch vụ, đối tượng đo và phương pháp thống kê khác nhau; biểu đồ đẹp vẫn sai nếu đặt nhầm hai đại lượng cạnh nhau.','c-flow','Đọc đúng phạm vi chỉ tiêu')
beat(c,'h07','Một phần tranh luận chính sách vì thế hướng tới thu nhập hộ gia đình, an sinh và niềm tin, thay vì chỉ thêm năng lực làm hàng. Đây là chuyện điều kiện để người dân muốn chi, không phải kết luận rằng tiết kiệm tự nó là xấu.','c-flow','Từ năng lực sản xuất tới nhu cầu')
beat(c,'h08','Doanh nghiệp cần người mua, còn người mua cần nguồn thu nhập và sự an tâm. Khi một mắt xích yếu đi, tăng công suất ở mắt xích khác có thể chưa giải quyết được điểm nghẽn.','c-sim','Tăng một mắt xích chưa đủ')
c=chapter('trade','Xuất khẩu giúp gì, và không thay được điều gì?')
beat(c,'t01','Hàng hóa không chỉ tìm người mua trong nước. Từ các cụm công nghiệp và cảng, chúng đi vào nhiều thị trường. Bản đồ ở đây là sơ đồ kết nối thương mại, không mô tả tuyến tàu thực hay khối lượng vận chuyển.','c-map','Kết nối ra nhiều thị trường')
beat(c,'t02','Xuất khẩu tạo đơn hàng cho doanh nghiệp và việc làm liên quan. Nhập khẩu mang vào nguyên liệu, thiết bị và sản phẩm. Cả hai cùng nằm trong chuỗi cung ứng, chứ không chỉ có một mũi tên hàng đi ra.','c-flow','Xuất khẩu và nhập khẩu cùng hiện diện')
beat(c,'t03','Trong tính GDP theo chi tiêu, xuất khẩu ròng là xuất khẩu trừ nhập khẩu. Điều này không có nghĩa nhập khẩu là xấu; phép trừ giúp tránh tính phần giá trị được tạo ở nước ngoài vào sản lượng trong nước.','c-chart','Xuất khẩu ròng = Xuất khẩu − Nhập khẩu')
beat(c,'t04','Hãy dùng một phép tính giả định: xuất khẩu tăng mười đơn vị, nhập khẩu tăng bảy, thì phần chênh tăng ba. Đây chỉ là minh họa số học, không phải đóng góp tăng trưởng thực tế của Trung Quốc.','c-chart','Ví dụ giả định: 10 − 7 = 3')
beat(c,'t05','Xuất khẩu mạnh có thể bù một phần nhu cầu yếu ở nơi khác, nhưng không vô hạn. Doanh nghiệp còn đối mặt thị hiếu, cạnh tranh, chi phí vận chuyển và chính sách thương mại của đối tác.','c-map','Đơn hàng ngoài nước có điều kiện')
beat(c,'t06','Một thay đổi thuế quan có thể khiến người mua, nhà cung cấp và địa điểm hoàn thiện sản phẩm điều chỉnh. Tuy vậy, một tuyến nối mới trên bản đồ không chứng minh toàn bộ chuỗi giá trị đã chuyển đi.','c-map','Một mắt xích đổi chỗ, cả chuỗi chưa chắc đổi')
beat(c,'t07','Bởi vậy, đọc sức mạnh xuất khẩu cần đi cùng khả năng tạo giá trị, thu nhập và đa dạng thị trường. Không nên lấy kim ngạch gộp để suy thẳng thành lợi nhuận hay mức sống của từng người.','c-flow','Kim ngạch ≠ Lợi nhuận ≠ Thu nhập hộ')
c=chapter('demography','Già hóa và bài toán năng suất')
beat(c,'d01','Có một chuyển động chậm hơn tàu hàng nhưng rất quan trọng: cơ cấu dân số. Theo công bố thống kê cuối năm hai nghìn không trăm hai mươi lăm, người từ sáu mươi tuổi trở lên chiếm hai mươi ba phần trăm dân số.','c-sim','Cuối 2025: người 60+ chiếm 23%')
beat(c,'d02','Mốc tuổi phải được giữ rõ. Hai mươi ba phần trăm ở đây là nhóm sáu mươi trở lên, không phải sáu mươi lăm trở lên. Đổi mốc tuổi mà giữ nguyên con số sẽ làm biểu đồ sai nghĩa.','c-compare','60+ không phải 65+')
beat(c,'d03','Già hóa tác động tới nhu cầu chăm sóc, chi tiêu công, thị trường lao động và kế hoạch của gia đình. Nhưng tỷ lệ tuổi không tự quyết định một kết cục kinh tế duy nhất; năng suất và cách tổ chức xã hội vẫn quan trọng.','c-flow','Dân số tác động qua nhiều kênh')
beat(c,'d04','Trong mô phỏng nhà máy này, cùng một nhóm người có thể làm ra nhiều giá trị hơn nếu kỹ năng, công cụ và quy trình tốt lên. Không phải chỉ đếm có bao nhiêu robot, mà phải hỏi hiệu quả thực sự tăng thế nào.','c-sim','Năng suất không chỉ là số robot')
beat(c,'d05','Đầu tư công nghệ có thể mở cơ hội, đồng thời đòi hỏi vốn và chuyển đổi kỹ năng. Việc làm ở từng ngành có thể thay đổi khác nhau; một cảnh tự động hóa không chứng minh toàn bộ người lao động đều được lợi hoặc mất việc.','c-compare','Công nghệ có cơ hội và chi phí chuyển đổi')
beat(c,'d06','Vì thế, thách thức dài hạn là phối hợp năng suất, đào tạo và mạng lưới hỗ trợ. Đó là một bài toán nhiều năm, không thể kiểm bằng số bán hàng của riêng một tháng.','c-flow','Năng suất · Kỹ năng · Hỗ trợ chuyển đổi')
c=chapter('policy','Ba phép thử để đọc tăng trưởng')
beat(c,'p01','Quay lại con số tổng. GDP trong chín tháng đầu năm hai nghìn không trăm hai mươi sáu tăng bốn phẩy sáu phần trăm so với cùng kỳ, theo ước tính sơ bộ của cơ quan thống kê.','c-chart','9 tháng đầu 2026: GDP +4,6%')
beat(c,'p02','Theo quý so với cùng kỳ, lần lượt là năm phẩy không, bốn phẩy ba và bốn phẩy năm phần trăm. Đó không phải tăng trưởng so với quý liền trước, và cũng chưa phải kết quả cả năm.','c-chart','Q1 / Q2 / Q3: cùng kỳ, không phải liền quý')
beat(c,'p03','Một chính sách có thể nâng cầu trước mắt, nhưng cần hỏi tiền tới đâu, ai thực sự chi, và nghĩa vụ nào được tạo thêm. Hỗ trợ đầu tư, hỗ trợ hộ gia đình và xử lý nghĩa vụ cũ có đường truyền khác nhau.','c-flow','Tiền tới ai? Đi qua kênh nào?')
beat(c,'p04','Phép thử thứ nhất: hoạt động mới có tạo hiệu quả và dòng thu nhập lâu dài không? Nếu chỉ tăng số dự án mà bỏ qua nhu cầu, tăng trưởng hiện tại có thể đi cùng áp lực xử lý trong tương lai.','c-sim','1 / Hiệu quả, không chỉ khối lượng')
beat(c,'p05','Phép thử thứ hai: thu nhập và sự an tâm của hộ gia đình có cải thiện không? Một nền kinh tế muốn cân bằng hơn cần nhìn cả bên sản xuất lẫn điều kiện để thị trường trong nước hấp thụ hàng hóa, dịch vụ.','c-sim','2 / Thu nhập và sự an tâm')
beat(c,'p06','Phép thử thứ ba: rủi ro được giải quyết hay chỉ chuyển từ nơi này sang nơi khác? Tái cơ cấu nghĩa vụ và hoàn thiện dự án cần được phân biệt với việc đẩy cam kết sang một bảng cân đối mới.','c-flow','3 / Giải quyết hay chuyển chỗ rủi ro?')
beat(c,'p07','Các phép thử này không đưa ra một dự báo chắc chắn. Chúng giúp đọc tin mới mà không bị một con số hoặc một hình ảnh dẫn đi quá xa, nhất là khi các ngành và địa phương đang khác nhịp.','c-compare','Đọc điều kiện, tránh một kết luận duy nhất')
c=chapter('ending','Đọc đúng những chuyển động cùng tồn tại')
beat(c,'e01','Trung Quốc vì thế có thể đồng thời sở hữu năng lực sản xuất lớn và gặp áp lực từ bất động sản, sức mua, dân số. Những điều ấy không tự loại trừ nhau; chúng tương tác qua thu nhập, tài sản, đơn hàng và niềm tin.','c-flow','Những chuyển động cùng tồn tại')
beat(c,'e02','Nếu nhớ một sơ đồ, hãy nhớ vòng kết nối: sản xuất tạo thu nhập, thu nhập hỗ trợ nhu cầu, nhu cầu nuôi doanh nghiệp; nhà ở, nghĩa vụ tài chính và chính sách có thể làm từng đường nối mạnh lên hoặc yếu đi.','c-sim','Sản xuất → Thu nhập → Nhu cầu')
beat(c,'e03','Khi gặp một số liệu mới, hãy hỏi nó đo kỳ nào, theo giá nào, là mức hay tốc độ tăng, và có đại diện cho điều đang được kết luận không. Bốn câu hỏi nhỏ giúp nhìn một nền kinh tế lớn rõ hơn.','c-compare','Kỳ đo · Giá · Mức hay tăng · Phạm vi')
beat(c,'e04','Bạn muốn đi sâu vào bất động sản, xe điện hay thương mại Trung Quốc? Chia sẻ phần bạn quan tâm ở bình luận, và theo dõi để cùng kiểm tra những câu chuyện kinh tế qua số liệu và cơ chế phía sau.','c-closing','Bạn muốn đi sâu vào động cơ nào?')
c['beats'][-1]['phase']='cta'
for c in chapters:
 c['text']=' '.join(b['text'] for b in c['beats']);c['wordCount']=len(c['text'].split())
content={'schema':'china-economy/1','id':'kinh-te-trung-quoc','title':'Kinh tế Trung Quốc: sản xuất mạnh, sức mua mắc ở đâu?',
 'fps':30,'targetSeconds':600,'voiceId':'6adFm46eyy74snVn6YrT','asOf':'2026-11-13','chapters':chapters,
 'brandPolicy':{'forbiddenVisibleText':['Tyranno'],'channelBrand':None},
 'facts':{'gdpYTD2026':4.6,'gdpQuarters2026':[5.0,4.3,4.5],'manufacturingYTD2026':5.6,'constructionYTD2026':-4.1,'servicesYTD2026':5.2,
 'propertyInvestmentYTD2026':-20.6,'householdConsumptionNominalYTD2026':3.6,'householdConsumptionRealYTD2026':2.7,'age60PlusShareEnd2025':23.0},
 'researchSources':[{'id':'nbs-gdp','title':'NBS: Q3 2026 preliminary GDP accounts','url':'https://www.stats.gov.cn/english/PressRelease/202610/t20261021_1965671.html'},
 {'id':'nbs-economy','title':'NBS: national economy first three quarters2026','url':'https://www.stats.gov.cn/english/PressRelease/202610/t20261019_1965619.html'},
 {'id':'nbs-property','title':'NBS: real-estate development Jan–Sep2026','url':'https://www.stats.gov.cn/english/PressRelease/202610/t20261020_1965663.html'},
 {'id':'nbs-households','title':'NBS: household income/consumption Jan–Sep2026','url':'https://www.stats.gov.cn/english/PressRelease/202610/t20261020_1965660.html'},
 {'id':'nbs-population','title':'NBS: Statistical Communiqué2025','url':'https://www.stats.gov.cn/english/PressRelease/202602/t20260228_1962661.html'},
 {'id':'worldbank','title':'World Bank: Rebalancing Growth, July2026','url':'https://www.worldbank.org/en/news/press-release/2026/07/07/rebalancing-growth-china-economic-update'},
 {'id':'imf','title':'IMF: China2025 ArticleIV, published2026','url':'https://www.imf.org/-/media/files/publications/cr/2026/english/1chnea2026001-source-pdf.pdf'}]}
(r/'content.json').write_text(json.dumps(content,ensure_ascii=False,indent=2),encoding='utf-8');(r/'script.txt').write_text('\n\n'.join(c['text'] for c in chapters)+'\n',encoding='utf-8')
print({'chapters':len(chapters),'beats':sum(len(c['beats']) for c in chapters),'words':sum(c['wordCount'] for c in chapters),'chars':sum(len(c['text']) for c in chapters)})
