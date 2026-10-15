# Let's Go Safari

**Status:** Working (2026-10-14). Double-click in the app starts the game under Wine; JVS goes over a pipe to RavenGun's board `LGS`; full screen through gamescope. Played 5:49 minutes, and 5:38 minutes with a gamepad (steering with the left stick, coloured buttons). This is a driving game, not a light gun game. Not measured: camera switch, wipers, horn, fireworks, the real PS Move.

## 1. Platform and cabinet

- SEGA RingWide, Windows, executable `GameSampR_RingWide.exe` (a test-mode executable `GameTestR_RingWide.exe` also exists).
- One player: a steering wheel, four coloured buttons (red, blue, yellow, green), gear lever up/down, camera change, window wipers, horn, fireworks. 22 switch bits on the board.
- RavenGun ships no games: you need your own copy of the game folder.

## 2. What the game needs

- Wine with its own prefix copy (`Prefix = ravengun-test-lgs`).
- RavenGun provides the cabinet hardware the game expects, including a local network service the game talks to on start (port 40100).
- gamescope for a full-screen picture (without it the game opens a window with a title bar).
- Region: `PcbRegion = USA` in the profile.

## 3. The official start script, or why there is none

On the cabinet the RingWide system software starts the game. RavenGun starts it itself, no scripts: [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Launch]
Mode = direct

[Display]
Gamescope = true

[Input]
Route = jvs
Layout = LGS
Board = LGS
ComPort = COM4
JvsTransport = pipe
```

- **MEASURED:** the game talks JVS over the pipe `TeknoParrot_JVS`, not over COM4 (COM4 received 0 packets). RavenGun's daemon is the board `LGS`.
- **MEASURED (earlier rounds):** on start the game opened a local TCP connection (port 40100) and waited for a message that never came; it never created a window. With the loader's default route (`TP_REMOTETHREAD=off`) that service step no longer occurs.
- `[Bindings]` in the profile (keyboard): red/blue/yellow/green = `A` `S` `D` `F`, change view `Q`, wipers `W`, horn `E`, fireworks `R`, wheel left/right = arrow keys (the loader's "Use Keyboard/Button For Axis" must then be 1).

## 5. Input

- Steering: the left stick of a gamepad (`LeftX = wheel`) writes byte 12 of the shared memory (`Layout = LGS`, signal `wheel`). **MEASURED:** the game never asks the board for the analog axis, so steering comes only from the shared memory. Without a pad, the light gun's horizontal aim steers.
- START: the pad's Start, or key `1`. Coin: key `5` (free play is on).
- Gamepad map in `[Gamepad]`: `A = trigger` (red), `B = reload` (blue), `X = grenade` (yellow), `Y = aux1` (green), `Start = start`, `Back = coin`. Assign the pad in the app under Controllers, Gamepads.
- Positions of camera change, wipers, horn, fireworks and the lever bits were not measured yet.

## 6. Timing

- 17:33 run: 5:49 minutes. Gamepad run at 18:35: 5:38 minutes (steering by left stick, contact sheet `bench-captures/LGS/seq_sheet.png`). **MEASURED.**
- Boot to attract and frame pacing: not measured.

## 7. What we saw on screen

Full-screen game, the vehicle steering with the stick, START and the coloured buttons responding.

## 8. Current state and open questions

- Not measured: camera switch, wipers, horn, fireworks, the real Move.
- The board's extra switch bits are only partly mapped.

## 9. What we tried and what did not work

- The early rounds with the loader's remote-thread injection stalled on the local service step (section 4); the default route fixed that.
- `Windowed = 0` alone did not give a full-screen picture; gamescope did.

## 10. What is Linux-specific, and what differs on Windows

- Full screen needs gamescope under Wine.
- The JVS board is a pipe with the RavenGun daemon behind it; a real cabinet has a serial board.
- A gamepad or the light gun's aim is the steering wheel, which has no real equivalent on the Wine side.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
