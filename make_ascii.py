from PIL import Image, ImageOps, ImageEnhance

SRC = r"C:\Users\himan\Downloads\prof Profile.jpeg"
OUT = r"D:\Claude Local Session\github-profile-readme\ascii_art.txt"

RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

COLS = 40
ASPECT = 0.46  # monospace glyphs are ~2x taller than wide

def to_ascii(path, cols=COLS):
    img = Image.open(path).convert("L")

    # crop to a tighter head+shoulders frame (drop excess background/torso)
    w, h = img.size
    left = int(w * 0.10)
    right = int(w * 0.90)
    top = 0
    bottom = int(h * 0.85)
    img = img.crop((left, top, right, bottom))

    img = ImageOps.autocontrast(img, cutoff=0.5)
    img = ImageEnhance.Contrast(img).enhance(1.15)
    img = ImageEnhance.Sharpness(img).enhance(1.5)

    w, h = img.size
    rows = max(1, int(cols * (h / w) * ASPECT))
    img = img.resize((cols, rows), Image.LANCZOS)
    pixels = list(img.getdata())

    BG_THRESHOLD = 168  # pixels lighter than this are treated as background -> blank

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

art = to_ascii(SRC)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(art)
print(art)
