# Far Cry Paradise Lost

**Status:** Not working yet. The game creates its Direct3D 9 device but never draws a frame.

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
- `[Wine] Prefix = ravengun-test-dxvk`, `DllOverrides = d3d9=n,b`, `Runner = wrapper`
- `[Display] Gamescope = false`; in the user layer set `CustomResolution` to 1920x1080 (the game then passes its mode switch)
- `[Input] Route = tp-shm`, `Layout = FarCryPipe`

## 5. Input

Layout `FarCryPipe` (**INFERRED**): test, service, start (P1/P2), trigger (P1/P2), one coin bit, grenade P1/P2, menu up/down on the volume keys. Aim: one byte per axis. Not tried in the game.

## 6. Timing

Not measured: no frame is ever presented.

## 7. What we saw on screen

**MEASURED** (2026-10-15): without gamescope at 1920x1080, fullscreen, the D3D9 device is created, but nothing is presented (no DXVK HUD): the main thread runs its message loop and draws nothing. Black picture.

## 8. Current state and open questions

- Gets past the earlier hangs (window creation, mode switch) but then draws nothing.
- With the `W:` drive, it stays waiting on the D3D device at about 60% CPU.
- Open (assumption, not measured): the game waits for cabinet hardware (its I/O or a start condition). Also unknown: whether the `d3dx9_32` from Microsoft would change anything; it did not help when tried.

## 9. What we tried and what did not work

- Under gamescope: the main thread hangs in `UpdateWindow` right after `CreateWindow`/`ShowWindow`.
- Without gamescope, default mode: hangs in `ChangeDisplaySettings` (switch to 800x600).
- Without gamescope and with a 1920x1080 custom resolution: passes both, creates the device, no Present.
- Microsoft's `d3dx9_32` added: no change (so it is not in the profile).

## 10. What is Linux-specific, and what differs on Windows

Wine-specific: the window and mode-switch hangs depend on gamescope and on the resolution the game asks for. The `W:` drive mapping replaces the cabinet's `subst` command. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
