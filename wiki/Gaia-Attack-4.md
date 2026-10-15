# Gaia Attack 4

**Status:** Not working yet (parked). The game starts and runs through the JVS handshake, but the picture stays black.

## 1. Platform and cabinet

Taito Type X2 cabinet (a PC based light-gun board). The game is `game.exe` (Windows, 32-bit); up to four players (the layout knows P3/P4 triggers, **INFERRED**).

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with Wine's built-in d3d9.
- The Type X2 cabinet I/O board (a JVS board on a pipe) is emulated by RavenGun.
- Region: the game reads a `REGION` line from its own `MINIGUN.INI`; the profile field is `Region = E` (English) (**INFERRED**).

## 3. The official start script, or why there is none

No official start script is used. The original cabinet boots Windows straight into the game (or its launcher); RavenGun starts the game's executable itself, from a double-click in the RavenGun app.

## 4. The route we use

Windows route on RavenGun's own OpenParrot-compatible core, direct launch:

- `[Game] Type = OpenParrot`
- `[Input] Route = tp-shm`, `Layout = MusicGunGun2Pipe`
- Per-game environment (from the migration of the old env file): `TP_REMOTETHREAD=off` (the loader's default entry-point trampoline), `WINEDLLOVERRIDES=d3d9=b` (Wine's built-in d3d9), `RG_LOADER_FPFIX=true` (a copy of the loader without `CONTEXT_FLOATING_POINT`, see below), `RG_JVS_BOARD=true` (default JVS board behind the pipe).

## 5. Input

Layout `MusicGunGun2Pipe` (**INFERRED**): the control word has six bits: P1 trigger (bit 0), P2 trigger (bit 2), volume up/down (bits 4/5), and for four-player games P3/P4 triggers (bits 6/7). Aim: eight one-byte channels with stride 4 from offset 12 (P1 X/Y, P2, P3, P4), 0 = left/top. Start, coin, test, service and extra buttons go through the emulated JVS board. The layout table is incomplete. None of this has been tried, since the game stays black.

## 6. Timing

Not measured yet. No frame to time.

## 7. What we saw on screen

Black picture (**MEASURED**).

## 8. Current state and open questions

- **MEASURED** (round 11): the game starts, but there is no picture. A Wine crash caused by the loader (MXCSR forced to 0 by `SetThreadContext`) is worked around with `RG_LOADER_FPFIX`; the game then walks through the JVS chain (reset, address, identification, function list) but stays black and never starts polling the switches (command `0x20`).
- The `patches.ini` has two memory patches (gun writes off at `game.exe+0x113E80`, a NOP at `+0x1156C8`), both **disabled**; the OpenParrot-compatible core applies the equivalents itself, and the file is documentation. The shared loader patch is enabled.
- Our own core recognises the title (32-bit, table 2).
- Open: what makes the game start polling; see the same pattern in [Elevator Action Death Parade](Elevator-Action-Death-Parade), [Haunted Museum](Haunted-Museum) and [Haunted Museum II](Haunted-Museum-II).

## 9. What we tried and what did not work

- Without the floating-point fix: Wine crash (MXCSR becomes 0). Fixed by `RG_LOADER_FPFIX`.
- With the fix: JVS chain completes, still black, no `0x20` polling.
- Race hypothesis (not confirmed): the address-assignment step may be racing the loader's pipe helper, since runs saw 3 to 27 address assignments instead of 1 or 2. A planned test (delay the address reply) is not done.
- Not yet tried: sampling the main thread to see which call it repeats.

## 10. What is Linux-specific, and what differs on Windows

Wine-specific: the crash was Wine's `SetThreadContext` setting MXCSR to 0, which broke floating point in the game; RavenGun works around it with a loader copy that does not set that context part. On the cabinet the I/O board sits on a serial line; on Linux it is a pipe emulated by RavenGun. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
