"""
Convert a photo to ASCII art for the profile card.

Usage:
    python make_ascii.py              # reads config.PORTRAIT_SRC
    python make_ascii.py path/to.jpg  # override with a specific file
"""
import os
import sys

from PIL import Image, ImageOps, ImageEnhance

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, REPO_ROOT)
import config  # noqa: E402  (import must follow sys.path setup)

ASSETS_DIR = os.path.join(REPO_ROOT, "assets")
OUT = os.path.join(ASSETS_DIR, "ascii_art.txt")

RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

COLS = 42
ASPECT = 0.46  # monospace glyphs are ~2x taller than wide


def to_ascii(path, cols=COLS):
    img = Image.open(path).convert("L")

    # crop to head + upper chest only (drop background halo and torso)
    w, h = img.size
    left = int(w * 0.18)
    right = int(w * 0.82)
    top = int(h * 0.15)
    bottom = int(h * 0.72)
    img = img.crop((left, top, right, bottom))

    img = ImageOps.autocontrast(img, cutoff=0.5)
    img = ImageEnhance.Contrast(img).enhance(1.4)
    img = ImageEnhance.Sharpness(img).enhance(1.5)
    # push the studio backdrop (including its vignette) toward pure white
    img = img.point(lambda p: 255 if p > 120 else p)

    w, h = img.size
    rows = max(1, int(cols * (h / w) * ASPECT))
    img = img.resize((cols, rows), Image.LANCZOS)
    pixels = list(img.getdata())

    BG_THRESHOLD = 165  # pixels lighter than this are treated as background -> blank

    ramp_len = len(RAMP) - 1
    lines = []
    for r in range(rows):
        row_pixels = pixels[r * cols:(r + 1) * cols]
        row = []
        for p in row_pixels:
            if p >= BG_THRESHOLD:
                row.append(" ")
            else:
                v = (BG_THRESHOLD - p) / BG_THRESHOLD
                row.append(RAMP[int(v ** 0.9 * ramp_len)])
        lines.append("".join(row))
    return "\n".join(lines)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else config.PORTRAIT_SRC
    if not os.path.isabs(src):
        src = os.path.join(REPO_ROOT, src)
    if not os.path.exists(src):
        raise SystemExit(
            f"Photo not found: {src}\n"
            f"Either place your photo at that path, or run: python make_ascii.py <path>"
        )
    art = to_ascii(src)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(art)
    print(art)


if __name__ == "__main__":
    main()
