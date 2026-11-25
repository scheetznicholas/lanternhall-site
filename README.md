# lanternhallvr.com

Static site for Lanternhall, served by GitHub Pages. Edit `build.py` and run `python3 build.py` to regenerate the pages.

Tidings: `notice-src.json` (edited by `Tools/release/notice.ps1` in the game repo) becomes `notice.json`, which the game reads; its `latest` block comes from the releases' `code:` / `alpha_code:` front matter (the newest per channel; `notice-src.json` may only raise it). `report.html` decodes a player report from its link fragment, offline.
