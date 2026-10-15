# Transformers: Human Alliance

**Status:** Not working yet. The game runs but stays black and never opens the JVS pipe.

## 1. Platform and cabinet

SEGA RingEdge 2 cabinet (PC based). The game is `TF_Gun_R_Ring_dumped.exe`, Windows. Two-player light-gun game.

## 2. What the game needs

- RavenGun ships no games: you need your own copy of the game.
- Wine with a fullscreen gamescope session.
- The cabinet's JVS I/O board is emulated by RavenGun (generic SEGA gun board on a pipe).

## 3. The official start script, or why there is none

No official start script is used. The original cabinet boots Windows straight into the game (or its launcher); RavenGun starts the game's executable itself, from a double-click in the RavenGun app.

## 4. The route we use

Recipe copied from [SEGA Golden Gun](SEGA-Golden-Gun):

- `[Game] Type = TeknoParrot`, `EmulationProfile = SegaJvsLetsGoIsland`, `Executable = TF_Gun_R_Ring_dumped.exe`
- `[Launch] Mode = direct`
- `[Display] Gamescope = true` (fullscreen, `Windowed = 0`)
- `[Input] Route = jvs`, `Board = SegaGun2P`, `ComPort = COM4`, `JvsTransport = pipe`

## 5. Input

JVS over a pipe, generic SEGA gun board `SegaGun2P`: coin, start, test, service, triggers and aim come from the emulated board. Not tried in the game.

## 6. Timing

Not measured yet.

## 7. What we saw on screen

**MEASURED** (2026-10-15): black picture, with gamescope and also with a 1920x1080 Wine virtual desktop.

## 8. Current state and open questions

- The process runs (about 60% CPU) for 2+ minutes, stays black and never opens the JVS pipe.
- Open: what the game is waiting for before it initialises its I/O.

## 9. What we tried and what did not work

- Gamescope fullscreen: black, no JVS pipe.
- Wine virtual desktop at 1920x1080: same.

## 10. What is Linux-specific, and what differs on Windows

Windows game under Wine; the cabinet's I/O board is emulated by RavenGun over a pipe. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
