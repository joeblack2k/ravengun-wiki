# Dream Raiders

**Status:** Working (2026-10-14). Double-click in the app starts the game under Wine with JVS over a pipe to RavenGun's generic Sega gun board; played 6:39 minutes with the test pattern (START, shooting, result screen, new game). The first start asks for calibration, see section 5. Not yet played with a real PS Move.

## 1. Platform and cabinet

- SEGA RingWide, Windows, executable `Game.exe`.
- Two-player light gun game; JVS I/O board on a serial port (COM4 in the profile).
- RavenGun ships no games: you need your own copy of the game folder.

## 2. What the game needs

- Wine, started by RavenGun (`[Launch] Mode = direct`).
- RavenGun provides the cabinet hardware the game expects (the cabinet's I/O board is emulated).
- Region settings in the profile: `General/PcbRegion = JAPAN`, free play on (`General/FreePlay = 1`), `General/Windowed = 1`.

## 3. The official start script, or why there is none

On the arcade board the game is started by the RingWide system software. There is no script to reuse on a PC; RavenGun starts `Game.exe` directly. See [Official-Start-Scripts](Official-Start-Scripts).

## 4. The route we use

Profile `SDR`, emulation profile `SegaJvsDreamRaiders`.

```ini
[Launch]
Mode = direct

[Input]
Route = jvs
Board = SegaGun2P
ComPort = COM4
JvsTransport = pipe
```

- The game talks JVS over a Windows named pipe (`JvsTransport = pipe`); RavenGun's daemon is the I/O board behind that pipe. This is the same recipe as [Lets-Go-Island](Lets-Go-Island). **MEASURED** (2026-10-14).
- Board `SegaGun2P` is the generic Sega two-player gun board (14 switch bits, 8 analog channels; channels 0-3 are P1 X, P1 Y, P2 X, P2 Y). Which switch bit is trigger/reload/start per game, and the calibration window, were only partly measured: the game's own calibration (below) takes care of the aim range.

## 5. Input

- Coin: key `5`, START: key `1`. SERVICE: `F3`.
- Aim and trigger: PS Move, mouse or controller; **MEASURED** with the test pattern: shooting in the game works.

### First start: calibration

The game asks for calibration (CONTROLLER ADJUSTMENT) on a fresh setup. **MEASURED:**

1. Press SERVICE (`F3`) to reach CALIBRATION.
2. Press START (player 1).
3. Shoot the four corners of the screen in turn: top-left, top-right, bottom-left, bottom-right.

The calibration is saved and the prompt does not come back.

## 6. Timing

- Boot to attract: not measured separately.
- Played: 6:39 minutes (START, shooting, result screen, new game). **MEASURED.**
- Frame pacing: not measured.

## 7. What we saw on screen

The CONTROLLER ADJUSTMENT screen on the first start, then attract, the game with shots registering, a result screen and the start of a new game.

## 8. Current state and open questions

- Open: a real PS Move (only the test pattern was used).
- Open: player 2 and the exact meaning of every switch bit were not measured.
- Assumption: the calibration window of the original Windows loader profile for this game is 63..207 x 63..191 on the 0..255 axis scale; RavenGun uses the generic board and the in-game calibration instead.

## 9. What we tried and what did not work

Not measured yet beyond the working route (prepared in a first pass from the Let's Go Island recipe and it worked after the calibration step).

## 10. What is Linux-specific, and what differs on Windows

- On a real cabinet the JVS board is a physical serial device; here it is a pipe backed by RavenGun's daemon.
- No Windows-side UI of the original loader is used.
- The in-game texts depend on the region setting (`JAPAN`); other values are offered by the profile (`JAPAN|USA|JAP2N|EXPORT|CHINA`) but only `JAPAN` was tested.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
