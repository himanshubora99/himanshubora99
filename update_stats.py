import json
import os
import re
import time
import urllib.request

USERNAME = "himanshubora99"
TOKEN = os.environ["STATS_TOKEN"]
README_PATH = os.path.join(os.path.dirname(__file__), "README.md")

START_MARKER = "<!--STATS:START-->"
END_MARKER = "<!--STATS:END-->"


def api(path, accept="application/vnd.github+json"):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={"Authorization": f"token {TOKEN}", "Accept": accept, "User-Agent": "stats-script"}
    )
    with urllib.request.urlopen(req) as r:
        return r.status, json.load(r)


def fetch_stats():
    _, repos = api("/user/repos?per_page=100&affiliation=owner")
    owned_repos = [r for r in repos if not r["fork"]]
    total_stars = sum(r["stargazers_count"] for r in owned_repos)
    total_repos = len(owned_repos)

    _, user = api(f"/users/{USERNAME}")
    followers = user["followers"]

    _, search = api(f"/search/commits?q=author:{USERNAME}", accept="application/vnd.github.cloak-preview+json")
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
                status, stats = api(f"/repos/{full}/stats/contributors")
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


def render_block(s):
    loc = s["total_add"] + s["total_del"]
    return (
        f"{START_MARKER}\n"
        "```\n"
        f"Repos: .... {s['total_repos']} {{Contributed: {s['contributed_repos']}}} | Stars: {s['total_stars']}\n"
        f"Commits: .... {s['total_commits']} | Followers: .... {s['followers']}\n"
        f"Lines of Code on GitHub: {loc:,} ( {s['total_add']:,}++, {s['total_del']:,}-- )\n"
        "```\n"
        f"{END_MARKER}"
    )


def main():
    stats = fetch_stats()
    block = render_block(stats)
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = re.compile(re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER), re.DOTALL)
    if not pattern.search(content):
        raise RuntimeError("STATS markers not found in README.md")
    new_content = pattern.sub(block, content)
    with open(README_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)


if __name__ == "__main__":
    main()
