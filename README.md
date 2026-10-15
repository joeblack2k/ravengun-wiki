# RavenGun wiki

RavenGun runs arcade lightgun games on Linux: it starts each game itself (native Linux where the cabinet ran Linux,
Wine/Proton where it ran Windows) and feeds it input from a PS Move, a mouse or a game controller. This repository is
its community wiki: per title, what the game needs, the route RavenGun uses, the input, what was seen on screen and
where it stops — so others can build on it.

**Read it in the [Wiki tab](https://github.com/joeblack2k/ravengun-wiki/wiki)**, or start at [`wiki/Home.md`](wiki/Home.md).

RavenGun ships no games. You need your own legally obtained copies.

## Layout

| Path | What |
|---|---|
| `wiki/` | The pages (file name = page name). `Home`, `Compatibility`, `_Sidebar` and `_Footer` are generated. |
| `pages.tsv` | One line per game page: page name, title, profile folder, state, platform, date. |
| `tools/gen-index.py` | Writes `Home`, `Compatibility`, `_Sidebar` and `_Footer` from `pages.tsv`. |
| `tools/wiki-check.py` | Checks the pages: every page exists, links resolve, game pages have the same ten sections, nothing machine-specific. |

## License

Text: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Tools: GPL-3.0-or-later.
