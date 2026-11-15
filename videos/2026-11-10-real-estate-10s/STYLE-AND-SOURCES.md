# Phân tích mẫu và nguồn

Video tham chiếu do người dùng cung cấp: 22 phút 56,69 giây; 1920×1080, 30 fps. Đã xem 12 khung tại các mốc từ 0 giây tới 17 phút 12 giây và nhận dạng giọng nói 45 giây mở đầu. Bản ASR thô có lỗi chính tả, chỉ dùng nhận diện cấu trúc kể chuyện.

Đặc điểm áp dụng: câu hỏi gây tò mò → cơ chế nguyên nhân–kết quả bằng ngôn ngữ bình dân; footage đời sống phủ tối, micro trắng ở trung tâm, sóng âm chuyển động theo biên độ lời mới, phụ đề ngắn và tô từ đang đọc. Giữ tỷ lệ ngang 16:9. Tên hiển thị mới: GÓC NHÌN KINH TẾ. Không sử dụng logo, âm thanh hoặc footage trích từ kênh trong thành phẩm. Đây là hồ sơ cách dựng, không phải huấn luyện trọng số mô hình.

Kịch bản là giải thích khái quát một kênh tác động, không khẳng định mọi lần nhà giảm giá đều gây suy thoái và không phải số liệu thị trường hiện tại.

Nguồn cơ chế kinh tế:
- IMF, China 2025 Article IV Consultation (2026): https://www.imf.org/en/publications/cr/issues/2026/02/17/peoples-republic-of-china-2025-article-iv-consultation-press-release-staff-report-and-574028
- IMF, giải thích tác động tài sản nhà ở tới tiêu dùng: https://www.elibrary.imf.org/view/journals/002/2026/044/article-A001-en.xml

Footage minh họa, không đại diện một địa điểm hay sự kiện được xác minh trong lời dẫn:
- Vijay R / Pexels: https://www.pexels.com/video/aerial-view-of-apartment-buildings-in-the-city-15847247/
- Mikhail Nilov / Pexels: https://www.pexels.com/video/woman-counting-money-7735860/
- Giấy phép: https://www.pexels.com/license/

Âm thanh: ElevenLabs Adam, eleven_v3, tiếng Việt; bản gốc 9,8 giây, chỉnh tốc độ nhẹ 1,037× và thêm khoảng nghỉ đầu/cuối để khớp video 10 giây. Không sao chép giọng riêng của người dẫn trong tham chiếu.

Mã dựng có thể sửa và render lại trong economics/src/Root.tsx. Chạy trong economics: npm install; npx remotion render src/index.ts RealEstate ../bat-dong-san-10s.mp4 --codec=h264 --crf=18.
