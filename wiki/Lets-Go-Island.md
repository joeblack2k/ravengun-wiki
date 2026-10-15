# Let's Go Island: Lost on the Island of Tropics

**Status:** Working (2026-10-14). Double-click in the app starts the game under Wine with the OpenParrot loader; JVS goes over a pipe to RavenGun's own board `LGI`. Played 5:23 minutes on the TV in mouse mode (START, aim, shoot, continue after CONTINUE, up to a boss, score 36600). In-game text is Japanese. Not yet played with a real PS Move on this route.

## 1. Platform and cabinet

- SEGA RingWide, Windows, executable `LGI_RingW_F_safe.exe`.
- On-rails light gun game; two players.
- RavenGun ships no games: you need your own copy of the game folder.
- The 3D sibling is [Lets-Go-Island-3D](Lets-Go-Island-3D).

## 2. What the game needs

- Wine, a prefix copy with a **Wine virtual desktop** of 1920x1080.
- RavenGun provides the cabinet hardware the game expects.
- Region: the profile has `PcbRegion = JAPAN`; the game then shows Japanese text. Other region values exist in the loader profile but were not tried.

## 3. The official start script, or why there is none

The RingWide system software starts the game on the cabinet. RavenGun starts the executable itself, no scripts and no loader UI. See [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

```ini
[Game]
EmulationProfile = SegaJvsLetsGoIsland

[Launch]
Mode = direct

[Wine]
Prefix = ravengun-test-lgi
VirtualDesktop = 1920x1080
Runner = wrapper

[Input]
Route = jvs
Board = LGI
ComPort = COM4
JvsTransport = pipe
```

- The game talks JVS over the pipe `TeknoParrot_JVS`; RavenGun's daemon is the board. **MEASURED** (2026-10-14).
- Virtual desktop, because real full screen hangs in `ChangeDisplaySettingsExW` with a black picture and never connects, and window mode crashes the loader core on a window title that is a class atom (**MEASURED**, exit code 5).
- Default loader route (`TP_REMOTETHREAD=off`); there is no wait for a local service as in Let's Go Safari.

## 5. Input

- Board `LGI` with its own raw window: x 131..228, y 141..220, inverted; channel 0 = P1 Y, 1 = P1 X, 2 = P2 Y, 3 = P2 X. **MEASURED** on a 3x3 grid of test points: 0.2 / 0.5 / 0.8 of the screen produced 0.19-0.20 / 0.49 / 0.80 in the intro movie and in the game.
- The original loader's profile window (x 27..208, y 35..178) made the crosshair run 1.87 times too fast and disappear above 0.53 of the screen: the game expects a different window.
- START: hold key `1` briefly. Coin: key `5`. Trigger: mouse or Move trigger.

## 6. Timing

- Load about 70 seconds (**MEASURED** in an earlier run).
- 5:23 minutes of attract and play after the first attract picture. **MEASURED.**
- Frame pacing: not measured.

## 7. What we saw on screen

Japanese attract, the game with the crosshair following the aim, CONTINUE after dying, a boss stage and a score of 36600.

## 8. Current state and open questions

- Open: real PS Move buttons, sound, player 2, the game's own test menu and calibration, long sessions.
- Open question: where the raw aim window comes from (stored calibration, default or the profile).

## 9. What we tried and what did not work

- Original loader input (evdev): worked for START and coin but not for aim scaling.
- Full screen and window mode: see section 4. The virtual desktop was the working solution.

## 10. What is Linux-specific, and what differs on Windows

- The virtual desktop and the pipe-backed board are Wine/RavenGun specifics; on Windows the game uses a real full screen and a serial board.
- Use the profile's prefix name rather than the shared one.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
