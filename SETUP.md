# Setup — Use this as your own profile README

You can adopt this whole setup (neofetch-style ASCII card + live GitHub stats +
snake animation) for your own GitHub profile. Steps below take ~15 minutes.

## ⚠️ Read this before you fork — what you MUST change

This repo is MIT-licensed, so you're free to use the **code** (the Python
scripts, workflow YAMLs, SVG structure, layout, algorithms). **The MIT license
does NOT cover personal details.** The following are the original author's
identity, not code, and must be replaced in your fork:

| Must replace | Why (not just polite — legally required) |
|---|---|
| `NAME`, `HANDLE` in the card | Using someone else's name in your profile is impersonation. |
| `EMAIL` | You'd be publishing someone else's contact address as your own. |
| `LINKEDIN_HANDLE`, `LINKEDIN_URL` | Points to a real person; you'd be posing as them. |
| `PORTFOLIO_URL` | Ditto — someone else's site. |
| `UPTIME_ORIGIN` (DOB) | Personal data (GDPR-style protections apply in many jurisdictions). |
| `assets/ascii_art.txt` | Derived from the original author's photo. That's their **likeness** — covered by right-of-publicity laws, which are separate from copyright and can't be waived by MIT. |
| All contact links in `README.md` | Same reason as email/LinkedIn/portfolio above. |

**Short version:** MIT covers the *how* (the code and structure). It does not
cover the *who* (identity, contact, likeness). Every one of the fields above
must be replaced with your own before you publish your fork.

The steps below walk you through exactly what to change and where.

---

## 1. Fork and rename

1. Click **Fork** at the top of this repo.
2. In your fork's **Settings**, rename it to exactly `<your-github-username>/<your-github-username>` — that's the special repo name GitHub uses for profile READMEs.

## 2. Edit `config.py`

Every personal field lives in one file. Open `config.py` in your fork and change:

- `GITHUB_USERNAME` — your username
- `HANDLE` — the neofetch-style header (e.g. `"yourname@github"`)
- `UPTIME_ORIGIN` — a `(YYYY, M, D)` tuple. Use your birthday for a personal age, or use your GitHub account creation date if you'd rather not share DOB.
- `OS`, `LOCATION`, `LANGUAGES`, `FRAMEWORK`, `TOOLS` — whatever describes you
- `EMAIL`, `LINKEDIN_HANDLE`, `LINKEDIN_URL`, `PORTFOLIO_DISPLAY`, `PORTFOLIO_URL` — your contact info

## 3. Replace the ASCII portrait

You have two options:

**Option A — Auto-generate from a photo:**

1. Put a square headshot photo in the repo root as `photo.jpeg` (or set `PORTRAIT_SRC` in `config.py` to your filename).
2. Install Pillow: `pip install pillow`
3. Run: `python scripts/make_ascii.py`
4. This overwrites `assets/ascii_art.txt`. Commit it.

**Option B — Write ASCII by hand:**

Just edit `assets/ascii_art.txt` directly. Any monospace ASCII drawing works; aim for around 42 columns wide and 20-30 rows tall so the card layout balances.

## 4. Update `README.md`

Find and replace every `himanshubora99` in `README.md` with your own username. There are ~10 occurrences (raw SVG URLs, snake URLs, badge alt text). Also update:

- Email badge target — `mailto:` link
- LinkedIn badge — `href` URL
- Portfolio badge — `href` URL

## 5. Add a Personal Access Token for stats

The stats workflow needs to read your commits/LOC across public + private repos, which requires a PAT.

1. Go to [github.com/settings/tokens/new](https://github.com/settings/tokens/new)
2. Scopes: check **`repo`** and **`read:user`**
3. Generate → copy the token (starts with `ghp_`)
4. In your fork: **Settings → Secrets and variables → Actions → New repository secret**
5. Name: `STATS_TOKEN` (must match exactly). Value: paste the token.

## 6. Enable and trigger the workflows

1. Go to your fork's **Actions** tab. If prompted, click **"I understand my workflows, go ahead and enable them."**
2. Click **"Update GitHub stats"** in the left sidebar → **Run workflow** → **Run workflow**. Wait for the green ✓.
3. Click **"Generate contribution snake"** → **Run workflow** → **Run workflow**. Wait for the green ✓.

Both workflows will now run on their own cron schedules (stats: daily, snake: every 12h). You can manually re-run either anytime from the Actions tab.

## 7. Optional — enable private-repo contributions in the snake

By default the snake only shows your public contributions. If you want private-repo activity to count too:

- [github.com/settings/profile](https://github.com/settings/profile) → **Contributions & Activity** → check **"Include private contributions on my profile"** → save.

## That's it

Your profile card should now be live at `https://github.com/<your-username>`. If something looks off, check the **Actions** tab — every workflow run has a full log.

## Files at a glance

| File | What it does |
|---|---|
| `config.py` | Your personal fields — the only file you have to edit |
| `scripts/build_card.py` | Fetches your live GitHub stats and renders `assets/card_dark.svg` / `assets/card_light.svg` |
| `scripts/make_ascii.py` | Converts a photo to `assets/ascii_art.txt` |
| `assets/ascii_art.txt` | The text portrait embedded in the card SVG |
| `assets/card_dark.svg`, `assets/card_light.svg` | Rendered cards, auto-updated by the stats workflow |
| `README.md` | Your public profile — references the SVGs |
| `.github/workflows/update-stats.yml` | Daily refresh of the card |
| `.github/workflows/snake.yml` | Twice-daily refresh of the contribution snake |

## Inspired by

The neofetch-card format and general layout were inspired by
[Andrew6rant/Andrew6rant](https://github.com/Andrew6rant/Andrew6rant). This
implementation is written from scratch — no code is copied — but credit is
still due for the idea.
