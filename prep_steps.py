"""Иллюстрации из ChatGPT (~/Downloads) → img/*.webp через cwebp: первый экран и этапы «Как работает НИПТ»."""
import subprocess
from pathlib import Path

SRC = Path.home() / "Downloads"
OUT = Path(__file__).parent / "img"
STAMP = "ChatGPT Image 24 сент. 2026 г., "
MAP = [  # исходник, имя, параметры cwebp (этап 4 рисуется в SVG)
    ("14_18_36.png", "hero-placenta", []),                                 # плацента → ДНК в крови мамы, во всю ширину
    ("14_20_57.png", "step-1-blood", ["-crop", "23", "385", "640", "320"]),  # фрагмент инфографики: малыш, плацента, кровь мамы
    ("14_13_10 (3).png", "step-2-tube", ["-resize", "1400", "0"]),
    ("14_13_11 (4).png", "step-3-reads", ["-resize", "1400", "0"]),
    ("14_13_12 (5).png", "step-5-result", ["-resize", "1400", "0"]),
]
for src, name, args in MAP:
    dst = OUT / f"{name}.webp"
    subprocess.run(["cwebp", "-quiet", "-q", "80", "-m", "6", *args, str(SRC / (STAMP + src)), "-o", str(dst)], check=True)
    print(f"{name:16} {dst.stat().st_size / 1024:6.0f} КБ")
