# Haunted Museum II

**Status:** Not working yet (parked). The game starts and runs through the JVS handshake, but the picture stays black.

## 1. Platform and cabinet

Taito Type X2 cabinet. The game is `game.exe` (Windows, 32-bit), Taito, 2011. The dump we use is the **USA 1.00** build (**MEASURED**: the CRC of the first 0x400 bytes of the main module, `0x5a7fa241`, matches the USA 1.00 entry; the Japanese 1.01 build would give `0x42d54499`).

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with Wine's built-in d3d9.
- The Type X2 I/O board (JVS on a pipe) is emulated by RavenGun.
- Region: the game reads a `REGION` line from its own `haunted2.ini` (profile field `Region = E`, **INFERRED**).

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
- Only the patch set for version 2100 (USA 1.00) applies to this dump. The three patches for the 2101J build are kept as documentation and never applied (the core picks the 2100 branch from the CRC). The gun-write patch at `game.exe+0x9D970` is disabled and documentation only; the crash-NOP at `game.exe+0x1391` does nothing on this dump because the byte is already `0x90`.
- Open: same as [Gaia Attack 4](Gaia-Attack-4).

## 9. What we tried and what did not work

Same as [Gaia Attack 4](Gaia-Attack-4). The 2101J build is said to suppress a "Firmware Update Error" message, but that build is not the one we have.

## 10. What is Linux-specific, and what differs on Windows

Wine-specific: the MXCSR crash is worked around in the loader. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
