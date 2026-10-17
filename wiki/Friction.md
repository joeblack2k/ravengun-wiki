# Friction

**Status:** Starts (2026-10-17). With `Windowed = 1` under gamescope the game shows its attract ("FRICTION", 2 coins per play) in a 4:3 picture. Play has not been measured.

## 1. Platform and cabinet

Unique PC based light-gun cabinet (**INFERRED**). The game is a 32-bit Windows program, `Friction.exe` (1,327,104 bytes), Direct3D 9, 640x480 by default. Two players.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with DXVK for Direct3D 9 (`[Launch] Dxvk = true`).
- The native `d3dx9_42.dll` and `d3dcompiler_42.dll` from the DirectX redistributable (`[Launch] NativeDlls = d3dx9_42, d3dcompiler_42`). With Wine's own d3dx9 the game's HLSL shaders do not compile (**MEASURED**: "Shader UI_VS is not supported"); with the native pair the loading screens appear.
- Cabinet I/O is provided by RavenGun.

## 3. The official start script, or why there is none

No official start script is used. The original cabinet boots Windows straight into the game (or its launcher); RavenGun starts the game's executable itself, from a double-click in the RavenGun app.

## 4. The route we use

Windows route, direct, in a dedicated Wine prefix:

- `[Game] Type = OpenParrot`, `EmulationProfile = Friction`
- `[Launch] Mode = direct`, `Dxvk = true`, `NativeDlls = d3dx9_42, d3dcompiler_42`
- `[Wine] Prefix = ravengun-test-dxvk`, `DllOverrides = d3d9=n,b`, `Runner = wrapper`
- `[Display] Gamescope = true` with `Windowed = 1` (kept on, so the TV never shows a desktop)
- `[Input] Route = tp-shm`, `Layout = Friction`

**Why `Windowed = 1`:** with `Windowed = 0` the game stayed black under gamescope; windowed lets gamescope present it. Imported config: resolution 640x480, free play off, custom crosshairs off.

## 5. Input

Layout `Friction` (control word at offset 8; **INFERRED** from the layout file):

| Function | Key/bit |
|---|---|
| Test | bit 0 |
| Coin 1 / coin 2 | bits 1 / 11 |
| Trigger P1 / P2 | bits 2 / 3 |
| Start P1 / P2 | bits 5 / 6 |
| Reload P1 / P2 | bits 9 / 10 |
| Menu select | F4 (volume up) |
| Menu down | F5 (volume down) |

Aim is one byte per axis (0 = left/top). None of this has been tried in a running level.

## 6. Timing

**MEASURED** (2026-10-15): loading screens within seconds. The time to the attract after the 2026-10-17 change, and a five-minute run, have not been recorded.

## 7. What we saw on screen

**MEASURED:**

- 2026-10-17: with `Windowed = 1` under gamescope, the attract screen ("FRICTION", 2 COINS PER PLAY) in a 4:3 picture.
- Earlier (2026-10-15), under gamescope with `Windowed = 0`: black, the main thread spinning in `UpdateWindow`/`NtUserRedrawWindow` (Wine's message loop, about 100,000 context switches per second).
- Without gamescope, fullscreen 1920x1080: "ALLOCATING MEMORY POOLS" at 60 fps, then black with 4 draw calls at 7 fps; the window then disappeared behind the desktop.
- With the `rg-compat` option `RG_COMPAT_PAINT=1` (sends one `WM_PAINT` from `UpdateWindow`, as Windows does) and `Windowed = 1` at 1920x1080: "LOADING LEVEL" at about 7 fps, then the game exited by itself after about 2.5 minutes.

## 8. Current state and open questions

- The game starts and shows its attract; it is not yet called working.
- Open: coin, START and play (the level used to stay black or exit by itself), and the input layout, which has not been exercised in a level.

## 9. What we tried and what did not work

- Wine's built-in d3d9 (wined3d): fails with "Shader UI_VS is not supported by the target hardware" (2026-10-14). Fixed by DXVK plus the native d3dx9_42/d3dcompiler_42.
- Gamescope with `Windowed = 0`: endless `UpdateWindow` loop, black. Fixed by `Windowed = 1`.
- No gamescope: draws briefly, then black, and the window is lost behind the desktop.

## 10. What is Linux-specific, and what differs on Windows

On Linux this is a Wine game, and the failing behaviour is Wine-specific (message loop and window-clip handling under gamescope). On Windows the game runs directly with its own d3dx9 runtime; on Linux you must supply the native d3dx9_42 and d3dcompiler_42 (from the Steam DirectX redistributable) because Wine's replacement does not compile the shaders. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
