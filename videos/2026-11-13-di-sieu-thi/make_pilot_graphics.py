"""Original, explicitly illustrative graphics for this pilot's worked example."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
OUT = ROOT / 'long/assets'
OUT.mkdir(parents=True, exist_ok=True)
INK, PAPER, ACCENT = '#1c1b18', '#f1ebdf', '#e85e3e'


def font(size, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/' + ('arialbd.ttf' if bold else 'arial.ttf'), size)


def label(draw, xy, text, size=44, fill=INK, bold=False, anchor=None):
    draw.text(xy, text, font=font(size, bold), fill=fill, anchor=anchor)


def carton(draw, x, y, color):
    draw.rounded_rectangle((x, y, x + 150, y + 230), radius=15, fill=color)
    draw.polygon([(x, y), (x + 32, y - 48), (x + 119, y - 48), (x + 150, y)], fill=color)
    draw.line((x + 32, y - 48, x + 32, y - 18, x + 119, y - 18), fill=PAPER, width=4)
    draw.ellipse((x + 43, y + 72, x + 107, y + 136), fill=PAPER)


def prices(total=False, revised=False):
    im = Image.new('RGB', (1920, 1080), PAPER)
    d = ImageDraw.Draw(im)
    label(d, (90, 65), 'VÍ DỤ GIẢ ĐỊNH · KHÔNG PHẢI GIÁ BÁN', 28, '#6b665d')
    d.line((960, 180, 960, 820), fill='#c7beae', width=2)
    carton(d, 390, 310, '#689b83')
    carton(d, 1190, 310, '#689b83')
    carton(d, 1370, 310, '#689b83')
    label(d, (465, 180), 'MUA 1 HỘP', 42, anchor='mm', bold=True)
    label(d, (1340, 180), 'MUA 2 HỘP', 42, anchor='mm', bold=True)
    label(d, (465, 630), '30.000đ', 88, anchor='mm', bold=True)
    label(d, (1340, 630), '50.000đ', 88, anchor='mm', bold=True)
    label(d, (465, 735), '30.000đ / hộp', 40, anchor='mm')
    label(d, (1340, 735), '25.000đ / hộp', 40, anchor='mm')
    if total:
        d.rounded_rectangle((605, 840, 1315, 950), radius=18, fill=INK)
        label(d, (960, 895), 'CHI THÊM 20.000đ' if revised else 'TỔNG CHI: +20.000đ', 50, PAPER, True, 'mm')
    else:
        label(d, (960, 895), 'Giá mỗi hộp thấp hơn. Tổng tiền cao hơn.', 44, anchor='mm')
    im.save(OUT / ('total-change.jpg' if revised else 'total-example.jpg' if total else 'price-example.jpg'), quality=95)


prices()
prices(True)
prices(True, True)
im = Image.new('RGB', (1600, 1100), '#eee7da')
d = ImageDraw.Draw(im)
d.rounded_rectangle((190, 95, 1410, 1010), radius=28, fill='#fffaf1')
label(d, (280, 160), 'TRƯỚC KHI ĐI', 32, '#807665')
label(d, (280, 245), 'Mua gì, bao nhiêu?', 66, bold=True)
for y, text in [(440, 'Món cần mua'), (610, 'Số lượng sẽ dùng'), (780, 'Đồ ở nhà còn lại')]:
    d.rounded_rectangle((285, y - 25, 340, y + 30), radius=8, outline='#799882', width=5)
    label(d, (385, y), text, 48, anchor='lm')
label(d, (280, 940), 'Minh họa cách ghi · tự điền theo nhu cầu', 28, '#807665')
im.save(OUT / 'shopping-list.jpg', quality=95)
