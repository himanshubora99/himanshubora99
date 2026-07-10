from xml.sax.saxutils import escape

ART_PATH = r"D:\Claude Local Session\github-profile-readme\ascii_art.txt"
OUT_PATH = r"D:\Claude Local Session\github-profile-readme\ascii_portrait.svg"

FONT_SIZE = 10
LINE_HEIGHT = 11
CHAR_W = 6.0  # approx monospace advance at this font-size

with open(ART_PATH, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

cols = max(len(l) for l in lines)
rows = len(lines)
width = round(cols * CHAR_W) + 6
height = rows * LINE_HEIGHT + 6

tspans = []
for i, line in enumerate(lines):
    y = (i + 1) * LINE_HEIGHT
    tspans.append(f'<tspan x="3" y="{y}">{escape(line)}</tspan>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}px" height="{height}px" font-family="Consolas,Menlo,monospace" font-size="{FONT_SIZE}px">
<style>
text, tspan {{ white-space: pre; }}
.art {{ fill: #57606a; }}
@media (prefers-color-scheme: dark) {{
  .art {{ fill: #8b949e; }}
}}
</style>
<text class="art" fill="#57606a">
{chr(10).join(tspans)}
</text>
</svg>
'''

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(svg)

print(width, height)
