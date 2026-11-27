"""Builds the static pages for lanternhallvr.com (GitHub Pages). Run: python3 build.py"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&'
         'family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">')
YT = "https://www.youtube.com/@LanternhallGames"
MAIL = "support@lanternhallvr.com"
# The Roblox place's public link. None until the place is public: the home page's Roblox card then shows only its badge.
# Set it to the place URL and the card gains a "Play on Roblox" button.
ROBLOX_URL = None
ROBLOX_CTA = (f'<div class="cta"><a class="btn" href="{ROBLOX_URL}">Play on Roblox</a></div>' if ROBLOX_URL else "")

import glob, html, json, os, re


def load_releases():
    """releases/<version>.md: a front-matter block (version, date, channel, title, announce) then '- ' bullets."""
    out = []
    for path in glob.glob("releases/*.md"):
        meta, bullets = {}, []
        text = open(path, encoding="utf-8").read().replace("\r\n", "\n")
        m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            body = m.group(2)
        else:
            body = text
        for line in body.splitlines():
            if line.startswith("- "):
                bullets.append(line[2:].strip())
        meta.setdefault("version", os.path.basename(path)[:-3])
        meta["bullets"] = bullets
        out.append(meta)
    out.sort(key=lambda r: [int(x) for x in re.findall(r"\d+", r["version"])], reverse=True)
    return out


RELEASES = load_releases()
LATEST = RELEASES[0] if RELEASES else None


def load_roblox():
    """roblox/releases.json (made by roblox_import.py from the Roblox repo's release log + roblox/notes.json), newest first.
    It never feeds notice.json or the Discord Action: both read releases/*.md only."""
    if not os.path.exists("roblox/releases.json"): return []
    doc = json.load(open("roblox/releases.json", encoding="utf-8"))
    if doc.get("schema") != 1: raise SystemExit("roblox/releases.json: unknown schema")
    return doc.get("releases") or []


ROBLOX_RELEASES = load_roblox()


def head(title, desc, page, og_image="assets/hero.jpg", bar=""):
    """`bar`: extra markup inside the sticky header, under the links (the guide's book bar)."""
    nav = [("index.html", "Home"), ("guide.html", "Guide"), ("updates.html", "Updates"), ("support.html", "Support"), ("privacy.html", "Privacy")]
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == page else ""}>{t}</a>' for h, t in nav)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://lanternhallvr.com/{og_image}">
<meta name="theme-color" content="#17110c">
<link rel="icon" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="style.css">
</head><body>
<header class="nav"><div class="nav-in">
<a class="brand" href="index.html"><img src="assets/favicon.png" alt="">Lanternhall</a>
<nav class="nav-links">{links}</nav>
</div>{bar}</header>
"""


VERSION = (f'<a class="ver" href="updates.html">v{LATEST["version"]} {LATEST.get("channel", "")} &middot; Release notes</a>' if LATEST else "")

FOOT = f"""<footer><div class="foot-in">
<span>&copy; 2026 Lanternhall Games</span>{VERSION}
<nav><a href="support.html">Support</a><a href="privacy.html">Privacy</a><a href="{YT}">YouTube</a><a href="mailto:{MAIL}">{MAIL}</a></nav>
</div></footer>
</body></html>
"""

INDEX = head("Lanternhall: co-op VR quests for Meta Quest",
             "Lanternhall is a four-player co-op VR quest game for Meta Quest 3 and 3S. Light your lantern and brave Cinderkeep.",
             "index.html") + f"""
<div class="hero"><img src="assets/hero.jpg" alt="Four Lantern Folk adventurers face the Emberking in his throne dome"></div>
<div class="tagline">
<h1>Light your lantern. Brave the keep.</h1>
<h2 class="ways-h">Two ways to play</h2>
<div class="ways">
<div class="card way"><h3>🥽 Meta Quest (VR)</h3><p class="way-for">Quest 3 and 3S</p>
<p>A four-player co-op VR quest game for Meta Quest. Gather your party in Lanternhall, step onto the gate stone,
and fight your way through Cinderkeep to the throne of the Emberking.</p>
<div class="cta"><a class="btn" href="{YT}">Watch on YouTube</a><a class="btn ghost" href="support.html">Support &amp; FAQ</a></div>
<span class="badge">Open beta in December &middot; full release January</span></div>
<div class="card way"><h3>🎮 Roblox</h3><p class="way-for">PC, phone and tablet</p>
<p>The same hall and the same quests, built for Roblox. Gather your party in Lanternhall and fight through Cinderkeep
with mouse or touch.</p>
{ROBLOX_CTA}<span class="badge">Coming to Roblox: beta in December &middot; full release January</span></div>
</div>
<div class="cta"><a class="btn ghost" href="guide.html">📖 Read the Bearer's Guide</a></div>
</div>
<main>
<section>
<h2>The quest</h2>
<div class="grid">
<div class="card"><h3>Four friends, one keep</h3><p>Team up with up to three friends. Swords, shields, bows and torches, real hand-to-hand
VR combat, and a party that falls if you don't watch each other's backs.</p></div>
<div class="card"><h3>A castle full of puzzles</h3><p>Turn the boiler valves, ride the Belfry lift, ring the great bell and
solve the Gallery of Kings, about half an hour of handcrafted rooms from the Gatehouse to the throne.</p></div>
<div class="card"><h3>The Emberking</h3><p>A three-phase boss fight. Stagger him, strike the crown, dodge his turrets
and win the Emberking's Crown for your avatar.</p></div>
<div class="card"><h3>The First King</h3><p>In the Gallery of Kings a giant stone king wakes, crushes his own statues and
turns on you. Break his glowing joints, climb his back when he kneels and strike the rune.</p></div>
<div class="card"><h3>&#x1F525; The Ember Pit</h3><p>Step through the iron gate in the Main Hall and survive wave after wave of the keep's
fiercest: Cindershanks, archers, bats, knights, gold turrets and a boss every fifth wave. Clear 15 waves free; the Pit Masters board
remembers the bravest.</p></div>
<div class="card"><h3>Your Lantern Folk</h3><p>Dress your avatar in the Robing Room: hair, hats, tunics, colours and frames.
Play on Normal, or swear the Oath for one-hit Hard mode and Ironheart rewards.</p></div>
</div>
</section>
<section>
<h2>From Cinderkeep</h2>
<div class="shots">
<figure><img src="assets/shot-king.jpg" alt="The First King on his dais, the Gilded Hulker beside him" loading="lazy"><figcaption>The First King</figcaption></figure>
<figure><img src="assets/shot-throne.jpg" alt="The Emberking's throne dome" loading="lazy"><figcaption>The Throne Dome</figcaption></figure>
<figure><img src="assets/shot-belfry.jpg" alt="The Cinder Belfry lift climbing the shaft" loading="lazy"><figcaption>The Cinder Belfry lift</figcaption></figure>
<figure><img src="assets/shot-boiler.jpg" alt="The great boiler in the Forge Boiler House" loading="lazy"><figcaption>The Forge Boiler House</figcaption></figure>
<figure><img src="assets/shot-bell.jpg" alt="The great bell in the Bell Chamber" loading="lazy"><figcaption>The Bell Chamber</figcaption></figure>
<figure><img src="assets/shot-robing.jpg" alt="Trying on a hat in the Looking Glass" loading="lazy"><figcaption>The Robing Room</figcaption></figure>
</div>
</section>
<section>
<h2>At a glance</h2>
<ul class="specs">
<li>Meta Quest 3 &amp; 3S</li><li>1&ndash;4 player co-op</li><li>Hubs of up to 8</li><li>Voice chat</li>
<li>Standing or seated</li><li>Snap or smooth turning</li><li>Left- or right-handed</li><li>Normal &amp; Hard</li><li>Wave mode</li>
</ul>
</section>
</main>
""" + FOOT

SUPPORT = head("Support: Lanternhall", "Help, FAQ and contact for Lanternhall.", "support.html") + f"""
<main class="doc">
<h1>Support</h1>
<p class="meta">Stuck, found a bug, or need to report a player? Email <a href="mailto:{MAIL}">{MAIL}</a>.
Include your in-game name, your headset (Quest 3 or 3S) and what happened. Screenshots or a short clip help a lot.</p>

<h2>Frequently asked</h2>
<details><summary>How do I play with friends?</summary>
<p>At the Fellowship Board in Lanternhall, choose <b>Private Hall</b>. Your hall gets a six-rune code. Friends choose
<b>Join by Code</b> and enter it. Or everyone presses <b>Quick Play</b> to join an open hall. The same menu is on your wrist.</p></details>
<details><summary>How do we start the quest together?</summary>
<p>Walk to the Cinderkeep gate and stand on the gate stone together. Up to four of you go in as a party, into your own quest room,
and you come back to Lanternhall together afterwards.</p></details>
<details><summary>The board says it can't connect.</summary>
<p>Check that your headset is online, then press <b>Sign in again</b> on the network page of your wrist menu. The board's corner
shows the reason if it still fails. Please include that message if you email us.</p></details>
<details><summary>Can I play seated, or with my left hand?</summary>
<p>Yes. Open your wrist menu, go to <b>Comfort</b>, and choose standing or seated, snap or smooth turning, and your sword hand.
<b>Redo Setup</b> on the same page walks you through the first-time setup again.</p></details>
<details><summary>How do I mute or report someone?</summary>
<p>Open your wrist menu's <b>Fellowship</b> tab (or poke a name on the Fellowship Board) and poke the player. Their card has
<b>Mute</b> (you stop hearing them, only for you), <b>Block</b> (their voice, emotes and name are hidden from you, and you won't
be matched into their halls), <b>Report</b> and, if you are the hall's host, <b>Show the Door</b> (they leave and can't come back
to that hall for 15 minutes). Nobody is told that you muted or blocked them.</p>
<p>A report is kept on your headset and, where available, sent to us at once. You can also send it yourself from the
Settings Book's <b>Safety</b> page: it opens a page that lets you copy it or email it to <a href="mailto:{MAIL}">{MAIL}</a>.
Please don't post reports in public channels. Meta's own reporting tools on your headset work too.</p></details>
<details><summary>Is my progress saved?</summary>
<p>Your level, unlocks and settings are saved on your headset. Uninstalling the game or clearing its data removes them.</p></details>
</main>
""" + FOOT

PRIVACY = head("Privacy Policy: Lanternhall", "How Lanternhall handles your information.", "privacy.html") + f"""
<main class="doc">
<h1>Privacy Policy</h1>
<p class="meta">Lanternhall, by Lanternhall Games &middot; Effective November 2026 &middot; Updated with version 0.19.0 (reports, hall news)</p>

<p>This policy explains what information Lanternhall (the VR game for Meta Quest) uses, why, and who handles it.
We keep it short because we collect very little. Questions: <a href="mailto:{MAIL}">{MAIL}</a>.</p>

<h2>What we don't do</h2>
<ul>
<li>No ads, and no selling or renting of your information.</li>
<li>No accounts or passwords with us. We never ask for your real name, address or payment details.</li>
<li>We don't record your voice chat.</li>
</ul>

<h2>Information the game uses</h2>
<ul>
<li><b>Player name.</b> The name you choose in the game is shown to other players in the same hall or quest.
Names are filtered for offensive words.</li>
<li><b>Anonymous player ID.</b> To play online, the game signs in anonymously to Unity Gaming Services, which gives your
copy of the game a random player ID. It is not linked to your name or Meta account by us.</li>
<li><b>Multiplayer connection data.</b> When you join a hall or quest, Unity's multiplayer services (Lobby, Relay and
Distributed Authority) process connection details such as your IP address, session codes and the in-game state
(positions, actions) needed to keep players in sync.</li>
<li><b>Voice chat.</b> If you allow microphone access, your voice is sent live to the other players in your hall or
party through Unity's Vivox service. You can deny the microphone and still play.</li>
<li><b>On your headset.</b> Your progress, unlocks, avatar look and settings are stored only on your headset. The game also keeps a
small technical log on the headset to help diagnose connection problems. It is not uploaded.</li>
<li><b>Player reports.</b> If you report a player, the report holds the reason you chose, the time, the game version, where it
happened (hub, quest or Pit, and the hall code and session), how many players were there, and the in-game name and anonymous
player ID of you and of the player you reported. It never holds voice recordings or anything about the other players. It is kept on
your headset; it is sent to us through Unity's Moderation service when that is available, or only if you send it yourself
(the report page decodes it in your browser: it is not sent to our website).</li>
<li><b>Hall news.</b> The game reads a small public notice file (<code>notice.json</code>) from this website when it starts and every
few minutes while you play, to show news on the Crier's Board and tell you when a new version is out. Nothing about you is sent
with that request beyond what any web request carries (such as your IP address, handled by GitHub Pages). Offline, it is skipped.</li>
<li><b>Crash and diagnostic data.</b> The Unity engine may send anonymous crash and performance diagnostics to Unity to help
fix bugs.</li>
</ul>

<h2>Who processes it</h2>
<p>Online features are provided by Unity Technologies (Unity Gaming Services, including Moderation, and Vivox). The game is distributed through the
Meta Horizon Store, so Meta's own terms and privacy policy apply to your Meta account and the store.
See <a href="https://unity.com/legal/game-player-and-app-user-privacy-policy">Unity's privacy policy</a> and
<a href="https://www.meta.com/legal/privacy-policy/">Meta's privacy policy</a>.</p>

<h2>Children</h2>
<p>Lanternhall is intended for teens and adults and is not directed to children under 13. If you believe a child under 13 has
used the online features, contact us and we will help remove any associated data we are able to.</p>

<h2>Your choices</h2>
<ul>
<li>Play offline, or deny the microphone, to limit what is shared.</li>
<li>Change your player name at any time in the game.</li>
<li>Uninstall the game or clear its data to remove everything stored on your headset.</li>
<li>Email us to ask about, or request deletion of, any data tied to your anonymous player ID.</li>
</ul>

<h2>Changes</h2>
<p>If this policy changes, we will update it on this page and change the date above.</p>
</main>
""" + FOOT

def release_html(r):
    items = "".join(f"<li>{html.escape(b)}</li>" for b in r["bullets"])
    chan = f'<span class="chan">{html.escape(r.get("channel", ""))}</span>' if r.get("channel") else ""
    title = f' &middot; {html.escape(r["title"])}' if r.get("title") else ""
    return (f'<article class="rel" id="v{r["version"]}"><h2>v{r["version"]}{title} {chan}</h2>'
            f'<p class="meta">{html.escape(r.get("date", ""))}</p><ul>{items}</ul></article>')


def roblox_release_html(r):
    items = "".join(f"<li>{html.escape(b)}</li>" for b in r["bullets"])
    title = f' &middot; {html.escape(r["title"])}' if r.get("title") else ""
    return (f'<article class="rel"><h2>v{html.escape(r["version"])}{title} <span class="chan">Roblox</span></h2>'
            f'<p class="meta">{html.escape(r.get("date", ""))}</p><ul>{items}</ul></article>')


def rel_tabs(current):
    """The Quest / Roblox tabs. Each pane carries its own copy, so the shown tab is marked without scripts."""
    tabs = [("quest", "🥽 Meta Quest"), ("roblox", "🎮 Roblox")]
    return ('<nav class="rel-tabs" aria-label="Platform">' + "".join(
        f'<a href="#{k}"{" aria-current=\"true\"" if k == current else ""}>{t}</a>' for k, t in tabs) + "</nav>")


# The Roblox pane shows only when #roblox is the target (CSS :target); otherwise the Quest pane shows, so its #v<version> anchors work.
UPDATES = head("Updates: Lanternhall", "Release notes for Lanternhall, the co-op VR quest game for Meta Quest, and its Roblox version.",
               "updates.html") + f"""
<main class="doc">
<h1>Updates</h1>
<p class="meta">Release notes for every build of Lanternhall, newest first.</p>
<section class="rel-pane" id="roblox">{rel_tabs("roblox")}
<p class="meta">The Roblox version opens its public beta in December, with the full release in January. These are its latest updates.</p>
{"".join(roblox_release_html(r) for r in ROBLOX_RELEASES)}
</section>
<section class="rel-pane" id="quest">{rel_tabs("quest")}
{"".join(release_html(r) for r in RELEASES)}
</section>
</main>
""" + FOOT

NOTFOUND = head("Lost in the keep: Lanternhall", "Page not found.", "") + """
<main class="doc" style="text-align:center"><h1>Lost in the keep</h1>
<p class="meta">That page isn't here. Maybe it fell down the Belfry shaft.</p>
<p><a class="btn" href="index.html">Back to Lanternhall</a></p></main>
""" + FOOT

# ---------------------------------------------------------------- guide.html: the Bearer's Guide (G-web-guide.md in the game repo)
# Reads guide/guide.json (schema lanternhall.guide/1, the game's export, copied with its plates into guide/img/ by guide_import.py).
# Every word of guide text comes from that export (the game's docs/specs/G-game-guide-pages.md); nothing is retyped here. A side's
# `web` text replaces its body on the site. A great foe's sealed sides, with his Fells in and Tip, fold into one closed <details>.

GUIDE_JSON = "guide/guide.json"
GUIDE_IMG = "guide/img/"
# The credits block (G-web §6, the game's docs/credits.md). "Voices by Cameron Clanton." is added the day a build ships his recordings.
GUIDE_CREDITS = "Lanternhall is made by Nicholas Scheetz (ShadowStorm)."
FLAME_SVG = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><symbol id="g-flame" viewBox="0 0 16 20">'
             '<path d="M8 1C9 6 14 8.5 14 13.5A6 6 0 0 1 2 13.5C2 10.5 4 8.6 5.2 6.6c.3 2.2 1.1 3.3 2.3 3.5C6.8 7 7 4 8 1z"/></symbol></svg>')
FACT_NAMES = (("fellsIn", "Fells in"), ("where", "Where"), ("tip", "Tip"))
COUNT_NAMES = {"foe": ("foe", "foes"), "boss": ("great foe", "great foes"), "topic": ("topic", "topics")}


def webp_size(path):
    """(width, height) from a .webp header (VP8, VP8L or VP8X); a missing file stops the build."""
    if not os.path.exists(path): raise SystemExit(f"guide: {path} is missing (run python guide_import.py)")
    b = open(path, "rb").read(30)
    kind = b[12:16]
    if kind == b"VP8X": return 1 + int.from_bytes(b[24:27], "little"), 1 + int.from_bytes(b[27:30], "little")
    if kind == b"VP8 ": return int.from_bytes(b[26:28], "little") & 0x3FFF, int.from_bytes(b[28:30], "little") & 0x3FFF
    if kind == b"VP8L":
        bits = int.from_bytes(b[21:25], "little")
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    raise SystemExit(f"guide: {path} is not a webp")


def g_img(pid, alt, sizes=None, lazy=True):
    """The big file as src; with `sizes`, the _s file joins it in a srcset."""
    big = f"{GUIDE_IMG}{pid}.webp"
    w, h = webp_size(big)
    srcset = ""
    if sizes:
        small = f"{GUIDE_IMG}{pid}_s.webp"
        srcset = f' srcset="{small} {webp_size(small)[0]}w, {big} {w}w" sizes="{sizes}"'
    return (f'<img src="{big}"{srcset} width="{w}" height="{h}" alt="{html.escape(alt)}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async">')


def g_lines(text):
    """Each line of a side is its own line; an emoji-led line needs no bullet."""
    return "".join(f'<p class="g-l">{html.escape(l.strip())}</p>' for l in text.split("\n") if l.strip())


def g_side(s, tag="h4"):
    return f'<{tag}>{html.escape(s["heading"])}</{tag}>{g_lines(s.get("web") or s["body"])}'


def g_fierce(n):
    flames = "".join(f'<svg class="g-fl{" on" if i < n else ""}" viewBox="0 0 16 20" aria-hidden="true"><use href="#g-flame"/></svg>' for i in range(5))
    return f'<p class="g-fierce" role="img" aria-label="Fierceness {n} of 5">{flames}</p>'


def g_facts(facts, keys):
    rows = "".join(f"<dt>{name}</dt><dd>{html.escape(facts[k])}</dd>" for k, name in FACT_NAMES if k in keys and facts.get(k))
    return f'<dl class="g-facts">{rows}</dl>' if rows else ""


PLATE_SIZES = "(min-width: 900px) 360px, (min-width: 552px) 480px, calc(100vw - 72px)"


def g_head(it):
    return (f'<h3>{html.escape(it["name"])}</h3><p class="g-epi">{html.escape(it.get("epithet", ""))}</p>'
            f'{g_fierce(int(it.get("danger", 0)))}')


def g_foe(it, lazy):
    sides = "".join(g_side(s) for s in it["sections"])
    return (f'<article class="g-card g-foe" id="{it["id"]}"><div class="g-plate">{g_img(it["image"], it["alt"], PLATE_SIZES, lazy)}</div>'
            f'<div class="g-text">{g_head(it)}{g_facts(it.get("facts") or {}, ("fellsIn", "where", "tip"))}{sides}</div></article>')


def g_boss(it, lazy):
    facts = it.get("facts") or {}
    open_sides = "".join(g_side(s) for s in it["sections"] if not s.get("sealed"))
    sealed = [s for s in it["sections"] if s.get("sealed")]
    inset = ""
    if it.get("inset"):
        inset = (f'<figure class="g-inset">{g_img(it["inset"], it["name"] + ", the way through his armour", "(min-width: 600px) 480px, calc(100vw - 104px)")}'
                 f'</figure>')
    # the inset sits at the top of the side it heads in the book (His Armour, underImage): every inset shows the way in
    at = next((i for i, s in enumerate(sealed) if s.get("underImage")), 0)
    fold = g_facts(facts, ("fellsIn", "tip")) + "".join((inset if i == at else "") + g_side(s) for i, s in enumerate(sealed))
    return (f'<article class="g-card g-boss" id="{it["id"]}"><div class="g-plate">{g_img(it["image"], it["alt"], PLATE_SIZES, lazy)}</div>'
            f'<div class="g-text">{g_head(it)}{g_facts(facts, ("where",))}{open_sides}</div>'
            f'<details class="g-fold"><summary>⚠ Spoilers: how to fell it</summary>{fold}</details></article>')


def g_topic(it):
    cap = next((s for s in it["sections"] if s["heading"] == "Caption"), None)
    rest = [s for s in it["sections"] if s is not cap]
    figcap = f"<figcaption>{g_lines(cap.get('web') or cap['body'])}</figcaption>" if cap else ""
    fig = f'<figure class="g-vig">{g_img(it["image"], it["alt"], "(min-width: 900px) 440px, calc(100vw - 72px)")}{figcap}</figure>'
    sides = "".join(g_side(s, "h3" if i == 0 else "h4") for i, s in enumerate(rest))
    return f'<article class="g-card g-topic" id="{it["id"]}">{fig}{sides}</article>'


def g_note(it):
    return '<div class="g-note">' + "".join(f'<p class="g-nh">{html.escape(s["heading"])}</p>{g_lines(s.get("web") or s["body"])}'
                                            for s in it["sections"]) + "</div>"


def g_tail(pid):
    return f'<div class="g-tail">{g_img(pid, "")}</div>' if pid else ""


def g_book(book, state):
    out = [f'<section class="g-book" id="book-{book["id"]}"><h2>{html.escape(book["emoji"])} {html.escape(book["title"])}</h2>'
           f'<p class="g-line">{html.escape(book["line"])}</p>']
    cards, tail = [], ""
    two = " g-two" if all(i["kind"] in ("page", "topic") for i in book["items"]) else ""

    def flush():
        if cards: out.append(f'<div class="g-cards{two}">{"".join(cards)}</div>')
        if tail: out.append(g_tail(tail))
        cards.clear()

    for it in book["items"]:
        k = it["kind"]
        if k == "page":
            out.append(g_note(it))
        elif k == "world":
            flush()
            c = it.get("colour", "#E8662A").lstrip("#")
            r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
            out.append(f'<div class="g-world" id="{book["id"]}-{it["id"]}" style="background:rgba({r},{g},{b},.18);border-color:#{c}">'
                       f'<h3>{html.escape(it["emoji"])} {html.escape(it["name"])}</h3><p>{html.escape(it.get("line", ""))}</p></div>')
            tail = it.get("tailpiece", "")
        elif k in ("foe", "boss"):
            cards.append((g_foe if k == "foe" else g_boss)(it, lazy=state["lazy"]))
            state["lazy"] = True
        elif k == "topic":
            cards.append(g_topic(it))
    flush()
    out.append('<p class="g-up"><a href="#contents">↑ Contents</a></p></section>')
    return "".join(out)


def build_guide():
    guide = json.load(open(GUIDE_JSON, encoding="utf-8"))
    if guide.get("schema") != "lanternhall.guide/1": raise SystemExit(f"{GUIDE_JSON}: unknown schema {guide.get('schema')!r}")
    books = sorted(guide["books"], key=lambda b: b.get("order", 0))
    ids = ["contents"] + [f"book-{b['id']}" for b in books]
    for b in books:
        for it in b["items"]:
            if it["kind"] == "world": ids.append(f"{b['id']}-{it['id']}")
            elif it["kind"] != "page":
                ids.append(it["id"])
                if not it.get("alt", "").strip(): raise SystemExit(f"guide: {it['id']} has no Alt: text")
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup: raise SystemExit(f"guide: duplicate anchors {dup}")
    contents = []
    for b in books:
        n = {}
        for it in b["items"]:
            if it["kind"] in COUNT_NAMES: n[it["kind"]] = n.get(it["kind"], 0) + 1
        count = " &middot; ".join(f"{v} {COUNT_NAMES[k][v != 1]}" for k, v in n.items())
        contents.append(f'<a class="g-bookcard" href="#book-{b["id"]}"><span class="g-be" aria-hidden="true">{html.escape(b["emoji"])}</span>'
                        f'<b>{html.escape(b["title"])}</b><span class="g-bl">{html.escape(b["line"])}</span><span class="g-bn">{count}</span></a>')
    bar = ('<nav class="g-bar" aria-label="Books">' + '<span aria-hidden="true">&middot;</span>'.join(
        f'<a href="#book-{b["id"]}">{html.escape(b["emoji"])} {html.escape(b.get("plaque", b["title"]).split(" · ")[-1])}</a>' for b in books) + "</nav>")
    intro = guide.get("intro", "")
    desc = html.escape(re.sub(r"^\W+", "", intro))   # the intro without its leading emoji
    state = {"lazy": False}   # the first foe's plate loads at once; every other picture is lazy
    body = "".join(g_book(b, state) for b in books)
    return (head("The Bearer's Guide · Lanternhall", desc, "guide.html", og_image="guide/img/og_guide.jpg", bar=bar) +
            f'<main class="guide">{FLAME_SVG}<div class="g-top" id="contents"><h1>The Bearer\'s Guide</h1>'
            f'<p class="g-intro">{html.escape(intro)}</p><nav class="g-books" aria-label="Contents">{"".join(contents)}</nav></div>'
            f'{body}<aside class="g-credits"><p>{html.escape(GUIDE_CREDITS)}</p></aside></main>\n' + FOOT)

# ---------------------------------------------------------------- tidings: notice.json (Round T §7)

NOTICE_SRC = "notice-src.json"
CHANNELS = ("Beta", "Alpha")
NOTICE_PLACES = ("Beta", "Alpha", "Roblox")
ID_RE = re.compile(r"^[a-z0-9-]{1,32}$")
ISO_RE = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")


def glyphs(s):
    """Length the way the game counts it: an emoji (with its variation selector) is one."""
    return len([c for c in s if c not in "\ufe0f\u200d"])


def derive_latest(releases):
    """The newest build per channel from releases/*.md: `code:` is the build of the release's `channel`, `alpha_code:` the
    Alpha flavour of the same version (Round T §8: 0.19.0 = 1900 Beta / 1901 Alpha)."""
    latest = {}
    for r in releases:
        cands = []
        chan = r.get("channel", "Alpha")
        if r.get("code", "").isdigit() and chan in CHANNELS: cands.append((chan, int(r["code"])))
        if r.get("alpha_code", "").isdigit(): cands.append(("Alpha", int(r["alpha_code"])))
        for c, code in cands:
            if c not in latest or code > latest[c]["code"]:
                latest[c] = {"version": r["version"], "code": code}
    return latest


def build_notice():
    src = {"schema": 1, "notices": []}
    if os.path.exists(NOTICE_SRC):
        src = json.load(open(NOTICE_SRC, encoding="utf-8"))
    latest = derive_latest(RELEASES)
    for chan, o in (src.get("latest") or {}).items():   # a manual override can only RAISE the release-derived value
        if chan in CHANNELS and isinstance(o, dict) and str(o.get("code", "")).isdigit():
            if chan not in latest or int(o["code"]) > latest[chan]["code"]:
                latest[chan] = {"version": str(o.get("version", "")), "code": int(o["code"])}
    notices = src.get("notices") or []
    if len(notices) > 3: raise SystemExit("notice-src.json: at most 3 notices")
    out = []
    for n in notices:
        nid = n.get("id", "")
        if not ID_RE.match(nid): raise SystemExit(f"notice id {nid!r}: must be [a-z0-9-], 1-32 characters")
        title = n.get("title") or "Hear ye!"
        text = n.get("text", "")
        if not 1 <= glyphs(title) <= 24: raise SystemExit(f"notice {nid}: title 1-24 characters")
        if glyphs(text) > 160 or text.count("\n") > 3: raise SystemExit(f"notice {nid}: text at most 160 characters and 3 line breaks")
        for k in ("from", "until"):
            if n.get(k) and not ISO_RE.match(n[k]): raise SystemExit(f"notice {nid}: {k} must be UTC ISO-8601 (2026-11-24T00:00:00Z)")
        e = {"id": nid, "title": title, "text": text}
        for k in ("from", "until"):
            if n.get(k): e[k] = n[k]
        e["wrist"] = "never" if n.get("wrist") == "never" else "once"
        # Notice places (bible §4.10, decisions 2026-11-25): Beta, Alpha, Roblox; no list = all three. Quest builds before 0.20.0 read
        # a list naming only Roblox as both flavours, so the notice app holds Roblox-only notices until 0.20.0 is the latest release.
        ch = [c for c in (n.get("channels") or list(NOTICE_PLACES)) if c in NOTICE_PLACES]
        e["channels"] = ch or list(NOTICE_PLACES)
        out.append(e)
    # `updated` is stamped by Tools/release/notice.ps1 in notice-src.json; else the newest release date (stable between builds)
    updated = src.get("updated") or ((RELEASES[0].get("date", "2026-01-01") + "T00:00:00Z") if RELEASES else "2026-01-01T00:00:00Z")
    doc = {"schema": 1, "updated": updated, "latest": {c: latest[c] for c in CHANNELS if c in latest}, "notices": out}
    data = json.dumps(doc, ensure_ascii=False, indent=1) + "\n"
    if len(data.encode("utf-8")) > 8192: raise SystemExit("notice.json is over 8 KB: the game would ignore it")
    open("notice.json", "w", encoding="utf-8", newline="\n").write(data)


# ---------------------------------------------------------------- report.html (Round T §5): static, no network requests at all

REPORT = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:; base-uri 'none'; form-action 'none'">
<meta name="referrer" content="no-referrer">
<link rel="icon" href="data:,">
<title>Send a player report: Lanternhall</title>
<style>
:root{--bg:#17110c;--panel:#241a12;--ink:#f3e6cf;--dim:#bfae93;--gold:#f2c25c;--line:#4a3726}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:720px;margin:0 auto;padding:24px 16px 48px}
h1{color:var(--gold);font-size:1.6rem;margin:0 0 4px}
.meta{color:var(--dim);margin:0 0 20px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px;margin:0 0 16px;overflow-wrap:anywhere}
table{border-collapse:collapse;width:100%}
th{color:var(--dim);font-weight:600;text-align:left;vertical-align:top;padding:4px 12px 4px 0;white-space:nowrap}
td{padding:4px 0}
.btns{display:flex;flex-wrap:wrap;gap:10px;margin:8px 0 16px}
button,a.btn{background:var(--gold);color:#1b130c;border:0;border-radius:8px;padding:10px 16px;font:600 1rem system-ui,sans-serif;text-decoration:none;cursor:pointer}
a.btn.ghost{background:transparent;color:var(--gold);border:1px solid var(--gold)}
pre{white-space:pre-wrap;margin:0;color:var(--dim);font-size:.85rem}
.warn{color:#ffb4a0}
</style></head><body><main>
<h1>Send a player report</h1>
<p class="meta">This page reads the report from the link itself, here in your browser. Nothing on this page is sent anywhere until you choose to.</p>
<div id="none" class="card" hidden><p class="warn">No report found in this link.</p>
<p>Open it from the game: Settings Book &rsaquo; Safety &rsaquo; Thy reports &rsaquo; the report &rsaquo; Send.</p></div>
<div id="has" hidden>
<div class="card"><table id="tbl"></table></div>
<div class="btns"><button id="copy" type="button">Copy the report</button><a id="mail" class="btn ghost" href="#">Email it to MAILADDR</a></div>
<p id="copied" class="meta" hidden>Copied.</p>
<p>Or send it to a moderator as a Discord direct message. Never post reports in public channels.</p>
<div class="card"><pre id="raw"></pre></div>
</div>
<script>
(function(){
  var MAIL="MAILADDR";
  function b64url(s){s=s.replace(/-/g,"+").replace(/_/g,"/");while(s.length%4)s+="=";var bin=atob(s),bytes=new Uint8Array(bin.length);
    for(var i=0;i<bin.length;i++)bytes[i]=bin.charCodeAt(i);return new TextDecoder("utf-8").decode(bytes);}
  var h=location.hash.replace(/^#/,""),rec=null;
  if(h.indexOf("r1.")===0){try{rec=JSON.parse(b64url(h.substring(3)));}catch(e){rec=null;}}
  if(!rec||typeof rec!=="object"){document.getElementById("none").hidden=false;return;}
  var WHY={1:"Hurtful words or voice",2:"Spoiling the play",3:"Unfit name or look",4:"Something else"};
  var who=rec.who||{},by=rec.by||{};
  var rows=[["Report",rec.c],["When (UTC)",rec.t],["Build",rec.b],["Why",WHY[rec.why]||rec.why],["Where",[rec.where,rec.scene,rec.area].filter(Boolean).join(" \u00b7 ")],
    ["Hall code",rec.hall],["Session",rec.sid],["Bearers present",rec.n],
    ["Reported",[who.name,who.raw&&who.raw!==who.name?"(typed: "+who.raw+")":"",who.tag?"tag "+who.tag:""].filter(Boolean).join(" ")],["Reported id",who.id],
    ["By",[by.name,by.tag?"tag "+by.tag:""].filter(Boolean).join(" ")],["By id",by.id]];
  var shown=rows.filter(function(r){return r[1]!==undefined&&r[1]!==null&&r[1]!=="";});
  var tbl=document.getElementById("tbl");
  shown.forEach(function(r){var tr=document.createElement("tr"),th=document.createElement("th"),td=document.createElement("td");
    th.textContent=r[0];td.textContent=String(r[1]);tr.appendChild(th);tr.appendChild(td);tbl.appendChild(tr);});
  var text="Lanternhall player report\n\n"+shown.map(function(r){return r[0]+": "+r[1];}).join("\n")+"\n\n(raw) "+JSON.stringify(rec);
  document.getElementById("raw").textContent=JSON.stringify(rec,null,1);
  var code=rec.c||"LH-??????";
  document.getElementById("mail").href="mailto:"+MAIL+"?subject="+encodeURIComponent("Player report "+code)+"&body="+encodeURIComponent(text+"\n\nAnything to add:\n");
  document.getElementById("copy").onclick=function(){
    function done(){document.getElementById("copied").hidden=false;}
    function fallback(){var ta=document.createElement("textarea");ta.value=text;document.body.appendChild(ta);ta.select();try{document.execCommand("copy");done();}catch(e){}document.body.removeChild(ta);}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done,fallback);}else fallback();
  };
  document.getElementById("has").hidden=false;
})();
</script>
</main></body></html>
""".replace("MAILADDR", MAIL)

build_notice()
for name, body in [("index.html", INDEX), ("guide.html", build_guide()), ("updates.html", UPDATES), ("support.html", SUPPORT),
                   ("privacy.html", PRIVACY), ("404.html", NOTFOUND), ("report.html", REPORT)]:
    open(name, "w", encoding="utf-8", newline="\n").write(body)
open("CNAME", "w", newline="\n").write("lanternhallvr.com\n")
open(".nojekyll", "w").write("")
open("README.md", "w", encoding="utf-8", newline="\n").write("# lanternhallvr.com\n\nStatic site for Lanternhall, served by GitHub Pages. "
                             "Edit `build.py` and run `python3 build.py` to regenerate the pages.\n\n"
                             "Tidings: `notice-src.json` (edited by `Tools/release/notice.ps1` in the game repo) becomes `notice.json`, which the game "
                             "reads; its `latest` block comes from the releases' `code:` / `alpha_code:` front matter (the newest per channel; "
                             "`notice-src.json` may only raise it). `report.html` decodes a player report from its link fragment, offline.\n\n"
                             "The Bearer's Guide: `guide.html` is built from `guide/guide.json` and `guide/img/`, which `python guide_import.py` "
                             "copies from the game repo (its guide export and web plates); rerun it, then build.py, when the guide changes.\n\n"
                             "Roblox: the Updates page's Roblox tab reads `roblox/releases.json`, which `python roblox_import.py` makes from the "
                             "Roblox repo's `docs/releases.json` (versions and dates) and the player-facing notes in `roblox/notes.json`. It lives "
                             "outside `releases/` so the Discord Action and `notice.json` never see it. `ROBLOX_URL` in build.py stays None "
                             "until the Roblox place is public.\n")
print("ok")
