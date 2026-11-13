# Finance cast — thư viện nhân vật hoạt hình 2D gốc

30 người trưởng thành hư cấu để kể chuyện tài chính đời thường. Các vai trò là vai diễn kể chuyện, không khẳng định chuyên môn hay đưa lời khuyên đầu tư. Không mô phỏng người thật hoặc sao chép nhân vật trong ảnh tham khảo.

`roster.ts` là danh sách chuẩn dùng khi render. Bản dữ liệu tương ứng ở `workflows/reference-video/finance-cast.json`. Mỗi nhân vật có phối hợp kiểu tóc, trang phục, vóc dáng và phụ kiện riêng; không chỉ đổi màu một hình.

## Dùng trong cảnh

```tsx
import {Character} from './finance-cast';
<svg viewBox="0 0 1920 1080">
  <Character id={1} x={500} y={900} scale={1.35}
    emotion="worried" pose="shrug" frame={frame} speaking={false}/>
</svg>
```

`x,y` là vị trí bàn chân. Hệ tọa độ gốc ở tư thế đứng xấp xỉ ±105px ngang, -485..0px dọc; khi duỗi tay chừa tới ±210px ngang. `flip` lật hướng nhân vật nhưng không nên dùng để lật văn bản kèm theo. Đường viền, da, quần áo, tay, đầu, mắt và miệng đều là SVG, điều khiển theo frame; không gọi mô hình tạo video.

- Biểu cảm: `neutral`, `happy`, `worried`, `surprised`, `thinking`, `confident`.
- Tư thế: `idle`, `talk`, `point`, `shrug`, `give`, `receive`, `celebrate`.
- `speaking`: bật nhịp miệng đơn giản. Đây **không phải** lip-sync tiếng Việt hay căn âm vị; có thể tắt cho cảnh lời dẫn ngoài hình. Cần ánh xạ bằng take/timing thật cho nhân vật nói.
- `frame`: chớp mắt, chuyển động đầu, thân và tay đều tái lập được theo frame, không CSS animation.

`CastSheet` là bảng 1920×1080 chứa đủ 30 nhân vật. `CastMotion` là composition 1920×1080, 30fps, 360 frame/12 giây để kiểm chuyển động: sáu nhân vật, sáu nhịp tư thế/biểu cảm. Hai composition này không có nhạc hoặc lời, không chứa thương hiệu kênh. Không coi thư viện hoặc kiểm render là người dùng đã duyệt phong cách.

Xuất 30 SVG nền trong suốt từ thư mục `cinematic/`: `node src/finance-cast/export-cast.cjs ../../../videos/BATCH/cast-library`. SVG tĩnh dùng tư thế đứng; chuyển động dùng component `Character` trực tiếp.

## Giới hạn

Đây là cutout SVG 2D, không phải 3D hay footage, và không phải asset tạo bằng ImageGen. Các thao tác tài chính/đạo cụ và tương tác giữa người phải được dựng trong cảnh mẹ; một tư thế đưa tay không tự chứng minh đã trao một vật. Khi dùng nhiều người, đặt đạo cụ theo vị trí bàn tay và căn phản ứng theo đúng câu nói.
