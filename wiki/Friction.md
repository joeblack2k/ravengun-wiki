# Friction

**Status:** Not working yet. The loading screens render with DXVK, but the level stays black.

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
- `[Display] Gamescope = true` (kept on, so the TV never shows a desktop)
- `[Input] Route = tp-shm`, `Layout = Friction`

Imported config: resolution 640x480, free play off, custom crosshairs off.

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

**MEASURED** (2026-10-15): loading screens within seconds; "ALLOCATING MEMORY POOLS" at 60 fps without gamescope; "LOADING LEVEL" at about 7 fps; with the paint workaround below the game exits by itself after about 2.5 minutes (exit code 0).

## 7. What we saw on screen

**MEASURED:**

- Under gamescope: black screen. The main thread spins forever in `UpdateWindow`/`NtUserRedrawWindow` (Wine's message loop, about 100,000 context switches per second), both fullscreen and windowed.
- Without gamescope, fullscreen 1920x1080: "ALLOCATING MEMORY POOLS" at 60 fps, then black with 4 draw calls at 7 fps; the window then disappears behind the desktop.
- With the `rg-compat` option `RG_COMPAT_PAINT=1` (sends one `WM_PAINT` from `UpdateWindow`, as Windows does) and `Windowed = 1` at 1920x1080, under gamescope: "LOADING LEVEL" with a picture, about 7 fps. This workaround is not in the profile yet.

## 8. Current state and open questions

- Not playable. The level stays black or the game exits by itself.
- Open: why the level does not draw (4 draw calls, 7 fps), and putting the paint workaround into the profile.
- The input layout has not been exercised in a level.

## 9. What we tried and what did not work

- Wine's built-in d3d9 (wined3d): fails with "Shader UI_VS is not supported by the target hardware" (2026-10-14). Fixed by DXVK plus the native d3dx9_42/d3dcompiler_42.
- Gamescope fullscreen: endless `UpdateWindow` loop, black.
- No gamescope: draws briefly, then black, and the window is lost behind the desktop.

## 10. What is Linux-specific, and what differs on Windows

On Linux this is a Wine game, and the failing behaviour is Wine-specific (message loop and window-clip handling under gamescope). On Windows the game runs directly with its own d3dx9 runtime; on Linux you must supply the native d3dx9_42 and d3dcompiler_42 (from the Steam DirectX redistributable) because Wine's replacement does not compile the shaders. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
