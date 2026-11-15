# Nghiên cứu và nguồn tư liệu — Kinh tế Trung Quốc

Ngày chốt tài liệu: **13/11/2026**. Bản ghi đối chiếu kịch bản và thiết kế với các công bố gốc đã lưu. Đây là kiểm tra nguồn và phạm vi diễn giải; không thay cho việc xem/nghe liên tục bản phim xuất cuối và không xác nhận chấp thuận của người xem.

## Số liệu trong lời dẫn và biểu đồ

| Chỉ tiêu | Con số dùng | Kỳ, cách đo và giới hạn | Nguồn gốc |
| --- | --- | --- | --- |
| GDP | +4,6% | Chín tháng đầu 2026 so cùng kỳ, giá so sánh; hạch toán sơ bộ, chưa phải kết quả cả năm | [NBS, 21/10/2026](https://www.stats.gov.cn/english/PressRelease/202610/t20261021_1965671.html) |
| GDP từng quý | Q1 +5,0%; Q2 +4,3%; Q3 +4,5% | Từng quý so cùng kỳ năm trước; không phải so quý liền trước đã điều chỉnh mùa vụ; không cộng ba tỷ lệ | [NBS, Bảng 2](https://www.stats.gov.cn/english/PressRelease/202610/t20261021_1965671.html) |
| Chế tạo / xây dựng / dịch vụ | +5,6% / −4,1% / +5,2% | Giá trị tăng thêm chín tháng đầu 2026, so cùng kỳ, giá so sánh, cùng bảng GDP sơ bộ. Dịch vụ là khu vực III; không phải doanh thu, lợi nhuận hay chỉ tiêu sản lượng công nghiệp trên quy mô được chỉ định | [NBS, Bảng 1 và ghi chú giá](https://www.stats.gov.cn/english/PressRelease/202610/t20261021_1965671.html) |
| Đầu tư phát triển bất động sản | −20,6% | Tháng 1–9/2026 so cùng kỳ, nguồn ghi tính trên cơ sở so sánh được; không phải mức giảm giá mọi căn nhà | [NBS, 20/10/2026](https://www.stats.gov.cn/english/PressRelease/202610/t20261020_1965663.html) |
| Chi tiêu tiêu dùng bình quân đầu người | Danh nghĩa +3,6%; thực +2,7% | Chín tháng đầu 2026 so cùng kỳ, khảo sát hộ; mức tăng thực đã điều chỉnh giá. Không phải mọi hộ đều tăng chi như vậy, toàn bộ tiêu dùng GDP hoặc tổng bán lẻ | [NBS, mục II và Bảng 1](https://www.stats.gov.cn/english/PressRelease/202610/t20261020_1965660.html) |
| Người từ 60 tuổi trở lên | 23,0% | Cuối 2025, không phải năm 2026. Bảng nguồn ghi nhóm **65+ là 15,9%**; không được dùng 23% cho mốc 65 tuổi | [NBS, Thông cáo thống kê 2025](https://www.stats.gov.cn/english/PressRelease/202602/t20260228_1962661.html) |

Các số trên khớp bản công bố lưu cục bộ. Không đổi nhãn đầu tư BĐS thành giá nhà hoặc tự gán là tốc độ thực. NBS ghi dữ liệu GDP trong công bố không bao gồm GDP Hồng Kông, Ma Cao và Đài Loan. Bản đồ kết nối không mở rộng phạm vi thống kê hoặc khẳng định chủ quyền.

## Nhận định, giả định và giới hạn

[World Bank — Rebalancing Growth, 07/07/2026](https://www.worldbank.org/en/news/press-release/2026/07/07/rebalancing-growth-china-economic-update) hỗ trợ phần điều chỉnh BĐS, nhu cầu nội địa, an sinh và hỗ trợ chuyển đổi kỹ năng. Dự báo 4,4% năm 2026 và 4,3% năm 2027 trong tài liệu là dự báo tại thời điểm công bố; video không dùng chúng làm kết quả thực tế hay thay ước tính GDP chín tháng NBS.

[IMF — China: 2025 Article IV Consultation, công bố 18/02/2026](https://www.imf.org/-/media/files/publications/cr/2026/english/1chnea2026001-source-pdf.pdf) đã được tải và trích văn bản thành 121 trang. Báo cáo nhân viên hoàn thành 28/01/2026; Hội đồng kết thúc tham vấn 13/02/2026. Đây là **tham vấn 2025 xuất bản năm 2026**, không phải tham vấn 2026. PDF trang 2–3 nêu nhu cầu tư nhân yếu, rủi ro điều chỉnh BĐS và khuyến nghị tái cân bằng sang tiêu dùng; trang 3 nêu già hóa và năng suất. Những nhận định này hỗ trợ quy nguồn World Bank/IMF trong lời dẫn; dự báo IMF không được coi là kết quả đã xảy ra. File, URL, SHA256 và thời điểm tải được giữ trong `research/imf-2025-article-iv-receipt.json`.

- Xuất khẩu ròng là xuất khẩu trừ nhập khẩu theo phần phương pháp GDP của NBS. Ví dụ **10 − 7 = 3** chỉ là số học, không phải kim ngạch hoặc đóng góp tăng trưởng thực. `t03/t04` phân biệt mức và thay đổi giả định; cột cuối là tổng chênh lệch, không cộng thêm 3 lần nữa.
- Phân bổ hộ `r05/h02/h03/p05/e02` dùng 45/30/25, 50/30/20, 50/25/25, 55/25/20 và 50/25/25; mỗi bộ bằng 100 phần. Không phải cơ cấu tiết kiệm Trung Quốc, khuyến nghị tài chính hay dự báo phản ứng chính sách.
- Mô phỏng nhà máy dùng năng lực/đơn hàng giả định: 8 năng lực, 5 đơn hàng cho đầu ra minh họa 5; 8 so với 4 cho 4. Không gắn các đơn vị hình vẽ với số công nhân, sản lượng hay năng suất thực. Kỹ năng/công cụ/quy trình là cơ chế, không phải ước lượng lợi ích công nghệ.
- Mô phỏng nhà ở không mô tả doanh nghiệp thật; các vai biểu thị quan hệ khái niệm, không có hệ số truyền dẫn cố định hay quy kết trách nhiệm cho tổ chức thực.
- Đường nối bản đồ và độ rộng dòng chảy không phải tuyến tàu, luồng hàng, tỷ trọng thương mại, bằng chứng cả chuỗi giá trị đã chuyển đi hoặc ranh giới được khẳng định. Các kênh tác động không đồng nghĩa mọi hộ và ngành phản ứng giống nhau.

## Tư liệu thực sự được chọn

`data.json` hiện dùng **8 nguồn riêng biệt**, sáu ảnh và hai clip ở `f07/h05/d05/e04`; thư viện 20 ứng viên không có nghĩa tất cả đều xuất hiện. Mỗi ID dùng một lần. Tư liệu chỉ minh họa bối cảnh; không chứng minh số liệu hoặc tình trạng tài chính, ý định và kết quả của người/doanh nghiệp trong hình.

Ảnh đang được đặt `cover`, điểm ngắm 50%/50%, phóng/di ngang nhẹ, lớp tối và chữ phủ; đó là thay đổi khung trình bày. Clip tắt âm nguồn, giữ tốc độ gốc. Khoảng dùng dưới đây lấy từ dữ liệu dựng, không phải quan sát bản MP4 cuối.

| Cảnh / ID | Tác giả, nguồn và giấy phép | Ngày và địa điểm | Biến đổi và giới hạn |
| --- | --- | --- | --- |
| f07 / cn-auto-assembly | **Siyuwj**, [Geely assembly line in Beilun, Ningbo](https://commons.wikimedia.org/wiki/File:Geely_assembly_line_in_Beilun,_Ningbo.JPG), [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) | Chụp 22/12/2011; Bắc Luân, Ninh Ba | Thumbnail → JPEG, chuẩn bị bản public; cắt `cover`/chuyển động nhẹ. Geely, không phải BYD hay mặc định xe điện; không chứng minh sản lượng/việc làm |
| f07 / cn-toy-assembly-workers | **Encik Tekateki**, [Pengeluaran produksi Rubik Kiub](https://commons.wikimedia.org/wiki/File:Pengeluaran_produksi_Rubik_Kiub.png), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 27/12/2022; Quảng Đông, chưa xác nhận nhà máy/thành phố | Thumbnail → JPEG, cắt/chuyển động nhẹ; công nhân lắp khối xếp hình. Không suy ra lương, quyền lao động hay điều kiện chung cả nước |
| h05 / cn-clip-guangzhou-retail | **LayG Traveller**, [Busy Guangzhou shopping center lifestyle scene](https://www.pexels.com/video/busy-guangzhou-shopping-center-lifestyle-scene-36692153/), [Pexels License](https://www.pexels.com/license/) | Đăng 23/03/2026, ngày quay chưa xác nhận; Quảng Châu | Bản dẫn xuất 0–9 giây, 720p/30fps H.264, bỏ âm; dùng khung [0,162), tức [0,5,400) giây. Người qua quầy CoCo, không chứng minh mua hàng hoặc tăng tiêu dùng |
| h05 / cn-shanghai-supermarket | **Shwangtianyuan**, [Qingmei Xianshi at Guohe Road, Yangpu District](https://commons.wikimedia.org/wiki/File:Qingmei_Xianshi_at_Guohe_Road,_Yangpu_District-20251021.jpg), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) | 21/10/2025; đường Quốc Hòa, Dương Phố, Thượng Hải | Thumbnail → JPEG, cắt/chuyển động nhẹ; mặt tiền siêu thị. Không chứng minh giỏ hàng, niềm tin, giá hay doanh số |
| d05 / cn-industry-robots | **Cory M. Grenier**, [Automated Robots Replace Workers in China](https://commons.wikimedia.org/wiki/File:Automated_Robots_Replace_Workers_in_China.jpg), [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0) | 08/05/2010; Trung Quốc, chưa rõ thành phố | Thumbnail → JPEG, cắt/chuyển động nhẹ. Chỉ thấy thiết bị tự động hóa; khẳng định trong tên tệp không được dùng làm bằng chứng mất việc |
| d05 / cn-silk-suzhou | **Caitriana Nicholson**, [Silk processing line](https://commons.wikimedia.org/wiki/File:Silk_processing_line_(7440308376).jpg), [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0) | 13/06/2012; Nhà máy tơ lụa số 1 Tô Châu | Thumbnail → JPEG, cắt/chuyển động nhẹ. Máy kéo/xử lý tơ; không phải robot, xe điện hay pin. Địa chỉ tác giả ở Bắc Kinh không phải nơi chụp |
| e04 / cn-clip-shenzhen-night | **LayG Traveller**, [Spectacular Shenzhen skyline at night](https://www.pexels.com/video/spectacular-shenzhen-skyline-at-night-35987653/), [Pexels License](https://www.pexels.com/license/) | Đăng 03/02/2026, ngày quay chưa xác nhận; Thâm Quyến | Bản dẫn xuất 0–9 giây, 720p/30fps H.264, bỏ âm; dùng khung [0,194), tức [0,6,467) giây. Cảnh đêm, không chứng minh tăng trưởng/giá nhà/lấp đầy |
| e04 / cn-shanghai-skyline | **Gankbank789**, [Shanghai Skyline 2025](https://commons.wikimedia.org/wiki/File:Shanghai_Skyline_2025.jpg), [CC0](https://creativecommons.org/publicdomain/zero/1.0/deed.en) | 07/07/2025; Lục Gia Chủy nhìn từ Bến Thượng Hải | Thumbnail → JPEG, cắt/chuyển động nhẹ; đường chân trời thành phố, không phải chỉ báo kinh tế |

## Quyền sử dụng và biên nhận

Các ảnh CC BY-SA và bản phái sinh của chính ảnh đó giữ nguyên giấy phép tương ứng, cùng tên tác giả/tác phẩm/nguồn và ghi thay đổi. Các sơ đồ, biểu đồ và mô phỏng được tạo riêng; không nhận là cảnh quay thực. Không áp điều khoản độc quyền lên các ảnh giấy phép mở. Nhãn hàng thực trong bối cảnh không hàm ý xác nhận nội dung.

Các clip được dẫn xuất trực tiếp từ URL video chính thức; không lưu bản 4K gốc trên đĩa. Hash ràng buộc bản dẫn xuất đã lưu, không phải toàn bộ tệp gốc từ xa. Ngày đăng nguồn không phải ngày quay.

`source-receipts.json` giữ hash nguồn và bản public; `sources-candidates.json` giữ quan sát/giới hạn/giấy phép; `sources/selected-photo-metadata.json` giữ metadata Commons; `sources/videos/download-receipts.json` giữ URL và biến đổi clip. `research/source-receipts.json` giữ năm công bố đã lưu, IMF có biên nhận bổ sung riêng. Âm thanh và bản phối có hồ sơ tại `audio-sources.json` và `sound-cues.json`; đo loudness không đồng nghĩa nghe liên tục. Phải ghi nhận việc xem bản xuất cuối riêng với kiểm tra nguồn này.
