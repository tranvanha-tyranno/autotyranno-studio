import json, hashlib
from pathlib import Path

BASE = Path('docs/video-references/2026-11-13-user-samples')
OUT = Path('docs/video-references/2026-11-14-content-study/analyses')

def c(start,end,title,question,claim,example,mechanism,transition,payoff,emphasis,beats=None,risks=None):
    return dict(start=start,end=end,title=title,question=question,claim=claim,evidence_example=example,mechanism=mechanism,transition=transition,payoff=payoff,emphasis=emphasis,confidence='high_for_caption_structure_not_source_truth',boundary_basis='agent_inferred_from_caption_turn',beats=beats or [],risks=risks or [])

def b(start,end,focus,job):
    return dict(start=start,end=end,focus=focus,narrative_job=job)

def r(start,end,observation,action,avoid):
    return dict(start=start,end=end,observation=observation,action=action,avoid=avoid,status='proposed_editorial_guidance_from_reference_not_verified_on_new_output')

def write(vid,spine,chapters,observations,rules,sheets,verdict):
    folder=BASE/vid
    meta=json.loads((folder/'metadata.json').read_text(encoding='utf-8'))
    caps=json.loads((folder/'transcript.json').read_text(encoding='utf-8'))
    receipt=json.loads((folder/'media-receipt.json').read_text(encoding='utf-8'))
    data={'schema':'reference-content-analysis/1','study_date':'2026-11-14','source':{'id':vid,'url':f'https://www.youtube.com/watch?v={vid}','title':meta['title'],'channel':meta['channel'],'transcript_path':(folder/'transcript.json').as_posix(),'transcript_sha256':hashlib.sha256((folder/'transcript.json').read_bytes()).hexdigest(),'media_path':(folder/'reference.mp4').as_posix(),'media_sha256_receipt':receipt['sha256'],'metadata_duration_seconds':meta['duration'],'official_chapters':meta.get('chapters'),'chapter_origin':'agent editorial inference; metadata has no official chapters'},'coverage':{'method':'full_caption_reread_plus_named_sampled_contact_sheets','reviewed_start':min(x['start'] for x in caps),'reviewed_end':max(x['start']+x['duration'] for x in caps),'caption_rows':len(caps),'caption_full_read':True,'continuous_av_review':False,'audio_listened':False,'all_shots_reviewed':False,'source_claims_independently_verified':False,'sheets_actually_opened':[(folder/'sheets'/s).as_posix() for s in sheets],'limits':['Caption có thể sai năm, đơn vị, tên riêng; mốc là biên lời gần đúng, không phải cut đến frame.','Dữ kiện và lời chuyên gia được phân tích như điều người kể nói, chưa xác minh độc lập.','Không có analytics retention; nhu cầu người xem là suy luận biên tập.','Sheet chỉ hỗ trợ quan sát tại pixel/mốc ghi trên sheet, không xác nhận xem/nghe liên tục.']},'central_spine':spine,'chapters':chapters,'observations':observations,'transferable_rules':rules,'editorial_verdict':verdict}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f'{vid}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    def tm(t): return f'{int(t)//60:02}:{t%60:05.2f}'
    text=[f'# Phân tích nội dung: {meta["title"]}',f'\nNguồn: {meta["channel"]} — https://www.youtube.com/watch?v={vid}',f'\nNgày 14/11/2026: đọc lại toàn bộ {len(caps)} dòng caption từ {tm(data["coverage"]["reviewed_start"])} đến {tm(data["coverage"]["reviewed_end"])}. Metadata không có chapter chính thức; mọi chương dưới đây do agent suy luận từ lời. Không xem/nghe liên tục; chưa xác minh dữ kiện nguồn; không có số đo retention.','\n## Trục kể',f'\n{spine}','\n## Bản đồ chương và điểm nhấn']
    for idx,x in enumerate(chapters,1):
        text += [f'\n### {idx}. {tm(x["start"])}–{tm(x["end"])} — {x["title"]}',f'\n**Câu hỏi:** {x["question"]}',f'\n**Một ý phải hiểu:** {x["claim"]}',f'\n**Ví dụ/bằng chứng người kể đưa ra:** {x["evidence_example"]}',f'\n**Cơ chế:** {x["mechanism"]}',f'\n**Câu nối có chức năng gì:** {x["transition"]}',f'\n**Điểm trả lời:** {x["payoff"]}',f'\n**Cần nhấn vào:** {x["emphasis"]}']
        if x['beats']:
            text += ['\n| Mốc | Đang nói về gì | Vai trò lập luận |','|---|---|---|']+[f'| {tm(y["start"])}–{tm(y["end"])} | {y["focus"]} | {y["narrative_job"]} |' for y in x['beats']]
        if x['risks']: text += ['\n**Điểm yếu/giới hạn:** '+'; '.join(x['risks'])]
    text += ['\n## Quan sát đối chiếu với lỗi nội dung luông tuồng']+['\n- '+o for o in observations]
    text += ['\n## Quy tắc áp dụng khi viết mới','\nĐây là đề xuất biên tập từ tham khảo, chưa phải cải tiến đã được duyệt trên bản dựng mới.']
    for x in rules: text += [f'\n- **{tm(x["start"])}–{tm(x["end"])}:** {x["observation"]} **Áp dụng:** {x["action"]} **Tránh:** {x["avoid"]}']
    text += ['\n## Khung hình đã mở','\n'+'\n'.join('- '+s for s in data['coverage']['sheets_actually_opened']),f'\n## Kết luận biên tập có phạm vi\n\n{verdict}',f'\nTranscript SHA256 `{data["source"]["transcript_sha256"]}`. MP4 hash từ receipt cũ `{receipt["sha256"]}`; lượt này không thay lượt kiểm toàn vẹn MP4 hiện tại.']
    (OUT/f'{vid}.md').write_text('\n'.join(text)+'\n',encoding='utf-8')

europe=[
c(0.4,60.4,'Hook: giàu có nhưng nhiều người xuống đường','Tại sao phát triển cao không xóa bất mãn?','Nhiều chi tiết đời thường đặt ra một nghịch lý chung cần giải thích.','Người kể ghép Paris, Berlin, người thuê nhà cao tuổi ở Madrid, đình công ở Ý và Serbia.','Đối lập hình dung thịnh vượng với trường, lương, tiền thuê; từ hiện tượng sang câu hỏi.','Hai câu hỏi ở 44.7 và 52.4 chuyển liệt kê địa điểm sang nguyên nhân.','Hứa giải thích vì sao chuyện nhỏ châm ngòi phản ứng lớn.','Nghịch lý thịnh vượng–đời sống; không nhấn mọi nước cùng lúc.',risks=['Danh sách hơn 40 giây trước câu hỏi; không bê nguyên độ dài vào bài ngắn.']),
c(60.4,71.9,'Giới hạn luận điểm','Có một nguyên nhân hoặc tổ chức chung không?','Mỗi nơi có vấn đề riêng; mẫu số chung nguồn đề xuất là niềm tin vào ngày mai.','Caveat không có một phong trào chung điều khiển tất cả.','Không biến đồng thời thành nhân quả giả.','Chọn Pháp để bắt đầu kiểm luận điểm.','Tìm điểm chung nhưng giữ khác biệt địa phương.','Một giới hạn ngắn rồi trở lại ca cụ thể.'),
c(71.9,351.29,'Tầng một: bốn trường hợp và xung đột đời sống','Bất mãn xuất hiện dưới dạng nào ở từng nơi?','Kinh tế phát triển vẫn có thể đi với dịch vụ căng, ngân sách hữu hạn và nhà ở khó tiếp cận.','Nguồn đưa phản đối trường học Pháp, tương lai người trẻ Đức, một ca cưỡng chế Madrid và nhà ở Bồ Đào Nha.','Mỗi ca: vấn đề đời sống → nguyên nhân/đánh đổi → kết luận địa phương.','Đổi nước nhưng giữ dây ngân sách, người trẻ hoặc nhà ở; cuối mục hỏi ai hưởng thành quả.','Có chất liệu cụ thể trước khi nghe mô hình.','Mỗi ca một căng thẳng: dịch vụ–ngân sách; tương lai–nghĩa vụ; hấp dẫn đô thị–khả năng ở; đầu tư–phân phối.',[
b(71.9,157.19,'Pháp: giáo dục sang phúc lợi','Yêu cầu riêng mở thành giới hạn ngân sách; chốt bài học ở 149.69.'),
b(157.19,228.29,'Đức: ba câu hỏi cá nhân','Dịch vĩ mô sang việc làm, thuê nhà, ổn định; giữ caveat không đại diện mọi người trẻ.'),
b(228.29,298.99,'Tây Ban Nha: một ca thuê nhà','Cá nhân làm cửa vào cho cung nhà, du lịch và đánh đổi kiểm soát thuê.'),
b(298.99,351.29,'Bồ Đào Nha: điểm đến hấp dẫn','Nối hai ca nhà ở, hỏi thành quả phát triển tới ai.')],['Năm và thống kê là phát biểu trong caption, chưa được lượt này xác minh.','Nhà ở trở lại ở tầng cơ chế; phải thêm thông tin mỗi lần quay lại.']),
c(351.29,427.89,'Nhánh thương mại tách khỏi luận điểm','Dịch vụ chuyển tiền liên quan người lao động ra sao?','Quảng bá dịch vụ không phải bằng chứng nguyên nhân khủng hoảng.','Người kể đưa quy mô, đối tác, tiện ích, ưu đãi, mã và link nhà tài trợ.','Cầu từ thành quả lao động sang gửi tiền, rồi lợi ích/demo/CTA.','426.3–429.39 nói quay lại bài và chỉ rõ nước kế.','Có ranh giới để trở về mạch chính.','Nhận diện sponsor; không học claim, giá hay ưu đãi.',risks=['Nhánh khoảng 76.6 giây làm đứt chuỗi ca; không tự thêm sponsor vào bài của người dùng.']),
c(427.89,628.9,'Tầng một tiếp: ngân sách và trách nhiệm','Mọi bất mãn có bắt đầu từ chi phí sinh hoạt?','Có ca về phân bổ chi phí, có ca về công khai và trách nhiệm.','Nguồn đặt Ý, Bỉ, Serbia, Albania, Hy Lạp cạnh nhau.','Từ lương–quốc phòng, hưu trí–ngân sách sang thảm kịch, công trình và trách nhiệm.','534.1 phản đề không phải biểu tình nào cũng do giá; 628.9 gom ca sang cơ chế.','Không quy tất cả về lạm phát.','Phân biệt áp lực kinh tế với mất niềm tin.',[
b(427.89,484.89,'Ý: lương và quốc phòng','Có caveat thêm quốc phòng không đồng nghĩa bớt giáo dục một-một.'),
b(484.89,534.1,'Bỉ: ai chịu chi phí','Đổi từ khoản chi sang công bằng phân bổ.'),
b(534.1,582.5,'Serbia: thảm kịch sang chính trị','Phản ví dụ cho giải thích chỉ bằng giá; claim bầu cử cần kiểm riêng.'),
b(582.5,628.9,'Albania, Hy Lạp: công khai','Khép ca, mở mô hình tổng hợp.')]),
c(628.9,1010.1,'Tầng hai: đời sống → cơ hội → niềm tin','Các ca nối qua cơ chế nào?','Sức ép vật chất gây bất mãn mạnh hơn khi cơ hội, phân bổ và tiếng nói suy yếu.','Giỏ hàng 100→120, số liệu nguồn dẫn về nhà, tuổi trẻ, phúc lợi, quốc phòng và callback nhà ga.','Giá/thuê ăn vào thu nhập; già hóa bó ngân sách; niềm tin đổi cách tiếp nhận khó khăn; mạng xã hội khuếch đại.','Đổi nguyên nhân nhưng cùng hướng khoảng cách lời hứa–trải nghiệm.','Câu hỏi đầu có mô hình quan hệ thay cho danh sách nước.','Mỗi đoạn một tâm điểm; lạm phát nhấn tốc độ khác mức; nhà ở nhấn thời hạn xây khác hạn trả thuê.',[
b(628.9,690.0,'Giá cả','Sửa hiểu lầm bằng giỏ hàng; sau đó mới mở năng lượng và nhóm chịu ảnh hưởng.'),
b(690.0,745.5,'Nhà ở','Xây nhiều năm trong khi tiền thuê phải trả tháng này.'),
b(745.5,796.5,'Người trẻ','Từ khó tháng này tới nghi ngờ con đường tiến thân.'),
b(796.5,849.5,'Phúc lợi','Già hóa và thu ngân sách, có caveat chưa phải sụp đổ.'),
b(849.5,895.9,'Quốc phòng','Nguồn tiền và kết quả phải giải thích; không đánh đổi một-một.'),
b(895.9,926.8,'Thế hệ','Có phản biện về đóng góp và hỗ trợ qua lại của người già.'),
b(926.8,970.4,'Niềm tin','Callback Serbia thêm ý nghĩa giải trình.'),
b(970.4,1010.1,'Mạng xã hội','Tách tác nhân lan truyền khỏi nguyên nhân vật chất.')],['6 phút 21 giây với tám tiểu mục dễ thành danh sách nếu không giữ trục.','Nhiều thống kê liền nhau; chỉ giữ số thay đổi suy luận.']),
c(1010.1,1105.3,'Vì sao có bạo lực?','Vì sao chỉ một phần chuyển sang đối đầu?','Không đồng nhất mọi người tham gia; leo thang có nhiều tác nhân.','Nguồn phân biệt người ôn hòa, nhóm đối đầu, người lợi dụng và bốn cơ chế leo thang.','Bất mãn tích tụ + pha trộn nhóm + tương tác cưỡng chế + lan truyền cảm xúc.','Khép bằng hậu quả đổi tâm điểm cải cách sang trật tự rồi mở kịch bản.','Hình bạo lực không đại diện toàn phong trào.','Tác nhân khác nhau và hệ quả đổi đề nghị luận.'),
c(1105.3,1167.0,'Kịch bản có điều kiện và lựa chọn','Điều gì có thể đổi đường đi tiếp theo?','Kết quả phụ thuộc đời sống và khả năng xử lý, không phải dự báo chắc.','Ba khả năng nguồn đề xuất: hạ nhiệt, lặp đợt, khủng hoảng sâu; hỗ trợ mục tiêu, nhà ở, giáo dục.','Mỗi kịch bản có điều kiện; tách trước mắt với dài hạn.','1138.6 đổi từ dự báo sang có thể làm gì.','Có tiêu chí theo dõi thay vì cảm giác báo động.','Nếu–thì và điều kiện; giải pháp phải nối đúng nguyên nhân.',risks=['Danh sách giải pháp rộng; bài mới cần ít đòn bẩy và điều kiện thực thi hơn.']),
c(1167.0,1246.4,'Payoff: trả nghịch lý đầu bài','Khủng hoảng có đồng nghĩa sụp đổ và biểu tình nói gì?','Thịnh vượng hiện tại không tự bảo đảm niềm tin tương lai.','Nguồn giới hạn suy luận từ vài cảnh bạo lực, gom năm bài toán và quay lại lời hứa–đời sống.','Khép vòng từ đường phố về tăng trưởng, phúc lợi, cơ hội và giải quyết bất đồng.','1202 tách câu chốt khỏi danh sách, CTA chỉ tới sau trả lời.','Trả câu hỏi ở cấp nguyên tắc.','Một câu kết nén được toàn bài, không mở ý mới.',risks=['Cường độ tiêu đề khủng hoảng toàn diện mạnh hơn phạm vi ca; không học máy móc giật gân.']),
c(1246.4,1251.0,'CTA sau câu trả lời','Người xem nên làm gì tiếp?','Xin đăng ký nằm ngoài phần chứng minh.','Nhận diện người dẫn, đăng ký, hẹn gặp lại.','Hoàn tất nội dung rồi xin hành động.','Kết thúc.','Không bỏ lửng câu hỏi để ép CTA.','Ngắn, giữ trọn câu kết.')]

write('w3z43Hlzq3c','Nhiều sự kiện địa phương → sức ép sinh hoạt/cơ hội → phân bổ/trách nhiệm/niềm tin → giới hạn cách nhìn sụp đổ → thịnh vượng không tự bảo đảm niềm tin.',europe,[
'Phân đoạn rõ bằng chức năng dù không có chapter chính thức. Ca có kết luận cục bộ rồi đổi cấp từ ca sang cơ chế ở 10:28.9.',
'10:48.5–11:05 sửa một hiểu lầm: giá cao và lạm phát hạ có thể cùng đúng. Sheet 10-02 thấy xe hàng ở 10:54–10:55; chưa kiểm đủ bằng hình phép 100→120 trong lượt này.',
'Sheet 10-01 thấy ca Albania/Hy Lạp đến 10:25, mascot ở 10:28.5–10:30. Đây là đổi chức năng khi tổng hợp, không chứng minh nhịp cut/SFX.',
'Điểm yếu: bốn ca đầu, sponsor, năm ca sau, tám cơ chế tạo tải lớn. Không học lượng mục/độ dài; học mỗi mục thêm điều mới và cắt phần lặp.',
'Mọi thống kê, bầu cử và dẫn nguồn là đối tượng phân tích cách kể; chưa dùng thay research sự thật.'
],[
r(44.7,71.9,'Chi tiết trước câu hỏi, caveat sau câu hỏi.','Viết một câu hỏi trung tâm và giới hạn; hook chỉ hứa điều thân bài trả được.','Phóng đại khủng hoảng mà không có cách trả.'),
r(149.69,157.19,'Ca Pháp chốt ngân sách–dịch vụ rồi đổi nước.','Cuối mỗi chương phải có một câu người xem mang theo.','Hết ví dụ thì nhảy ví dụ mới chỉ để đủ thời lượng.'),
r(628.9,665.0,'Đổi từ ca sang cơ chế, sửa hiểu lầm bằng một so sánh.','Tách cái gì xảy ra với vì sao; hình cho thấy một biến đúng lúc giải.','Cắt theo từ khóa mà không thấy quan hệ.'),
r(740.7,745.5,'Nhiều năm xây đối lập tiền thuê tháng này.','Đánh đổi cần hai phía có thời hạn/đơn vị cụ thể.','Lặp khó khăn lớn mà không nói khó ở đâu.'),
r(926.8,970.4,'Nhà ga trở lại để nói trách nhiệm.','Callback phải thêm cách hiểu; ghi rõ kết luận mới.','Dùng lại ảnh chỉ lấp cảnh.'),
r(1167.0,1246.4,'Giới hạn sụp đổ rồi trả nghịch lý niềm tin.','Viết payoff sau outline, đối chiếu lời hứa hook; CTA sau payoff.','Cuối bài mở chủ đề hoặc chỉ nhắc tiêu đề.')
],['10-01.jpg','10-02.jpg'],'Đáng học hai tầng ca → cơ chế và kết luận trả nghịch lý. Không bê lượng quốc gia, tám nguyên nhân, số liệu dày hoặc quảng cáo; chuyển thành ít chương có câu hỏi, kết luận và cầu nối nhân quả riêng.')

vinh=[
c(0.0,43.0,'Hook: vị trí tốt, đời sống chưa tốt','Vì sao gần trung tâm vẫn cần tái thiết?','Vị trí trên bản đồ không tự tạo điều kiện sống tốt.','Nguồn đối lập Hồ Gươm/vành đai/khu đô thị với ngõ, tắc, ngập, cứu hộ.','Kỳ vọng–thực trạng; cư dân chịu hệ quả, không chỉ tài sản.','Hai câu hỏi dự án là gì và vì sao cần.','Đặt lời giải một nghịch lý, không phải tour tiện ích.','Khoảng cách vị trí–trải nghiệm.',risks=['Địa lý, dân số và vai trò tăng trưởng do nguồn đưa, chưa xác minh.']),
c(43.0,51.0,'Disclaimer nguồn/góc nhìn','Tổng hợp hay kết luận chuyên môn?','Người kể giới hạn tư cách và mời đính chính.','Caption nói tổng hợp nhiều nguồn, có quan điểm cá nhân.','Đặt kỳ vọng trước thân bài.','Vào bài ngay ở 51.0.','Không rẽ sang chủ đề mới.','Ngắn và đúng phạm vi; disclaimer không hợp thức dữ kiện sai.'),
c(51.0,144.37,'Bối cảnh có nhân quả','Vì sao manh mún tích tụ?','Nguồn dùng địa hình khó và phát triển tự phát để giải thích hiện trạng.','Đất trũng, nghề cũ, đầu tư thiếu đồng bộ, ao hồ/xưởng/dân cư xen kẽ, dự án chậm.','Chi phí nền/ngập → ít đồng bộ → phát triển lẻ → nút thắt đời sống.','139.41–144.37 gom thành bốn điểm nghẽn.','Lịch sử tạo lý do cho chương chẩn đoán.','Chỉ giữ bối cảnh giải thích hiện tại.',risks=['Cách gọi xóm liều/thu nhập thấp cần bối cảnh tôn trọng, không gán mặc định nguy cơ xã hội cho cư dân.']),
c(144.37,301.65,'Chẩn đoán: bốn điểm nghẽn','Cần sửa gì trước khi nói dự án?','Giao thông, nước, cứu hộ, dịch vụ công là bốn tiêu chí đời sống.','Bề rộng ngõ, quét nước, vụ cháy nguồn nhắc, đất xanh/hạ tầng xã hội.','Hẹp/thiếu nối → tắc và cản cứu hộ; nền/cống → ngập; thiếu quỹ đất → thiếu dịch vụ.','Dẫn chuyên gia ở 289.33 chuyển sang quy hoạch tổng thể.','Có tiêu chí đánh giá lời giải phía sau.','Mỗi đoạn một vấn đề và người chịu ảnh hưởng.',[
b(144.37,186.45,'Giao thông','Ngõ hẹp và thiếu trục nối, ví dụ giờ cao điểm.'),
b(186.45,217.29,'Ngập/nước thải','Chi tiết quét nước làm mỏ neo đời thường.'),
b(217.29,252.73,'Cứu hộ','Từ bất tiện lên rủi ro tính mạng.'),
b(252.73,301.65,'Công viên, trường, y tế','Nhu cầu để so quỹ đất kế hoạch.')]),
c(301.65,435.38,'Đặt lời giải và tự phản biện bằng số','Dân tăng mà cây xanh/đường cũng tăng bằng cách nào?','Cần cơ chế giải thích chứ không chỉ số đẹp.','Nguồn liệt kê diện tích, vốn, phân vùng, dân, đất xanh, hạ tầng, đường, metro dự kiến.','Bảng trước–sau tạo nghịch lý; ba mô hình được hứa trả lời.','396.74–406.18 tự hỏi số có mờ ảo không rồi mở nén–TOD–15 phút.','Thuật ngữ có lý do xuất hiện.','Chỉ nhấn nghịch lý, không buộc nhớ cả bảng.',risks=['Bảng số ~95 giây dễ quá tải; chọn số thật sự tạo câu hỏi.','Dự thảo/tương lai không được kể như kết quả đã đạt.']),
c(435.38,674.5,'Mô hình 1: đất, cộng đồng và nguồn lực','Thêm sàn mà bớt chiếm đất, rồi tiền đâu?','Nén chiều cao khác với chỉ thêm nhà cao tầng.','Hộp xếp ngang/chồng, Roppongi, Thượng Hải, Đà Nẵng, Phú Mỹ Hưng theo lời nguồn.','Giữ diện tích sàn/giảm chân công trình; chỉnh trang đan xen; giá trị tăng tài trợ hạ tầng.','541.46 nêu đất đang có người; 613.86 hỏi tiền; 674.5 hỏi người đông đi bằng gì.','Ba mắt xích đất → cộng đồng → tài chính trước giao thông.','Hộp chỉ giải một quan hệ, sau đó phải trở về người và tiền.',[
b(435.38,518.1,'Hộp và nén','Thao tác trước–sau minh họa dùng chiều cao.'),
b(518.1,541.46,'Hạ tầng ngầm','Điều kiện mặt đất thực sự thoáng.'),
b(541.46,597.7,'Có cư dân hiện hữu','Tự phản biện ví dụ đất trống; tái thiết đan xen.'),
b(597.7,674.5,'Nguồn lực từ đất','Vòng tiền và quyền lợi người dân trong vòng ấy.')],['So sánh quốc tế không chứng minh dự án sẽ đạt giống.','Giá đất tăng không tự tạo ngân sách; phải có thu hồi giá trị thực thi được.']),
c(674.5,862.94,'Mô hình 2: TOD giải hệ quả mật độ','Nhiều người hơn đi bằng gì?','Nén nhà cần vận tải lớn; giao thông là điều kiện của mô hình một.','Định nghĩa TOD, bán kính, cấp ga, value capture, Hồng Kông, các tuyến dự kiến.','Mật độ → nhu cầu đi → gom quanh ga → đổi phương tiện; đất hỗ trợ hạ tầng.','Câu hỏi có trước thuật ngữ; 862.94 phản biện việc lặt vặt cũng đi tàu sao.','Ba mô hình không phải ba tiện ích song song.','Mật độ–vận tải và cửa nhà–ga; giảm luật/số không phục vụ câu hỏi.',risks=['Caption năm luật/quyết định/tỷ lệ dễ nhận sai, phải kiểm bản gốc.','Không còn lựa chọn nào khác là khẳng định mạnh; phân biệt nhu cầu vận tải lớn với lựa chọn giải pháp duy nhất.']),
c(862.94,974.78,'Mô hình 3: 15 phút và việc hằng ngày','Đi chợ/đưa con/khám bệnh đều lên tàu?','Dịch vụ gần bổ sung giao thông đường dài.','Sáu nhu cầu, Paris, trải nghiệm Úc của người viết, cụm dịch vụ và công viên dự kiến.','Chức năng tách gây đi xa; trộn tại chỗ giảm nhu cầu đi, thời gian, chi phí.','Phản biện đời thường dẫn thuật ngữ; 974.78 chuyển sang tương lai.','Đất, đi xa, sống gần là ba nhiệm vụ phân biệt.','Hành vi mỗi ngày thay vì nhấn mỗi nhãn 15 phút.',risks=['Trải nghiệm cá nhân Úc không chứng minh toàn quốc hay dự án.','Mục tiêu tiếp cận không đồng nghĩa quyền lợi đã thực hiện.']),
c(974.78,1171.74,'Đối chiếu tương lai với bốn điểm nghẽn','Nếu làm đúng, đời sống khác ở đâu?','Hạng mục có nghĩa khi trả nhu cầu đầu bài.','Đường/ngõ/cứu hộ, kết nối vùng, hồ, cây xanh, trường/y tế được nguồn nêu.','Đường → cứu hộ; hồ+cống → điều tiết mưa; đất công → chỗ dịch vụ.','1171.74 từ đường–hồ–trường sang người và nhà.','1140.38–1143.7 gọi lại chổi quét nước như phép thử công trình giúp dân.','Giao thông nhấn an toàn; nước nhấn trữ–thoát; trường nhấn cung dịch vụ.',[
b(974.78,1077.58,'Đường/cứu hộ/kết nối','Trả hai điểm nghẽn giao thông và cứu hộ.'),
b(1077.58,1143.7,'Hồ/cây xanh/quét nước','Biến thấp trũng thành phần lời giải, callback đời thường.'),
b(1143.7,1171.74,'Trường/y tế','Khép tiêu chí công cộng.')],['Một số câu hết ngập/xe tới từng nhà mạnh hơn điều kiện hiện có; bài mới phải giữ điều kiện.','Sheet 19-01 thấy icon trữ/thoát ở 19:00, không đủ nói có phát lại cảnh quét nước.']),
c(1171.74,1287.38,'Nhà tôi thì sao?','Ai ở lại, ai đi và cộng đồng có đứt không?','An cư cần nhóm tác động, nơi ở và trình tự di chuyển.','Nguồn tách di dời/ở lại, quỹ đất nhà, cuốn chiếu, nhu cầu diện tích/giá.','Xây nhà/hạ tầng trước → chuyển sau → bớt đứt trường lớp/nếp sống.','Câu hỏi ngắn kéo từ bản đồ về hộ; cuối mở sinh kế.','Kiểm lợi ích bằng người chịu chuyển đổi.','Trình tự trước–sau và nhóm chịu tác động.',risks=['Cam kết 100%/ưu tiên cần kiểm pháp lý; không coi là bảo đảm có hiệu lực.']),
c(1287.38,1366.71,'Có nhà nhưng còn cách kiếm sống','Sinh kế có theo chỗ ở?','Giao nhà chưa đủ nếu mất mô hình kiếm sống.','Nghề cũ ở ngõ, không gian thương mại, đào tạo/việc làm, tiêu dùng dự kiến.','Đổi hình thái → đổi khách/không gian sản xuất → cần chuyển đổi sinh kế.','1366.71 cảnh báo đây mới là bản vẽ.','Không hoàn tất giả ở bước giao nhà.','Nhà khác nghề; một hộ cụ thể hơn câu kinh tế phát triển.',risks=['Dòng tiền/việc làm dự báo không phải thu nhập đã đo.']),
c(1366.71,1494.27,'Ba điều kiện thực thi','Điều gì khiến lời hứa thành thật hoặc hỏng?','Hạ tầng, vốn, đồng thuận là điều kiện chứ không phụ lục.','Nhà lên trước đường/trường/metro, vốn tư phụ thuộc vốn công, dự thảo và lấy ý kiến.','Lệch tiến độ → quá tải; lệch vốn → mất kết nối; thiếu công khai → rủi ro xã hội.','Hạ giọng từ viễn cảnh sang khả thi; 1488.15 gom ba điều kiện.','Checklist đánh giá thay vì chỉ tin phối cảnh.','Mỗi biến một kịch bản hỏng và điều cần kiểm.',[
b(1366.71,1416.31,'Hạ tầng trước/đồng thời','Phản ví dụ tiến độ kiểm được.'),
b(1416.31,1445.31,'Vốn công–tư khớp','Điểm phụ thuộc ngoài ranh giới.'),
b(1445.31,1494.27,'Minh bạch/ý kiến','Dự thảo khác quy định cuối; ba điều kiện chốt.')]),
c(1494.27,1524.0,'Kết: câu chuyện lớn và CTA','Ca này có nghĩa ngoài một phường?','Nguồn đặt tái thiết trong tầm nhìn đô thị rồi mời đánh giá.','Mục tiêu thủ đô/thu nhập dài hạn, bình luận và đăng ký từ 1511.35.','Mở từ riêng lên chung và tham gia của người xem.','CTA sau điều kiện nhưng thêm claim tham vọng mới.','Câu hỏi đầu có hiện trạng, cơ chế, điều kiện trả lời.','Kết bằng điều đã chứng minh, hỏi điều kiện nào quan trọng nhất.',risks=['Mục tiêu mới 1494–1511 dễ loãng payoff.','Caption hết 1520.947; đuôi đến duration 1524 chưa xem/nghe.'])]

write('1OGwWLvasIk','Vị trí tốt nhưng đời sống chưa tốt → bốn điểm nghẽn → nghịch lý tăng dân/tăng đất công → nén giải đất, TOD giải đi xa, 15 phút giải việc hằng ngày → nhà và nghề → điều kiện thực thi.',vinh,[
'Phân đoạn mạnh vì mỗi mô hình khép một bài toán rồi làm lộ bài toán kế. Đây khác ba bài định nghĩa đặt cạnh nhau.',
'Sheet 07-02 ở 07:36.5–07:45 thấy hộp đổi ngang sang chồng, một biến rõ. Sampling không xác nhận mượt hoặc toàn chuyển động.',
'Sheet 11-01 có công trình ↔ đất ở 11:10, chữ TOD ở 11:25–11:30, giao thông đông 11:33.5–11:36.5: vòng cơ chế → khái niệm → hậu quả thiếu nó.',
'Mạch quay về cư dân: ngập/cháy/trường rồi nhà tôi, nghề tôi. Thuật ngữ có nghĩa qua hành vi; nhu cầu khán giả vẫn là suy luận từ lời.',
'Nên cắt gọn bảng số trước mô hình, danh mục pháp lý/cấp TOD, kết nối vùng, mục tiêu mới cuối bài. Nhiều chi tiết không tự tạo chuyên nghiệp.',
'Dự thảo khác sẽ làm; vốn dự kiến khác vốn có; khách dự báo không bảo đảm sinh kế. Điều kiện cuối không xóa giọng chắc chắn quá mức trước đó.'
],[
r(396.74,435.38,'Tự hỏi dân tăng mà đất công tăng trước mô hình.','Nêu mâu thuẫn cần giải trước thuật ngữ.','Định nghĩa dài khi người xem chưa có lý do cần biết.'),
r(435.38,493.78,'Hộp giữ số lượng, đổi cách chiếm mặt sàn.','Mỗi cơ chế một biến: đầu → thao tác → cuối → kết luận.','Đổi chữ/icon rồi gọi giải thích.'),
r(674.5,686.1,'Nén nhà → người đông đi bằng gì → TOD.','Cầu nối: A giải X nhưng sinh Y; B xử lý Y.','Chỉ tiếp theo/thêm vấn đề khác.'),
r(862.94,874.42,'Chợ/con/khám bệnh tạo lý do 15 phút.','Chuyển hệ thống sang một hành vi đời thường cụ thể.','Nỗi đau chung chung không liên hệ cơ chế.'),
r(186.45,1143.7,'Quét nước trở lại sau hồ+cống.','Callback lần đầu vấn đề, lần sau phép thử lời giải; rải đúng hai mốc.','Nhắc lại lời/hình không thêm cách hiểu.'),
r(1171.74,1366.71,'Nhà và nghề thành hai câu hỏi riêng.','Mỗi chương một nhiệm vụ; đổi đối tượng chịu tác động thì đặt câu hỏi mới.','Trộn ở/việc/vốn/tăng trưởng dưới một mục quyền lợi.'),
r(1366.71,1494.27,'Ba điều kiện kèm cách có thể hỏng.','Chương giới hạn: phải đúng gì, hỏng gì, kiểm ở đâu.','Một câu cần minh bạch chiếu lệ.')
],['07-01.jpg','07-02.jpg','11-01.jpg','19-01.jpg'],'Đáng học kiến trúc câu hỏi nối nhân quả và tách nhà khỏi nghề. Giữ chẩn đoán → cơ chế → hệ quả → điều kiện; giảm bảng số/danh mục và giữ trạng thái dự thảo có điều kiện. Không sao chép lời, mascot, shot hoặc giọng bảo đảm của nguồn.')
