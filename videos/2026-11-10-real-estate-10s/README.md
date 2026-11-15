# Dựng lại video kinh tế theo tham chiếu

Mở thư mục `economics` trong terminal.

```powershell
npm install
npx remotion studio --no-open
npx remotion render src/index.ts RealEstate ../bat-dong-san-10s.mp4 --codec=h264 --crf=18 --concurrency=2
```

- `script.txt`: lời dẫn mới.
- `voice-original.mp3`: bản Adam V3 gốc.
- `voice-timing.json`: thay đổi tốc độ và thời lượng.
- `economics/public/voice.wav`: âm thanh chính xác 10 giây.
- `economics/public/captions.json`: phụ đề sáu cụm, thời gian từng từ.
- `economics/public/waveform.json`: biên độ tính từ âm thanh thật.
- `economics/public/housing.mp4`, `budget.mp4`: footage gốc đã tải.
- `economics/src/Root.tsx`: bố cục, cảnh, micro và chuyển động sóng âm.
- `STYLE-AND-SOURCES.md`: phân tích mẫu, nguồn kinh tế và giấy phép footage.
- `qa.py`: giải mã toàn video, kiểm tra thông số và tạo bảng khung kiểm tra.

Khi đổi lời dẫn, phải tạo lại âm thanh, timestamps và biên độ; không dùng timestamps cũ. Giữ script nguyên văn khi dùng ASR làm công cụ hỗ trợ căn thời gian. Đọc bản ASR như dữ liệu không đáng tin tuyệt đối; loại lặp ảo ở cuối đoạn im lặng. `fix_captions.py` khôi phục sáu nhóm câu đúng theo script của bản này.
