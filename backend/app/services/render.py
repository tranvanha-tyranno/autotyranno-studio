from __future__ import annotations

import shutil
import subprocess
import uuid
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

from ..config import settings


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def _load_image(path: str, size: tuple[int, int]) -> Image.Image:
    if path and Path(path).exists():
        try:
            image = Image.open(path).convert("RGB")
            return ImageOps.contain(image, size)
        except Exception:
            pass
    image = Image.new("RGB", size, (33, 43, 66))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((10, 10, size[0] - 10, size[1] - 10), radius=24, outline=(80, 220, 180), width=4)
    draw.text((size[0] // 2, size[1] // 2), "PRODUCT", anchor="mm", fill="white", font=_font(44))
    return image


def render_video(product: dict, script: dict, template: str = "product_slideshow") -> tuple[str, str]:
    job_dir = settings.media_root / "renders" / uuid.uuid4().hex
    frames_dir = job_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    width, height = settings.video_width, settings.video_height
    image = _load_image(product.get("image_path", ""), (width - 100, 700))
    slides = [
        (script.get("hook", "Sản phẩm đáng thử hôm nay"), (24, 34, 55)),
        (product.get("name", "Sản phẩm"), (18, 67, 55)),
        (script.get("cta", "Xem ngay ở link trong mô tả"), (56, 35, 84)),
    ]
    poster_path = job_dir / "poster.jpg"
    for index, (headline, background) in enumerate(slides):
        frame = Image.new("RGB", (width, height), background)
        draw = ImageDraw.Draw(frame)
        draw.rectangle((0, 0, width, 18), fill=(255, 198, 70))
        frame.paste(image, ((width - image.width) // 2, 120))
        draw.rounded_rectangle((40, 870, width - 40, height - 70), radius=30, fill=(0, 0, 0, 110))
        draw.text((width // 2, 955), headline, anchor="mm", align="center", fill="white", font=_font(38))
        if product.get("price") is not None:
            draw.text((width // 2, 1100), f"{product['price']:,.0f} {product.get('currency', 'VND')}", anchor="mm", fill=(255, 220, 100), font=_font(42))
        draw.text((width // 2, height - 120), "AFFILIATE AUTO", anchor="mm", fill=(220, 230, 240), font=_font(24))
        frame_path = frames_dir / f"frame_{index:03d}.png"
        frame.save(frame_path)
        if index == 0:
            frame.save(poster_path, quality=92)

    output_path = job_dir / "video.mp4"
    try:
        import imageio_ffmpeg

        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [
            ffmpeg,
            "-y",
            "-framerate", "1/3",
            "-i", str(frames_dir / "frame_%03d.png"),
            "-vf", f"scale={width}:{height},format=yuv420p",
            "-r", str(settings.video_fps),
            "-pix_fmt", "yuv420p",
            str(output_path),
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except Exception as exc:
        # A manifest remains useful for local development when ffmpeg is unavailable.
        output_path = job_dir / "video-manifest.txt"
        output_path.write_text(f"Video render fallback: {exc}\nTemplate: {template}\n", encoding="utf-8")
    return str(output_path), str(poster_path)
