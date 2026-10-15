# Rampage

**Status:** Working (2026-10-14). A double-click in RavenGun starts it under Wine/Proton. This is not a lightgun game: it is a joystick-and-attack game for three players. Coin, START, intro, walking and smashing in the city ($19,000 damage) were measured over 5:09 min.

## 1. Platform and cabinet

- ADRENALINE PC-based cabinet; 64-bit Unity game, `Game.exe` (about 650 KB) with a `Game_Data` folder. **INFERRED** from files.
- Three players, each with a joystick and an attack button.
- Template profile: TeknoParrot `Rampage` (revision 5), input layout `WartranTroopers`.

## 2. What the game needs

- Your own game folder; RavenGun ships no games.
- Wine/Proton with DXVK.
- GStreamer plug-ins with gst-libav: the intro movies have an AAC sound track, and without an AAC decoder the game exits with code 1 as soon as the intro film starts, even with only coin and START pressed.
- The cabinet's hardware checks are answered by a RavenGun drop-in (`dropin/`, placed in `Game_Data/Plugins`); RavenGun provides the cabinet hardware the game expects. The game also played without it.

## 3. The official start script, or why there is none

None. RavenGun starts it with `rg-direct` (no scripts, no TeknoParrotUi).

## 4. The route we use

**MEASURED** 2026-10-14:

```ini
[Launch]
Mode = direct

[Wine]
Prefix = ravengun-test-dxvk
DllOverrides = d3d11,d3d10core,dxgi=n,b
GStreamerPlugins = ~/.local/share/ravengun/tools/gst-extra/plugins
Runner = wrapper

[Input]
Route = tp-shm
Layout = WartranTroopers
```

Environment (per-game user profile): `TP_REMOTETHREAD=off`, a DXVK prefix (`RG_WINEPREFIX`), and `GST_PLUGIN_PATH` pointing at gst-libav. The template config is `General/Input API = DirectInput`, `General/Windowed = 0`. The game's `teknoparrot.ini` is absent in your folder and is not written (core defaults apply).

## 5. Input

Player 1 (**MEASURED**):

| Action | Control |
|---|---|
| move up (trigger signal) | up |
| move down (reload signal) | down |
| left (grenade signal) | left |
| right (aux1 signal) | right |
| attack | key F4 (volume up) |
| coin | key F5 (volume down) |
| start | key 1 |

Player 2: coin = key 5, START = key 2. Three players each have COINS, START, UP, DOWN, LEFT, RIGHT and ATTACK, plus Test Menu and Test Select. A dedicated Move layout is not made yet because the bit order for it is not confirmed.

## 6. Timing

- Played 5:09 min.
- Boot time and frame pacing: not measured yet.

## 7. What we saw on screen

Intro film, then walking and smashing buildings in a city, damage counter reaching $19,000.

## 8. Current state and open questions

- Not a lightgun game, so the Move aim does not matter; a Move button layout is still open.
- Players 2 and 3 were not exercised.

## 9. What we tried and what did not work

Without gst-libav the game quit with exit code 1 at the intro film (see section 2). `TP_POSTSTART_REMOTETHREAD_MS` is not used; `TP_REMOTETHREAD=off` is the working setting.

## 10. What is Linux-specific, and what differs on Windows

On Windows you would run it through TeknoParrot. On Linux the Unity player needs Wine/Proton with DXVK, an AAC decoder from GStreamer for the movies, and the `tp-shm` input bridge; the joystick directions are mapped onto the shared WartranTroopers layout bits.

This page covers the game and the loader: what you need to run this title and where it gets stuck.
