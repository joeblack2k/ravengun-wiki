# Haunted Museum II

**Status:** Working (2026-10-16). A double-click starts the game under Wine with the same recipe as [Gaia Attack 4](Gaia-Attack-4): attract, coin, START and the game. Gun calibration (P1 and P2) and the date ship with RavenGun; to recalibrate use TEST > GUN CHECK > START 1 and save with TEST.

## 1. Platform and cabinet

Taito Type X2 cabinet. The game is `game.exe` (Windows, 32-bit), Taito, 2011. The dump we use is the **USA 1.00** build (**MEASURED**: the CRC of the first 0x400 bytes of the main module, `0x5a7fa241`, matches the USA 1.00 entry; the Japanese 1.01 build would give `0x42d54499`).

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with Wine's built-in d3d9.
- The Type X2 I/O board (JVS on a pipe) is emulated by RavenGun.
- Region: the game reads a `REGION` line from its own `haunted2.ini` (profile field `Region = E`).
- The game needs a real `data` folder: Proton reports a linked folder as a folder plus a reparse point, and the game checks for a plain folder attribute; with a linked `data` it changed directory to the parent and showed SOUND ERROR. RavenGun makes `data` a real folder with links to its contents (`ViewRealDirs = data`).

## 3. The official start script, or why there is none

No official start script is used. The original cabinet boots Windows straight into the game (or its launcher); RavenGun starts the game's executable itself, from a double-click in the RavenGun app.

## 4. The route we use

Windows route on RavenGun's own OpenParrot-compatible core, direct launch; the recipe of [Gaia Attack 4](Gaia-Attack-4):

- `[Game] Type = OpenParrot`, `EmulationProfile = HauntedMuseum2`, `Executable = game.exe`
- `[Launch] Mode = direct`, `ViewRealDirs = data`
- `[Display] Gamescope = true` with `Windowed = 1`
- `[Input] Route = jvs`, `Board = TaitoGun`, `Layout = MusicGunGun2Pipe`

The JVS board `TaitoGun` answers the Taito commands (node 0); START of player 1/2 is P1 up/down. The environment is the same as for Gaia Attack 4 (`TP_REMOTETHREAD=off`, `WINEDLLOVERRIDES=d3d9=b`, `RG_LOADER_FPFIX=true`).

## 5. Input

JVS board `TaitoGun` over the pipe for coin, test, service and START, plus the layout `MusicGunGun2Pipe` for triggers and aim (see [Gaia Attack 4](Gaia-Attack-4)). The game folder's own README names mouse and left click as controls. **MEASURED** 2026-10-16 with the mouse as lightgun: coin, START and the game. Not measured with the real PS Move.

## 6. Timing

Played on 2026-10-16 through the attract, coin, START and into the game. The exact play duration and the time to attract were not recorded in the source notes.

## 7. What we saw on screen

**MEASURED** (2026-10-16): attract, coin, START and the game, full screen under gamescope.

## 8. Current state and open questions

- Working: double-click, attract, coin, START and the game.
- Gun calibration ships with RavenGun (made in the game's test menu in mouse mode); the P1 and P2 calibration and the date are shipped, and one coin per credit is set.
- Open: play with the real PS Move.

## 9. What we tried and what did not work

Same path as [Gaia Attack 4](Gaia-Attack-4): the Wine MXCSR crash fixed by `RG_LOADER_FPFIX`; the JVS chain completing but a black picture until the reconnecting pipe, the requested channel count, the `TaitoGun` board and `Windowed = 1` under gamescope were in place. The data-folder fix (`ViewRealDirs`) removed the SOUND ERROR.

## 10. What is Linux-specific, and what differs on Windows

Wine-specific: the MXCSR crash is a Wine behaviour worked around in the loader. Proton's reparse-point report for linked folders is the reason for `ViewRealDirs`. On the cabinet the I/O board sits on a serial line; on Linux it is a pipe emulated by RavenGun. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
