# Gaia Attack 4

**Status:** Working (2026-10-16). A double-click starts the game under Wine on RavenGun's JVS board `TaitoGun`; attract, coin, START, area select and a mission were played for 5.5 minutes. Gun calibration ships with RavenGun; to recalibrate use TEST > GUN CHECK > START 1 and save with TEST.

## 1. Platform and cabinet

Taito Type X2 cabinet (a PC based light-gun board). The game is `game.exe` (Windows, 32-bit); up to four players (the layout knows P3/P4 triggers, **INFERRED**).

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with Wine's built-in d3d9.
- The Type X2 cabinet I/O board (a JVS board on a pipe) is emulated by RavenGun.
- Region: the game reads a `REGION` line from its own `MINIGUN.INI`; the profile field is `Region = E` (English).

## 3. The official start script, or why there is none

No official start script is used. The original cabinet boots Windows straight into the game (or its launcher); RavenGun starts the game's executable itself, from a double-click in the RavenGun app.

## 4. The route we use

Windows route on RavenGun's own OpenParrot-compatible core, direct launch:

- `[Game] Type = OpenParrot`, `EmulationProfile = GaiaAttack4`, `Executable = game.exe`
- `[Launch] Mode = direct`
- `[Display] Gamescope = true` with `Windowed = 1` in the config (black without it)
- `[Input] Route = jvs`, `Board = TaitoGun`, `Layout = MusicGunGun2Pipe`

Per-game environment: `TP_REMOTETHREAD=off` (the loader's default entry-point trampoline), `WINEDLLOVERRIDES=d3d9=b` (Wine's built-in d3d9), `RG_LOADER_FPFIX=true` (a copy of the loader without `CONTEXT_FLOATING_POINT`, see section 10).

The route reached the picture in several steps (**MEASURED** 2026-10-16):

1. The game closes the JVS pipe after its first board check and opens it again. The direct launcher accepted only one connection, which gave "I/O ERROR 2"; now every connection is answered.
2. The game then asks the board for 10 analog channels while a plain board has 8, and the old board answered with an error report ("I/O ERROR"); now the board returns as many channels as requested, as the TeknoParrot board does.
3. START of the Taito gun games is on P1 up/down (as in the TeknoParrot profile), so the board is `TaitoGun` instead of the generic `SegaGun2P`.
4. The factory gun calibration sits about 20% off the picture (X x1.2, Y -0.16). The gun was calibrated in the game's test menu in mouse mode and the calibration ships with RavenGun as seed data.
5. Under gamescope the picture is black without `Windowed = 1`; with it the game is full screen.

## 5. Input

JVS board `TaitoGun` over the pipe: coin, test, service and START (P1 up/down starts player 1/2), plus the board's analog channels. Triggers and aiming come through the shared-memory layout `MusicGunGun2Pipe` (**INFERRED**): P1 trigger (bit 0), P2 trigger (bit 2), volume up/down (bits 4/5), and for four-player games P3/P4 triggers (bits 6/7); aim is eight one-byte channels with stride 4 from offset 12, 0 = left/top.

**MEASURED** 2026-10-16 with the mouse as lightgun: coin, START, area select and the test menu (including GUN CHECK) work. Not measured with the real PS Move.

## 6. Timing

A run of 5.5 minutes (attract, coin, START, area select, mission) on 2026-10-16. Time from double-click to attract not recorded.

## 7. What we saw on screen

**MEASURED** (2026-10-16): the attract, the coin and START, the AREA SELECT screen and a mission, full screen under gamescope; the test menu with GUN CHECK.

## 8. Current state and open questions

- Working: double-click, attract, coin, START, area select and a mission for 5.5 minutes.
- Open: play with the real PS Move, and the layout table, which is incomplete.
- The game's shipped patch notes describe memory patches (gun writes off and similar) that RavenGun's OpenParrot-compatible core applies itself.

## 9. What we tried and what did not work

- Without the floating-point fix: Wine crash (MXCSR becomes 0). Fixed by `RG_LOADER_FPFIX`.
- With the fix, the JVS chain completed but the game stayed black and never polled the switches; the four steps in section 4 (reconnecting pipe, channel count, board type, calibration) plus `Windowed = 1` under gamescope solved it.
- A race hypothesis about address assignment turned out not to be the cause.

## 10. What is Linux-specific, and what differs on Windows

Wine-specific: the crash was Wine's `SetThreadContext` setting MXCSR to 0, which broke floating point in the game; RavenGun works around it with a loader copy that does not set that context part. On the cabinet the I/O board sits on a serial line; on Linux it is a pipe emulated by RavenGun. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
