import json
import os
import time
import urllib.request
from xml.sax.saxutils import escape

REPO_DIR = os.path.dirname(__file__)
ASCII_PATH = os.path.join(REPO_DIR, "ascii_art.txt")
USERNAME = "himanshubora99"

FONT_SIZE = 16
LINE_H = 20
CHAR_W = 9.6  # approx Consolas advance width at 16px
ASCII_X = 15
INFO_X = 420
TOP_Y = 30
MARGIN = 25

THEMES = {
    "dark": dict(
        bg="#161b22", ascii_fill="#c9d1d9", base="#c9d1d9",
        key="#ffa657", value="#a5d6ff", cc="#616e7f",
        add="#3fb950", delc="#f85149",
    ),
    "light": dict(
        bg="#f6f8fa", ascii_fill="#24292f", base="#24292f",
        key="#953800", value="#0a3069", cc="#c2cfde",
        add="#1a7f37", delc="#cf222e",
    ),
}


def get_token():
    env_token = os.environ.get("STATS_TOKEN")
    if env_token:
        return env_token
    import subprocess
    p = subprocess.run(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\n\n",
        capture_output=True, text=True
    )
    for line in p.stdout.splitlines():
        if line.startswith("password="):
            return line[len("password="):]
    raise RuntimeError("no token")


def api(token, path, accept="application/vnd.github+json"):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={"Authorization": f"token {token}", "Accept": accept, "User-Agent": "card-script"}
    )
    with urllib.request.urlopen(req) as r:
        return r.status, json.load(r)


def fetch_stats(token):
    _, repos = api(token, "/user/repos?per_page=100&affiliation=owner")
    owned_repos = [r for r in repos if not r["fork"]]
    total_stars = sum(r["stargazers_count"] for r in owned_repos)
    total_repos = len(owned_repos)

    _, user = api(token, f"/users/{USERNAME}")
    followers = user["followers"]

    _, search = api(token, f"/search/commits?q=author:{USERNAME}", accept="application/vnd.github.cloak-preview+json")
    total_commits = search["total_count"]
    contributed = {item["repository"]["full_name"] for item in search.get("items", [])}

    total_add = 0
    total_del = 0
    for r in owned_repos:
        full = r["full_name"]
        stats = None
        status = None
        for _ in range(5):
            try:
                status, stats = api(token, f"/repos/{full}/stats/contributors")
            except Exception:
                stats = None
            if status == 200 and stats:
                break
            time.sleep(2)
        if not stats or status != 200:
            continue
        for c in stats:
            if c.get("author") and c["author"].get("login") == USERNAME:
                for w in c["weeks"]:
                    total_add += w["a"]
                    total_del += w["d"]

    return {
        "total_repos": total_repos,
        "contributed_repos": max(len(contributed), total_repos),
        "total_stars": total_stars,
        "followers": followers,
        "total_commits": total_commits,
        "total_add": total_add,
        "total_del": total_del,
    }


def kv_line(y, key, dots_n, value):
    plain = f". {key}: {'.' * dots_n} {value}"
    markup = (
        f'<tspan x="{INFO_X}" y="{y}" class="cc">. </tspan>'
        f'<tspan class="key">{escape(key)}</tspan>:'
        f'<tspan class="cc"> {"." * dots_n} </tspan>'
        f'<tspan class="value">{escape(value)}</tspan>'
    )
    return plain, markup


def build_info_lines(stats):
    loc = stats["total_add"] + stats["total_del"]
    rows = []  # (plain_text_or_None_for_header, markup, is_header)
    y = TOP_Y

    rows.append(("header", "himanshu@github", f'<tspan x="{INFO_X}" y="{y}">himanshu@github</tspan>'))
    y += LINE_H
    rows.append(("kv", *kv_line(y, "OS", 12, "Windows")))
    y += LINE_H
    rows.append(("kv", *kv_line(y, "Languages.Programming", 4, "Dart, JavaScript")))
    y += LINE_H
    rows.append(("kv", *kv_line(y, "Framework", 12, "Flutter")))
    y += LINE_H * 2
    rows.append(("header", "- Contact", f'<tspan x="{INFO_X}" y="{y}">- Contact</tspan>'))
    y += LINE_H
    rows.append(("kv", *kv_line(y, "Email", 6, "himanshubora98@gmail.com")))
    y += LINE_H
    rows.append(("kv", *kv_line(y, "LinkedIn", 8, "himanshu-bora-5265a9185")))
    y += LINE_H
    rows.append(("kv", *kv_line(y, "Portfolio", 13, "himanshubora.com")))
    y += LINE_H * 2
    rows.append(("header", "- GitHub Stats", f'<tspan x="{INFO_X}" y="{y}">- GitHub Stats</tspan>'))
    y += LINE_H

    repos_plain = f". Repos: .... {stats['total_repos']} {{Contributed: {stats['contributed_repos']}}} | Stars: ........... {stats['total_stars']}"
    repos_markup = (
        f'<tspan x="{INFO_X}" y="{y}" class="cc">. </tspan>'
        f'<tspan class="key">Repos</tspan>:<tspan class="cc"> .... </tspan>'
        f'<tspan class="value">{stats["total_repos"]}</tspan> '
        f'{{<tspan class="key">Contributed</tspan>: <tspan class="value">{stats["contributed_repos"]}</tspan>}} | '
        f'<tspan class="key">Stars</tspan>:<tspan class="cc"> ........... </tspan>'
        f'<tspan class="value">{stats["total_stars"]}</tspan>'
    )
    rows.append(("kv", repos_plain, repos_markup))
    y += LINE_H

    commits_plain = f". Commits: ............... {stats['total_commits']} | Followers: ....... {stats['followers']}"
    commits_markup = (
        f'<tspan x="{INFO_X}" y="{y}" class="cc">. </tspan>'
        f'<tspan class="key">Commits</tspan>:<tspan class="cc"> ............... </tspan>'
        f'<tspan class="value">{stats["total_commits"]}</tspan> | '
        f'<tspan class="key">Followers</tspan>:<tspan class="cc"> ....... </tspan>'
        f'<tspan class="value">{stats["followers"]}</tspan>'
    )
    rows.append(("kv", commits_plain, commits_markup))
    y += LINE_H

    loc_plain = f". Lines of Code on GitHub: {loc:,} ( {stats['total_add']:,}++, {stats['total_del']:,}-- )"
    loc_markup = (
        f'<tspan x="{INFO_X}" y="{y}" class="cc">. </tspan>'
        f'<tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc">. </tspan>'
        f'<tspan class="value">{loc:,}</tspan> ( '
        f'<tspan class="add">{stats["total_add"]:,}</tspan><tspan class="add">++</tspan>, '
        f'<tspan class="delc">{stats["total_del"]:,}</tspan><tspan class="delc">--</tspan> )'
    )
    rows.append(("kv", loc_plain, loc_markup))

    max_len = max(len(plain) for kind, plain, markup in rows if kind == "kv")

    final_tspans = []
    for kind, plain, markup in rows:
        if kind == "header":
            dash_n = max_len - len(plain) + 2
            final_tspans.append(f'{markup} -{"-" * max(dash_n, 3)}')
        else:
            final_tspans.append(markup)

    return final_tspans, y, max_len


def build_svg(theme_name, ascii_lines, info_tspans, height, width):
    t = THEMES[theme_name]
    ascii_tspans = []
    y = TOP_Y
    for line in ascii_lines:
        ascii_tspans.append(f'<tspan x="{ASCII_X}" y="{y}">{escape(line)}</tspan>')
        y += LINE_H

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" font-family="Consolas,Menlo,monospace" width="{width}px" height="{height}px" font-size="{FONT_SIZE}px">
<style>
.key {{fill: {t['key']};}}
.value {{fill: {t['value']};}}
.add {{fill: {t['add']};}}
.delc {{fill: {t['delc']};}}
.cc {{fill: {t['cc']};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="{width}px" height="{height}px" fill="{t['bg']}" rx="15"/>
<text x="{ASCII_X}" y="{TOP_Y}" fill="{t['ascii_fill']}">
{chr(10).join(ascii_tspans)}
</text>
<text x="{INFO_X}" y="{TOP_Y}" fill="{t['base']}">
{chr(10).join(info_tspans)}
</text>
</svg>
'''
    return svg


def main():
    token = get_token()
    stats = fetch_stats(token)

    with open(ASCII_PATH, "r", encoding="utf-8") as f:
        ascii_lines = f.read().splitlines()

    info_tspans, info_last_y, max_len = build_info_lines(stats)
    ascii_last_y = TOP_Y + LINE_H * (len(ascii_lines) - 1)
    height = max(ascii_last_y, info_last_y) + MARGIN
    width = int(INFO_X + max_len * CHAR_W + MARGIN)

    for theme in THEMES:
        svg = build_svg(theme, ascii_lines, info_tspans, height, width)
        out_path = os.path.join(REPO_DIR, f"card_{theme}.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {out_path} ({width}x{height})")


if __name__ == "__main__":
    main()
