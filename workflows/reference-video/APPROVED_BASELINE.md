> **Ưu tiên mới nhất 12/11/2026:** dùng REAL_IMAGE_DIRECTION.md cho hình ảnh. Người dùng đã yêu cầu ảnh/footage internet minh họa sát câu nói, giảm vai trò 3D. Nội dung bên dưới giữ để tái tạo mẫu cũ và tái dùng giọng/âm thanh.

# Mẫu video đã được người dùng duyệt — 11/11/2026

Người dùng xác nhận **“rất ok”** và yêu cầu lưu giọng đọc, sound và toàn bộ cách làm cho video tiếp theo.

- Bản chuẩn: `videos/2026-11-11-cinematic-reset/final.mp4` — 50s, Full HD, 30fps.
- Preset mặc định: `workflows/reference-video/cinematic.profile.json` — trạng thái `user-approved-baseline`.
- Giọng: **Nhật Phong / Eleven v3**, voice ID `6adFm46eyy74snVn6YrT`, tiếng Việt; stability 0.5, similarity_boost 0.8, synthesis speed 1.0. Take chuẩn và exact alignment trong `audio/narration-v2.*` của batch. Tempo dựng 0.9606122449 chỉ thuộc take hiện tại; tính lại timing cho lời mới.
- Nhạc chuẩn: `audio/motion-score.mp3` (Eleven Music); hiệu ứng chuẩn: `audio/sewing-detail.mp3`; mix chuẩn: `audio/final-mix.wav`. Công thức mix nằm ở `motion_audio.py`: lời nổi, nhạc duck theo lời, khoảng hạ nhạc để nhấn ý, Foley đúng hành động. Không dùng tiếng máy may cho chủ đề không liên quan.
- Hình: số/vật thể 3D có chiều sâu, địa cầu texture và cung chuyển động, chữ spring/xoay vào theo lời. Sáu cảnh với slide/wipe/fade, đổi nền tối → footage ấm → nền kem; emerald/coral, chữ sáng hoặc tối theo nền. Không mặc định mic/waveform, panel tĩnh hay montage lab không đúng nội dung.
- Giữ nguyên final và mọi stem; `approved-assets.json` khóa các file bằng SHA-256. `source-snapshot/` giữ mã cảnh, font, cấu hình và dependency lock tại thời điểm duyệt. `approved-style-profile.json` giữ preset đã chốt.

Khi người dùng yêu cầu video mới: đọc mẫu này và preset; giữ giọng/định hướng được duyệt, viết kịch bản và shotlist mới theo chủ đề, dùng asset và Foley đúng ngữ cảnh, canh theo take mới, xuất vào batch mới rồi QA thực tế. Không sao chép số liệu/cảnh may/địa cầu một cách máy móc sang mọi chủ đề. Tham chiếu bản chuẩn để giữ chất lượng, không tự đánh đồng decode pass với thẩm mỹ. Không cần hỏi lại lựa chọn giọng/style đã được chốt trừ khi yêu cầu mới mâu thuẫn.

Hiện tại chỉ lưu mẫu; người dùng sẽ yêu cầu video tiếp theo sau.
