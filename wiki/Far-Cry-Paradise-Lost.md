# Far Cry Paradise Lost

**Status:** Starts (2026-10-17). Under gamescope with `Windowed = 1` the game shows its attract text ("PULL TRIGGER TO START", free play) on a black background. The background and play have not been measured.

## 1. Platform and cabinet

Global VR PC based cabinet (**INFERRED**). The game is `Farcry_R.exe`, a Windows Direct3D 9 title for two players.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with DXVK for D3D9.
- A drive letter `W:` pointing at the game folder: the cabinet's `Runme.bat` does `subst W: .`, `w:`, `Farcry_r.exe`, and the game checks the drive letter (`WinMain` compares `_getdrive()` with `W`) and opens `w:\arcade_*.txt`.
- The game asks for exclusive fullscreen.
- Cabinet I/O is provided by RavenGun (assumption: the game waits for it).

## 3. The official start script, or why there is none

The cabinet's `Runme.bat` (**MEASURED** from the file): `subst W: .`, switch to `w:`, run `Farcry_r.exe`. RavenGun mimics it with a drive mapping.

## 4. The route we use

- `[Game] Type = TeknoParrot`, `EmulationProfile = FarCry`, `Executable = Farcry_R.exe`
- `[Launch] Mode = direct`, `Drives = W=.`, `Exe = W:\Farcry_R.exe`
- `[Wine] Prefix = ravengun-test-dxvk` (DXVK for Direct3D 9)
- `[Display] Gamescope = true`, with `Windowed = 1` in the imported config
- `[Input] Route = tp-shm`, `Layout = FarCryPipe`

**Why `Windowed = 1` under gamescope:** the game asks for exclusive full screen; without gamescope it hung in the mode switch, and under gamescope with `Windowed = 0` its main thread hung in `UpdateWindow`. Windowed under gamescope gets it past both and it draws.

## 5. Input

Layout `FarCryPipe` (**INFERRED**): test, service, start (P1/P2), trigger (P1/P2), one coin bit, grenade P1/P2, menu up/down on the volume keys. Aim: one byte per axis. Not tried in the game.

## 6. Timing

Not measured yet: neither the time to the attract text nor a five-minute run has been recorded.

## 7. What we saw on screen

**MEASURED** (2026-10-17): the attract text "PULL TRIGGER TO START" with FREE PLAY on a black background. Earlier (2026-10-15, without gamescope at 1920x1080) the D3D9 device was created and nothing was presented.

## 8. Current state and open questions

- The game reaches its attract text; it is not yet called working.
- Open: why the background stays black, and input and play (not measured).
- Earlier hypothesis: the game waits for cabinet hardware (its I/O); not confirmed.

## 9. What we tried and what did not work

- Under gamescope with `Windowed = 0`: the main thread hangs in `UpdateWindow` right after `CreateWindow`/`ShowWindow`.
- Without gamescope, default mode: hangs in `ChangeDisplaySettings` (switch to 800x600).
- Without gamescope and with a 1920x1080 custom resolution: passes both, creates the device, no Present (the main thread runs its message loop).
- Microsoft's `d3dx9_32` added: no change (so it is not in the profile).
- Under gamescope with `Windowed = 1`: the attract text shows (2026-10-17).

## 10. What is Linux-specific, and what differs on Windows

Wine-specific: the window and mode-switch hangs depend on gamescope and on the resolution the game asks for. The `W:` drive mapping replaces the cabinet's `subst` command. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
