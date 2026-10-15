# Point Blank X

**Status:** Working (2026-10-15). Starts with a double-click in the RavenGun app, takes coins, START, mode and stage select, and plays with score and continue. One open cosmetic issue: a white background in the attract movie. The first start needs a one-time language change in the test menu.

## 1. Platform and cabinet

- Namco ES4 PC-based arcade board; a Windows executable (`PBX100-2-NA-MPR0-A63.exe`). **INFERRED** from the profile.
- It is a lightgun game with a ticket dispenser: the cabinet reports a ticket status that the game checks at boot.
- RavenGun uses the TeknoParrot profile `PointBlankX` (revision 9) as its template and runs the game under Wine/Proton.

## 2. What the game needs

- Your own copy of the game folder; RavenGun ships no games.
- Wine/Proton with a Vulkan-capable GPU, and gamescope (the profile sets `[Display] Gamescope = true`).
- The cabinet's I/O board is emulated by RavenGun's I/O bridge (see section 5).
- A one-time language setting through the test menu (section 8).

## 3. The official start script, or why there is none

There is no start script for this title. On a real ES4 cabinet the game is started by the cabinet's own software. The community normally starts it through TeknoParrot's own UI on Windows; RavenGun replaces that step: the app starts the game itself.

## 4. The route we use

**MEASURED** (2026-10-15): a double-click in the RavenGun app, no scripts.

```ini
[Launch]
Mode = direct

[Display]
Gamescope = true
GamescopePath = /usr/bin/gamescope

[Input]
Route = tp-shm
Layout = PointBlankX
```

`Route = tp-shm` means the daemon writes the cabinet's input into a shared-memory block the game side reads. `Layout = PointBlankX` is a layout of its own, taken from the TeknoParrot "PointBlankPipe" definition. The profile's `[Config]` keeps `General/Input API = RawInput`, `General/Windowed = 0` and `General/Render Hook = Present`; the crosshair and border options are off.

## 5. Input

Layout `PointBlankX` (control word at offset 8):

| Signal | Bit |
|---|---|
| coin 1 | 0x1 |
| service | 0x2 |
| test | 0x4 |
| menu down (volume down, key F5) | 0x10 |
| enter (volume up, key F4) | 0x20 |
| player 1 start / trigger | 0x40 / 0x80 |
| player 2 start / trigger | 0x400 / 0x800 |

Aim is one byte per axis (P1 X/Y at offsets 12/16, P2 X/Y at 20/24), left/top = 0. The layout is marked incomplete: "menu up" has no signal, and the 0-at-left/top direction is an **assumption** that was checked on the bench.

Mouse mode (default keys): coin = 5, START = 1, test = 0. Three coins were used to start a game.

## 6. Timing

- Played **5.5 minutes** (**MEASURED**): coins, START, mode and stage select, play with score and continue.
- Boot time and frame pacing: not measured yet.

## 7. What we saw on screen

**MEASURED:** the game reached its mode and stage select and was played with score and a continue prompt. On the very first start the ticket dispenser reported `21-1` and the language was `ja-JP` (Japanese text). The attract movie shows a white background.

## 8. Current state and open questions

**First start, one time only:**

1. Press TEST (key 0) to open the test menu.
2. Open OTHERS > LANGUAGE and set it to `en-US` (F5 chooses, F4 enters).
3. Leave the menu. From then on the game starts directly in English; the setting is stored in the game's save data (`TeknoParrot/F|G/savedata.bin` in your local view).

Open: the white background in the attract movie; "menu up" is missing in the layout; real Move controller play has not been recorded for this title.

## 9. What we tried and what did not work

- The ticket dispenser error `21-1` at the first start is cleared through the test menu together with the language change; no further workaround was needed.
- Nothing else failed in the recorded run. Earlier attempts with a generic layout are not documented here.

## 10. What is Linux-specific, and what differs on Windows

- On Windows the game runs through TeknoParrot's UI with its own input handling. On Linux RavenGun starts the game directly under Wine/Proton, inside gamescope, and supplies the input and the emulated I/O board itself.
- The `PointBlankX` layout and the `[Input]` settings are RavenGun-specific; the language/ticket test-menu step is the same on any host.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
