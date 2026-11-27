"""Brings the Roblox version's release list in from the Roblox repo, read only. Run after a Roblox publish, then build.py:
    python roblox_import.py [path to the Roblox repo, default ../Lanternhall-Roblox]

- Reads <repo>/docs/releases.json (written by its tools/publish.ps1: a list of {version, saved, live, at}). Only the version and
  the date are used; the place versions are never copied.
- Joins the newest COUNT versions with the player-facing notes in roblox/notes.json (written for the site by hand) and writes
  roblox/releases.json: {"schema": 1, "releases": [{version, date, title?, bullets}]}, newest first.
- Stops if one of those versions has no note, so dev text never reaches the site: add the note, then run it again.
The Roblox data lives in roblox/, never releases/: the Discord Action posts only new releases/*.md files, and notice.json's
`latest` comes only from releases/*.md.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "Lanternhall-Roblox"))
SRC = os.path.join(REPO, "docs", "releases.json")
NOTES = os.path.join(HERE, "roblox", "notes.json")
OUT = os.path.join(HERE, "roblox", "releases.json")
COUNT = 10   # back to 0.64.0 (Fair Play) at the first import


def vkey(v): return [int(x) for x in re.findall(r"\d+", v)]


def main():
    log = json.load(open(SRC, encoding="utf-8"))
    if not isinstance(log, list): raise SystemExit(f"{SRC}: expected a list of {{version, saved, live, at}}")
    first = {}   # version -> the date it first went live (a version published twice keeps its first date)
    for e in log:
        v, at = str(e.get("version", "")), str(e.get("at", ""))
        if not re.fullmatch(r"\d+\.\d+\.\d+", v) or not re.match(r"\d{4}-\d\d-\d\d", at): continue
        first.setdefault(v, at[:10])
    notes = json.load(open(NOTES, encoding="utf-8"))["notes"]
    newest = sorted(first, key=vkey, reverse=True)[:COUNT]
    missing = [v for v in newest if not (notes.get(v) or {}).get("bullets")]
    if missing: raise SystemExit("roblox_import: write a player-facing note in roblox/notes.json for " + ", ".join(missing))
    out = []
    for v in newest:
        r = {"version": v, "date": first[v]}
        if notes[v].get("title"): r["title"] = notes[v]["title"]
        r["bullets"] = list(notes[v]["bullets"])
        out.append(r)
    data = json.dumps({"schema": 1, "releases": out}, ensure_ascii=False, indent=1) + "\n"
    open(OUT, "w", encoding="utf-8", newline="\n").write(data)
    print(f"roblox/releases.json: {len(out)} versions, {out[0]['version']} ({out[0]['date']}) to {out[-1]['version']}")


if __name__ == "__main__":
    main()
