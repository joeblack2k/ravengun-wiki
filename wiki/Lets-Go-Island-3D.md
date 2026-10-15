# Let's Go Island 3D: Lost on the Island of Tropics

**Status:** Working (2026-10-14). Double-click in the app starts the game under Wine with the OpenParrot loader; JVS goes over a pipe to RavenGun's own board `LGI3D`. Played 5:15 minutes on the TV in mouse mode (START, aim, shoot, combos, score 37500). The picture is red-cyan 3D. Not yet played with a real PS Move on this route.

## 1. Platform and cabinet

- SEGA RingEdge, Windows, executable `LGI.exe` (same build family as [Lets-Go-Island](Lets-Go-Island), but the USA version).
- On-rails light gun game with a red-cyan 3D mode and a 2D button on the cabinet.
- RavenGun ships no games: you need your own copy of the game folder.

## 2. What the game needs

- Wine, a copy of the shared prefix with a **Wine virtual desktop** of 1920x1080 (see section 4).
- RavenGun provides the cabinet hardware the game expects.
- Region: profile `DongleRegion`/`PcbRegion` set to USA (the game runs with those values).
- Anaglyph (red-cyan) glasses for the 3D picture. The 2D button was not checked.

## 3. The official start script, or why there is none

The cabinet starts the game through the RingEdge system software. RavenGun starts `LGI.exe` itself: daemon, then the direct runner, Wine and the OpenParrot-based loader. No script or loader UI. See [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Launch]
Mode = direct

[Wine]
Prefix = ravengun-test-lgi3d
VirtualDesktop = 1920x1080
Runner = wrapper

[Input]
Route = jvs
Board = LGI3D
ComPort = COM4
JvsTransport = pipe
```

- Why a virtual desktop (**MEASURED**): in real full screen the game hangs in `ChangeDisplaySettingsExW` with a black picture and never connects to the JVS pipe; in window mode the loader's core crashes on a window title that is a class atom, and the game exits with code 5. A Wine virtual desktop of 1920x1080 with `Windowed = 0` gives a full-screen picture without a title bar.
- The game uses the loader's default route (`TP_REMOTETHREAD=off`) and the pipe `TeknoParrot_JVS`; the waiting-for-local-service step of [Lets-Go-Safari](Lets-Go-Safari) does not occur here.
- The daemon is the JVS board behind the pipe (`ravengunctl iobridge` shows thousands of packets, address 1, switch and analog polls).

## 5. Input

- Board `LGI3D`: the game expects the window of the original loader profile. Raw value = 255 - (27 + 181 x) for X and 255 - (35 + 143 y) for Y, so raw x 47..228 and y 77..220, inverted. **MEASURED** against the crosshair (with the LGI window the crosshair was 0.53 times too small).
- START: hold key `1` briefly (**MEASURED**). Coin: key `5`. Trigger: left mouse button or the Move trigger. Start bit is bit 7 of byte 0 of player 1, trigger bit 1.
- Calibration: after loading, the game runs a 3D calibration in red-cyan; follow its prompts.

## 6. Timing

- Loading takes about 70 seconds, LGI3D a little longer, then the 3D calibration (**MEASURED** in an earlier run).
- 5:15 minutes of attract and play after the first attract picture. **MEASURED.**
- Frame pacing: not measured.

## 7. What we saw on screen

Red-cyan 3D attract, the game with the crosshair following the aim, combos and a score of 37500.

## 8. Current state and open questions

- Open: real PS Move, player 2, sound, long sessions, the 2D button, whether shots hit targets in every stage (earlier: only trigger bit and crosshair were measured, later the score).
- Where the aim window comes from (stored calibration, defaults or the profile) is not settled.

## 9. What we tried and what did not work

- The original loader's own evdev input: START and coins arrived, but the crosshair ran 1.87 times too fast on LGI. Hence the daemon is the board with its own window.
- Full screen and window modes: see section 4.

## 10. What is Linux-specific, and what differs on Windows

- The virtual desktop is a Wine workaround; on Windows the game goes full screen on its own.
- The JVS board is a pipe backed by the RavenGun daemon instead of a serial device.
- Wine's prefix copy is a RavenGun detail: use the profile's `Prefix` rather than the shared prefix.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
