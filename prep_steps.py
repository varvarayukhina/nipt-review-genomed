"""Иллюстрации из ChatGPT (~/Downloads) → img/*.webp: первый экран и этапы «Как работает НИПТ».

Картинки готовятся под Retina (ширина на экране × 2): обрезка и увеличение — sips (macOS),
сжатие — cwebp q88 с -sharp_yuv. При q80 и без увеличения картинки выходили «пиксельными».
"""
import subprocess
import tempfile
from pathlib import Path

SRC = Path.home() / "Downloads"
OUT = Path(__file__).parent / "img"
STAMP = "ChatGPT Image 24 сент. 2026 г., "
MAP = [  # исходник, имя, обрезка (x, y, w, h) или None, итоговая ширина (этап 4 рисуется в SVG)
    ("14_18_36.png", "hero-placenta", None, 2880),               # плацента → ДНК в крови мамы, во всю ширину (1440 × 2)
    ("14_20_57.png", "step-1-blood", (23, 385, 640, 320), 1440),  # фрагмент инфографики: малыш, плацента, кровь мамы
    ("14_13_10 (3).png", "step-2-tube", None, 1774),
    ("14_13_11 (4).png", "step-3-reads", None, 1774),
    ("14_13_12 (5).png", "step-5-result", None, 1774),
]
with tempfile.TemporaryDirectory() as tmp:
    for src, name, crop, width in MAP:
        png = Path(tmp) / f"{name}.png"
        cmd = ["sips", "-s", "format", "png"]
        if crop:
            x, y, w, h = crop
            cmd += ["-c", str(h), str(w), "--cropOffset", str(y), str(x)]
        subprocess.run([*cmd, str(SRC / (STAMP + src)), "--out", str(png)], check=True, capture_output=True)
        subprocess.run(["sips", "--resampleWidth", str(width), str(png)], check=True, capture_output=True)
        dst = OUT / f"{name}.webp"
        subprocess.run(["cwebp", "-quiet", "-q", "88", "-m", "6", "-sharp_yuv", str(png), "-o", str(dst)], check=True)
        print(f"{name:16} {dst.stat().st_size / 1024:6.0f} КБ")
