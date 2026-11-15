# Tạo hình v2 — Comic biểu cảm mạnh, hơi hài hước

Phản hồi trực tiếp của người dùng: nhân vật vòng đầu chưa ưa mắt. Sau đó người dùng chọn **“Comic biểu cảm mạnh, hơi hài hước”**. Mặc định là `comic`; sheet tập trung hai người trưởng thành hư cấu Minh và Lan trong ba tình huống. Giữ nguyên thư viện cũ, chưa mở rộng lại 30 nhân vật và chưa tự coi tạo hình mới đã được duyệt.

- `toon`: khuôn mặt lớn, mắt có tròng trắng/mí mắt, lông mày lệch nhẹ, nét đậm mượt; tóc, đường hàm và trang phục casual gốc. Đây là hướng gần tinh thần ảnh tham khảo hơn, không sao chép mascot.
- `comic`: mặt vuông/rộng hơn, tóc khối gợn mạnh, nét dày tương phản, áo sọc và jacket khác hẳn toon.
- `line`: đầu nhỏ hơn, nét thanh, mặt/người dài hơn và trang phục tiết chế hơn, dành cho minh họa người trưởng thành.

`CandidateSheet`: composition 1920×1080, 1 frame, ba cột: hỏi xoáy / nhận ra vấn đề / nhẹ nhõm. Cả ba là comic. Các nhánh `toon`/`line` được giữ trong mã như phác thảo chưa chọn. Không dựng video hay gọi API từ module này.

## CharacterV2

Feet pivot: `x,y` là bàn chân. Bounds idle khoảng x±105, y -530..12; tư thế duỗi tay tới x±225. `scale` giữ nguyên đơn vị SVG. Cấu trúc tay có vai, khuỷu và cổ tay thực sự, không chỉ xoay một khối tay thẳng. Bàn tay mở có ngón, đối lập với khối nắm tay của bản đầu.

```tsx
import {CharacterV2,getHandAnchors} from './finance-cast-v2';
const actor = {id:2 as const,x:1250,y:930,scale:1.3,
  pose:'give' as const,emotion:'confident' as const,frame,
  flip:true,variant:'comic' as const,gaze:'right' as const};
const palm=getHandAnchors(actor).right;
<CharacterV2 {...actor}/>
// Put the receipt near palm.x,palm.y. No text inside the flipped character.
```

`getHandAnchors` nhận cùng props với component, trả `left/right` theo giải phẫu trước khi lật, gồm `x,y` tâm lòng bàn tay, `wristX,wristY`, `angle`, `local`. Đã tính bob theo frame, scale và flip. `right` luôn là tay phải của nhân vật; khi flip, nó nằm bên trái màn hình.

Local wrist references (x/y, trước scale/flip, nhịp frame có sai số nhỏ khoảng 2px):

| Pose | Tay phải | Tay trái |
| --- | --- | --- |
| idle | 77,-179 | -77,-179 |
| talk | 164,-280 | -77,-179 |
| give | 174,-185 | -77,-179 |
| receive | 154,-185 | -154,-185 |
| point | 163,-334 | -77,-179 |
| shrug | 153,-305 | -153,-305 |
| celebrate | 128,-398 | -128,-398 |

Tại feet x400/1500 y930 scale1.3, tay hai người chưa thể chạm cùng vật ở x900 bằng tỷ lệ tự nhiên. Cần cho người tiến lại gần, hoặc chuyển vật thật từ lòng bàn tay Lan qua vùng giữa đến lòng bàn tay Minh. Không coi đưa tay gần một vật là đã nhận/trao vật.

`gaze` điều khiển tròng mắt trái/giữa/phải theo hệ local; flip sẽ lật hướng nhìn. `speaking` vẫn là hoạt họa miệng theo nhịp frame, **không phải** đồng bộ âm vị tiếng Việt. Lời nói và phản ứng phải căn theo audio take thật ở scene mẹ. Không có mouth motion mặc định khi `speaking=false`.

Geometry, mood and pose are source-controlled SVG/React. No raster AI generation, no paid requests. Các phương án chưa qua duyệt thẩm mỹ người dùng; cần xem actual render của sheet và proof excerpt trước khi chọn.
