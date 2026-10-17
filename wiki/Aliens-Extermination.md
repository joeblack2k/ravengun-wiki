# Aliens: Extermination

**Status:** Starts (2026-10-17). A double-click shows the boot screen (version 1.0.3 US), the Global VR and PlayMechanix logos and the attract loop with free play and "press start". The boot screen still reports "I/O ERROR: no GVRIO card found" and "no Aliens guns found"; input has not been measured.

## 1. Platform and cabinet

Global VR "PC Based" light-gun cabinet (**INFERRED**, from the platform column of the goal list). The game is a 32-bit Windows program (`aliens.exe`; the dump we use has it under `DATA/`, 89,698,304 bytes). Players: 2. Special buttons per player: grenade and flame.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine/Proton with a 32-bit capable prefix (**INFERRED**).
- The cabinet hardware the game expects (its I/O and cabinet checks) is provided by RavenGun; there is no user step for it.
- A light-gun input source: PS Move, mouse or a game controller.

## 3. The official start script, or why there is none

No official start script is used. The original cabinet boots Windows straight into the game (or its launcher); RavenGun starts the game's executable itself, from a double-click in the RavenGun app.

## 4. The route we use

Windows route, started directly (no helper shell chain). Profile keys in `game.ini` (**MEASURED** from the file):

- `[Game] Type = TeknoParrot`, `EmulationProfile = AliensExtermination`, `Executable = aliens.exe;aliens dehasped.exe` (the dump we use has the game program under `DATA/`)
- `[Launch] Mode = direct`, `PeFillPages = true`
- `[Display] Gamescope = true`, with `Windowed = 1` at 1920x1080
- `[Input] Route = tp-shm`, `Layout = AliensExtermination`

**Why `PeFillPages`:** the game program carries a small runtime component right behind the end of its code section. Windows maps the last page of a section completely, including the bytes after the stored size; Wine zero-fills them, so the game read a cleared field and crashed about 18 seconds after launch. With `PeFillPages = true` RavenGun runs a local copy of the executable in its view folder in which every section is extended to its page boundary, as Windows maps it. The original file on the game folder is never changed. A copy whose header differed from the original made the loader core stop with exit code 1337, so the header is kept identical.

The profile comes from the TeknoParrot profile template (revision 14). Free play is on in the imported config.

## 5. Input

The tp-shm layout `AliensExtermination` is the closest available one, not a measured choice (**INFERRED** from the layout file):

| Function | Mapped to |
|---|---|
| Coin 1 / coin 2 | coin buttons |
| P1 start / trigger | start / trigger |
| Special (grenade) | the grenade button |
| Flame | extra button 1 |
| Test, service | test, service |
| Volume up / down | menu keys |

Aim is one byte per axis (0 = left/top); the second player uses the second pair of axes. **Not measured in the game yet.** The boot screen says it finds no Global VR I/O card and no Aliens guns, so a dedicated input layout or board may be needed.

## 6. Timing

Attract is reached after the boot screen and the two logos. The time from the double-click to the attract and a five-minute run have not been recorded yet. The earlier crash about 18 seconds after launch (2026-10-15) is gone.

## 7. What we saw on screen

**MEASURED** (2026-10-17): the boot screen with "VERSION 1.0.3 US", the Global VR and PlayMechanix logos, then the attract with FREE PLAY and PRESS START. The boot screen lists the two I/O messages mentioned above.

## 8. Current state and open questions

- The game starts and shows its attract. Not yet called working: coin, START, aiming and play are not measured.
- Open: the two I/O messages on the boot screen (no Global VR I/O card, no Aliens guns) and the input layout, which is only the closest available one.

## 9. What we tried and what did not work

- Without `PeFillPages`: the game died about 18 s after launch with an access violation (a read from a cleared field). Fixed by the section extension described in section 4.
- Not tried: other Wine versions or a different prefix; graphics were not the issue.

## 10. What is Linux-specific, and what differs on Windows

This is a Windows game, so on Linux it runs under Wine with RavenGun's loader. The Wine-specific part is the section mapping: Wine clears the bytes between the stored size of a section and the end of its page, where Windows maps what the file holds; `PeFillPages` reproduces the Windows mapping in a local copy. On the real cabinet the game runs on Windows with its own I/O hardware; RavenGun replaces that hardware with its own emulated I/O. See [Wine-Notes](Wine-Notes) and [Running-on-Linux](Running-on-Linux).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
