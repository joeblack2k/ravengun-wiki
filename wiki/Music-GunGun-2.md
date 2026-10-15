# Music GunGun 2

**Status:** Working (2026-10-15). Double-click in the app starts the game under Wine with the OpenParrot loader, using the HD build from your dump and RavenGun's JVS board plus the shared-memory layout for aiming. Attract, coin, START, training choice, songs with a score and hi-score entry; played 5.5 minutes.

## 1. Platform and cabinet

- Taito Type X2, Windows, 32-bit, executable `game.exe` (a rhythm shooting game; "Mug Ver.[Nov 15 2010]" in its error window).
- Two-player light gun layout.
- RavenGun ships no games: you need your own copy of the game folder.

## 2. What the game needs

- Wine with its **built-in** Direct3D 9 (`WINEDLLOVERRIDES=d3d9=b`).
- A screen mode of 1920x1080. The standard `game.exe` asks hard-coded for 1360x768 and Xwayland offers no such mode, so the game shows "Direct3D initialisation failed" (also with DXVK). The dump contains an HD build (`Patch/HD/game.exe`), which differs only in those four bytes (1920x1080).
- A loader copy without `CONTEXT_FLOATING_POINT` (see section 4).
- RavenGun provides the cabinet hardware the game expects.

## 3. The official start script, or why there is none

On a Type X2 cabinet the system's own launcher starts the game. On RavenGun the app starts the game directly through the loader. See [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Game]
Type = OpenParrot
EmulationProfile = MusicGunGun2

[Launch]
Mode = direct
ViewLinks = game.exe -> Patch/HD/game.exe

[Input]
Route = jvs
Board = SegaGun2P
JvsTransport = pipe
Layout = MusicGunGun2Pipe
```

- **`ViewLinks`:** in RavenGun's view of your game folder `game.exe` links to `Patch/HD/game.exe`; your game folder is not changed. **MEASURED** (2026-10-15).
- **Loader patch "OpenParrotLoader without CONTEXT_FLOATING_POINT":** under Wine, `SetThreadContext` with the floating-point flag sets MXCSR to 0 on the 32-bit thread, so the first inexact SSE operation (Mesa, in Direct3D 9 setup) raises exception `0xC00002B5`. RavenGun uses a loader copy without that flag (**MEASURED**, tested with Wine 9.0 to 11.19).
- A second patch entry (a jump to a function that always returns true at `Game.exe+0x137C70`) exists in `patches.ini` for documentation and is disabled; the loader core applies it itself.
- Default loader route (`TP_REMOTETHREAD=off`, entry-point trampoline).

## 5. Input

- JVS board `SegaGun2P` over the pipe gives coin, START, test, service; the shared-memory layout `MusicGunGun2Pipe` gives the triggers and aiming (one byte per axis from offset 12; trigger P1 bit 0, P2 bit 2, volume up/down bits 4/5).
- Coin: key `5`. START: key `1`. **MEASURED** (2026-10-15): coin, START, shooting and score.
- With the fixed no-input board that `rg-direct` uses by default, the game stayed in the calibration screen of its test mode; hence the daemon's board.

## 6. Timing

- Played: 5.5 minutes. **MEASURED.**
- Boot to attract and frame pacing: not measured.

## 7. What we saw on screen

Attract, training choice, songs with a running score and a hi-score entry. Before the HD build: the game's own error window "Direct3D initialisation failed".

## 8. Current state and open questions

- Open: real PS Move, player 2, sound and timing accuracy of the rhythm game.
- Which other build folders (`4K`, `ORI`, a multi-head fix) behave differently is not known.

## 9. What we tried and what did not work

- Standard `game.exe`: error window about Direct3D, with built-in d3d9 and with DXVK (no matching display mode).
- Fixed input board without keys: stuck in the test-mode calibration screen.
- Loader with the floating-point context flag: crash on the first SSE operation.

## 10. What is Linux-specific, and what differs on Windows

- Xwayland's missing 1360x768 mode forces the HD build; on a Windows cabinet the 1360x768 monitor mode exists.
- The MXCSR problem is a Wine bug; the loader copy works around it.
- The JVS board is a pipe backed by the daemon.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
