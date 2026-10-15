# Robin Hood

**Status:** Not working yet. The game opens a Direct3D 9 device at 1280x720 but never presents a frame.

## 1. Platform and cabinet

ICE PC based cabinet (**INFERRED**). The game is `game.exe`, Windows Direct3D 9. Two players.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with DXVK for D3D9; the game asks for exclusive fullscreen (diagnosis 2026-10-14).
- Cabinet I/O is provided by RavenGun.

## 3. The official start script, or why there is none

No official start script is used. The original cabinet boots Windows straight into the game (or its launcher); RavenGun starts the game's executable itself, from a double-click in the RavenGun app.

## 4. The route we use

- `[Game] Type = TeknoParrot`, `EmulationProfile = WartranTroopers`, `Executable = game.exe`
- `[Launch] Mode = direct`
- `[Wine] Prefix = ravengun-test-dxvk`, `DllOverrides = d3d9=n,b`, `Runner = wrapper`
- `[Display] Gamescope = true`
- `[Input] Route = tp-shm`, `Layout = WartranTroopers`

## 5. Input

Four-player shooter layout (test, service, coins, start, trigger, reload, grenade, extra per player; aim one byte per axis). Not tried in the game.

## 6. Timing

Not measured yet.

## 7. What we saw on screen

**MEASURED** (2026-10-15, with the loader's sampling thread): D3D9 at 1280x720, but no Present; black.

## 8. Current state and open questions

- The main thread sits in its message loop and draws nothing; the process uses about 57% CPU, spent in `/proc` reads (`GetThreadTimes`).
- Open: what the game is waiting for before it draws (assumption: something with the cabinet environment).

## 9. What we tried and what did not work

- Direct launch with DXVK in gamescope: D3D9 device created, no Present. No variants recorded yet.

## 10. What is Linux-specific, and what differs on Windows

Windows game under Wine/DXVK. The heavy `/proc` polling is how Wine implements Windows thread-time calls. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
