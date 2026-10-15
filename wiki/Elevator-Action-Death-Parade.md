# Elevator Action Death Parade

**Status:** Not working yet. The game runs but the picture stays black; it never opens the JVS pipe.

## 1. Platform and cabinet

Taito Type X2 cabinet (the PC based Type X2 board, **INFERRED**), two-player light-gun game. Windows executable `Game.exe`.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with DXVK or built-in d3d9 (not decided).
- The Type X2 cabinet I/O board is emulated by RavenGun (a JVS board on a pipe).
- English text is present in the game data (`msg_us`, `_e`).

## 3. The official start script, or why there is none

No official start script is used. The original cabinet boots Windows straight into the game (or its launcher); RavenGun starts the game's executable itself, from a double-click in the RavenGun app.

## 4. The route we use

Windows route with a JVS board, copied from the [Music GunGun 2](Music-GunGun-2) recipe:

- `[Game] Type = OpenParrot`, `EmulationProfile = EADP`, `Executable = Game.exe`
- `[Launch] Mode = direct`
- `[Display] Gamescope = true`
- `[Input] Route = jvs`, `Board = SegaGun2P`, `JvsTransport = pipe`, `Layout = EADP`

So: start, coin, test and service go through the emulated JVS board; triggers and aiming go through the shared-memory `EADP` layout.

## 5. Input

Layout `EADP` (**INFERRED** from the layout file):

- P1 trigger (bit 0), P1 button 4 (bit 1, mapped to reload), P2 trigger (bit 2), P2 button 4 (bit 3), volume up/down (bits 4/5).
- Aim: one byte per axis, 0 = left/top.
- Start, coin, test, service: via the JVS board.

Not tried in the game.

## 6. Timing

Not measured: no attract was reached.

## 7. What we saw on screen

**MEASURED** (2026-10-15): a 1920x1080 window in gamescope, about 55% CPU, black picture. The game never opens the JVS pipe and prints no debug strings.

## 8. Current state and open questions

- Black picture and no JVS traffic: the same pattern as [Gaia Attack 4](Gaia-Attack-4).
- Open: what the main loop is waiting for (assumption: something before the I/O initialisation).

## 9. What we tried and what did not work

- Profile with JVS board over a pipe in gamescope: black, no JVS pipe activity. Nothing else tried yet.

## 10. What is Linux-specific, and what differs on Windows

Windows game under Wine. On the cabinet the I/O board is real hardware on a serial line; on Linux RavenGun emulates the board and exposes the line as a pipe. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
