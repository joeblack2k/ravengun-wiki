# Cooper's 9

**Status:** Starts (2026-10-17). With `Windowed = 1` under gamescope the game shows its own screen "PLEASE CALIBRATE THE GUN". Calibration and play have not been measured.

## 1. Platform and cabinet

Konami PC based cabinet (**INFERRED**). The game is `game.exe` (41,066,496 bytes), a Windows Direct3D 9 title for up to two players.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with DXVK for D3D9 (`DllOverrides = d3d9=n,b` in a dedicated prefix).
- Cabinet I/O is provided by RavenGun.

## 3. The official start script, or why there is none

No official start script is used. The original cabinet boots Windows straight into the game (or its launcher); RavenGun starts the game's executable itself, from a double-click in the RavenGun app.

## 4. The route we use

- `[Game] Type = TeknoParrot`, `EmulationProfile = WartranTroopers`, `Executable = game.exe`
- `[Launch] Mode = direct`
- `[Wine] Prefix = ravengun-test-dxvk` (a dedicated prefix with DXVK for Direct3D 9)
- `[Display] Gamescope = true`, with `Windowed = 1` in the imported config
- `[Input] Route = tp-shm`, `Layout = WartranTroopers`

**Why `Windowed = 1`:** with `Windowed = 0` the process ran but no window became visible under gamescope. Setting the game to windowed lets gamescope present it full screen.

Imported config: 1280x720 custom resolution available (off), FPS limit 60 (on), cursor hidden. A second layout `WartranTroopersKonami` exists for Konami test menus (see [Gashaaaan](Gashaaaan)).

## 5. Input

Four-player shooter layout (test, service, coins, start, trigger, reload, grenade, extra button per player; aim one byte per axis). Not tried in the game.

## 6. Timing

Not measured: neither the time to the first screen nor a five-minute run has been recorded.

## 7. What we saw on screen

**MEASURED** (2026-10-17): the game's own calibration screen, "PLEASE CALIBRATE THE GUN". With `Windowed = 0` there was no visible window (2026-10-14).

## 8. Current state and open questions

- The game starts and reaches its calibration prompt; it is not yet called working.
- Open: gun calibration, coin and START, and a five-minute attract or play run. The input layout is the closest available one.

## 9. What we tried and what did not work

Direct launch with DXVK in gamescope and `Windowed = 0`: process alive, no visible window. Fixed by `Windowed = 1`.

## 10. What is Linux-specific, and what differs on Windows

Windows game under Wine/DXVK; window-handling behaviour under gamescope is the usual suspect on Linux. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
