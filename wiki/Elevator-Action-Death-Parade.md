# Elevator Action Death Parade

**Status:** Starts (2026-10-16). A double-click runs the game over RavenGun's JVS board with PhysX 2.8 system software installed: logo, intro and game scenes in the attract. The picture is a narrow portrait strip, and controls and calibration have not been measured.

## 1. Platform and cabinet

Taito Type X2 cabinet (the PC based Type X2 board, **INFERRED**), two-player light-gun game. Windows executable `Game.exe`.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with DXVK or the built-in d3d9.
- The **NVIDIA PhysX 2.8 system software** (loader 2.8.1, SDK 2.8.0). Without it the game crashes after the logo, because creating the PhysX SDK returns nothing; a newer 2.8.4 core from another game does not work. RavenGun's setup step installs the system software into the prefix.
- The Type X2 cabinet I/O board is emulated by RavenGun (a JVS board on a pipe).
- English text is present in the game data (`msg_us`, `_e`).

## 3. The official start script, or why there is none

No official start script is used. The original cabinet boots Windows straight into the game (or its launcher); RavenGun starts the game's executable itself, from a double-click in the RavenGun app.

## 4. The route we use

Windows route with a JVS board, copied from the [Music GunGun 2](Music-GunGun-2) recipe:

- `[Game] Type = OpenParrot`, `EmulationProfile = EADP`, `Executable = Game.exe`
- `[Launch] Mode = direct`
- `[Display] Gamescope = true`
- `[Input] Route = jvs`, `Board = TaitoEADP`, `JvsTransport = pipe`, `Layout = EADP`

The board `TaitoEADP` answers the Taito commands (node 0) and maps Enter to START. Coin, test and service go through the emulated JVS board; triggers and aiming go through the shared-memory `EADP` layout.

## 5. Input

Layout `EADP` (**INFERRED** from the layout file):

- P1 trigger (bit 0), P1 button 4 (bit 1, mapped to reload), P2 trigger (bit 2), P2 button 4 (bit 3), volume up/down (bits 4/5).
- Aim: one byte per axis, 0 = left/top.
- Start (Enter), coin, test, service: via the JVS board; Select is aux 1.

Not measured in the game yet.

## 6. Timing

Not measured yet: neither the time to the logo nor a five-minute run has been recorded.

## 7. What we saw on screen

**MEASURED** (2026-10-16): the logo, the intro and game scenes in the attract loop. The picture is a narrow portrait strip in the middle of the output, because the cabinet has a portrait screen (`Multi Screen = 1` does not start).

## 8. Current state and open questions

- The game starts by double-click and runs its attract; it is not yet called working.
- Open: the portrait strip, the button layout (Enter = START, Select = aux 1) and gun calibration.

## 9. What we tried and what did not work

- First runs (2026-10-15): a black picture with no JVS traffic, with the generic gun board; the board `TaitoEADP` with the Taito commands fixed the JVS side.
- The game crashed after the logo until the PhysX 2.8 system software was installed; PhysX 2.8.4 from another game did not substitute for it, with wined3d or with DXVK.
- `Multi Screen = 1` (to get the second screen) does not start.

## 10. What is Linux-specific, and what differs on Windows

Windows game under Wine. On the cabinet the I/O board is real hardware on a serial line; on Linux RavenGun emulates the board and exposes the line as a pipe. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
