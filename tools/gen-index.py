#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Writes Home.md, Compatibility.md, _Sidebar.md and _Footer.md of the RavenGun wiki from pages.tsv.

pages.tsv: one line per game page, tab-separated: Page, Title, profile folder, WORKING | STARTS | SKIPPED | NOT YET, platform, date.
Usage: gen-index.py [WIKI-DIR]   (default: ../wiki next to this folder; pages.tsv is read from the parent folder)
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "wiki")
GENERAL = [("Compatibility", "Compatibility", "every title with its platform and state"),
           ("Running-on-Linux", "Running on Linux", "installing RavenGun, the first-run wizard, your game folder"),
           ("Loader-Architecture", "Loader architecture", "how RavenGun starts a game: routes, profiles, drop-ins, input bridges"),
           ("Official-Start-Scripts", "Official start scripts", "what the cabinets' own start scripts do, and how RavenGun reads them"),
           ("Wine-Notes", "Wine notes", "Wine/Proton fixes and options: movies, DXVK, audio, window handling")]
STAND = ("Overall (2026-10-17): 52 of 54 counted titles start (96%); Raw Thrills titles are not counted "
         "(Police Trainer 2 and Crossfire: Maximum Paintball use Raw Thrills I/O), nor are skipped titles.")
SCOPE = "This page covers the game and the loader: what you need to run this title and where it gets stuck."


def rows():
    out = []
    for line in open(os.path.join(HERE, "pages.tsv"), encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) < 4 or not f[0].strip():
            continue
        f += [""] * (6 - len(f))
        out.append({"page": f[0], "title": f[1], "state": f[3], "platform": f[4], "date": f[5]})
    return sorted(out, key=lambda r: r["title"].lower()[4:] if r["title"].lower().startswith("the ") else r["title"].lower())


def main():
    rs = rows()
    work = [r for r in rs if r["state"] == "WORKING"]
    starts = [r for r in rs if r["state"] == "STARTS"]
    skipped = [r for r in rs if r["state"] == "SKIPPED"]
    rest = [r for r in rs if r["state"] not in ("WORKING", "STARTS", "SKIPPED")]
    notyet = rest

    home = ["# RavenGun", "",
            "RavenGun runs arcade lightgun games on Linux. It starts each game itself — native Linux where the cabinet ran "
            "Linux, Wine/Proton (with Vulkan where possible) where it ran Windows — and feeds it input from a PS Move, a "
            "mouse or a game controller. The goal: on a freshly installed SteamOS PC, a first-run wizard asks for the "
            "permissions it needs and for the folder with your game backups, and from then on you double-click a game "
            "and play, with per-game options in the app. No TeknoParrot tools or loaders are needed.", "",
            "RavenGun ships no games. You need your own legally obtained copies.", "",
            "This wiki collects what was learned per title, so others can build on it. **%d titles are Working** (started "
            "with a double-click and played for at least five minutes) and **%d more Start** (the game shows its own "
            "logo or attract by double-click; play is not yet measured). %s See [Compatibility](Compatibility); the other "
            "pages say where each title stops." % (len(work), len(starts), STAND), "",
            "## How to read a game page", "",
            "Every game page has the same ten sections: platform and cabinet, what the game needs, the official start "
            "script, the route RavenGun uses, input, timing, what was seen on screen, current state, what did not work, "
            "and what is Linux-specific. Claims are labelled **MEASURED** (seen or measured on a test machine) or "
            "**INFERRED** (read from the game's files or derived); an assumption is called one.", "",
            "## General pages", ""]
    home += ["- [%s](%s): %s" % (t, p, d) for p, t, d in GENERAL]
    home += ["", "## Working (%d)" % len(work), ""]
    home += ["- [%s](%s)%s" % (r["title"], r["page"], " — " + r["platform"] if r["platform"] else "") for r in work]
    home += ["", "## Starts: attract or title on screen (%d)" % len(starts), ""]
    home += ["- [%s](%s)%s" % (r["title"], r["page"], " — " + r["platform"] if r["platform"] else "") for r in starts]
    home += ["", "## Skipped (%d)" % len(skipped), ""]
    home += ["- [%s](%s)%s" % (r["title"], r["page"], " — " + r["platform"] if r["platform"] else "") for r in skipped]
    home += ["", "## Not working yet (%d)" % len(rest), ""]
    home += ["- [%s](%s)%s" % (r["title"], r["page"], " — " + r["platform"] if r["platform"] else "") for r in rest]
    home += ["", SCOPE, ""]

    comp = ["# Compatibility", "",
            "One line per title. **Working** means: started with a double-click in RavenGun on a test machine (a Steam "
            "Deck-class PC on a TV, lightgun via PS Move or a mouse) and played for at least five minutes of attract or "
            "gameplay. **Starts** means: double-click shows the game's own logo, attract or title screen, but play has not been "
            "measured yet. **Skipped** means the owner's rule excluded the title (Japanese text and/or a 4:3 picture "
            "without a 16:9 mode). " + STAND + " The game page has the details and the date. This is a snapshot of one "
            "setup, not a promise.", "",
            "| Title | Platform | State |", "|---|---|---|"]
    for r in work + starts + skipped + rest:
        label = {"WORKING": "Working", "STARTS": "Starts", "SKIPPED": "Skipped"}.get(r["state"], "Not working yet")
        state = label + (" (%s)" % r["date"] if r["date"] and r["state"] != "NOT YET" else "")
        comp.append("| [%s](%s) | %s | %s |" % (r["title"], r["page"], r["platform"] or "—", state))
    comp += ["", "RavenGun ships no games. You need your own legally obtained copies.", "", SCOPE, ""]

    side = ["**[Home](Home)**", ""] + ["- [%s](%s)" % (t, p) for p, t, d in GENERAL]
    side += ["", "**Working**", ""] + ["- [%s](%s)" % (r["title"], r["page"]) for r in work]
    side += ["", "**Starts**", ""] + ["- [%s](%s)" % (r["title"], r["page"]) for r in starts]
    side += ["", "**Skipped**", ""] + ["- [%s](%s)" % (r["title"], r["page"]) for r in skipped]
    side += ["", "**Not working yet**", ""] + ["- [%s](%s)" % (r["title"], r["page"]) for r in rest] + [""]

    foot = ["MEASURED = seen or measured on a test machine · INFERRED = read from the game's files or derived · "
            "RavenGun ships no games: you need your own copy."]

    for name, lines in (("Home", home), ("Compatibility", comp), ("_Sidebar", side), ("_Footer", foot)):
        with open(os.path.join(WIKI, name + ".md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + ("\n" if not lines[-1] == "" else ""))
    print("written: Home, Compatibility, _Sidebar, _Footer (%d working, %d starts, %d skipped, %d not yet)" % (len(work), len(starts), len(skipped), len(rest)))


if __name__ == "__main__":
    main()
