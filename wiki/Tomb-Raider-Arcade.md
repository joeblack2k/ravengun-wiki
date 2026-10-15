# Tomb Raider Arcade

**Status:** Working (2026-10-14). A double-click in RavenGun starts the game under Proton with RavenGun's own BepInEx plugin, which takes input over TCP. Coin, START, aiming, shooting and one level were played for 5:24 min in mouse mode.

## 1. Platform and cabinet

- ADRENALINE PC-based cabinet; a 64-bit Unity game, `Game.exe` (about 652 KB) with a `Game_Data` folder.
- Four-player lightgun layout; template profile TeknoParrot `TombRaider` (revision 6), input layout `WartranTroopers`.

## 2. What the game needs

- Your own game folder; RavenGun ships no games.
- Proton (GE-Proton) with a prefix; the first start takes about half a minute to create it.
- BepInEx 5.4.21.0 (x64, Mono) from the official BepInEx project, installed once on your machine, and RavenGun's own Unity plugin, built locally with `scripts/build-unity-plugin.sh` (needs your game's `Assembly-CSharp.dll` to build against; nothing is copied or changed).
- RavenGun provides the cabinet hardware the game expects. The cabinet's own USB I/O board was what blocked the game originally ("IO BOARD ERROR", "Base not found"); the plugin solves that.

## 3. The official start script, or why there is none

None. The game runs from its own cabinet; on Windows the community uses TeknoParrot. RavenGun starts it itself.

## 4. The route we use

**MEASURED** 2026-10-14: daemon -> Proton with the BepInEx plugin, input over TCP; no scripts and no TeknoParrot.

```ini
[Loader]
PostStartMs = 3000

[Wine]
DllOverrides = winhttp=n,b

[Input]
Route = unity-tcp
```

`winhttp=n,b` loads BepInEx's doorstop. The plugin opens a TCP server on port **33610**; if the BepInEx log (`LogOutput.log` in the local view) shows "TCP Server is listening on Port 33610", the plugin works. `ravengunctl status` shows "Unity game: ... connected, 120 packets/s" when the daemon is attached.

## 5. Input

- Coin: key **5** (players 1..4 = keys 5..8). The game counts coins in quarters ("1/4 credits"), so insert four.
- START: key **1** (players 1..4 = keys 1..4). **Hold the key briefly**: a very short tap does not count (**MEASURED**).
- TEST: key 0. Esc quits.
- Aim and trigger: from Move or mouse. The Y origin of the aim is `bottom` (measured); if the in-game crosshair sits systematically off, adjust `scale_x`, `scale_y`, `offset_x`, `offset_y` for the game in `packaging/aagames-games.json`.
- Move buttons can be mapped to `key:5` and `key:1` in the app's button layout.

## 6. Timing

- Played 5:24 min (**MEASURED**).
- First start also builds the Proton prefix (about 30 s). Frame pacing: not measured yet.

## 7. What we saw on screen

Coin and START, aiming with a crosshair, shooting, and a level played through.

## 8. Current state and open questions

- Not yet played with the real Move buttons.
- A drift of the aim over a session was noted once (2026-10-09) while the setup around the gun had changed; not conclusively explained.

## 9. What we tried and what did not work

- The original blocker was the USB I/O board, not anything else; solved by the plugin.
- A very short START tap is ignored; hold it.

## 10. What is Linux-specific, and what differs on Windows

On Windows people use TeknoParrot or DemulShooter-style injection. On Linux RavenGun uses Proton plus its own BepInEx plugin that talks TCP to the daemon, so no TeknoParrot is involved.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
