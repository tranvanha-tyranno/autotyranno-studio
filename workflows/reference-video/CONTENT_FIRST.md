# Viết bài có trục, chia phần rõ, nhấn đúng ý — 14/11/2026

Người dùng bác chất lượng nội dung: lời luông tuồng, phân đoạn không rõ, chưa nhấn được điều từng đoạn đang nói. Đây là yêu cầu sửa cách viết và nghiên cứu nguồn. Đọc hồ sơ mới tại `docs/video-references/2026-11-14-content-study/`, đặc biệt chapter maps, `OWN_SCRIPT_DIAGNOSIS.md` và `REWRITE_EXERCISE.md`.

## Trước khi viết

Chọn một câu hỏi đủ cụ thể để người xem nhận ra điều đáng tò mò hoặc hệ quả với họ. Viết trước câu trả lời dự kiến bằng một câu, các điều chưa chắc và ví dụ nào có thể chứng minh/giải thích câu trả lời. Nếu câu trả lời chứa bốn đề tài ngang nhau, thu hẹp bài. Không dùng thời lượng mười phút làm lý do thêm kiến thức cho đủ.

Nghiên cứu mẫu theo **câu hỏi → lập luận → ví dụ → kết luận → lý do đi tiếp**. Tách lời nguồn đang khẳng định, sự thật đã kiểm độc lập và suy luận biên tập. Không chuyển sponsor thành một chương giải thích, không học các số/năm ASR sai hoặc xem lượt xem là bằng chứng nhân quả cho một thủ pháp. Ghi rõ mốc đọc và media đã kiểm; không gọi đọc caption/contact sheet là nghe/xem liên tục.

## Viết dàn chương trước lời hoàn chỉnh

Mỗi chương cần:

1. **Một câu hỏi** phát sinh từ điều người xem vừa biết.
2. **Một câu trả lời/luận điểm chính**, không phải nhãn chủ đề như “kinh tế”, “giải pháp”.
3. **Một cơ chế có mắt xích**: điều gì thay đổi, vì sao dẫn đến điều gì, điều kiện nào có thể làm kết quả khác.
4. **Ví dụ hoặc chứng cứ cụ thể**. Phân biệt số giả định, hình bối cảnh, tư liệu và dữ kiện có nguồn. Phản ví dụ dùng để kiểm kết luận, không chỉ để thêm “tuy nhiên”.
5. **Một điểm nhấn**: câu nào thật sự phải nhớ, hình cần làm rõ quan hệ nào. Một cảnh cần tâm điểm đọc được; không bày mọi con số/tiêu đề cùng lúc.
6. **Câu chốt** cho câu hỏi của chương, rồi **cầu nối có lý do** sang câu hỏi tiếp. “Tiếp theo là…” không đủ giải thích quan hệ.

Chương có thể dài ngắn khác nhau theo việc cần giải. Không ép mọi chương vào sáu câu, không ép mọi phim có cùng số chương hoặc nhịp cắt. Các trường trong bản đồ là công cụ biên tập, không được đọc nguyên như biểu mẫu trong lời thoại.

Đối với chuyện kể, nhân vật phải có mục tiêu/lựa chọn, nhận thông tin mới và chịu hệ quả có quan hệ nhân quả. Tên nhân vật lặp lại không tự tạo chuyện. Có thể chọn lối phân tích thay vì nhân vật nếu phù hợp đề tài; không dựng một nhân vật hình thức chỉ để gọi là storytelling.

## Đọc phản biện lời hoàn chỉnh

Đọc cả script ở dạng lời nghe liền mạch. Chưa cần dựng đẹp. Tự trả lời và ghi quan sát cụ thể cho sáu chiều:

| Chiều kiểm | Câu cần trả lời |
|---|---|
| Cấu trúc | Nếu bỏ tiêu đề trên màn hình, người nghe có nhận ra đang chuyển vấn đề và vì sao không? |
| Trọng tâm | Đoạn này làm việc gì? Bỏ nó có mất một mắt xích, chứng cứ hoặc hệ quả cần thiết không? |
| Căn cứ | Ví dụ có thật sự làm rõ kết luận không? Nó chứng minh được tới đâu? Có đang dùng một tiệm hư cấu để kết luận cả nền kinh tế không? |
| Tiến triển | Chương sau thêm hiểu biết mới hay chỉ nhắc lại ý cũ bằng phép tính/ẩn dụ khác? Câu hỏi nối có được trả không? |
| Trả lời lời hứa | Kết có trả đúng câu hỏi mở đầu bằng những gì đã giải thích, trước CTA không? |
| Lời nói tự nhiên | Có nhịp câu ngắn/dài theo ý, từ cụ thể và tình huống dễ theo dõi không? Có đang đọc một danh sách caveat/thuật ngữ đều đều không? |

Ghi cả điểm còn yếu và sửa chúng; không tự viết “accepted” chỉ vì đủ ô. Agent đọc và phản biện được script không đồng nghĩa người dùng duyệt video. Tài liệu tham khảo không huấn luyện trọng số mô hình.

## Bản đồ nội dung và chốt kiểm trước giọng mới

Lưu `editorial-map.json` tại batch (hoặc thư mục cha chứa các take của chính batch). Schema `reference-video-editorial/1` gồm:

```json
{
  "schema": "reference-video-editorial/1",
  "title": "Tên bài",
  "centralQuestion": "Một câu hỏi trung tâm",
  "thesis": "Câu trả lời dự kiến",
  "viewerStake": "Vì sao người xem cần hiểu",
  "hookPromise": "Bài hứa làm rõ điều gì",
  "exclusions": ["Nhánh chủ động không bàn trong bài này"],
  "units": [
    {"id": "h01", "phase": "hook", "text": "Lời thực tế của hook."},
    {"id": "d01", "phase": "disclaimer", "text": "Lời miễn trừ đúng phạm vi."},
    {"id": "c01", "phase": "content", "text": "Lời thực tế của chương một."},
    {"id": "c02", "phase": "content", "text": "Lời thực tế của chương kết."},
    {"id": "cta01", "phase": "cta", "text": "Lời kêu gọi cụ thể liên quan."}
  ],
  "chapters": [
    {
      "id": "chapter-1", "title": "Tên có nội dung", "unitIds": ["c01"],
      "question": "Chương này trả lời gì?", "answer": "Luận điểm của chương",
      "mechanism": "Các mắt xích và điều kiện", "whyItMatters": "Hệ quả với người xem",
      "takeaway": "Chốt một ý",
      "evidenceExamples": [{"kind": "illustrative", "detail": "Ví dụ có phạm vi rõ"}],
      "emphasis": {"spokenQuote": "Lời thực tế của chương một.", "visualFocus": "Quan hệ cần thấy", "purpose": "Vì sao phải nhấn"},
      "bridge": {"reason": "Kết quả này còn để lại vấn đề nào", "nextQuestion": "Câu hỏi của chương sau"}
    },
    {
      "id": "chapter-final", "title": "Trả lời câu mở", "unitIds": ["c02"],
      "question": "Câu hỏi cuối", "answer": "Câu trả lời",
      "mechanism": "Tổng hợp các mắt xích đã có", "whyItMatters": "Ý nghĩa",
      "takeaway": "Chốt bài",
      "evidenceExamples": [{"kind": "illustrative", "detail": "Gọi lại ví dụ đã giải"}],
      "emphasis": {"spokenQuote": "Lời thực tế của chương kết.", "visualFocus": "Kết quả đã giải", "purpose": "Trả lời hook"}
    }
  ],
  "payoff": {"answer": "Câu trả lời cuối cho hook", "unitIds": ["c02"]},
  "review": {"status": "revision_needed"}
}
```

Đây là ví dụ hình dạng, chưa là map được duyệt. Sau khi đọc đầy đủ và sửa, `review` ghi `status: accepted`, `method: full_script_read`, `reviewer: {kind: agent, name: tên người/agent kiểm}`, `unresolvedIssues: []`. `checks` có sáu key `structure`, `focus`, `evidence`, `progression`, `payoff`, `spokenNaturalness`, mỗi key có `decision: accepted` và `observation` cụ thể sau đọc. `contentSHA256` lấy bằng `editorial_gate.content_hash(document)`; nó pin cả lời lẫn lý do của chương, không chỉ tiêu đề. Thay script/map phải đọc và ghi review lại. Không tự lấy hash làm chứng nhận văn hay.

### Bỏ phần miễn trừ đọc riêng khi người dùng yêu cầu

Mặc định không có `structurePolicy`, hoặc đặt `hook-disclaimer-content-cta`, vẫn yêu cầu bốn phần. Khi người dùng trực tiếp yêu cầu bỏ opening disclaimer, đặt `structurePolicy: "no-spoken-disclaimer-user-requested"`; thứ tự lời lúc đó là `hook → content → cta`, không thêm một unit disclaimer để đi vòng yêu cầu. Ghi nguồn chỉ dẫn người dùng trong hồ sơ brief/review của batch. Đây là tùy chọn thực hiện yêu cầu đã có, không phải một lượt xin phép mới. Bản bánh mì documentary dùng tùy chọn này; câu “tiệm giả định” được lồng vào nội dung để giữ đúng phạm vi ví dụ, không mở một bài miễn trừ dài. Thay policy cũng thay hash nội dung và cần đọc review lại như thay script.

`emphasis.spokenQuote` phải là đúng trích đoạn lời đọc, giữ dấu âm/dương, dấu phân cách số và dấu câu; chỉ khoảng trắng/NFC được chuẩn hóa. Không bỏ dấu `-` rồi coi `-2,8` và `2,8` là cùng câu nhấn.

```powershell
python -X utf8 workflows/reference-video/editorial_gate.py videos/BATCH/editorial-map.json --report videos/BATCH/review/editorial-check.json
```

`eleven_audio.generate()` kiểm map **trước khi đọc credential, ghi ý định request hoặc gửi timed TTS mới**. Mỗi take cần khớp nguyên các unit liên tiếp trong map đã đọc; không được lấy một map cũ để hợp thức hóa lời mới. Receipt giọng mới lưu path/hash map. Đây là kiểm tự động trong phạm vi công việc agent được giao, không thêm bước xin phép người dùng.

Exact take đã có và cache đúng request vẫn dùng được để sửa hình, không bắt viết lại lời/thu lại âm thanh của batch cũ. Sound/music không đi qua kiểm bản đồ lời này. Kiểm coverage/hash chỉ bắt thiếu chương và review lỗi thời; không thể đo độ hay, nhịp nghe, độ đúng mọi nguồn, chất lượng phim hoặc sự chấp thuận của người dùng.

Sau khi script vững mới tìm hình theo từng mệnh đề, thu exact Nhật Phong khi tác vụ sản xuất được yêu cầu, và dựng điểm nhấn. Nghiên cứu lần này không đổi renderer, không tạo giọng/nhạc/video mới và không đổi trạng thái các bản bị bác thành đạt.
