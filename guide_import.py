"""Brings the Bearer's Guide in from the game repo (G-web-guide.md §5, §7). Run after every release that changes the guide pages
file or a plate, then run build.py:   python guide_import.py [path to the game repo, default ../RecRoomCopy]

- guide/guide.json      a verbatim copy of Lanternhall/Captures/guide/guide.json (the game's `Lanternhall/Guide/Export Web JSON`)
- guide/img/<id>.webp   the web plates, resized from the 1200 px web copies of Tools/lh_plate_post.py. Each id is taken from the newest of
                        Lanternhall/Captures/guide/web/ and Art/Export/*/web/ (fix rounds stage their web copies there):
                          plates   <id>.webp 1024 px + <id>_s.webp 480 px
                          insets, vignettes   <id>.webp 512 px + <id>_s.webp 320 px
                          tailpieces   <id>.webp 256 px wide, cropped to the ornament
- guide/img/og_guide.jpg   the social card: pl_emberking on parchment, 1200 x 630
Fails if an entry's picture or its Alt: text is missing. Files in guide/img/ that the guide no longer uses are removed.
"""
import glob, json, os, shutil, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "RecRoomCopy"))
SRC_JSON = os.path.join(GAME, "Lanternhall", "Captures", "guide", "guide.json")
OUT = os.path.join(HERE, "guide")
IMG = os.path.join(OUT, "img")
PAPER = (0xF2, 0xE3, 0xC2)
SIZES = {"plate": (1024, 480), "inset": (512, 320), "vignette": (512, 320), "tailpiece": (256,)}


def source(pid):
    cands = glob.glob(os.path.join(GAME, "Lanternhall", "Captures", "guide", "web", pid + ".webp"))
    cands += glob.glob(os.path.join(GAME, "Art", "Export", "*", "web", pid + ".webp"))
    if not cands:
        raise SystemExit(f"guide_import: no web copy of {pid} (Lanternhall/Captures/guide/web or Art/Export/*/web)")
    return max(cands, key=os.path.getmtime)


def save(im, width, path):
    h = round(im.height * width / im.width)
    im.resize((width, h), Image.LANCZOS).save(path, "WEBP", quality=82, method=6)


def main():
    guide = json.load(open(SRC_JSON, encoding="utf-8"))
    if guide.get("schema") != "lanternhall.guide/1":
        raise SystemExit(f"guide_import: unknown schema {guide.get('schema')!r}")
    need = {}   # id -> kind
    for book in guide["books"]:
        for it in book["items"]:
            if it["kind"] == "world" and it.get("tailpiece"):
                need[it["tailpiece"]] = "tailpiece"
            if it["kind"] in ("foe", "boss", "topic"):
                if not it.get("image") or not it.get("alt", "").strip():
                    raise SystemExit(f"guide_import: {it['id']} has no picture or no Alt: line")
                need[it["image"]] = "vignette" if it["kind"] == "topic" else "plate"
                if it.get("inset"):
                    need[it["inset"]] = "inset"
    os.makedirs(IMG, exist_ok=True)
    shutil.copyfile(SRC_JSON, os.path.join(OUT, "guide.json"))
    made = {"og_guide.jpg"}
    for pid, kind in sorted(need.items()):
        src = source(pid)
        im = Image.open(src)
        if kind == "tailpiece":
            im = im.convert("RGBA")
            im = im.crop(im.getchannel("A").getbbox())
        else:
            im = im.convert("RGB")
        for i, w in enumerate(SIZES[kind]):
            name = pid + ("_s" if i else "") + ".webp"
            save(im, w, os.path.join(IMG, name))
            made.add(name)
        print(f"{pid:18} {kind:9} <- {os.path.relpath(src, GAME)}")
    # social card: the Emberking's plate centred on parchment
    plate = Image.open(source("pl_emberking")).convert("RGB").resize((630, 630), Image.LANCZOS)
    card = Image.new("RGB", (1200, 630), PAPER)
    card.paste(plate, ((1200 - 630) // 2, 0))
    card.save(os.path.join(IMG, "og_guide.jpg"), "JPEG", quality=86, optimize=True, progressive=True)
    for f in os.listdir(IMG):
        if f not in made:
            os.remove(os.path.join(IMG, f))
            print("removed stale", f)
    total = sum(os.path.getsize(os.path.join(IMG, f)) for f in made)
    print(f"guide.json {os.path.getsize(os.path.join(OUT, 'guide.json'))} bytes, {len(made)} images, {total // 1024} KB")


if __name__ == "__main__":
    main()
