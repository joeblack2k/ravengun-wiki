#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Writes Home.md, Compatibility.md, _Sidebar.md and _Footer.md of the RavenGun wiki from pages.tsv.

pages.tsv: one line per game page, tab-separated: Page, Title, profile folder, WORKING | NOT YET, platform, date.
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
    rest = [r for r in rs if r["state"] != "WORKING"]

    home = ["# RavenGun", "",
            "RavenGun runs arcade lightgun games on Linux. It starts each game itself — native Linux where the cabinet ran "
            "Linux, Wine/Proton (with Vulkan where possible) where it ran Windows — and feeds it input from a PS Move, a "
            "mouse or a game controller. The goal: on a freshly installed SteamOS PC, a first-run wizard asks for the "
            "permissions it needs and for the folder with your game backups, and from then on you double-click a game "
            "and play, with per-game options in the app. No TeknoParrot tools or loaders are needed.", "",
            "RavenGun ships no games. You need your own legally obtained copies.", "",
            "This wiki collects what was learned per title, so others can build on it. **%d of %d titles work** from a "
            "double-click (see [Compatibility](Compatibility)); the other pages say where each title stops." % (len(work), len(rs)), "",
            "## How to read a game page", "",
            "Every game page has the same ten sections: platform and cabinet, what the game needs, the official start "
            "script, the route RavenGun uses, input, timing, what was seen on screen, current state, what did not work, "
            "and what is Linux-specific. Claims are labelled **MEASURED** (seen or measured on a test machine) or "
            "**INFERRED** (read from the game's files or derived); an assumption is called one.", "",
            "## General pages", ""]
    home += ["- [%s](%s): %s" % (t, p, d) for p, t, d in GENERAL]
    home += ["", "## Working (%d)" % len(work), ""]
    home += ["- [%s](%s)%s" % (r["title"], r["page"], " — " + r["platform"] if r["platform"] else "") for r in work]
    home += ["", "## Not working yet (%d)" % len(rest), ""]
    home += ["- [%s](%s)%s" % (r["title"], r["page"], " — " + r["platform"] if r["platform"] else "") for r in rest]
    home += ["", SCOPE, ""]

    comp = ["# Compatibility", "",
            "One line per title. **Working** means: started with a double-click in RavenGun on a test machine (a Steam "
            "Deck-class PC on a TV, lightgun via PS Move or a mouse) and played for at least five minutes of attract or "
            "gameplay. The game page has the details and the date. This is a snapshot of one setup, not a promise.", "",
            "| Title | Platform | State |", "|---|---|---|"]
    for r in work + rest:
        state = "Working" + (" (%s)" % r["date"] if r["date"] else "") if r["state"] == "WORKING" else "Not working yet"
        comp.append("| [%s](%s) | %s | %s |" % (r["title"], r["page"], r["platform"] or "—", state))
    comp += ["", "RavenGun ships no games. You need your own legally obtained copies.", "", SCOPE, ""]

    side = ["**[Home](Home)**", ""] + ["- [%s](%s)" % (t, p) for p, t, d in GENERAL]
    side += ["", "**Working**", ""] + ["- [%s](%s)" % (r["title"], r["page"]) for r in work]
    side += ["", "**Not working yet**", ""] + ["- [%s](%s)" % (r["title"], r["page"]) for r in rest] + [""]

    foot = ["MEASURED = seen or measured on a test machine · INFERRED = read from the game's files or derived · "
            "RavenGun ships no games: you need your own copy."]

    for name, lines in (("Home", home), ("Compatibility", comp), ("_Sidebar", side), ("_Footer", foot)):
        with open(os.path.join(WIKI, name + ".md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + ("\n" if not lines[-1] == "" else ""))
    print("written: Home, Compatibility, _Sidebar, _Footer (%d working, %d not yet)" % (len(work), len(rest)))


if __name__ == "__main__":
    main()
