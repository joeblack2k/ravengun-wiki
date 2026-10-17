# Transformers: Human Alliance

**Status:** Starts (2026-10-17). With `Windowed = 1` under gamescope the game shows "SYSTEM INITIALIZING" and then its attract ("PRESS START BUTTON", free play), with JVS over the pipe. Play, aiming and the lever have not been measured.

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
- `[Display] Gamescope = true` with `Windowed = 1`
- `[Input] Route = jvs`, `Board = SegaGun2P`, `ComPort = COM4`, `JvsTransport = pipe`

**Why `Windowed = 1`:** with `Windowed = 0` under gamescope the picture stayed black and the game never opened the JVS pipe (60% CPU for minutes). Windowed under gamescope makes it open the pipe and draw.

## 5. Input

JVS over a pipe, generic SEGA gun board `SegaGun2P`: coin, start, test, service, triggers and aim come from the emulated board. The JVS pipe is opened by the game. Not measured in play; the lever is not measured.

## 6. Timing

Not measured: the time to the attract and a five-minute run have not been recorded.

## 7. What we saw on screen

**MEASURED** (2026-10-17): SYSTEM INITIALIZING, then the attract with PRESS START BUTTON and FREE PLAY. Earlier (2026-10-15): black, with gamescope and also with a 1920x1080 Wine virtual desktop.

## 8. Current state and open questions

- The game starts and shows its attract; it is not yet called working.
- Open: coin, START, aiming and the lever (not measured).

## 9. What we tried and what did not work

- Gamescope with `Windowed = 0`: black, no JVS pipe.
- Wine virtual desktop at 1920x1080: same.
- Gamescope with `Windowed = 1`: the game opens the JVS pipe and shows the attract (2026-10-17).

## 10. What is Linux-specific, and what differs on Windows

Windows game under Wine; the cabinet's I/O board is emulated by RavenGun over a pipe. See [Wine-Notes](Wine-Notes).

This page covers the game and the loader: what you need to run this title and where it gets stuck.
