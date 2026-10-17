# Robin Hood

**Status:** Starts (2026-10-17). With `Windowed = 1` under gamescope the game shows its attract ("PRESS START BUTTON", free play). Play has not been measured.

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
- `[Wine] Prefix = ravengun-test-dxvk` (DXVK for Direct3D 9)
- `[Display] Gamescope = true`, with `Windowed = 1` in the imported config
- `[Input] Route = tp-shm`, `Layout = WartranTroopers`

**Why `Windowed = 1`:** with `Windowed = 0` the game created its Direct3D 9 device at 1280x720 but never presented a frame, because it asks for exclusive full screen. Windowed under gamescope draws.

## 5. Input

Four-player shooter layout (test, service, coins, start, trigger, reload, grenade, extra per player; aim one byte per axis). Not tried in the game.

## 6. Timing

Not measured: the time to the attract and a five-minute run have not been recorded.

## 7. What we saw on screen

**MEASURED** (2026-10-17): the attract with PRESS START BUTTON and FREE PLAY. Earlier (2026-10-15) with `Windowed = 0`: the device was created at 1280x720 and nothing was presented.

## 8. Current state and open questions

- The game starts and shows its attract; it is not yet called working.
- Open: coin, START and play (not measured).

## 9. What we tried and what did not work

Direct launch with DXVK in gamescope and `Windowed = 0`: D3D9 device created, no Present, the main thread in its message loop with about 57% CPU in `/proc` reads. Fixed by `Windowed = 1`.

## 10. What is Linux-specific, and what differs on Windows

Windows game under Wine/DXVK. The heavy `/proc` polling is how Wine implements Windows thread-time calls. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
