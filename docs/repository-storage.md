# Lưu mã nguồn và dữ liệu trên GitHub

Theo yêu cầu ngày 15/11/2026, repo lưu cả mã nguồn **và video/dữ liệu liên quan**,
đồng thời lọc video dư. Danh sách cụ thể nằm trong [media-publication.json](media-publication.json).

## Nội dung được lưu

- Backend, frontend, workflow Python, source Remotion và các file khóa dependency.
- Kịch bản, prompt, cấu hình, timeline, editorial map, nghiên cứu và ghi nhận phản hồi.
- 14 bản xuất được chọn: bản mới nhất hữu ích của từng nhánh, baseline đã duyệt và hai preview so sánh; bản bread-lab vẫn được ghi rõ là preview tạm.
- Hai phim AI ảnh thật và quán cà phê có cả bản gốc chất lượng cao `final.mp4` và bản `github-final-720p.mp4` nhẹ hơn. Bản 720p dùng H.264 CRF 24, giữ nguyên audio; đường dẫn/hash gốc được ghi trong manifest.
- Đợt bổ sung lưu 10 mix cuối/excerpt chuẩn: 9 file WAV và một WAV được nén ZIP không mất dữ liệu. Giữ một bản canonical của mỗi mix để khôi phục đúng audio; mix bread-lab vẫn là bản tạm khi OpenAI narration bị chặn.
- Media đã có trên GitHub, ảnh/footage nguồn sản xuất, take âm thanh nén và tài nguyên cần thiết trong `videos/`.
- URL, transcript và hồ sơ phân tích tham chiếu trong `docs/video-references/`.
- Snapshot source theo batch để giữ khả năng đối chiếu bản đã render.
- Báo cáo nghiên cứu/cài đặt skill; nguồn bên ngoài được xác định bằng URL, commit và hash trong các báo cáo.

Video, âm thanh, ảnh, PDF và font dùng **Git LFS** theo `.gitattributes`.
Git lưu pointer nhỏ; Git LFS lưu nội dung thật và dùng chung object cho các file có cùng nội dung.

## Nội dung giữ ở máy, không đưa lên GitHub

- `.secrets/`, `.env` chứa khóa, tài khoản, cookie, phiên trình duyệt và dữ liệu Studio riêng.
- Database đang chạy, cache, log, `node_modules`, build frontend và output tạm.
- Các thư mục `bundle`, `bundle-*`, `*-bundle`, `*-bundle-*`, `production-public`, `render-public*` bên trong `videos/`: đây là bản sao phục vụ renderer, không phải bản video lưu trữ.
- `docs/video-skills/*/sources/`: repo bên thứ ba giải nén, archive tải xuống và ví dụ đi kèm. Báo cáo/receipt nghiên cứu vẫn được lưu.
- Bản sao media staging tại `workflows/reference-video/cinematic/public/`; các JSON phục vụ import composition vẫn được lưu theo quy tắc hiện có.
- Ledger học tập local tại `workflows/reference-video/learning-data/` theo chính sách hiện có.
- Bản render bị thay thế, silent/picture pass, chunk, proof, frame QA, WAV normalized/music bed/stem trung gian có thể dựng lại và các bản sao của cùng mix. Báo cáo QA/receipt vẫn được lưu; mix cuối được chọn là ngoại lệ có lưu trữ.
- Video tham chiếu tải từ bên ngoài và ảnh mẫu trích xuất; giữ nguyên tại máy cùng hồ sơ nguồn.
- HTML thô trong `research/sfx-source-pages/` có token website bên thứ ba. URL nguồn/giấy phép và receipt vẫn được lưu.

Các quy tắc trên chỉ lọc khỏi Git, không xóa dữ liệu local. Không bỏ toàn bộ
`render-attempts/` hay `source-snapshot/`: chúng có thể chứa receipt và source riêng.
`videos/.gitignore` có danh sách media được giữ; thêm video mới cần lựa chọn và cập nhật danh sách này.
Các bản xuất cũ hoặc WAV trung gian đã lọc cần dữ liệu local nếu muốn tái hiện chính xác chúng.

## Lấy đầy đủ dữ liệu ở máy khác

```powershell
git lfs install
git clone --recurse-submodules https://github.com/tranvanha-tyranno/autotyranno-studio.git
cd autotyranno-studio
git lfs pull
```

Mix của phim lạm phát bánh mì nằm trong ZIP để giảm dung lượng. Khi cần render
trên checkout mới, giải nén vào đúng thư mục; nội dung khôi phục đã được kiểm
tra khớp SHA-256 với WAV gốc:

```powershell
Expand-Archive -LiteralPath 'videos/2026-11-14-o-banh-mi-va-lam-phat/audio/final-mix.wav.zip' -DestinationPath 'videos/2026-11-14-o-banh-mi-va-lam-phat/audio'
```

Nếu chỉ cần code trước, có thể clone với `GIT_LFS_SKIP_SMUDGE=1`, rồi tải từng batch:

```powershell
$env:GIT_LFS_SKIP_SMUDGE = '1'
git clone --recurse-submodules https://github.com/tranvanha-tyranno/autotyranno-studio.git
Remove-Item Env:GIT_LFS_SKIP_SMUDGE
cd autotyranno-studio
git lfs pull --include="videos/<ten-batch>/**"
```

Dependency và bundle render được dựng lại theo README của từng workflow.
Credential được cấu hình riêng trên máy mới; không nằm trong repo.
