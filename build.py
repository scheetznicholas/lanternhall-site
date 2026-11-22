"""Builds the static pages for lanternhallvr.com (GitHub Pages). Run: python3 build.py"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&'
         'family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">')
YT = "https://www.youtube.com/@LanternhallGames"
MAIL = "support@lanternhallvr.com"

import glob, html, os, re


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


def head(title, desc, page):
    nav = [("index.html", "Home"), ("updates.html", "Updates"), ("support.html", "Support"), ("privacy.html", "Privacy")]
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == page else ""}>{t}</a>' for h, t in nav)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://lanternhallvr.com/assets/hero.jpg">
<meta name="theme-color" content="#17110c">
<link rel="icon" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="style.css">
</head><body>
<header class="nav"><div class="nav-in">
<a class="brand" href="index.html"><img src="assets/favicon.png" alt="">Lanternhall</a>
<nav class="nav-links">{links}</nav>
</div></header>
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
<p>A four-player co-op VR quest game for Meta Quest. Gather your party in Lanternhall, step onto the gate stone,
and fight your way through Cinderkeep to the throne of the Emberking.</p>
<div class="cta"><a class="btn" href="{YT}">Watch on YouTube</a><a class="btn ghost" href="support.html">Support &amp; FAQ</a></div>
<span class="badge">Beta coming soon</span>
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
<p>You can leave a hall at any time from the Fellowship Board or your wrist menu. To report a player, email us their in-game name,
the hall code if you have it, and what happened. Meta's own reporting tools on your headset also work.</p></details>
<details><summary>Is my progress saved?</summary>
<p>Your level, unlocks and settings are saved on your headset. Uninstalling the game or clearing its data removes them.</p></details>
</main>
""" + FOOT

PRIVACY = head("Privacy Policy: Lanternhall", "How Lanternhall handles your information.", "privacy.html") + f"""
<main class="doc">
<h1>Privacy Policy</h1>
<p class="meta">Lanternhall, by Lanternhall Games &middot; Effective November 2026</p>

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
<li><b>Crash and diagnostic data.</b> The Unity engine may send anonymous crash and performance diagnostics to Unity to help
fix bugs.</li>
</ul>

<h2>Who processes it</h2>
<p>Online features are provided by Unity Technologies (Unity Gaming Services and Vivox). The game is distributed through the
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


UPDATES = head("Updates: Lanternhall", "Release notes for Lanternhall, the co-op VR quest game for Meta Quest.", "updates.html") + f"""
<main class="doc">
<h1>Updates</h1>
<p class="meta">Release notes for every build of Lanternhall, newest first.</p>
{"".join(release_html(r) for r in RELEASES)}
</main>
""" + FOOT

NOTFOUND = head("Lost in the keep: Lanternhall", "Page not found.", "") + """
<main class="doc" style="text-align:center"><h1>Lost in the keep</h1>
<p class="meta">That page isn't here. Maybe it fell down the Belfry shaft.</p>
<p><a class="btn" href="index.html">Back to Lanternhall</a></p></main>
""" + FOOT

for name, body in [("index.html", INDEX), ("updates.html", UPDATES), ("support.html", SUPPORT), ("privacy.html", PRIVACY), ("404.html", NOTFOUND)]:
    open(name, "w", encoding="utf-8", newline="\n").write(body)
open("CNAME", "w").write("lanternhallvr.com\n")
open(".nojekyll", "w").write("")
open("README.md", "w", encoding="utf-8").write("# lanternhallvr.com\n\nStatic site for Lanternhall, served by GitHub Pages. "
                             "Edit `build.py` and run `python3 build.py` to regenerate the pages.\n")
print("ok")
