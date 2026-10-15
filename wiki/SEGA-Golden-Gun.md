# SEGA Golden Gun

**Status:** Working (2026-10-15). Plays from a double-click in English (region EXPORT): attract, START, shooting with crosshair, score and continue; 5.5 minutes played in gamescope fullscreen 16:9.

## 1. Platform and cabinet

- SEGA RingWide, Windows PC board; executable `exe/RingGunR_RingWide.exe` (about 4.7 MB).
- Two-player gun game. Template profile: TeknoParrot `GG` (revision 18), emulation profile `SegaJvsGoldenGun`.

## 2. What the game needs

- Your own game folder; RavenGun ships no games.
- Wine/Proton and gamescope.
- A region setting: `General/PcbRegion` and `General/DongleRegion` are both set to `EXPORT`.
- The cabinet's JVS I/O board is emulated by RavenGun: RavenGun provides the cabinet hardware the game expects.

## 3. The official start script, or why there is none

None. The game normally runs on its own cabinet's system; the community starts it through TeknoParrot. RavenGun starts it directly.

## 4. The route we use

**MEASURED** 2026-10-15. The recipe is the one used for Let's Go Island ([Let's Go Island](Lets-Go-Island) has the details):

```ini
[Launch]
Mode = direct

[Display]
Gamescope = true
GamescopePath = /usr/bin/gamescope

[Input]
Route = jvs
Board = SegaGun2P
ComPort = COM4
JvsTransport = pipe
```

JVS runs over a pipe into Wine's emulated `COM4`. Other template values: `General/FreePlay = 1`, `General/Windowed = 0`, `General/Input API = RawInput`, `General/HideCursor = 0`.

**Region:** use `EXPORT` for English text. With `JAPAN` this dump showed Chinese text. The region options are `JAPAN|USA|JAP2N|EXPORT|CHINA`.

## 5. Input

Board `SegaGun2P` (generic SEGA gun board 837-14572: 2 players, 14 switch bits, 8 analog channels of 10 bit; channels 0..3 = P1 X, P1 Y, P2 X, P2 Y). Per player: START, trigger, reload, grenade; shared TEST and SERVICE; two coins. The calibration window in the board (0..255) is the full axis. Mouse mode: coin = 5, START = 1. **MEASURED:** START, shooting, crosshair and score all work.

## 6. Timing

- Played 5.5 minutes (**MEASURED**).
- Boot time and frame pacing: not measured yet.

## 7. What we saw on screen

Attract in English, START, shooting with a visible crosshair, score, and a continue screen. The window fills the TV (16:9) inside gamescope. In a desktop window it also ran, but the rest of the desktop stays on screen.

## 8. Current state and open questions

- Real Move and second player not recorded.
- The gun calibration window of this title is not fitted; the full 0..255 range is used.

## 9. What we tried and what did not work

Region `JAPAN` gives Chinese text with this dump; `EXPORT` fixes it. Windowed mode works but leaves the desktop visible.

## 10. What is Linux-specific, and what differs on Windows

On Windows TeknoParrot provides the JVS emulation. On Linux RavenGun runs a JVS dialect in its daemon and gives the game a pipe on `COM4`; gamescope provides fullscreen.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
