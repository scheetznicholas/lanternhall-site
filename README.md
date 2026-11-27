# lanternhallvr.com

Static site for Lanternhall, served by GitHub Pages. Edit `build.py` and run `python3 build.py` to regenerate the pages.

Tidings: `notice-src.json` (edited by `Tools/release/notice.ps1` in the game repo) becomes `notice.json`, which the game reads; its `latest` block comes from the releases' `code:` / `alpha_code:` front matter (the newest per channel; `notice-src.json` may only raise it). `report.html` decodes a player report from its link fragment, offline.

The Bearer's Guide: `guide.html` is built from `guide/guide.json` and `guide/img/`, which `python guide_import.py` copies from the game repo (its guide export and web plates); rerun it, then build.py, when the guide changes.

Roblox: the Updates page's Roblox tab reads `roblox/releases.json`, which `python roblox_import.py` makes from the Roblox repo's `docs/releases.json` (versions and dates) and the player-facing notes in `roblox/notes.json`. It lives outside `releases/` so the Discord Action and `notice.json` never see it. `ROBLOX_URL` in build.py stays None until the Roblox place is public.
