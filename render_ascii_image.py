from PIL import Image, ImageDraw, ImageFont

ART_PATH = r"D:\Claude Local Session\github-profile-readme\ascii_art.txt"
OUT_PATH = r"D:\Claude Local Session\github-profile-readme\ascii_portrait.png"
FONT_PATH = r"C:\Windows\Fonts\consola.ttf"

FONT_SIZE = 6
LINE_HEIGHT = 7

with open(ART_PATH, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

# measure a character cell
bbox = font.getbbox("M")
char_w = bbox[2] - bbox[0] + 1
cols = max(len(l) for l in lines)
rows = len(lines)

img_w = cols * char_w
img_h = rows * LINE_HEIGHT

img = Image.new("RGB", (img_w, img_h), color=(13, 17, 23))  # GitHub dark bg
draw = ImageDraw.Draw(img)

for i, line in enumerate(lines):
    draw.text((0, i * LINE_HEIGHT), line, font=font, fill=(201, 209, 217))

img.save(OUT_PATH)
print(img_w, img_h)
