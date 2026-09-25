"""Картинки из ChatGPT (~/Downloads) → img/*.webp: обрезка прозрачных полей, уменьшение, WebP с альфой."""
from pathlib import Path
from PIL import Image

SRC = Path.home() / "Downloads"
OUT = Path(__file__).parent / "img"
STAMP = "ChatGPT Image 25 сент. 2026 г., "
MAP = {  # исходник → (имя, максимальная сторона)
    "11_21_54 (1).png": ("hero-tube", 1100),
    "11_21_54 (2).png": ("ic-office", 360),
    "11_21_55 (3).png": ("ic-partner", 360),
    "11_21_55 (4).png": ("ic-home", 360),
    "11_21_55 (5).png": ("ic-chromosomes", 280),
    "11_21_56 (6).png": ("ic-drop", 280),
    "11_21_56 (7).png": ("ic-calendar", 280),
    "11_21_56 (8).png": ("ic-doctor", 280),
    "11_21_56 (9).png": ("ic-shield", 280),
}
OUT.mkdir(exist_ok=True)
for src, (name, side) in MAP.items():
    im = Image.open(SRC / (STAMP + src)).convert("RGBA")
    box = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    im = im.crop(box)
    im.thumbnail((side, side), Image.LANCZOS)
    dst = OUT / f"{name}.webp"
    im.save(dst, "WEBP", quality=86, method=6)
    print(f"{name:16} {im.size[0]:4}×{im.size[1]:<4} {dst.stat().st_size/1024:6.0f} КБ")
